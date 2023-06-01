from pydantic.networks import MultiHostDsn


class MysqlDsn(MultiHostDsn):
    allowed_schemes = {
        'mysql',
        'mysql+aiomysql',
        'mysql+pymysql'
    }
    user_required = True

    __slots__ = ()
