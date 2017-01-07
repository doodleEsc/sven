"""
metaclass for model
"""

from sven.db.field import Field


class ModelMetaClass(type):
    """
    model metaclass
    """

    def __new__(mcs, name, bases, attrs):

        if name == 'Model':
            return super().__new__(mcs, name, bases, attrs)

        table_name = attrs.get('__table__', None) or name
        mapping = dict()
        primary_key = None
        fields = []

        for k, v in attrs.items():
            if isinstance(v, Field):
                mapping[k] = v
                if v.primary_key:
                    if primary_key:
                        pass    # code here to raise duplicate primary key error
                    primary_key = k
                else:
                    fields.append(k)

        if not primary_key:
            pass  # code here to raise none primary key here

        # remove original attrs
        for k in mapping.keys():
            attrs.pop(k)

        escaped_fields = list(map(lambda x: '`%s`' % x, fields))

        attrs['__mapping__'] = mapping
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primary_key
        attrs['__fields__'] = fields
        attrs['__select__'] = 'SELECT `%s`, %s FROM `%s`'\
                              % (primary_key, ', '.join(escaped_fields), table_name)
        attrs['__insert__'] = 'INSERT INTO `%s` (%s, `%s`) VALUES (%s)' \
                              % (table_name, ', '.join(escaped_fields), primary_key, \
                                 ', '.join(['?' for n in range(len(escaped_fields)+1)]))
        attrs['__update__'] = 'UPDATE `%s` SET %s WHERE `%s`=?' \
                              % (table_name, ', '.join(map(lambda f: '`%s`=?' % f, fields)),\
                                 primary_key)
        attrs['__delete__'] = 'DELETE FROM `%s` WHERE `%s`=?' % (table_name, primary_key)
        return super().__new__(mcs, name, bases, attrs)
