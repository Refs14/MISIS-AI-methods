from rasa_sdk          import Action, Tracker
from rasa_sdk.events   import SlotSet
from rasa_sdk.executor import CollectingDispatcher
 
from datetime import datetime as dt
from typing import Any, Text, Dict, List
import sqlite3
import random
 
# поиск 3 локаций с наименьшими ценами для введенной игры
class ActionGameMinPrices(Action):
 
    def name(self) -> Text:              # регистрируем имя действия
        return "action_game_min_prices"
 
    def run(self, dispatcher:CollectingDispatcher, tracker:Tracker, domain:Dict[Text,Any]) -> List[Dict[Text, Any]]:
 
        info_game = tracker.get_slot("GAME")

        conn = sqlite3.connect('misis.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT g.name, round(p.price*l.currency_weight, 2) as rouble_price, l.country from price as p, localization as l, game as g where l.localization_id=p.localization_id and g.game_id=p.game_id and g.name = 'Contra' order by rouble_price limit 3")
        data_raw = cursor.fetchall()
        if(len(data_raw)==0):
            dispatcher.utter_message(text=f'Игра не найдена: ее нет в базе данных или название введено неверно')
        else:
            dispatcher.utter_message(text=f'Вот топ-3 низких цен и их стран за игру {data_raw[0][0]}\n')
            for el in data_raw:
                data = list(el)
                dispatcher.utter_message(text=f'Цена: {data[1]} рубля, страна: {data[2]}\n')

        return []
# предложить рандомную игру и 3 самые низкие цены
class ActionRandomGame(Action):
 
    def name(self) -> Text:              # регистрируем имя действия
        return "action_random_game"
 
    def run(self, dispatcher:CollectingDispatcher, tracker:Tracker, domain:Dict[Text,Any]) -> List[Dict[Text, Any]]:
 
        index = random.randint(1, 100)

        conn = sqlite3.connect('misis.db')
        cursor = conn.cursor()
        index = random.randint(1, 100)
        cursor.execute(f"SELECT g.name, round(p.price*l.currency_weight, 2) as rouble_price, l.country from price as p, localization as l, game as g where l.localization_id=p.localization_id and g.game_id=p.game_id and g.game_id = {index} order by rouble_price limit 3")
        data_raw = cursor.fetchall()

        data = [list(row) for row in data_raw]
        dispatcher.utter_message(text=f'Вот топ 3 низких цен для игры {data[0][0]}:')
        for i in range(3):
            dispatcher.utter_message(text=f'Игра стоит {data[i][1]} рубля в {data[i][2]}')

        return []
    
# поиск самых дешевых игр (без разделения на локации)
class ActionCheapestGame(Action):
 
    def name(self) -> Text:              # регистрируем имя действия
        return "action_cheapest_game"
 
    def run(self, dispatcher:CollectingDispatcher, tracker:Tracker, domain:Dict[Text,Any]) -> List[Dict[Text, Any]]:

        conn = sqlite3.connect('misis.db')
        cursor = conn.cursor()
        cursor.execute(f'''SELECT g.name, round(MIN(p.price*l.currency_weight), 2) as rouble_price, l.country 
                from price as p, localization as l, game as g 
                where 
                        l.localization_id=p.localization_id 
                        and
                        g.game_id=p.game_id 
                group by g.name
                order by rouble_price limit 3''')
        data_raw = cursor.fetchall()

        for i in range(3):
            dispatcher.utter_message(text=f'Игра {data_raw[i][0]} стоит {data_raw[i][1]} рубля в {data_raw[i][2]}')

        return []
    
# поиск рандомной игры определенного жанра по мминимальной цене
class ActionRandomGameInGenre(Action):
 
    def name(self) -> Text:              # регистрируем имя действия
        return "action_random_game_in_genre"
 
    def run(self, dispatcher:CollectingDispatcher, tracker:Tracker, domain:Dict[Text,Any]) -> List[Dict[Text, Any]]:
 
        genre_number = tracker.get_slot("GENRE_NUMBER")
        test = 2
        dispatcher.utter_message(text=f'GENRE_NUMBER: {genre_number}')

        conn = sqlite3.connect('misis.db')
        cursor = conn.cursor()

        cursor.execute(f'''SELECT g.name, round(MIN(p.price*l.currency_weight), 2) as rouble_price, l.country, gen.name
                from price as p, localization as l, game as g, genre as gen, game_genre as gg
                where 
                        l.localization_id=p.localization_id 
                        and
                        g.game_id=p.game_id
                        and
                        gg.game_id = g.game_id
                        and
                        gen.genre_id = gg.genre_id
                        and
                        gen.genre_id = {test}
                group by g.name
                order by rouble_price''')
        #data_raw = cursor.fetchall()

        #data = list(data_raw[random.randint(1, len(data_raw))])
        #dispatcher.utter_message(text=f'Игра {data[0]} стоит {data[1]} рубля в {data[2]}')

        conn.close()
        return []

class ActionChooseOption(Action):
 
    def name(self) -> Text:              # регистрируем имя действия
        return "action_choose_option"
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(buttons = [
                {"payload": "/game_min_prices", "title": "Найти топ 3 низких цен для игры"},
                {"payload": "/random_game", "title": "Найти топ 3 низких цен для случайной игры"},
                {"payload": "/cheapest_game", "title": "Найти топ 3 самые дешевые игры"},
                {"payload": "/random_game_in_genre", "title": "Найти рандомную игру из жанра"}
            ])
        return []
    

class ActionGetGenre(Action):
    def name(self):
        return "action_get_genre"

    def run(self, dispatcher, tracker, domain):
        genres = [(0,'казуальная'),
        (1,'экшен'),
        (2,'шутер'),
        (3,'RPG'),
        (4,'стратегия'),
        (5,'хоррор'),
        (6,'стелс'),
        (7,'приключение'),
        (8,'файтинг'),
        (9,'выживание')]
        dispatcher.utter_message(text="Выберите номер жанра:")
        for i in range(10):
            dispatcher.utter_message(text=f'{i+1}. {genres[i][1]}')
        return []
