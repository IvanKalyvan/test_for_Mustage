from pydantic import BaseModel
from typing import Optional, Union

class ExpenseCreate(BaseModel):

    title: str
    expensesUAH: Optional[Union[int, float]]

class ExpenseUpdate(BaseModel):

    id: int = None
    title: str = None
    inUAH: Optional[Union[int, float]] = None