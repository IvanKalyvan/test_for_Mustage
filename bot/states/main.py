from aiogram.fsm.state import State, StatesGroup

class ExpenseForm(StatesGroup):

    title = State()
    expensesUAH = State()

class StatementOfExpenses(StatesGroup):

    start_date = State()
    end_date = State()