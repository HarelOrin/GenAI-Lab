import strawberry
from .core_endpoint import CoreEndpoint

@strawberry.type
class IndexQuery(CoreEndpoint):
    pass
