from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.main import main, skip_keyboard
from api import update_expenses
from states.main import ExpenseFormUpdate

router = Router()

@router.message(F.text == "Відредагувати статтю")
async def create_expense(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Enter expense id (if you dont want change paragraph, press \"Skip\" under message!!!)", reply_markup=skip_keyboard)
    await state.set_state(ExpenseFormUpdate.id)

@router.message(ExpenseFormUpdate.id)
async def create_expense_id(message: Message, state: FSMContext):

    await state.update_data(id=message.text)
    await message.answer("Enter expense title", reply_markup=skip_keyboard)
    await state.set_state(ExpenseFormUpdate.title)

@router.message(ExpenseFormUpdate.title)
async def create_expense_title(message: Message, state: FSMContext):

    await state.update_data(title=message.text)
    await message.answer("Enter expense in UAH", reply_markup=skip_keyboard)
    await state.set_state(ExpenseFormUpdate.inUAH)

@router.message(ExpenseFormUpdate.inUAH)
async def create_expense_inUAH(message: Message, state: FSMContext):

    await state.update_data(inUAH=message.text)

    data = await state.get_data()
    request_data = {}

    for paragraph in data:

        if data[paragraph] != " ":
            request_data[paragraph] = data[paragraph]

    await state.clear()
    response = await update_expenses("/expenses", request_data)
    if response.status == 200:

        await message.answer("Updated expenses!")

    else:

        await message.answer("Failed to update expenses!")

@router.callback_query(F.data == "skip")
async def skip_callback(callback: CallbackQuery, state: FSMContext):

    current_state = await state.get_state()

    if current_state == "ExpenseFormUpdate:id":

        await state.update_data(id=" ")
        await state.set_state(ExpenseFormUpdate.title)
        await callback.message.answer("Enter expense in UAH", reply_markup=skip_keyboard)

    elif current_state == "ExpenseFormUpdate:title":

        await state.update_data(title=" ")
        await state.set_state(ExpenseFormUpdate.inUAH)
        await callback.message.answer("Enter expense in UAH", reply_markup=skip_keyboard)

    elif current_state == "ExpenseFormUpdate:inUAH":

        await state.update_data(inUAH=" ")
        data = await state.get_data()
        request_data = {}

        for paragraph in data:

            if data[paragraph] != " ":

                request_data[paragraph] = data[paragraph]

        await state.clear()
        response = await update_expenses("/expenses", request_data)
        if response.status == 200:

            await callback.message.answer("Updated expenses!")

        else:

            await callback.message.answer("Failed to update expenses!")