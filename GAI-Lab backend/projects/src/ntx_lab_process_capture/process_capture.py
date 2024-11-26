import kryon_config_client
import ntx_llm_proc_capt
from tasks.describe_process_activities import describe_process_activities
from tasks.generate_process_text import generate_process_text


def init(config_client: kryon_config_client.ConfigClient):
    process_capture_config = config_client.get_general_config("process-capture")
    capture_client = ntx_llm_proc_capt.init(config=process_capture_config)
    return {
        "describe_process_activities": describe_process_activities(process_capture_config),
        "generate_process_text": generate_process_text(capture_client),
    }
