import logging
import re

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import requests

API_TOKEN = '5666514620:AAFj2Nu7atG636tjYyaM-npiB0AYsuAEnts'
API_BASE_URL = 'http://127.0.0.1:8000/api'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Main menu keyboard
main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(types.KeyboardButton("About"), types.KeyboardButton("Courses"), types.KeyboardButton("Books"))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Welcome to the Bot!", reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: message.text == "About")
async def show_about(message: types.Message):
    response = requests.get(f"{API_BASE_URL}/info/")
    print(response.json())  # Javobni konsolga chiqaring

    if response.status_code == 200:
        info = response.json()

        # Tekshirib ko'rish uchun qisman konsolga chiqaramiz
        print(info)

        # Agar javob list bo'lsa, birinchi elementni oling
        if isinstance(info, list):
            info = info[0]

        about_info = (
            f"Address: {info['address']}\n"
            f"Phone: {info['phone']}\n"
            f"Link: {info['link']}"
        )

        # Rasm URL sini oling va requests yordamida yuklab oling
        image_url = info['image']
        image_response = requests.get(image_url)

        if image_response.status_code == 200:
            image_data = image_response.content
            await message.answer_photo(photo=image_data, caption=about_info)
        else:
            await message.answer("Error retrieving image.")
    else:
        await message.answer("Error retrieving information.")


@dp.message_handler(lambda message: message.text == "Courses")
async def show_courses(message: types.Message):
    response = requests.get(f"{API_BASE_URL}/courses/")
    if response.status_code == 200:
        courses = response.json()
        for course in courses:
            await message.answer(course['title'], reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                types.KeyboardButton(course['title'])))
    else:
        await message.answer("Error retrieving courses.")


@dp.message_handler(lambda message: message.text in [course['title'] for course in requests.get(f"{API_BASE_URL}/courses/").json()])
async def course_detail(message: types.Message):
    course_title = message.text
    response = requests.get(f"{API_BASE_URL}/courses/")
    if response.status_code == 200:
        courses = response.json()
        print(courses)  # Javobni konsolga chiqaramiz

        for course in courses:
            if course['title'] == course_title:
                course_info = (
                    f"Title: {course['title']}\n"
                    f"Description: {course['description']}\n"
                    f"Price: ${course['price']}"
                )

                # Rasm URL sini oling va requests yordamida yuklab oling
                image_url = course['image']
                image_response = requests.get(image_url)

                if image_response.status_code == 200:
                    image_data = image_response.content
                    await bot.send_photo(chat_id=message.chat.id, photo=image_data, caption=course_info)
                else:
                    await message.answer("Error retrieving course image.")
                break
    else:
        await message.answer("Error retrieving course details.")


@dp.message_handler(lambda message: message.text == "Books")
async def show_books(message: types.Message):
    response = requests.get(f"{API_BASE_URL}/books/")
    if response.status_code == 200:
        books = response.json()
        keyboard = InlineKeyboardMarkup(row_width=1)
        for book in books:
            keyboard.add(InlineKeyboardButton(text=book['title'], callback_data=f"book_{book['id']}"))
        await message.answer("Here are our available books:", reply_markup=keyboard)
    else:
        await message.answer("Error retrieving books.")


@dp.callback_query_handler(lambda c: re.match(r'^book_\d+$', c.data))
async def book_details(callback_query: types.CallbackQuery):
    book_id = callback_query.data.split('_')[1]
    response = requests.get(f"{API_BASE_URL}/books/{book_id}/")
    if response.status_code == 200:
        book = response.json()
        book_info = (
            f"Title: {book['title']}\n"
            f"Description: {book['description']}"
        )

        # PDF URL sini oling va requests yordamida yuklab oling
        pdf_url = book['pdf']
        pdf_response = requests.get(pdf_url)

        if pdf_response.status_code == 200:
            pdf_data = pdf_response.content
            await bot.send_document(chat_id=callback_query.from_user.id, document=pdf_data, caption=book_info)
        else:
            await bot.send_message(chat_id=callback_query.from_user.id, text="Error retrieving book PDF.")
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text="Error retrieving book details.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
