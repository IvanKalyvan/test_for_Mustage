from fastapi import FastAPI

from expenses.routers import expenses
app = FastAPI(title="Mustage")
app.include_router(expenses)