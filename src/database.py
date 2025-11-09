# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from sqlalchemy import inspect, text
import logging

# Database URL from environment variable (MySQL in Docker, SQLite fallback for local dev)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para obtener una sesión de BD en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_canvas_id_column():
    """Ensure dashboards.canvas_id column exists in the connected database.

    If the column is missing this will add it (as NULLable), populate it for
    existing rows using the dashboard id, and then make it NOT NULL and UNIQUE.
    This is a small, safe migration to align runtime schema with the models.
    """
    try:
        inspector = inspect(engine)
        if 'dashboards' not in inspector.get_table_names():
            # no dashboards table yet, nothing to do
            return

        cols = {c['name'] for c in inspector.get_columns('dashboards')}
        if 'canvas_id' in cols:
            return

        logging.info("Applying lightweight migration: adding dashboards.canvas_id column")
        # Add column as nullable first
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE dashboards ADD COLUMN canvas_id VARCHAR(36) NULL"))
            # populate existing rows with the id (string) to avoid NULLs
            conn.execute(text("UPDATE dashboards SET canvas_id = CAST(id AS CHAR) WHERE canvas_id IS NULL"))
            # make column NOT NULL
            conn.execute(text("ALTER TABLE dashboards MODIFY canvas_id VARCHAR(36) NOT NULL"))
            # create unique index
            try:
                conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_dashboards_canvas_id ON dashboards(canvas_id)"))
            except Exception:
                # Some MySQL versions don't support IF NOT EXISTS for CREATE INDEX; ignore if it fails
                try:
                    conn.execute(text("CREATE UNIQUE INDEX idx_dashboards_canvas_id ON dashboards(canvas_id)"))
                except Exception:
                    logging.warning("Could not create unique index on dashboards.canvas_id; it may exist already or the DB doesn't support the statement")

    except Exception as e:
        # Log but don't crash the whole service on migration failure
        logging.exception(f"Failed to ensure dashboards.canvas_id column: {e}")


# Run the small schema alignment on import so it executes during container startup
ensure_canvas_id_column()