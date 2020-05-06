import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(host, user, password, database):
    global __factory
    if __factory:
        return

    engine = sa.create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}', echo=False)
    __factory = orm.sessionmaker(bind=engine, autoflush=True)

    from . import __models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
