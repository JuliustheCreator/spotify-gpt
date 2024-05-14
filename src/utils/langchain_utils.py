"""
This module provides a wrapper class for the LLM model from the langchain_community package.

The LLM class provides a wrapper for the Ollama class from the langchain_community package. The class provides a simple interface for querying the LLM model with a given prompt. The class also provides a method for setting the system prompt for the LLM model.

Classes:
    ParserError: Custom exception for parser errors
    XRecommendations: Parser class for parsing LLM string output to JSON
    LLM: A wrapper class for the LLM
    RecommendationLLM: A wrapper class for the LLM for music recommendations
    ExplanationLLM: A wrapper class for the LLM for explaining music recommendations
"""

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_core.prompts import MessagesPlaceholder
from collections import namedtuple
from datetime import datetime


###################
## Custom Errors ##
###################

class ParserError(Exception):
    """Custom exception for parser errors."""
    pass


def validate_response_format(func):
    """
    This decorator handles parser errors and raises a custom exception if the parser fails.
    """
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            if "Input to ChatPromptTemplate is missing variables" in str(e):
                raise ParserError(f"Response is not in the expected JSON format: {e}")
            else:
                raise
    return wrapper


#######################
## JSON Parser Class ##
#######################


class XRecommendations(BaseModel):
    """Explanations for a list of recommended songs"""
    Recommendation = namedtuple("Recommendation", ["song", "artist", "explanation"])
    recommendations: list[Recommendation] = Field(..., title="Recommendations", 
                                                  description="List of songs with artists and reasons.")


#########################
## LLM Wrapper Classes ##
#########################

class LLM():
    def __init__(self, model_type: str = "llama3", debug: bool = True):
        self.debug = debug
        try:
            self.llm = Ollama(model = model_type)
            if self.debug: self._debug(f"Initialized {self.__class__.__name__} with model: {self.llm.model}")
        
        except Exception as e:
            raise Exception(f"Error initializing LLM: {e}")
        
        self.output_parser = StrOutputParser()
        self.system_prompt = ""
    
    def __repr__(self) -> str:
        return f"LLM(model={self.llm.model})"

    def __str__(self) -> str:
        return f"LLM(model={self.llm.model})"
    
    def __call__(self, prompt: str) -> str:
        return self._query(prompt)

    def _set_system_prompt(self, system_prompt: str):
        """
        Set the system prompt for the LLM model.
        """
        self.system_prompt = system_prompt
        if self.debug: 
            self._debug(f"Setting system prompt:\n{self._indent(system_prompt, 2)}")

    def _set_output_parser(self, output_parser: str):
        """
        Set the output parser for the LLM model.
        """
        self.output_parser = output_parser
        if self.debug: 
            self._debug(f"Setting output parser:\n{self._indent(output_parser, 2)}")
    
    def _query(self, prompt: str) -> str:
        """
        Query the LLM model with a given prompt.
        """

        if self.debug: 
            self._debug(f"Querying LLM with User Prompt:\n{self._indent(str(prompt), 2)}")

        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("user", "{input}")
            ])
            chain = prompt | self.llm | self.output_parser
            result = chain.invoke({"input": prompt})
            if self.debug: self._debug(f"Query result:\n{self._indent(str(result), 2)}")
            return result
        
        except Exception as e:
            self._debug(f"Error querying LLM:\n{self._indent(str(e), 2)}")
            return f"Error: {e}"
    
    def _debug(self, message):
        """
        Print debug messages to terminal if debug is enabled.
        """
        if self.debug:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            name = self.__class__.__name__
            address = hex(id(self))
            print(f"\nDEBUG [{timestamp}] ({name} @ {address}):\n{self._indent(message, 2)}\n")
    
    def _indent(self, message: str, level: int = 1, indent: int = 4) -> str:
        """
        Indent a message by a given number of spaces.
        """
        indention = " " * (indent * level)
        return '\n'.join(f"{indention}{line}" for line in str(message).split('\n'))


class RecommendationLLM(LLM):
    def __init__(self, model: str = "llama3", debug: bool = True):
        super().__init__(model, debug)

        with open("src/utils/prompts/recommendation_prompt.txt", "r") as f: 
            system_prompt = f.read().strip() 
        
        self._set_system_prompt(system_prompt)
    

    def __call__(self, top_tracks: str = None, top_artists: str = None, candidate_pool: str = None) -> str:
        """
        Combine multiple inputs into a single prompt and query the LLM model.
        """
        if top_tracks is None: top_tracks = []
        if top_artists is None: top_artists = []
        if candidate_pool is None: candidate_pool = []

        data = {
            "Top Tracks": [{'name': track['name'], 'artist': track['artist']} for track in top_tracks],
            "Top Artists": [{'name': artist['name']} for artist in top_artists],
            "Candidate Pool": [{'name': song['name'], 'artist': song['artist']} for song in candidate_pool]
        }

        prompt = (
            f"User Preferences:\n"
            f"Top Tracks: {data['Top Tracks']}\n"
            f"Top Artists: {data['Top Artists']}\n"
            f"Candidate Pool: {data['Candidate Pool']}\n"
            f"Based on the provided information, please recommend 7 songs from the candidate pool, ensuring a balance of variety and alignment with the user's preferences. "
            f"Explain your selection process step-by-step."
        )

        return self._query(prompt)

class ExplanationLLM(LLM):
    def __init__(self, model: str = "llama3", debug: bool = True):
        super().__init__(model, debug)

        self._set_output_parser(PydanticOutputParser(pydantic_object = XRecommendations))
        
        with open("src/utils/prompts/explanation_prompt.txt", "r") as f:
            system_prompt = f.read().strip()  

        self._set_system_prompt(system_prompt)
        
    
    @validate_response_format
    def _query(self, prompt: str) -> str:
        """
        Query the LLM model with a given prompt, also handles parser errors
        """

        return super()._query(prompt)
        

# test = RecommendationLLM()
# test._set_system_prompt("You are a music recommender and curator")

# print(
#     test("What is your role? What input are you expecting from me?")
# )