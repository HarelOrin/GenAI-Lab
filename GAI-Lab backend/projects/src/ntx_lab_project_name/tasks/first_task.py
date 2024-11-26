from form_consts import FIRST_TASK

from projects.src.BaseTask import BaseTask


class first_task(BaseTask):
    def __init__(self, function_executing_project_logic):
        """
        Initializes the first_task task's metadata and all it's logical dependencies.
        Dependencies:
            function_executing_project_logic(SampleText: str, InputForSecondTask: str) -> dict: The function that executes the project logic.
        Forwarded Data:
            InputForSecondTask (str): The input given in first task form, but used in the next task.
        """
        super().__init__(
            task_name="first_task",
            project_name="project_name",
            output_type="form",  # "form" if there is another task after this one, "artifact" if this is the last task
            data_type="json",  # type of output
            is_raw_output_file=True,
            file_suffix="json",
        )

        self.function_executing_project_logic = function_executing_project_logic  # Inversion of Control

    async def execute(self, SampleText: str, InputForSecondTask) -> dict:
        """
        Executes the first_task task when calling this class like a function.
        The execute function is in charge of:
        - Manipulating the input data from the Lab to match the project packge API
        - Returning output of API and all other data for creating dynamic form for next step
        Args:
            SampleText (str): Input specified in the form. the name of the argument should match the "name" field of this input in the form.
            InputForSecondTask (str): Input given in first task form, but used in the next task.
        Returns:
            output_json (dict): The output of the project logic in JSON format.
            InputForSecondTask (str): The input given in first task form, but used in the next task.
        """
        manipulated_input = self.task_helper_function(SampleText)

        output_json = self.function_executing_project_logic(manipulated_input)

        return output_json, InputForSecondTask

    def build_dynamic_form(self, output_json: dict, InputForSecondTask: str) -> dict:
        """
        Create the dynamic sections that depend on the parameters to be inserted into the form
        """
        InputForSecondTask_section = {
            "type": "Text-Short",
            "name": "InputFromFirstTask",
            "value": InputForSecondTask,
        }
        output_json_section = {"type": "object", "properties": {}}
        for key, value in output_json.items():
            output_json_section["properties"][key] = {
                "type": "Choice-Single",
                "title": key,
                "name": key,
                "choices": ["choice1", "choice2", "choice3"],
                "description": f"Please choose the BPMN element type that"
                f" describes your unknown visio object best - {value}",
            }

        """
            Inject the dynamic sections into the form
        """
        full_form = FIRST_TASK
        form = full_form["input"]["properties"]
        form["invisSection"]["properties"]["InputForSecondTask"] = InputForSecondTask_section
        form["output_json_section"] = output_json_section

        return output_json, full_form

    def task_helper_function(self, SampleText: str) -> str:
        """
        Helper function to manipulate the input data from the Lab to match the project package API
        """
        return SampleText
