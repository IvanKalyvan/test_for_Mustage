from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main import main
router = Router()

@router.message(CommandStart())
async def start(message: Message):

    await message.answer("Welcome, admin)", reply_markup=main)