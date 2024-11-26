from ntx_algo_to_bpmn_converter import visio_to_bpmn, visio_to_bpmn_with_metrics
from tasks.tag_metrics import tag_metrics

from projects.src.ntx_lab_diagram_ingestion.tasks.convert_visio_to_bpmn import (
    convert_visio_to_bpmn,
)


def init():
    return {
        "convert_visio_to_bpmn": convert_visio_to_bpmn(visio_to_bpmn),
        "tag_metrics": tag_metrics(visio_to_bpmn_with_metrics),
    }
