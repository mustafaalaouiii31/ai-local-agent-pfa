"""
LLM Client

Handles communication with the local Ollama server.
"""

import ollama
import logging
from time import perf_counter


class LLMClient:
    """
    Client used to communicate with a local LLM through Ollama.
    """

    def __init__(self, model_name: str = "llama3.2"):
        """
        Initialize the LLM client.

        Parameters
        ----------
        model_name : str
            Name of the Ollama model.
        """

        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to the local LLM.

        Parameters
        ----------
        prompt : str
            Prompt sent to the model.

        Returns
        -------
        str
            Generated response.
        """

        started = perf_counter()
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        logging.getLogger(__name__).info(
            "[PERF] Ollama: %.3fs", perf_counter() - started
        )
        return response["message"]["content"]
