import dependency_datatype  # type: ignore
from project_package import (  # type: ignore
    ClientFromProject,
    function_executing_project_logic,
)
from tasks import first_task, second_task

"""
In the project file we initialize the task's dependencies and logic, then pass them to the task's constructor, initiating the task to be ready for execution. any dependencies that are not specific to this project (meaning other projects may use them in their initialization) should be passed as arguments to the init function.
"""


def init(some_external_dependency: dependency_datatype.Type):
    project_client = ClientFromProject(dependency=some_external_dependency)
    return {
        "first_task": first_task(function_executing_project_logic=function_executing_project_logic),
        "second_task": second_task(project_client_with_logic_methods=project_client),
    }
