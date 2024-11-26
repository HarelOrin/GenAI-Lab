from form_consts import FIRST_TASK

from projects.src.BaseTask import BaseTask


class second_task(BaseTask):
    def __init__(self, project_client_with_logic_methods: ClientFromProject):  # type: ignore
        """
        Initializes the second_task task's metadata and all it's logical dependencies.
        Dependencies:
            project_client_with_logic_methods (ClientFromProject): The client object from the project package that executes the project logic.
                Methods:
                    func(InputFromFirstTask: str, count) -> str: The function that executes the project logic.
        """
        super().__init__(
            task_name="second_task",
            project_name="project_name",
            output_type="artifact",  # "form" if there is another task after this one, "artifact" if this is the last task
            data_type="text",  # type of output
            is_raw_output_file=False,
        )

        self.project_client_with_logic_methods = project_client_with_logic_methods  # Inversion of Control

    async def execute(self, InputFromFirstTask: str, **kwargs) -> dict:
        """
        Executes the second_task task when calling this class like a function.
        The execute function is in charge of:
        - Manipulating the input data from the Lab to match the project packge API
        - Returning output of API
        Args:
            InputFromFirstTask (str): Input specified in the form. the name of the argument should match the "name" field of this input in the form.
            **kwargs: Additional dynamic parameters generated by output of previous task.
        Returns:
            result (str): The output of the project logic in text format.
        """
        count = 0
        for value in kwargs.values():
            if value == "choice2":
                count += 1

        result = self.project_client_with_logic_methods.func(InputFromFirstTask, count)

        return result