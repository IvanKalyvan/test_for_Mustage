import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Table, Column, String, BigInteger, Numeric, TIMESTAMP, func
from src.database import metadata

Expenses = Table(

    "Expenses",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("inUAH", Numeric(10, 2), nullable=False),
    Column("inUSD", Numeric(10, 2), nullable=False),
    Column("createdAt", TIMESTAMP, nullable=False, default=func.now()),

)
