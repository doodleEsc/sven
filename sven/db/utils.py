"""
database utils
"""
import aiomysql

__pool = None


async def create_pool(loop, **kwargs):
    global __pool
    __pool = await aiomysql.create_pool(
        loop=loop,
        host=kwargs.get('host', 'localhost'),
        port=kwargs.get('port', 3306),
        user=kwargs['user'],
        password=kwargs['password'],
        db=kwargs['database'],
        charset=kwargs.get('charset', 'utf8'),
        autocommit=kwargs.get('autocommit', True),
        maxsize=kwargs.get('maxsize', 10),
        minsize=kwargs.get('minsize', 1)
    )


async def select(sql, args, size=None):
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.excute(sql, args)
        return await cur.fetchmany(size) if size else cur.fetchall()


async def excute(sql, args, autocommit=True):
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()

        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.excute(sql, args)
                affected = cur.rowcount
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise e

        return affected

