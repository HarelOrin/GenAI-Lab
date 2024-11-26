from typing import Optional

import strawberry
from pydash import get
from strawberry.scalars import JSON
from strawberry.types import Info

from resolvers.src import Resolvers


@strawberry.type
class CoreEndpoint:
    @strawberry.field(description="get project")
    async def get_project(self, info: Info, id: Optional[str] = None) -> JSON:
        resolvers: Resolvers = get(info, "context.service_context.resolvers")
        auth_client = get(info, "context.service_context.auth")
        token = info.context["request"].headers["authorization"]
        token_data = await auth_client.authenticate(token) if token and token != "Bearer undefined" else False
        project = await resolvers.core_resolver.get_project(id=id, token_data=token_data)
        return project

    @strawberry.field(description="get result")
    async def get_result(self, info: Info, file_path: str) -> JSON:
        resolvers: Resolvers = get(info, "context.service_context.resolvers")
        result = await resolvers.core_resolver.get_result(file_path=file_path)
        return result

    @strawberry.field(description="ping response")
    async def ping_response(self, info: Info, workflow_id: str, step: str) -> JSON:
        resolvers: Resolvers = get(info, "context.service_context.resolvers")
        result = await resolvers.core_resolver.ping_response(workflow_id=workflow_id, step=step)
        return result
