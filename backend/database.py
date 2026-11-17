from collections.abc import Generator
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()
APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
database_url = make_url(os.getenv("DATABASE_URL", "sqlite:///./shريان_test.db"))
if APP_ENV == "production" and database_url.get_backend_name() == "sqlite":
    raise RuntimeError("Configure a persistent MySQL DATABASE_URL for production.")
if database_url.drivername == "mysql":
    database_url = database_url.set(drivername="mysql+pymysql")

query = dict(database_url.query)
ssl_mode = query.pop("ssl-mode", query.pop("ssl_mode", "")).upper()
url_ssl_ca = query.pop("ssl-ca", query.pop("ssl_ca", None))
database_url = database_url.set(query=query)
DATABASE_URL = database_url.render_as_string(hide_password=False)

connect_args = {"check_same_thread": False} if database_url.get_backend_name() == "sqlite" else {}
if database_url.get_backend_name() == "mysql":
    ssl_ca = os.getenv("DB_SSL_CA") or url_ssl_ca
    if ssl_ca:
        connect_args.update(
            ssl_ca=ssl_ca,
            ssl_verify_cert=True,
            ssl_verify_identity=True,
        )
    elif APP_ENV == "production":
        raise RuntimeError("Set DB_SSL_CA to the database provider's CA certificate path.")
    elif ssl_mode and ssl_mode != "DISABLED":
        connect_args["ssl"] = {"check_hostname": False, "verify_mode": True}

engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
