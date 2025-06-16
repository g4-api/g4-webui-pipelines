import json
import os
import requests
from typing import List, Union, Generator, Iterator


class Pipeline:
    def __init__(self) -> None:
        # ── Configuration ─────────────────────────────────────────────────────────
        self.name: str = os.getenv("PIPELINE_NAME", "Custom MCP Router")
        self.agent_url: str = os.getenv(
            "AGENT_URL",
            "http://host.docker.internal:9955/api/v4/g4/mcp/completions"
        )
        self.stream: bool = os.getenv("PIPELINE_CHAT_MODE", "BULK").upper() == 'STREAM'

    # ── Lifecycle hooks ──────────────────────────────────────────────────────────
    async def on_startup(self) -> None:
        print(f"on_startup: {__name__}")

    async def on_shutdown(self) -> None:
        print(f"on_shutdown: {__name__}")

    # ── Main entry point ─────────────────────────────────────────────────────────
    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[dict],
        body: dict
    ) -> Union[str, Generator, Iterator]:
        """
        Forward the conversation context to an external agent (HTTP service)
        and return its reply back to Open-WebUI.
        """
        # Force non-streaming mode
        body["stream"] = False

        # Log incoming body
        print('------------------- BODY -----------------------')
        print(json.dumps(body, indent=4))
        print('------------------- BODY END -------------------\n')

        # Prepare request for external MCP server
        json_data = {
            "chat_id": body.get("chat_id"),
            "session_id": body.get("session_id"),
            "user_message": user_message,
            "model": model_id,
            "messages": messages,
            "body": body
        }

        print('------------------- REQUEST --------------------')
        print(json.dumps(json_data, indent=4))
        print('------------------- REQUEST END ----------------\n')

        try:
            response = requests.post(self.agent_url, json=json_data)
            response.raise_for_status()
            data = response.json()

            for choice in data.get("choices", []):
                message = choice.get("message", {})
                if "annotations" in message:
                    message.pop("annotations")

            print('------------------- RESPONSE -------------------')
            print(json.dumps(data, indent=4))
            print('------------------- RESPONSE END ---------------\n')

            print('[✅ RETURNING TO OPEN-WEBUI]')
            print(json.dumps(data, indent=2))
            return data

        except requests.exceptions.RequestException as exc:
            print('[❌ MCP SERVER ERROR]', str(exc))
            return str(exc)
