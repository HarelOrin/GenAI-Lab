from projects.src.BaseTask import BaseTask


class generate_process_text(BaseTask):
    def __init__(self, capture_client):
        """
        Initializes the generate_process_text task.
        Dependencies:
            capture_client (SimpleNamespace - "async_construct_process_activities"): The client from the ntx_llm_proc_capt package that constructs a process from a list of activities.
                Inputs:
                    ProcessActivities (JSON): The list of activities prior user intervention.
                    RoleName (str): The name of the role that the process belongs to.
                    ProcessName (str): The name of the process.
                    ActionsMetadata (JSON): The metadata for the actions in the process.
                    kwargs (dict): Dynamically generated arguments describing user intervention:
                        {index}Name (str): The name of the activity at the given index.
                        {index}Relevance (bool): The relevance of the activity at the given index.
                Outputs:
                    res (str): The response from the client.
        """
        super().__init__(
            task_name="generate_process_text",
            project_name="process_capture",
            output_type="artifact",
            data_type="text",
            is_raw_output_file=False,
        )

        self.capture_client = capture_client

    async def execute(
        self,
        ProcessActivities: str,
        RoleName: str,
        ProcessName: str,
        ActionsMetadata: str,
        **kwargs,
    ) -> str:
        """
        Executes the generate_process_text task.
        Args:
            ProcessActivities (str): The JSON representation of the list of activities prior user intervention.
            RoleName (str): The name of the role that the process belongs to.
            ProcessName (str): The name of the process.
            ActionsMetadata (str): The JSON representation of the metadata for the actions in the process.
            **kwargs: Dynamically generated arguments describing user intervention.
                {index}Name (str): The name of the activity at the given index.
                {index}Relevance (bool): The relevance of the activity at the given index.
        Returns:
            str: The response from the client.
        """
        updated_activities = []

        for index, activity_info in enumerate(ProcessActivities):
            new_name_key = f"{index}Name"

            if new_name_key in kwargs.keys():
                activity_info["activity_name"] = kwargs[new_name_key]

            new_relevance_key = f"{index}Relevance"

            if new_relevance_key in kwargs.keys():
                activity_info["relevant"] = kwargs[new_relevance_key]

            updated_activities.append(activity_info)

        res = await self.capture_client.async_construct_process_activities(
            process_data=updated_activities,
            process_name=ProcessName,
            role_name=RoleName,
            action_metadata=self._decode_base64(ActionsMetadata),
        )

        return res
