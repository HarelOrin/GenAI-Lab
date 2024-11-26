from nintex_llm_skuid_app_generator import SkuidGAIClient
from tasks.generate_app import generate_app
from tasks.get_schema import get_schema
from tasks.update_schema import update_schema


def init():

    skuid_client = SkuidGAIClient()

    return {
        "get_schema": get_schema(skuid_client),
        "update_schema": update_schema(skuid_client),
        "generate_app": generate_app(skuid_client),
    }
