import base64
import http
import json
import logging
from urllib.parse import quote

logger = logging.getLogger()


class BaseTask:
    def __init__(
        self,
        task_name: str,
        project_name: str,
        output_type: str,
        data_type: str,
        is_raw_output_file: bool,
        file_suffix: str = None,
    ):
        self.task_name = task_name
        self.project_name = project_name
        self.data = {
            "output_type": output_type,
            "data_type": data_type,
            "is_raw_output_file": is_raw_output_file,
            "file_suffix": file_suffix,
        }
        logger.debug(f"Initialized {self.task_name} of {self.project_name}")

    async def __call__(self, *args, **kwargs) -> dict:
        try:
            input_data = self._handle_input(kwargs)
            result = await self.execute(**input_data)
            logger.debug(f"[{self.task_name}] Executed successfully")

            if self.data["output_type"] == "form":
                raw, output = self.build_dynamic_form(*result)
            else:
                raw, output = self._format_output(result, self.data["data_type"])

            response = {"code": http.HTTPStatus.OK, "value": output, "raw_output": raw}
            return response
        except Exception as e:
            logger.error(f"Error in {self.project_name}: {e}")
            raise Exception(f"Error in {self.project_name}: {e}")

    async def execute(self, *args, **kwargs):
        logger.error(f"Task {self.task_name} not implemented in {self.project_name}")
        raise NotImplementedError(f"Task {self.task_name} not implemented in {self.project_name}")

    def build_dynamic_form(self, *args, **kwargs) -> tuple:
        raise NotImplementedError("build_dynamic_form() must be implemented in a subclass")

    def _handle_input(self, input_data: dict) -> dict:
        if input_data:
            try:
                func_input = {}
                for key, value in input_data.items():
                    if isinstance(value, dict) and "value" in value:
                        if value.get("type") == "File upload":
                            func_input[key] = base64.b64decode(value.get("value"))
                        else:
                            func_input[key] = value.get("value")
                    else:
                        func_input[key] = value

                return func_input
            except Exception as e:
                raise (f"Error in {self.task_name} decoding input data: {e}")

        return {}

    def _format_output(self, result, data_type: str) -> tuple:
        match data_type:
            case "text":
                return result, result
            case "bpmn":
                encoded_result = self._encode_base64(result)
                return encoded_result, encoded_result
            case "link":
                if isinstance(result, dict):
                    return result["link"]
                else:
                    return result, result

    def _encode_base64(self, data) -> str:
        if isinstance(data, str) or isinstance(data, bytes) or isinstance(data, bytearray):
            return base64.b64encode(quote(data).encode()).decode("utf-8")
        elif isinstance(data, dict):
            return base64.b64encode(json.dumps(data).encode()).decode("utf-8")
        else:
            raise ValueError("Unsupported data type for encoding to base64")

    def _decode_base64(self, data: str):
        data = base64.b64decode(data).decode("utf-8")
        if data.startswith("{") or data.startswith("["):
            return json.loads(data)
        return data
