import json
import logging

logging.getLogger("pika").setLevel(logging.INFO)

import os

import kryon_config_client
import nintex_secrets
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from clients.auth_client import AuthClient
from clients.queue_client.src.publisher_client import QueueClient
from resolvers.src import client
from service.src import (
    core_endpoint,
    d_ingestion,
    forms,
    proc_structure,
    skuid_apps,
    task_capture,
    wf_constructor,
)

logger = logging.getLogger()

logging.getLogger("pika").setLevel(logging.INFO)
logging.getLogger("PIL").setLevel(logging.INFO)
logging.getLogger("pymongo").setLevel(logging.INFO)
logging.getLogger("openai").setLevel(logging.INFO)
logging.getLogger("httpcore").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.INFO)
logging.getLogger().setLevel(logging.INFO)


def get_config():
    secrets_provider = nintex_secrets.init()
    config_client = kryon_config_client.init(secrets_provider=secrets_provider)
    config = config_client.get_general_config("gai-lab")
    return config


def get_context(config):
    return {
        "resolvers": client.init(config=config),
        "queue_client": QueueClient(),
        "auth": AuthClient()
    }


def main():
    logging.getLogger().setLevel(logging.NOTSET)
    logging.info("setting up service")

    service_port = int(os.getenv("PORT", 12345))
    core_schema = core_endpoint.SchemaGetter()()
    # forms_schema = forms.SchemaGetter()()
    # d_ingestion_schema = d_ingestion.SchemaGetter()()
    # task_capture_schema = task_capture.SchemaGetter()()
    # wf_constructor_schema = wf_constructor.SchemaGetter()()
    # proc_structure_schema = proc_structure.SchemaGetter()()
    config = get_config()
    context = get_context(config=config)
    core_app = GraphQLRouter(core_schema, context_getter=lambda: {"service_context": context})
    # forms_app = GraphQLRouter(forms_schema, context_getter=lambda: {"service_context": context})
    # d_ingestion_app = GraphQLRouter(d_ingestion_schema, context_getter=lambda: {"service_context": context})
    # task_capture_app = GraphQLRouter(task_capture_schema, context_getter=lambda: {"service_context": context})
    # wf_constructor_app = GraphQLRouter(wf_constructor_schema, context_getter=lambda: {"service_context": context})
    # proc_structure_app = GraphQLRouter(proc_structure_schema, context_getter=lambda: {"service_context": context})
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(core_app, prefix="/core_endpoint")
    # app.include_router(forms_app, prefix="/0")  # forms 2.0
    # app.include_router(d_ingestion_app, prefix="/1")  # diagram ingestion
    # app.include_router(task_capture_app, prefix="/2")  # task capture
    # app.include_router(wf_constructor_app, prefix="/3")  # workflow constructor
    # app.include_router(proc_structure_app, prefix="/4")  # process structure
    uvicorn.run(app, port=service_port, host="0.0.0.0")


if __name__ == "__main__":
    main()
