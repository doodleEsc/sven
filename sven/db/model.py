"""
model
"""

from sven.db.meta import ModelMetaClass
from sven.db.utils import select, excute


class Model(dict, metaclass=ModelMetaClass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def get_value(self, key):
        return getattr(self, key, None)

    def get_value_or_default(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mapping__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                setattr(self, key, value)
        return value

    @classmethod
    async def find_all(cls, where=None, args=None, **kwargs):
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        groupby = kwargs.get('groupby', None)
        if groupby:
            sql.append('group by')
            sql.append(groupby)

        orderby = kwargs.get('orderby', None)
        if orderby:
            sql.append('order by')
            sql.append(orderby)

        limit = kwargs.get('limit', None)
        if limit:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(str(limit))
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?,?')
                args.extend(map(lambda s: str(s), limit))
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(' '.join(sql).replace('?', '%s'), args)
        return [cls(**r) for r in rs]

    @classmethod
    async def find_number(cls, field, where=None, args=None):
        sql = ['select count(%s) from %s' % (field, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql).replace('?', '%s'), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    async def find(cls, pk):
        sql = '%s where %s=?' % (cls.__select__, cls.__primary_key__)
        rs = await select(sql.replace('?', '%s'), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.get_value_or_default, self.__field__))
        args.append(self.get_value_or_default(self.__primary_key__))
        rows = await excute(self.__insert__.replace('?', '%s'), args)
        return rows

    async def update(self):
        args = list(map(self.get_value, self.__field__))
        args.append(self.get_value(self.__primary_key__))
        rows = await excute(self.__update__.replace('?', '%s'), args)
        return rows

    async def remove(self):
        args = [self.get_value(self.__primary_key__)]
        rows = await excute(self.__delete__.replace('?', '%s'), args)
        return rows




