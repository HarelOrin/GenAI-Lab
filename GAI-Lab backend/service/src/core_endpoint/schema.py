from strawberry import Schema

from .mutations import IndexMutation
from .queries import IndexQuery


class SchemaGetter():
    def __call__(self):
        return Schema(query=IndexQuery,
                      mutation=IndexMutation,
                      )
