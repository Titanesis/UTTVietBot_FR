#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from datetime import datetime
import io

CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class VietBot(object):
    """ VietBot class wrapper
    """

    def __init__(self):
        # get the configuration if needed

        self.start_blocking()

    def _create_today_menu(self, dish):
        menu_of_the_day = "Aujourd'hui, tu peux manger {0}.".format(dish)
        return menu_of_the_day

    def _create_day_menu(self, day, dish):
        menu_of_the_day = "{0}, tu pourras manger {1}.".format(day, dish)
        return menu_of_the_day

    def askmenu_callback(self, hermes, intent_message):
        hermes.publish_end_session(intent_message.session_id, "")

        en_fr_dict = {
            "Monday": "Lundi",
            "Tuesday": "Mardi",
            "Wednesday": "Mercredi",
            "Thursday": "Jeudi",
            "Friday": "Vendredi"
        }

        menu_dict = {
            "Monday": "des boulettes de boeuf ou du poulet aux légumes",
            "Tuesday": "du poulet rôti ou du porc sauce piquante",
            "Wednesday": "du boeuf aux légumes ou des crevettes aigre-douce",
            "Thursday": "du poulet au curry ou du canard à l'ananas",
            "Friday": "des boulettes de porc ou du poisson aigre-doux"
        }

        if intent_message.slots.menuday:
            str_menu_day = intent_message.slots.menuday.first().value
            dt_menu_day = datetime.strptime(str_menu_day, '%Y-%m-%d %H:%M:%S +00:00')
        else:
            dt_menu_day = datetime.now()

        dt_today = datetime.now()
        day_name = dt_menu_day.strftime("%A")

        if dt_today.date() != dt_menu_day.date():
            sentence = self._create_day_menu(en_fr_dict[day_name], menu_dict[day_name])
        else:
            sentence = self._create_today_menu(menu_dict[day_name])

        hermes.publish_start_session_notification(intent_message.site_id, sentence, "VietBot_FR")

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self, hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'redTitan:MenuDuJour':
            self.askmenu_callback(hermes, intent_message)

    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    VietBot()