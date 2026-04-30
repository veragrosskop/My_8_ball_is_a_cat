from typing import Optional

from openai import OpenAI
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from abc import ABC, abstractmethod


class Client(ABC):
    """This class wraps all AI client functionality, depending on which client is used."""

    _api_key = None
    client = None
    model = None

    def __init__(self, model : str | None = None):
        self.set_api_key()
        if self._api_key:
            self.set_model(model=model)
            self.set_client()

    def get_api_key(self):
        return self._api_key

    @abstractmethod
    def set_api_key(self) -> None:
        """
        Sets the client api key based on the type of client.
        Returns a value Error if it could not find the API key.

        """
        pass

    @abstractmethod
    def set_model(self, model: str | None = None):
        """
        Sets the client model to use.
        :return:
        """
        pass

    @abstractmethod
    def set_client(self) -> None:
        """
        Initializes the client with the given api key.
        :return: None
        """
        pass

    @abstractmethod
    def get_response(self, prompt: str, instruction: str = None) -> str:
        """
        Sends a prompt with instructions to the client and returns the response.

        :param prompt: The prompt to send to the AI Client
        :param instruction: The instruction to send to the AI Client.
        This will indicate how the AI will behave when responding.
        :return: The response text from the client.

        """

        pass


class GenAIClient(Client):
    def __init__(self, model: str | None = None):

        super().__init__(model)

    def set_api_key(self) -> None:
        """
        Sets the client api key based on the type of client.
        Returns a value Error if it could not find the API key.

        """
        load_dotenv(override=True)  # loads .env into environment
        self._api_key = os.getenv("GENAI_API_KEY")

        if not self._api_key:
            raise ValueError("No API key found. Set GENAI_API_KEY in .env")

    def set_model(self, model: str | None = None):
        """
        Sets the client model to use.
        :return:
        """
        #TODO! validate inputs for model
        if model:
            self.model = model
        else:
            self.model = "gemini-3-flash-preview"

    def set_client(self) -> None:
        """
        Initializes the client with the given api key.
        :return:
        """
        self.client = genai.Client(api_key=self._api_key)

    def get_response(self, prompt: str, instruction: str = None) -> str:
        """
        Sends a prompt with instructions to the client and returns the response.
        :param prompt:
        :param instruction:
        :return:
        """
        response = self.client.models.generate_content(
            model=self.model,
            config=types.GenerateContentConfig(
                system_instruction=f"{instruction} Keep it short."),
            contents=prompt
        )
        return response.text

class OpenAIClient(Client):
    def __init__(self, model: str | None = None):
        super().__init__(model)

    def set_api_key(self) -> None:
        """
        Sets the client api key based on the type of client.
        Returns a value Error if it could not find the API key.

        """
        load_dotenv(override=True)  # loads .env into environment
        self._api_key = os.getenv("OPENAI_KEY")

        if not self._api_key:
            raise ValueError("No API key found. Set OPENAI_API_KEY in .env")

    def set_model(self, model: str | None = None):
        """
        Sets the client model to use.
        :return:
        """
        #TODO! validate inputs for model
        if model:
            self.model = model
        else:
            self.model = "gpt-5.4"

    def set_client(self) -> None:
        """
        Initializes the client with the given api key.
        :return:
        """

        self.client = OpenAI(api_key=self._api_key)

    def get_response(self, prompt: str, instruction: str = None) -> str:
        """
        Sends a prompt with instructions to the client and returns the response.
        :param prompt:
        :param instruction:
        :return:
        """

        response = self.client.responses.create(
            model=self.model,
            instructions=f"{instruction} Keep it short.",
            input=prompt
        )

        return response.output_text
