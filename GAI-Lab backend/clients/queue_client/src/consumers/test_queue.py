import asyncio
import http
import sys
import time

from utils import task_data

from clients.queue_client.src.consumer_client import ConsumerClient, infinite_loop

# Get a reference to the current module
current_module = sys.modules[__name__]


@task_data(output_type="artifact", data_type="text", is_raw_output_file=False)
def ExampleTask1(key1=None, key2=None):
    print("waiting for a while")
    time.sleep(3)
    print(f"Executing ExampleTask1 with key1={key1} and key2={key2}")
    response = {"code": http.HTTPStatus.OK, "value": "test output lorem ipsum", "raw_output": "test output lorem ipsum"}
    return response


def ExampleTask2(key1=None, key2=None):
    print(f"Executing ExampleTask2 with key1={key1} and key2={key2}")


def ExampleTask3(key1=None, key2=None):
    print(f"Executing ExampleTask3 with key1={key1} and key2={key2}")


if __name__ == "__main__":
    client = ConsumerClient("first", current_module)
    try:
        print("Starting consumer loop...")
        asyncio.run(client.loop.run_until_complete(infinite_loop()))
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        pass
