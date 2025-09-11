from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os


config = context.config
fileConfig(config.config_file_name)


def get_url():
    return os.getenv("DATABASE_URL")


target_metadata = None # אפשר לייבא את Base.metadata אם רוצים autogenerate


if context.is_offline_mode():
    context.configure(url=get_url(), literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()
else:
    connectable = engine_from_config(
        {"sqlalchemy.url": get_url()}, prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
