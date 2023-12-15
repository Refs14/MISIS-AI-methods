from rasa_sdk          import Action, Tracker
from rasa_sdk.events   import SlotSet
from rasa_sdk.executor import CollectingDispatcher
 
from datetime import datetime as dt
from typing import Any, Text, Dict, List
import sqlite3
import random
 
class ActionMinPriceForGame(Action):
 
    def name(self) -> Text:              # регистрируем имя действия
        return "action_find_prices"
 
    def run(self, dispatcher:CollectingDispatcher, tracker:Tracker, domain:Dict[Text,Any]) -> List[Dict[Text, Any]]:
 
        info_game = tracker.get_slot("GAME")

        conn = sqlite3.connect('misis.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT p.game, round(p.price*l.currency_weight, 2) as rouble_price, l.country from price as p, localization as l where l.localization_id=p.localization_id and p.game = '{info_game}' order by rouble_price limit 3")
        data_raw = cursor.fetchall()
        if(len(data_raw)==0):
            dispatcher.utter_message(text=f'Игра {info_game} не найдена: ее нет в базе данных или название введено неверно')
        else:
            dispatcher.utter_message(text=f'Вот топ-3 низких цен и их стран за игру {data_raw[0][0]}\n')
            for el in data_raw:
                data = list(el)
                dispatcher.utter_message(text=f'Цена: {data[1]} рубля, страна: {data[2]}\n')

        return []
    
class ActionOfferRandomGame(Action):
 
    def name(self) -> Text:              # регистрируем имя действия
        return "action_offer_random"
 
    def run(self, dispatcher:CollectingDispatcher, tracker:Tracker, domain:Dict[Text,Any]) -> List[Dict[Text, Any]]:
 
        index = random.randint(1, 100)

        conn = sqlite3.connect('misis.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT p.game, round(p.price*l.currency_weight, 2) as rouble_price, l.country from price as p, localization as l where l.localization_id=p.localization_id and p.price_id = '{index}' order by rouble_price limit 1")
        data_raw = cursor.fetchall()

        data = list(data_raw[0])
        dispatcher.utter_message(text=f'Игра {data[0]} стоит {data[1]} рубля в {data[2]}')

        return []