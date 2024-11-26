# queue_client.py

import asyncio
import base64
import concurrent.futures
import http
import json
import os
from urllib.parse import unquote

import kryon_config_client
import nintex_queue
import nintex_secrets

from clients.data_client.src import DataClient

from .consumers.utils import timer


def get_config():
    config_path = os.path.join(os.getcwd(), "service", "config.json")
    with open(config_path, "r") as config_file:
        return json.load(config_file)


class ConsumerClient:
    def __init__(self, project_name, module):
        secrets_provider = nintex_secrets.init()
        config = get_config()

        # Initialize queue
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
        self.queue_client.prepare_consumer(on_message_func=self.on_message, consumer_name=project_name)

        self.project = project_name
        self.module = module
        self.data_client = DataClient(config=config)

    # Fetches the task from the module
    def task_handler(self, task_name):
        if hasattr(self.module, task_name):
            task_func = getattr(self.module, task_name)
            return task_func
        else:
            print(f"Task {task_name} not found in test_queue")

    def handle_input(self, message):
        input_data = message.get("input", None)
        if input_data:
            try:
                input_data = unquote(base64.b64decode(input_data).decode("utf-8"))
                input_data = json.loads(input_data)
                message["input"] = input_data

                return input_data
            except Exception as e:
                raise ("[Consumer] Error decoding input data: " + str(e))

        return {}

    def on_message(self, message):
        try:
            # Retrieve input from message
            input = self.handle_input(message)

            # Execute the task
            task_name = message.get("taskName")
            if task_name:
                func = timer(self.task_handler(task_name))

                inference_time, output = func(**input)
            else:
                raise ("Task name not in message")

        except Exception as e:
            output = {
                "code": http.HTTPStatus.INTERNAL_SERVER_ERROR,
                "value": str(e),
                "raw_output": output["raw_output"] if "raw_output" in output else "error",
            }

            func.data["output_type"] = "error"

        asyncio.run(
            self.data_client.upload_entry(
                project=self.project,
                message_data=message,
                output=output,
                func_data=func.data,
                inference_time=inference_time,
            )
        )

        return message


async def infinite_loop():
    while True:
        await asyncio.sleep(999)
