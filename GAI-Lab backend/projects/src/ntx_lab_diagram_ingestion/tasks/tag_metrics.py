import base64
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))

from form_consts import METRIC_CHOICES, TAG_METRICS
from ntx_algo_to_bpmn_converter import VisioConversionMetrics

from projects.src.BaseTask import BaseTask


class tag_metrics(BaseTask):
    def __init__(self, visio_to_bpmn_with_metrics):
        """
        Initializes the tag_metrics task.
        Dependencies:
            visio_to_bpmn_with_metrics(VisioDiagram: bytearray) -> tuple[bytearray, VisioConversionMetrics](function): The function from the ntx_algo_to_bpmn_converter package that returns the conversion metrics of a Visio diagram.
        Forwarded Data:
            VisioDiagram (str): The base64 encoded string representation of the Visio diagram.
            conversionMetrics (VisioConversionMetrics): The conversion metrics of the Visio diagram.
        """
        super().__init__(
            task_name="tag_metrics",
            project_name="diagram_ingestion",
            output_type="form",
            data_type="bpmn",
            is_raw_output_file=False,
        )

        self.visio_to_bpmn_with_metrics = visio_to_bpmn_with_metrics

    async def execute(self, VisioDiagram: bytes) -> tuple[VisioConversionMetrics, dict]:
        """
        Executes the tag_metrics task.
        Args:
            VisioDiagram (str): The base64 encoded string representation of the Visio diagram.
            **kwargs: Additional optional parameters.
        Returns:
            tuple[VisioConversionMetrics, dict]: A tuple containing the VisioConversionMetrics object and a the form for next step.
        """
        VisioDiagramDecode: bytearray = bytearray(VisioDiagram)

        _, conversionMetrics = self.visio_to_bpmn_with_metrics(VisioDiagramDecode)

        return VisioDiagram, conversionMetrics

    def build_dynamic_form(self, VisioDiagram: str, conversionMetrics: VisioConversionMetrics) -> dict:
        VisioDiagram_section = {
            "type": "File upload",
            "title": "VisioDiagram",
            "single": True,
            "accepts": ".vsdx",
            "value": VisioDiagram,
        }
        conversionMetrics_section = {"type": "object", "properties": {}}
        for name in conversionMetrics.unknown_shape_names:
            conversionMetrics_section["properties"][name] = {
                "type": "Choice-Single",
                "title": name,
                "choices": METRIC_CHOICES,
                "description": f"Please choose the BPMN element type that"
                f" describes your unknown visio object best - {name}",
            }

        full_form = TAG_METRICS
        form = full_form["input"]["properties"]
        form["invisSection"]["properties"]["VisioDiagram"] = VisioDiagram_section
        form["conversionMetrics_section"] = conversionMetrics_section

        return conversionMetrics, full_form
