# Example usage
note this relies on type hints in the function definition and the Args: section of the docstring to extract better definitions of the parameters.

@tool_definition_decorator
def my_function(a: str, b: list) -> str:
    """
    My function description.

    Args:
        a (str): A string parameter representing something meaningful.
        b (list): A list parameter that holds some data.
    """
    return "success"

my_function.tool_definition
