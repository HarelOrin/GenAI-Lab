import base64
import binascii
import dataclasses
import http
from functools import partial
from typing import Callable

from clients.cache_client import CacheClient
from clients.data_client import DataClient
from clients.file_client import FileClient


@dataclasses.dataclass(frozen=True)
class CoreResolver:
    get_project: Callable
    get_result: Callable
    send_feedback: Callable
    ping_response: Callable


def jsonize(data: dict or list):
    if isinstance(data, dict):
        for field, value in data.items():
            if isinstance(value, bytes):
                try:
                    # Encode bytes as base64
                    encoded_value = base64.b64encode(value).decode("utf-8")
                    data[field] = encoded_value
                except (binascii.Error, UnicodeDecodeError):
                    # Ignore errors, as the field may not be valid base64-encoded bytes
                    pass
            elif isinstance(value, dict) or isinstance(value, list):
                # Recursively apply the transformation to nested dictionaries or lists
                jsonize(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            jsonize(item)


async def _get_project_impl(data_client: DataClient, id: str = None, token_data=False) -> list[dict]:
    data = await data_client.get_project(id=id)
    roles = token_data.get("realm_access").get("roles") if token_data else []
    filtered_data = []
    for doc in data:
        clearance = doc.get("clearance", 0)
        if clearance == 2 and "unreleased-approved" not in roles and "admin-access" not in roles:
            continue
        elif clearance == 1 and "internal-approved" not in roles and "admin-access" not in roles:
            continue
        jsonize(data=doc)
        filtered_data.append(doc)
    return filtered_data


async def _get_result_impl(file_client: FileClient, file_path: str):
    parts = file_path.rsplit("/", 1)  # Split the path at the last '/' to separate tenant_id and key.ext
    if len(parts) != 2:
        raise ValueError("The path format is incorrect. Expected format: 'tenant_id/key.doc_type'")

    tenant_id = parts[0]  # tenant_id is everything before the last '/'
    key_with_ext = parts[1]  # key with file extension
    key, doc_type = key_with_ext.rsplit(".", 1)
    file_base64 = file_client.download(key=key, doc_type=doc_type, tenant_id=tenant_id)
    if file_base64.startswith('"') and file_base64.endswith('"'):
        file_base64 = file_base64[1:-1]
    resp = {"file": file_base64, "filename": key_with_ext}
    jsonize(data=resp)
    return resp


async def _send_feedback_impl(
    data_client: DataClient,
    requestId: str,
    feedbackType: str,
    description: str = None,
    email: str = None,
):
    try:
        await data_client.send_feedback(
            requestId=requestId,
            feedbackType=feedbackType,
            description=description,
            email=email,
        )
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def _ping_response_impl(cache_client: CacheClient, data_client: DataClient, workflow_id: str, step: str):
    response = {"status": None, "workflow_id": workflow_id, "step": step}

    try:
        res = await cache_client.check_status(workflow_id=workflow_id, step=step)
        code = res.get("code")
        response["status"] = code

        match code:
            case http.HTTPStatus.ACCEPTED.value | http.HTTPStatus.PROCESSING.value:
                pass
            case http.HTTPStatus.OK.value:
                response["output"] = await data_client.get_output(workflow_id=workflow_id, step=step)
            case _:
                response["error"] = res.get("error")
    except Exception as e:
        response["status"] = http.HTTPStatus.INTERNAL_SERVER_ERROR.value
        response["error"] = str(e)

    return response


def init(config: dict):
    data_client = DataClient(config=config)
    file_client = FileClient()
    cache_client = CacheClient()
    return CoreResolver(
        **{
            "get_project": partial(_get_project_impl, data_client),
            "get_result": partial(_get_result_impl, file_client),
            "send_feedback": partial(_send_feedback_impl, data_client),
            "ping_response": partial(_ping_response_impl, cache_client, data_client),
        }
    )
