import dataclasses
import logging

from . import resolvers

logger = logging.getLogger()


@dataclasses.dataclass(frozen=True)
class Resolvers:
    core_resolver: resolvers.core_resolver.CoreResolver
    d_ingestion: resolvers.d_ingestion.DIngestionResolver
    forms: resolvers.forms.FormsResolver
    task_capture: resolvers.task_capture.TaskCaptureResolver
    wf_constructor: resolvers.wf_constructor.WorkflowConstructorResolver
    proc_structure: resolvers.proc_structure.ProcessStructureResolver
    skuid_apps: resolvers.skuid_apps.SkuidAppGenerator


def init(config: dict):
    def get_resolver(resolver_name: str, **kwargs):
        return getattr(resolvers, resolver_name).init(config=config, **kwargs)

    logger.info("Created resolvers")
    return Resolvers(
        **{
            "core_resolver": get_resolver(resolver_name="core_resolver"),
            "d_ingestion": get_resolver(resolver_name="d_ingestion"),
            "forms": get_resolver(resolver_name="forms"),
            "task_capture": get_resolver(resolver_name="task_capture"),
            "wf_constructor": get_resolver(resolver_name="wf_constructor"),
            "proc_structure": get_resolver(resolver_name="proc_structure"),
            "skuid_apps": get_resolver(resolver_name="skuid_apps"),
        }
    )
