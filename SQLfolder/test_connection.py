from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://project_tracker_user:ProjectTrackerDB@localhost:5432/project_tracker",
    echo=True
)

with engine.connect() as conn:
    result = conn.execute("SELECT 1;")
    print(result.scalar())
