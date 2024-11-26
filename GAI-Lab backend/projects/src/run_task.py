import asyncio
import base64
import importlib.util
import inspect
import sys
from pathlib import Path

import kryon_config_client
import nintex_secrets

from projects.src.default_inputs.example_inputs import inputs


def ready_file(file_path):
    try:
        with open(file_path, "rb") as file: return file.read()
    except Exception as e:
        return f"Error: {e}"


# ================== Replace the following values ==================
project_name = "process_capture"
task_name = "generate_process_text"
# --- Inputs: ---
# Seperated the long inputs to default_inputs/example_inputs file for readability.
input_dict = {
    "diagram_ingestion": {
        "tag_metrics": {
            "VisioDiagram": ready_file(r"C:\Users\OrinH\OneDrive - Nintex\Documents\GAI Lab examples\xor_example_01.vsdx")
        },
        "convert_visio_to_bpmn": {
            "VisioDiagram": ready_file(r"C:\Users\OrinH\OneDrive - Nintex\Documents\GAI Lab examples\xor_example_01.vsdx"),
            "orthogonal": "exclusiveGateway"
        }
    },
    "process_structure": {
        "apply_structure": {
            "ProcessDescription": "Give me a random process",
            "guidelines_flavor": "Griffith"
        }
    },
    "process_capture": {
        "describe_process_activities": {
            "RecordingFile": ready_file(r"C:\Users\OrinH\OneDrive - Nintex\Documents\GAI Lab examples\changeDetiles.sqlite"),
            "RoleName": "RoleNameTest",
            "ProcessName": "ProcessNameTest",
            "AnalysisMethod": "Vision LLM"
        },
        "generate_process_text": inputs['process_capture']['generate_process_text']
    },
    "skuid_app_generator": 
    {
        "get_schema": {
            "user_prompt": "UFO sighting"
        },
        "update_schema": {
            "user_prompt": "add field name threat_level as a PICKLIST",
            "response": inputs['skuid_app_generator']['update_schema']['response'],
            "messages_array": inputs['skuid_app_generator']['update_schema']['messages_array'],
            "original_prompt": "UFO sighting"
        },
        "generate_app": {
            "schema": inputs['skuid_app_generator']['update_schema']['response']
        }
    }
    
}
# ===================================================================


directory_name = "ntx_lab_" + project_name
module_path = Path(__file__).parent / directory_name
sys.path.insert(0, str(module_path))
my_module = importlib.import_module(project_name)
sys.path.pop(0)

async def run_task():

    if "config_client" in inspect.signature(my_module.init).parameters:
        secrets_provider = nintex_secrets.init()
        config_client = kryon_config_client.init(secrets_provider=secrets_provider)
        initiated_client = my_module.init(config_client)
    else:
        initiated_client = my_module.init()

    func = initiated_client[task_name]

    input = input_dict[project_name][task_name]

    result = await func(**input)
    print(result["raw_output"])


if __name__ == "__main__":
    asyncio.run(run_task())
