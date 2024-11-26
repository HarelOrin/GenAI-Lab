from typing import Optional

import strawberry
from pydash import get
from strawberry.scalars import JSON
from strawberry.types import Info

from clients.queue_client.src.publisher_client import QueueClient
from resolvers.src import Resolvers


@strawberry.type
class ResponseValidation:
    response: str
    status: int
    workflowId: str


@strawberry.type
class CoreEndpoint:
    @strawberry.mutation(description="Add Project Task to Queue")
    async def send_task(
        self, info: Info, workflowId: str | None, project_name: str, task_name: str, args: str
    ) -> ResponseValidation:
        queue_client: QueueClient = get(info, "context.service_context.queue_client")
        status, response, workflow_id = await queue_client.upload_message(
            project_name=project_name,
            task_name=task_name,
            input_data=args,
            workflow_id=workflowId,
        )
        return ResponseValidation(response=response, status=status.value, workflowId=workflow_id)

    @strawberry.mutation(description="Send feedback")
    async def send_feedback(
        self,
        info: Info,
        requestId: str,
        feedbackType: str,
        description: Optional[str] = None,
        email: Optional[str] = None,
    ) -> JSON:
        resolvers: Resolvers = get(info, "context.service_context.resolvers")
        result = await resolvers.core_resolver.send_feedback(
            requestId=requestId,
            feedbackType=feedbackType,
            description=description,
            email=email,
        )
        return result
