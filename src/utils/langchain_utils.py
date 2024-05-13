"""
This module provides a wrapper class for the LLM model from the langchain_community package.

The LLM class provides a wrapper for the Ollama class from the langchain_community package. The class provides a simple interface for querying the LLM model with a given prompt. The class also provides a method for setting the system prompt for the LLM model.

Classes:
    LLM: A wrapper class for the LLM
    RecommendationLLM: A wrapper class for the LLM for music recommendations
    ExplanationLLM: A wrapper class for the LLM for explaining music recommendations
"""

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from collections import namedtuple



"""
Below are additional classes and functions that are used in the LLM wrapper classes.
"""

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

class XRecommendations(BaseModel):
    """Explanations for a list of recommended songs"""
    Recommendation = namedtuple("Recommendation", ["song", "artist", "explanation"])
    recommendations: list[Recommendation] = Field(..., title="Recommendations", 
                                                  description="List of songs with artists and reasons.")

"""
Below are the LLM wrapper classes that provide a simple interface for querying the LLM model.
"""

class LLM():
    def __init__(self, model_type: str = "llama3", debug: bool = True):
        try:
            self.llm = Ollama(model = model_type)
        
        except Exception as e:
            raise Exception(f"Error initializing LLM: {e}")
        
        self.output_parser = StrOutputParser()
        self.system_prompt = ""
        self.debug = debug
    
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
        self._debug(f"Setting system prompt: {system_prompt}")
        self.system_prompt = system_prompt

    def _set_output_parser(self, output_parser: str):
        """
        Set the output parser for the LLM model.
        """
        self._debug(f"Setting output parser: {output_parser}")
        self.output_parser = output_parser
    
    def _query(self, prompt: str) -> str:
        """
        Query the LLM model with a given prompt.
        """
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("user", prompt)
            ])
            chain = prompt | self.llm | self.output_parser
            result = chain.invoke({"input": prompt})
            self._debug(f"Query result: {result}")
            return result
        
        except Exception as e:
            self._debug(f"Error querying LLM: {e}")
            return f"Error: {e}"
    
    def _debug(self, message):
        """
        Print debug messages to terminal if debug is enabled.
        """
        if self.debug:
            print(f"DEBUG: {message}")


class RecommendationLLM(LLM):
    def __init__(self, model = "llama2"):
        super().__init__(model)

        with open("src/utils/prompts/recommendation_prompt.txt", "r") as f:
            system_prompt = f.read() 
        
        self._set_system_prompt(system_prompt)


class ExplanationLLM(LLM):
    def __init__(self, model = "llama2"):
        super().__init__(model)

        self._set_output_parser(PydanticOutputParser(pydantic_object = XRecommendations))
        
        with open("src/utils/prompts/explanation_prompt.txt", "r") as f:
            system_prompt = f.read() 

        self._set_system_prompt(system_prompt)
    
    @validate_response_format
    def _query(self, prompt: str) -> str:
        """
        Query the LLM model with a given prompt, also handles parser errors
        """
        return super()._query(prompt)