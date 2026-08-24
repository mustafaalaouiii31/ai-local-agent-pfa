"""
Ollama Client

Communicates with the local LLM through Ollama.
"""

import ollama


class OllamaClient:
    """
    Client responsible for communicating
    with the local Ollama model.
    """

    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.1
    ):
        """
        Initialize the Ollama client.

        Parameters
        ----------
        model_name : str
            Name of the local Ollama model.

        temperature : float
            Controls the randomness of the model.
            A low value is preferred for a RAG/document agent.
        """

        self.model_name = model_name
        self.temperature = temperature

    # ==========================================================
    # GENERATE
    # ==========================================================

    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Send a prompt to Ollama and return the response.
        """

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        try:

            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": self.temperature
                }
            )

            return response[
                "message"
            ][
                "content"
            ].strip()

        except Exception as e:

            raise RuntimeError(
                f"Erreur lors de la communication avec "
                f"Ollama : {e}"
            ) from e