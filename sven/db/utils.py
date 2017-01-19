"""
database utils
"""
import aiomysql

__pool = None


async def create_pool(loop, host='localhost', port=3306, **kwargs):
    global __pool
    __pool = await aiomysql.create_pool(
        loop=loop,
        host=host,
        port=port,
        user=kwargs['user'],
        password=kwargs['password'],
        db=kwargs['db'],
        charset=kwargs.get('charset', 'utf8'),
        autocommit=kwargs.get('autocommit', True),
        maxsize=kwargs.get('maxsize', 10),
        minsize=kwargs.get('minsize', 1)
    )


async def select(sql, args, size=None):
    global __pool
    async with __pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql, args or ())
            rs = await cur.fetchmany(size) if size else cur.fetchall()
            return rs


async def execute(sql, args, autocommit=True):
    print(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql, args)
                affected = cur.rowcount
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise e

        return affected

