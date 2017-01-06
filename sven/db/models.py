import time, uuid

from sven.db.model import Model
from sven.db.field import StringField,BooleanField, FloatField, TextField
from sven.utils import util


class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=util.generate_id, column_type='varchar(50)')
    email = StringField(column_type='varchar(50)')
    passwd = StringField(column_type='varchar(50)')
    admin = BooleanField()
    name = StringField(column_type='varchar(50)')
    image = StringField(column_type='varchar(500)')
    created_at = FloatField(default=time.time)

if __name__ == '__main__':
    import asyncio
    from sven.db.utils import create_pool

    loop = asyncio.get_event_loop()
    # create_pool(loop, host='10.133.145.159',
    #             user='test', password='test', db='sven')

    async def test():
        await create_pool(loop, host='10.133.145.254',
                user='test', password='test', db='sven')

        # user = User(id='2', name='flz', email='flz@foxmail.com',passwd='123456',image='no image')
        # await user.save()
        r = await User.find_all(where='id=?', args=['1'])
        print(r)

    loop.run_until_complete(test())