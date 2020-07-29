import logging

def open_file_object(filepath):
    """
    :param filepath: this is the filepath to the file you will be opening
    :return: returns a byte object of the whole file
    """
    with open(filepath, 'rb') as f:
        file = f.read()
        return file


def write_file_object(filepath, file_contents):
    """
    :param filepath: this is the filepath to the file you will be editing
    :param file_contents: a byte object with the whole file
    :return: none
    """
    with open(filepath, 'wb') as f:
        f.write(file_contents)
        print('wrote to file')