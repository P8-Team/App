def output_formatter(objects: list, serializer_function):
    """

    :param objects: A generator of objects
    :param serializer_function: The serialization function, should be able to serialize a list.
    :return:
    """

    return serializer_function(objects)


def outputter(objects: list, serializer_function, output_function, *extra_args):
    formatted_output = output_formatter(objects, serializer_function)
    output_function(formatted_output, extra_args)
