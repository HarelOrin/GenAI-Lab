import base64

from ntx_algo_to_bpmn_converter import BPMNMappingType, VisioConversionConfig

from projects.src.BaseTask import BaseTask


class convert_visio_to_bpmn(BaseTask):
    def __init__(self, visio_to_bpmn):
        """
        Initializes the convert_visio_to_bpmn task.
        Dependencies:
            visio_to_bpmn(VisioDiagram: bytearray, config: VisioConversionConfig) -> bytearray (function): The function from the ntx_algo_to_bpmn_converter package that converts a Visio diagram to a BPMN diagram.
        """
        super().__init__(
            task_name="convert_visio_to_bpmn",
            project_name="diagram_ingestion",
            output_type="artifact",
            data_type="bpmn",
            is_raw_output_file=True,
            file_suffix="bpmn",
        )

        self.visio_to_bpmn = visio_to_bpmn

    async def execute(self, VisioDiagram: str, **kwargs) -> str:
        """
        Executes the convert_visio_to_bpmn task.
        Args:
            VisioDiagram (str): The base64 encoded string representation of the Visio diagram.
            **kwargs: Optional tagged metrics, if tag_metrics function was called first
        Returns:
            str: The base64 encoded string representation of the converted BPMN diagram.
        """
        VisioDiagram: bytearray = bytearray(VisioDiagram)
        config = VisioConversionConfig()

        for value in kwargs.values():
            mappingType = BPMNMappingType(value)
            config.keyword_to_bpmn_mapping[value] = mappingType

        res_ba = self.visio_to_bpmn(VisioDiagram, config)

        return res_ba
