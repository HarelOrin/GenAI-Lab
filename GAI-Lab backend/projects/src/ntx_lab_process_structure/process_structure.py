import kryon_config_client
from ntx_algo_proc_structure import TextToStructuredProcessConverter
from tasks import apply_structure


def init(config_client: kryon_config_client.ConfigClient):
    proc_structure_client = TextToStructuredProcessConverter(config_client=config_client)

    return {"apply_structure": apply_structure(proc_structure_client=proc_structure_client)}
