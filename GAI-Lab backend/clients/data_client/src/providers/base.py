import abc


class DbBaseProvider(abc.ABC):
    @abc.abstractmethod
    async def get_output(self, workflow_id: str, step: str) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def upload_entry(self, data: dict, code: int) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def upload_project(self, data: dict):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_project(self, id: str = None) -> list[dict]:
        raise NotImplementedError

    async def send_feedback(
        self,
        requestId: str,
        feedbackType: str,
        description: str = None,
        email: str = None,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def upload_result(self, data: dict):
        raise NotImplementedError

    @abc.abstractmethod
    async def upload_input(self, data: dict):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_result(self, request_id: str) -> dict:
        raise NotImplementedError
