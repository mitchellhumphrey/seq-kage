def open_file_object(filepath):
    """
    :param filepath: this is the filepath to the file you will be opening
    :return: returns a byte object of the whole file
    """
    f = open(filepath, 'rb')
    file = f.read()
    return file


def write_file_object(filepath, file_contents):
    """
    :param filepath: this is the filepath to the file you will be editing
    :param file_contents: a byte object with the whole file
    :return: none
    """
    f = open(filepath, 'wb')
    f.write(file_contents)
