from ntx_algo_proc_structure import GuidelinesFlavor, TextToStructuredProcessConverter

from projects.src.BaseTask import BaseTask


class apply_structure(BaseTask):
    def __init__(self, proc_structure_client: TextToStructuredProcessConverter):
        """
        Initializes the apply_structure task.
        Dependencies:
            proc_structure_client (TextToStructuredProcessConverter): The client object from the ntx_algo_proc_structure package that performs the text to structured process conversion.
                Methods:
                    apply_structure(ProcessDescription: str) -> str: Converts the given text to structured process.
        """

        super().__init__(
            task_name="apply_structure",
            project_name="process_structure",
            output_type="artifact",
            data_type="text",
            is_raw_output_file=False,
        )
        self.client = proc_structure_client

    async def execute(self, ProcessDescription: str, guidelines_flavor: str) -> str:
        """
        Executes the apply_structure task.
        Args:
            ProcessDescription (str): The text description of the process.
            GuidelinesFlavor (str): The flavor of the guidelines to be used.
        Returns:
            str: The structured process.
        """
        flavor = GuidelinesFlavor(guidelines_flavor)
        result = await self.client.apply_structure(ProcessDescription, flavor)

        return result
