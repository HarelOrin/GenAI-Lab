from datetime import datetime

from clients.cache_client.src import CacheClient
from clients.file_client.src import FileClient

from .providers import DbBaseProvider


def _get_db_provider(config: dict) -> DbBaseProvider:
    from . import providers

    provider_name = config["database_provider"]
    provider = getattr(providers, provider_name)
    return provider.init(config[provider_name])


class DataClient:
    def __init__(self, config: dict):
        self._provider = _get_db_provider(config=config)
        self.cache_client = CacheClient()
        self.file_client = FileClient()

    async def get_output(self, workflow_id: str, step: str) -> dict:
        return await self._provider.get_output(workflow_id=workflow_id, step=step)

    async def upload_entry(
        self, project: str, message_data: dict, output: dict, func_data: dict, inference_time: float
    ):
        unique_id = f"{message_data['workflowID']}/{message_data['taskName']}"
        data = {
            "project": project,
            "step": message_data.get("taskName"),
            "workflow_id": message_data.get("workflowID"),
            "output_type": func_data["output_type"],
        }

        # Separate function to handle input and output processing
        upload_output = await self.handle_input_and_output(
            message_data.get("input"), output, func_data, unique_id, self.file_client
        )

        # Build Entry
        data["input"] = message_data.get("input")  # Input has been modified directly
        data["output"] = upload_output
        data["inference_time"] = inference_time
        data["created_at"] = str(datetime.utcnow())
        data["updated_at"] = str(datetime.utcnow())

        code = await self._provider.upload_entry(data=data, code=output["code"])
        await self.cache_client.set_status(workflow_id=data["workflow_id"], step=data["step"], code=code)

    async def handle_input_and_output(
        self, input_data: dict, output: dict, func_data: dict, unique_id: str, file_client
    ) -> dict:
        # Manage file uploads
        for key, value in input_data.items():
            if value["type"] == "File upload":
                file_bytes = value["value"]
                path = await file_client.upload(file_bytes, key, value["extension"], unique_id)
                value["value"] = path

        # Manage output
        upload_output = {
            "value": output["value"],
            "data_type": func_data["data_type"],
        }

        if func_data["is_raw_output_file"] and output["raw_output"] != "error":
            output_file = await file_client.upload(
                output["raw_output"], input_data.get("taskName"), func_data["file_suffix"], unique_id
            )
            output["raw_output"] = "file"

            upload_output["file"] = func_data["is_raw_output_file"]
            upload_output["file_path"] = output_file

        if func_data["data_type"] == "tuple":
            for key, value in output["raw_output"].items():
                if value["is_file"]:
                    file_bytes = value["value"]
                    path = await file_client.upload(file_bytes, key, value["data_type"], unique_id)
                    value["value"] = path

        upload_output["raw_output"] = output["raw_output"]

        return upload_output

    async def upload_project(self, data: dict):
        await self._provider.upload_project(data=data)

    async def get_project(self, id: str = None) -> list[dict]:
        return await self._provider.get_project(id=id)

    async def send_feedback(
        self,
        requestId: str,
        feedbackType: str,
        description: str = None,
        email: str = None,
    ):
        await self._provider.send_feedback(
            requestId=requestId,
            feedbackType=feedbackType,
            description=description,
            email=email,
        )

    async def upload_result(self, data: dict):
        # @param data: {filename: str, file_bytes: str}
        new_data = data.copy()
        new_data["timestamp"] = str(datetime.utcnow())
        await self._provider.upload_result(data=new_data)

    async def upload_input(self, data: dict):
        new_data = data.copy()
        new_data["timestamp"] = str(datetime.utcnow())
        await self._provider.upload_input(data=new_data)

    async def get_result(self, request_id: str = None) -> dict:
        return await self._provider.get_result(request_id=request_id)
