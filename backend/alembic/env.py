# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
import os
import sys
from pathlib import Path
from urllib.parse import quote_plus

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.models import Base
from dotenv import load_dotenv

load_dotenv()

# this is the Alembic Config object
config = context.config

# Get database URL from environment - prefer the full URL if available
database_url = os.getenv("DATABASE_URL")

if not database_url:
    # Build database URL from individual components if DATABASE_URL is not set
    db_user = os.getenv("POSTGRES_USER", "neondb_owner")
    db_password = os.getenv("POSTGRES_PASSWORD", "npg_Q5yBEcL2vkAe")
    db_host = os.getenv("POSTGRES_HOST", "ep-gentle-bonus-abys3ek5-pooler.eu-west-2.aws.neon.tech")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "neondb")
    
    # URL encode the password to handle special characters
    encoded_password = quote_plus(db_password)
    database_url = f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}?sslmode=require"

# Don't set in config to avoid ConfigParser interpolation issues
# We'll use the database_url variable directly in the functions below

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for autogenerate support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Use our constructed database_url instead of config
    url = database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Create engine directly with our database_url
    from sqlalchemy import create_engine
    
    engine = create_engine(database_url, poolclass=pool.NullPool)

    with engine.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()