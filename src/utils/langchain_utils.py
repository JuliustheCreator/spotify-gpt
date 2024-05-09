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




class XRecommendations(BaseModel):
    """Explanations for a list of recommended songs"""
    Recommendation = namedtuple("Recommendation", ["song", "artist", "explanation"])
    recommendations: list[Recommendation] = Field(..., title="Recommendations", 
                                                  description="List of songs with artists and reasons.")

class LLM():
    def __init__(self, model = "llama2"):
        self.llm = Ollama(model)

        # This uses the StrOutputParser to convert the output to a string.
        self.output_parser = StrOutputParser()
        self.system_prompt = ""
    
    def __repr__(self) -> str:
        return f"LLM(model={self.llm.model})"

    def __str__(self) -> str:
        return f"LLM(model={self.llm.model})"
    
    def __call__(self, prompt) -> str:
        return self.__query(prompt)

    def _set_system_prompt(self, system_prompt):
        """
        Set the system prompt for the LLM model.
        """
        self.system_prompt = system_prompt

    def _set_output_parser(self, output_parser):
        """
        Set the output parser for the LLM model.
        """
        self.output_parser = output_parser
    
    def _query(self, prompt) -> str:
        """
        Query the LLM model with a given prompt.
        """
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("user", prompt)
            ])
            chain = prompt | self.llm | self.output_parser
            return chain.invoke({"input": prompt})
        
        except Exception as e:
            return f"Error: {e}"


class RecommendationLLM(LLM):
    def __init__(self, model = "llama2"):
        super().__init__(model)

        with open("src/utils/prompts/recommendation_prompt.txt", "r") as f:
            system_prompt = f.read() 
        
        self.__set_system_prompt(system_prompt)


class ExplanationLLM(LLM):
    def __init__(self, model = "llama2"):
        super().__init__(model)

        # This uses the PydanticOutputParser to convert the output to an XRcommendations object.
        self._set_output_parser(PydanticOutputParser(pydantic_object = XRecommendations))
        
        with open("src\utils\prompts\explanation_prompt.txt", "r") as f:
            system_prompt = f.read() 

        self._set_system_prompt(system_prompt)