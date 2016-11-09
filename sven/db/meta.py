"""
metaclass for model
"""

from .field import Field

class ModelMetaClass(type):
    """
    model metaclass
    """

    def __new__(cls, name, bases, attrs):

        if name == 'Model':
            return super().__new__(cls, name, bases, attrs)

        table_name = attrs.get('__table__', None) or name
        mapping = dict()
        primary_key = None
        fields = []

        for k, v in attrs.items():
            if isinstance(v, Field):
                mapping[k] = v
                if v.primary_key:
                    if primary_key:
                        pass #code here to raise duplicate primary key error
                    primary_key = k

                else:
                    fields.append(k)

        if not primary_key:
            pass #code here to raise none primary key here

        #remove original attrs
        for k in mapping.keys():
            attrs.pop(k)

        attrs['__mapping__'] = mapping
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primary_key
        attrs['__fields__'] = fields