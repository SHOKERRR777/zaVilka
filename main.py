# Основной файл
import sqlite3
import telebot
from telebot import types
from telebot.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

bot = telebot.TeleBot('8124101197:AAFZjfb9a8kJrZ3DufUo3-Z7gCIYq4VDMtE') # Токен бота

# Таблицы БД
def init_db():
    conn = sqlite3.connect('menufood.db')
    cur = conn.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS menufood(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_dish TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        weight_dish REAL NOT NULL,
        cost_dish REAL NOT NULL, 
        img_dish TEXT
        )""")
    conn.commit()
    
    cur.close()
    conn.close()

# Функция для добавления еды в меню
def add_food(name_dish, ingredients, weight_dish, cost_dish, img_dish):
    conn = sqlite3.connect('menufood.db')
    cur = conn.cursor()
    
    cur.execute("INSERT OR IGNORE INTO menufood (name_dish, ingredients, weight_dish, cost_dish, img_dish) VALUES (?, ?, ?, ?, ?)", 
                 (name_dish, ingredients, weight_dish, cost_dish, img_dish))
    conn.commit()
    
    cur.close()
    conn.close()

init_db() # Включаем наши таблицы бд

# Добавляем еду в меню
add_food("Гуляш куриный", "Куриная грудка, сметана 15%, томат", 149.00, 399.00, None)
add_food("Спагетти", "Спагетти, приправы восточные", 249.00, 149.00, None)

# Главное меню
@bot.message_handler(commands=['start'])
def main_menu(message):
    main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    look_menu = types.KeyboardButton("Посмотреть меню")
    make_order = types.KeyboardButton("Сделать заказ")
    my_order = types.KeyboardButton("Мои заказы")
    main_markup.add(look_menu, make_order, my_order)    
    
    # Приветствие
    main_photo = open('templates/эмблема-вилка-и-ложка-для-кафе-или-меню-закусочных-векторная-341453807.jpg', 'rb')
    bot.send_message(message.chat.id, "Вас приветствует <b>заВилка</b>! Выберите действие", parse_mode='html', reply_markup=main_markup)
    bot.send_photo(message.chat.id, main_photo)

@bot.message_handler(func=lambda message: message.text == "Посмотреть меню")
def look_menu_fun(message):
    menu_info = InlineKeyboardMarkup() # Позволяет запускать API-приложения
    
    menu_info.add(InlineKeyboardButton('Открыть меню "заВилка":', web_app=WebAppInfo(url="_github-pages-challenge-SHOKERRR777.shokerrr777.com")))
    bot.send_message(message.chat.id, "Для дальнейших действий Вам необходимо перейти в приложение снизу:", reply_markup=menu_info)
    bot.send_message(message.chat.id, "Вот так", reply_markup=ReplyKeyboardRemove())
    
# Запуск работы бота    
if __name__ == "__main__":
    bot.polling(none_stop=True)