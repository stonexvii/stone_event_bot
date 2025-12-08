from ..db_engine import engine
from ..tables import Base


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
