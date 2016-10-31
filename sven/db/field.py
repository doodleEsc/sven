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


class StringField(Field):
    """
    String Field
    """
    def __init__(self, name=None, column_type='varchar(100)', primary_key=False, default=None):
        super().__init__(name, column_type, primary_key, default)


class BooleanField(Field):
    """
    boolean Field
    """
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntegerField(Field):
    """
    Integer Field
    """
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):
    """
    Float Field
    """
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)


class TextField(Field):
    """
    Text Field
    """
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)


class DateTimeField(Field):
    """
    DateTime field
    """

    def __init__(self, name=None, default=None):
        super().__init__(name, 'datetime', False, default)

