import asyncio
import concurrent.futures
import http
import json
import os
import sys
import time
import uuid
from types import SimpleNamespace

import kryon_config_client
import nintex_queue
import nintex_secrets

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from clients.cache_client.src.client import CacheClient


class QueueClient:
    def __init__(self):
        secrets_provider = nintex_secrets.init()

        self.config_client = kryon_config_client.init(secrets_provider=secrets_provider)
        self.loop = asyncio.get_event_loop()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

        self.queue_client = nintex_queue.init(
            config_client=self.config_client,
            loop=self.loop,
            executor=self.executor,
            cache_client=None,
            provider="rabbitmq_pika",
        )

        self.cache_client = CacheClient()
        self.publisher = self.queue_client.prepare_publisher(publisher_name="gai-lab")

    def format_message(self, task_name, workflow_id, input_data):
        message = {"taskName": task_name, "workflowID": workflow_id, "input": input_data}
        return message

    async def upload_message(self, project_name, task_name, input_data, workflow_id=None):
        workflow_id = str(uuid.uuid4()) if workflow_id is None else workflow_id
        try:
            message = self.format_message(task_name, workflow_id, input_data)
            self.publisher.publish(message=message, queue=project_name)
            status = http.HTTPStatus.ACCEPTED
            response = "ACCEPTED"
        except Exception as e:
            status = {
                "value": http.HTTPStatus.INTERNAL_SERVER_ERROR.value,
                "error": f"Error uploading message: {e}",
            }
            response = str(e)

        await self.cache_client.set_status(workflow_id=workflow_id, step=task_name, code=status)
        return status, response, workflow_id


# Usage example
if __name__ == "__main__":
    inputs = [
        {
            "project_name": "TestQueue",
            "task_name": "ExampleTask1",
            "request_id": str(uuid.uuid4()),
            "input_data": {"key1": "value1", "key2": "value2"},
        },
        {
            "project_name": "TestQueue",
            "task_name": "ExampleTask2",
            "request_id": str(uuid.uuid4()),
            "input_data": {"key1": "value1", "key2": "value2"},
        },
        {
            "project_name": "AnotherQueue",
            "task_name": "DifferentTask",
            "request_id": str(uuid.uuid4()),
            "input_data": {"key3": "value3", "key4": "value4"},
        },
    ]

    client = QueueClient()

    for input in inputs:
        time.sleep(5)

        status, response, request_id = asyncio.run(
            client.upload_message(input["project_name"], input["task_name"], input["input_data"])
        )
        print(
            f"Uploaded message to {input['project_name']} queue with task name {input['task_name']} - Status: {status}, Response: {response}, Request ID: {request_id}"
        )
