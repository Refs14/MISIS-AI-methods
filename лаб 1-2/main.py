import sqlite3
import random

conn = sqlite3.connect('misis.db')

cursor = conn.cursor()

# создаем таблицу c ценами
cursor.execute('''CREATE TABLE localization
            	    (localization_id INTEGER PRIMARY KEY,
                    country TEXT,
                    currency TEXT,
                    currency_weight DOUBLE)''')

locals = [(1,'Россия', 'рубль', 1.0),
        (2,'Китай', 'юань', 12.66),
        (3,'Турция', 'лира', 3.09),
        (4,'Аргентина', 'песо', 0.24),
        (5,'Казахстан', 'тенге', 0.20),
        (6,'Германия', 'евро', 98.38),
        (7,'США', 'доллар США', 89.48),
        (8,'Япония', 'йена', 0.63),
        (9,'Швейцария', 'швейцарский франк', 103.29),
        (10,'Австралия', 'австралийский доллар', 59.95)]

# добавляем в таблицу localization 10 записей выше
cursor.executemany('INSERT INTO localization VALUES (?, ?, ?, ?)', locals)


# создаем таблицу c локализациями
cursor.execute('''CREATE TABLE price
            	    (price_id INTEGER PRIMARY KEY, 
                    game TEXT, 
                    price DOUBLE, 
                    localization_id INTEGER
                    FOREIGN KEY(localization_id) REFERENCES localization(localization_id))''')

#дубль цен из переменной locals
cur_weight = [1.0, 12.66, 3.09, 0.24, 0.20, 98.38, 89.48, 0.63, 103.29, 59.95]

#создаем list из 100 названий игр
file = open("games.txt")
file_str = file.read()
games = file_str.split('\n')

prices = []

for i in range(100):
    current_geme_price = random.uniform(300.0, 5000.0)
    for j in range(1, 11):
        prices.append((i*10+j, games[i], current_geme_price*random.uniform(0.8, 1.2)/cur_weight[j-1], j))

cursor.executemany('INSERT INTO price VALUES (?, ?, ?, ?)', prices)

conn.commit()

cursor.execute("""SELECT p.game, (p.price*l.currency_weight) as rouble_price, l.country FROM price as p, localization as l where p.localization_id=l.localization_id and p.game='Pac-Man' order by rouble_price limit 10""")
raw_data = cursor.fetchall()
print(list(raw_data))

conn.close()
