import redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = 'postgresql+asyncpg://skyfly_admin:123@localhost/skyfly_db'

engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)
Base = declarative_base()

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)