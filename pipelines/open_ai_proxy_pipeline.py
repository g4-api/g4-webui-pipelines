import json
from typing import List, Union, Generator, Iterator
import os
import requests


class Pipeline:
    def __init__(self) -> None:
        # ── Configuration ─────────────────────────────────────────────────────────
        # Read the pipeline name from the environment; default to a safe fallback.
        self.name: str = os.getenv("PIPELINE_NAME", "Custom MCP Router")

        # Read the agent endpoint from the environment; default to a local URL.
        # Using env-vars keeps code generic and avoids hard-coding secrets.
        self.agent_url: str = os.getenv(
            "AGENT_URL",
            "http://host.docker.internal:9955/api/v4/g4/mcp/completions")

        self.stream: bool = os.getenv("PIPELINE_CHAT_MODE", "BULK").upper() == 'STREAM'

    # ── Lifecycle hooks ──────────────────────────────────────────────────────────
    async def on_startup(self) -> None:
        """Runs once when the server (that hosts this pipeline) starts up."""
        print(f"on_startup: {__name__}")

    async def on_shutdown(self) -> None:
        """Runs once when the server is shutting down."""
        print(f"on_shutdown: {__name__}")

    # ── Main entry point ─────────────────────────────────────────────────────────
    def pipe(
        self,
        user_message: str,          # Latest message from the user
        model_id: str,              # Model that should handle the request
        messages: List[dict],       # Full chat history in Open-WebUI format
        body: dict                  # Raw JSON body from the request
    ) -> Union[str, Generator, Iterator]:
        """
        Forward the conversation context to an external agent (HTTP service)
        and return its reply back to Open-WebUI.

        The return value can be:
            • str         → immediate assistant reply
            • Generator   → streaming chunks
            • Iterator    → streaming chunks
        """

        #body['stream'] = False

        # ── Invoke external agent ───────────────────────────────────────────────
        try:
            json_data = {
                "chat_id": body.get('chat_id'),
                "session_id": body.get('session_id'),
                "user_message": user_message,
                "model": model_id,
                "messages": messages,
                "body": body,
            }

            response = requests.post(self.agent_url, json=json_data)

            # Raise for HTTP errors (4xx / 5xx)
            response.raise_for_status()

            # Parse JSON response; we expect a dict with "message" inside.
            data = response.json()

            # TODO: Remove on production
            print('------------------- BODY -----------------------')
            print(json.dumps(body, indent=4))
            print('------------------- BODY END -------------------\n\n')

            print('------------------- REQUEST --------------------')
            print(json.dumps(json_data, indent=4))
            print('------------------- REQUEST END ----------------\n\n')

            print('------------------- RESPONSE -------------------')
            print(json.dumps(data, indent=4))
            print('------------------- RESPONSE END ---------------\n\n')

            # Forward agent's reply to the UI.
            return data

        except requests.exceptions.RequestException as exc:
            # Network / HTTP problem → return error text so the UI can show it.
            return str(exc)
