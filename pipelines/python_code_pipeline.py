from typing import List, Union, Generator, Iterator
import subprocess

import requests


class Pipeline:
    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "python_code_pipeline"
        self.name = "Custom Agents Router"
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def pipe(
            self,
            user_message: str,
            model_id: str,
            messages: List[dict],
            body: dict) -> Union[str, Generator, Iterator]:

        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")
        print(user_message)
        print(model_id)
        print(messages)
        print(body)

        url = "http://host.docker.internal:5000/agent/007"
        json_data = {
            "user_message": user_message,
            "model_id": model_id,
            "messages": messages,
            "body": body
        }

        try:
            response = requests.post(url, json=json_data)
            response.raise_for_status()

            # Parse JSON response into a Python dict
            data = response.json()

            # Extract the "message" field
            message_value = data.get("message")

            return message_value

        except requests.exceptions.RequestException as e:
            return f"{e}"
