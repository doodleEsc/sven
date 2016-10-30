"""
table filed
"""


class Field(object):
    """
    base field
    """
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s %s:%s>' %(self.__class__.__name__, self.column_type, self.name)

