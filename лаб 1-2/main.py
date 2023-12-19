import sqlite3
import random

conn = sqlite3.connect('misis.db')

cursor = conn.cursor()

# создаем таблицу c локализациями
cursor.execute('''CREATE TABLE IF NOT EXISTS localization
                 (localization_id INTEGER PRIMARY KEY,
                    country TEXT,
                    currency TEXT,
                    currency_weight DOUBLE)''')

# создаем таблицу c играми
cursor.execute('''CREATE TABLE IF NOT EXISTS game
                 (game_id INTEGER PRIMARY KEY, 
                    name TEXT)''')

# создаем таблицу c ценами
cursor.execute('''CREATE TABLE IF NOT EXISTS price
                 (price_id INTEGER PRIMARY KEY, 
                    price DOUBLE, 
                    game_id INTEGER, 
                    localization_id INTEGER,
                    FOREIGN KEY(game_id) REFERENCES game(game_id),
                    FOREIGN KEY(localization_id) REFERENCES localization(localization_id))''')

# создаем таблицу c жанрами
cursor.execute('''CREATE TABLE IF NOT EXISTS genre
                 (genre_id INTEGER PRIMARY KEY, 
                    name TEXT)''')

# создаем таблицу для связи NxN между играми и жанрами
cursor.execute('''CREATE TABLE IF NOT EXISTS game_genre
                 (game_id INTEGER, 
                    genre_id INTEGER, 
                    FOREIGN KEY(game_id) REFERENCES game(game_id), 
                    FOREIGN KEY(genre_id) REFERENCES genre(genre_id))''')


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

#дубль цен из переменной locals
cur_weight = [1.0, 12.66, 3.09, 0.24, 0.20, 98.38, 89.48, 0.63, 103.29, 59.95]

#создаем list из 100 названий игр
file = open("games.txt")
file_str = file.read()
games = file_str.split('\n')
game_and_index = [[i+1, games[i]] for i in range(100)]

cursor.executemany('INSERT INTO game VALUES (?, ?)', game_and_index)

prices = []

for i in range(100):
    current_geme_price = random.uniform(300.0, 5000.0)
    for j in range(1, 11):
        prices.append((i*10+j, current_geme_price*random.uniform(0.8, 1.2)/cur_weight[j-1], i+1, j))

cursor.executemany('INSERT INTO price VALUES (?, ?, ?, ?)', prices)

genres = [(1,'казуальная'),
        (2,'экшен'),
        (3,'шутер'),
        (4,'RPG'),
        (5,'стратегия'),
        (6,'хоррор'),
        (7,'стелс'),
        (8,'приключение'),
        (9,'файтинг'),
        (10,'выживание'),]

cursor.executemany('INSERT INTO genre VALUES (?, ?)', genres)

game_genres = []
autoinc = 1
for i in range(1, 101):
    for j in range(1, 11):
        if(random.random() < 0.3):
            game_genres.append([i, j])

cursor.executemany('INSERT INTO game_genre VALUES (?, ?)', game_genres)

conn.commit()
conn.close()