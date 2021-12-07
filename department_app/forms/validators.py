"""
Department form, this module defines the following classes:

- `Unique`, custom validator that raise in case of object with given param is already exists
- `Exists`, custom validator that raise in case of object with given param does not exist
"""

from wtforms.validators import ValidationError


class Unique:
    """
    Custom validator that raise in case of object with given param is already exists
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = f'{model.__name__} with such name already exists'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)


class Exists:
    """
    Custom validator that raise in case of object with given param does not exist
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = f'{model.__name__} with such name doesn\'t exist'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if not check:
            raise ValidationError(self.message)
