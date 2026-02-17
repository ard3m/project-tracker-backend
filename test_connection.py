from sqlalchemy import create_engine, text

# 1. Create the engine using your correct connection string
engine = create_engine(
    "postgresql+psycopg2://project_tracker_user:ProjectTrackerDB@localhost:5432/project_tracker",
    echo=True,  # optional: prints SQL to help debugging
    future=True  # ensures SQLAlchemy 2.x style behavior
)

# 2. Open a connection and execute a simple test query
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("Database responded with:", result.scalar())
