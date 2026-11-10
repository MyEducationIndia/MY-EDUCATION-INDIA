from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool, text
from app.core.config import get_settings
from app.db.base import Base
import app.models  # noqa: F401 - register all SQLAlchemy models

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = get_settings()
sync_url = settings.SYNC_DATABASE_URL or settings.DATABASE_URL
# Automatically ensure synchronous driver is used for Alembic migrations
if sync_url.startswith("postgresql+asyncpg://"):
    sync_url = sync_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
elif sync_url.startswith("postgresql://"):
    sync_url = sync_url.replace("postgresql://", "postgresql+psycopg2://", 1)
elif sync_url.startswith("postgresql+psycopg://"):
    sync_url = sync_url.replace("postgresql+psycopg://", "postgresql+psycopg2://", 1)
config.set_main_option("sqlalchemy.url", sync_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        version_table_column_length=128,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        # Automatically expand version_num column length if alembic_version table already exists
        try:
            connection.execute(text("ALTER TABLE alembic_version ALTER COLUMN version_num TYPE VARCHAR(128);"))
            connection.commit()
        except Exception:
            pass

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            version_table_column_length=128,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
