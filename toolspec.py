import inspect
from docstring_parser import parse

def tool_definition_decorator(func):
    """
    A decorator that generates an OpenAI API-compliant tool definition for the decorated function.
    The tool definition is stored in the function's `tool_definition` attribute.

    You can use the decorator as usual:
    @tool_definition_decorator
    def my_func( param1: str, param2: list) -> bool:
        pass

    and then access the tool definition:
    my_func.tool_definition.

    Or you can manually decorate the function by calling the decorator directly:
    tool_definition_decorator( my_func) 

    And that will add the attribute to the function.
    """

    def get_json_type(python_type):
        """Map Python type annotations to OpenAI JSON Schema compatible types."""
        if python_type is str:
            return "string"
        elif python_type is int:
            return "integer"
        elif python_type is float:
            return "number"
        elif python_type is bool:
            return "boolean"
        elif python_type is list:
            return "array"
        elif python_type is dict:
            return "object"
        elif python_type is type(None):
            return "null"
        else:
            return "string"  # Fallback for unknown types

    # Get function signature and parameters
    sig = inspect.signature(func)
    parameters = {}
    required = []

    for name, param in sig.parameters.items():
        # Extract type from annotation
        python_type = param.annotation
        # Map to OpenAI JSON-compatible type
        json_type = get_json_type(python_type)

        # Default description (can be improved with docstrings or metadata)
        description = f"Parameter {name}"

        parameters[name] = {
            "type": json_type,
            "description": description
        }

        # Determine if parameter is required
        if param.default == inspect.Parameter.empty:
            required.append(name)
    
    # Parse the docstring
    docstring = inspect.getdoc(func)
    if docstring:
        parsed = parse(docstring)
        for param in parsed.params:
            if param.arg_name in parameters:
                parameters[param.arg_name]["description"] = param.description

    # Get function description from docstring, or default
    description = func.__doc__ or "No description provided."

    # Build the tool definition
    tool_definition = {
        "name": func.__name__,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": parameters,
            "required": required
        }
    }

    # Attach the tool definition as an attribute
    func.tool_definition = tool_definition

    # Return the original function (unmodified)
    return func


def build_list_of_tools( tool_list: list) ->list:
    toolspecs=[]
    for t in tool_list:
        if(hasattr(t,"tool_definition")):
            thistool = {"type":"function", "function":t.tool_definition }
            toolspecs.append(thistool)
    return toolspecs
    
