"""
Custom exceptions for validation, this module defines the following classes:

- `UniqueError`, exception that raise in case of object with given param is already exists
- `ExistsError`, exception that raise in case of object with given param does not exist
"""


class UniqueError(Exception):
    """
    Exception that raise in case of object with given param is already exists
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __repr__(self):
        return self.message


class ExistsError(Exception):
    """
    Exception that raise in case of object with given param does not exist
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __repr__(self):
        return self.message
