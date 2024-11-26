from projects.src.BaseTask import BaseTask


class generate_app(BaseTask):
    def __init__(self, skuid_client):
        """
        Initializes the generate_app task
        Dependencies:
            generate_app (str) -> dict : generates the app files and returns the directory path
                input: schema (dict)
                output: dir_path (str)
            deploy_app (str) -> dict : deploys the app and returns the link json
                input: temp_dir (str)
                output: link_json (dict)
        """
        super().__init__(
            task_name="generate_app",
            project_name="skuid_app_generator",
            output_type="artifact",
            data_type="link",
            is_raw_output_file=False,
        )

        self.generate_app = skuid_client.generate_app
        self.deploy_app = skuid_client.deploy_app

    async def execute(self, schema: str) -> dict:
        """
        Generates a Skuid app by user prompt
        Dependencies:
            generate_app(schema: dict) -> str
            deploy_app(temp_dir: str) -> dict
        """

        dir_path = self.generate_app(schema)
        link_json = await self.deploy_app(schema, dir_path)
        try:
            deployment_response = link_json["link"]
        except KeyError:
            deployment_response = link_json["error"]

        return deployment_response
