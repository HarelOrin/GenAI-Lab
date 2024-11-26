import asyncio
import importlib.util
import inspect
import sys
from pathlib import Path

import kryon_config_client
import nintex_secrets

from clients.queue_client.src.consumer_client import ConsumerClient, infinite_loop

secrets_provider = nintex_secrets.init()
config_client = kryon_config_client.init(secrets_provider=secrets_provider)
from projects.src.ntx_lab_diagram_ingestion import diagram_ingestion
from projects.src.ntx_lab_process_capture import process_capture

# sys.path.insert(0, str(Path.cwd() / "projects" / "src"))
from projects.src.ntx_lab_process_structure import process_structure
from projects.src.ntx_lab_skuid_app_generator import skuid_app_generator

# worker_projects = [
#     "process_structure",
#     "skuid_app_generator",
#     "process_capture",
#     "diagram_ingestion",
# ]

# def serve_tasks():

#     modules = []

#     original_sys_path = sys.path.copy()

#     for project_name in worker_projects:
#         directory_name = "ntx_lab_" + project_name
#         module_path = Path.cwd() / "projects" / 'src' / directory_name
#         sys.path.insert(0, str(module_path))
#         my_module = importlib.import_module(project_name)
#         modules.append(my_module)
#         sys.path[:] = original_sys_path
#         print(modules)

#     initiated_clients = []

#     for my_module in modules:
#         if "config_client" in inspect.signature(my_module.init).parameters:
#             secrets_provider = nintex_secrets.init()
#             config_client = kryon_config_client.init(secrets_provider=secrets_provider)
#             initiated_client = my_module.init(config_client)
#         else:
#             initiated_client = my_module.init()
#         initiated_clients.append(initiated_client)

#     # Init the modules gathered to initiate tasks
#     tasks_dict = {}
#     for initiated_client in initiated_clients:
#         tasks_dict.update(initiated_client)

#     return tasks_dict

project_dict = {
    "process_structure": process_structure,
    "skuid_app_generator": skuid_app_generator,
    "process_capture": process_capture,
    "diagram_ingestion": diagram_ingestion,
}

def get_module(module_name):
    
    module = project_dict[module_name] 
    initiated_client = module.init()
    return initiated_client


if __name__ == "__main__":

    current_module = get_module('skuid_app_generator') # change project name here

    client = ConsumerClient("first", current_module)
    try:
        print("Starting consumer loop...")
        asyncio.run(client.loop.run_until_complete(infinite_loop()))
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        pass
