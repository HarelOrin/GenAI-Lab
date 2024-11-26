import asyncio
import sys

from clients.queue_client.src.consumer_test import ConsumerClient, infinite_loop

# Get a reference to the current module
current_module = sys.modules[__name__]


def task_handler(task_name, input_data):
    if hasattr(current_module, task_name):
        task_func = getattr(current_module, task_name)
        task_func(**input_data)
    else:
        print(f"Task {task_name} not found in test_queue")


def DifferentTask(key3=None, key4=None):
    print(f"Executing ExampleTask1 with key1={key3} and key2={key4}")


if __name__ == "__main__":
    client = ConsumerClient("second", task_handler)
    try:
        asyncio.run(client.loop.run_until_complete(infinite_loop()))
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        pass
