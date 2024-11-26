import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))

from projects.src.BaseTask import BaseTask

from .form_consts import PRESENT_SCHEMA


class update_schema(BaseTask):
    def __init__(self, skuid_client):
        """
        Initiazes the update_schema task
        Dependencies:
            update_schema (str) -> dict : updates the app schema by user prompt
                input: user_peompt (str)
                input: response (dict)
                input: messages_array (list)
                inpuut: original_prompt (str)
                output: response_schema (dict)
        """
        super().__init__(
            task_name="update_schema",
            project_name="skuid_app_generator",
            output_type="form",
            data_type="json",
            is_raw_output_file=False,
        )

        self.update_schema = skuid_client.update_schema

    async def execute(self, user_prompt: str, response, messages_array, original_prompt) -> dict:
        """
        Regenerate the app schema by user prompt
        Dependencies:
            get_schema(user_prompt: str) -> dict
        """

        response_schema = await self.update_schema(user_prompt, response, messages_array)

        return response_schema, original_prompt

    def build_dynamic_form(self, response_schema: dict, original_prompt: str) -> dict:

        OriginalPrompt = {
            "type": "Text-Short",
            "name": "OriginalPrompt",
            "value": original_prompt,
        }

        Response = {
            "type": "Text-Short",
            "name": "Response",
            "value": response_schema["response"],
        }

        MessagesArray = {
            "type": "Text-Short",
            "name": "MessagesArray",
            "value": response_schema["messages_array"],
        }

        schema_results = (
            {
                "type": "Text-Display",
                "title": "Schema:",
                "description": response_schema["response"],
            },
        )

        full_form = PRESENT_SCHEMA
        form = full_form["input"]["properties"]
        form["invisSection"]["properties"]["OriginalPrompt"] = OriginalPrompt
        form["invisSection"]["properties"]["Response"] = Response
        form["invisSection"]["properties"]["MessagesArray"] = MessagesArray
        form["schema_results"] = schema_results

        return response_schema, full_form
