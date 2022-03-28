def output_formatter(objects: list, serializer_function):
    """

    :param objects: A generator of objects
    :param serializer_function: The serialization function, should be able to serialize a list.
    :return:
    """
    if not callable(serializer_function):
        raise TypeError("Serializer_function is not a callable function.")
    return serializer_function(objects)


def outputter(objects: list, serializer_function, output_function, *output_function_args):
    """

    :param objects: The list objects which should be serialized
    :param serializer_function: The function to serialize the objects. Should be able to serialize the list.
    :param output_function: The function making the output
    :param output_function_args: Arguments to the output function. The serialized objects will be first argument.
    :return:
    """
    if not callable(output_function):
        raise TypeError("output_function is not a function")

    formatted_output = output_formatter(objects, serializer_function)
    if len(output_function_args) > 0:
        output_function(formatted_output, output_function_args)
    else:
        output_function(formatted_output)
