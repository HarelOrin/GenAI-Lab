import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))

from projects.src.BaseTask import BaseTask

from .form_consts import PRESENT_SCHEMA


class get_schema(BaseTask):
    def __init__(self, skuid_client):
        """
        Initiazes the get_schema task
        Dependencies:
            get_schema (str) -> dict
                input: user_peompt (str)
                output: response_schema (dict)
        """
        super().__init__(
            task_name="get_schema",
            project_name="skuid_app_generator",
            output_type="form",
            data_type="json",
            is_raw_output_file=False,
        )

        self.get_schema = skuid_client.get_schema

    async def execute(self, user_prompt: str) -> dict:
        """
        executes the get_schema function
        args:
            user_peompt (str): user's case for incident management app schema
        returns:
            response_schema (dict): response schema
            original_prompt (str): original prompt
        """
        response_schema = await self.get_schema(user_prompt)

        original_prompt = user_prompt

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
