# Файл-Flask
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    try:
        conn = sqlite3.connect('menufood.db')
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM menufood")
        menu = cur.fetchall()
        
        menu_list = []
        for items in menu:
            menu_list.append({
                "name_dish" : items[0],
                "ingredients" : items[1],
                "weight_dish" : items[2],
                "cost_dish" : items[3],
                "img_dish" : items[4],
            })
        
        cur.close()
        conn.close()
        
    # Обработчик ошибок    
    except IOError as e:
        print(f"Произошла ошибка ввода/вывода: {e}")
    except TypeError as e:
        print(f"Произошла ошибка с типами данных: {e}")
        
    # Мы выводим наш список с данными словарями в html-файл, который будет принимать эти словари со значениями для создания API-приложения
    return render_template('menu_food_interface.html', menu_list=menu_list)

# Запускаем Flask-файл
if __name__ == "__main__":
    app.run(host='_github-pages-challenge-SHOKERRR777.shokerrr777.com', debug=True)