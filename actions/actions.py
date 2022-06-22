from datetime import datetime
from re import A
from time import time
from typing import Any, Text, Dict, List
from psycopg2 import Time
from rasa_sdk.events import SlotSet, ActionExecuted
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from regex import F
import spacy 


nlp = spacy.load("en_core_web_md")


class Name(Action):
    # calling for name  inputing and addressing  
    def name(self) -> Text:
        return "action_name"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = tracker.get_slot('name')

        dispatcher.utter_message(text='OK, {} can you please tell me the location you want to book a hotel in ?'.format(name))

        return []

class Location(Action):
    def name(self) -> Text:
        return "action_location"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        location = tracker.get_slot('location')

        dispatcher.utter_message(text='OK, so the location you want to find the  hotel is {}, when you want to check in on?'.format(location))

        return []

class Checkin(Action):

    def name(self) -> Text:
        return "action_check_in"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # duckling time
        checkin = tracker.get_slot('time').split("T00:00:00.000+00:00")
        checkin1 = ''.join(checkin)
        check_1 = checkin1.split("-")
        check_str = ''.join(check_1)
        check_int = int(check_str)


        # today time
        curr_time = str(datetime.date(datetime.now()))
        ct_list= curr_time.split("-")
        ct_str= ''.join(ct_list)
        ct_int=int(ct_str)
        
        # checking if today is not small then given date.
        if check_int > ct_int:
            dispatcher.utter_message(text="Your check in date is {}, when you want to check out?".format(checkin1))
            return[SlotSet("check_in", checkin1)]
    
        else:
            dispatcher.utter_message("Please enter the date greater than today.")
            dispatcher.utter_message("When you want to check in on?")
            return[ActionExecuted("action_back")]

class checkout(Action):
    def name(self) -> Text:
        return "action_check_out"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # duckling time 
        checkout = tracker.get_slot("time").split("T00:00:00.000+00:00")
        checkout1 = ''.join(checkout)
        checkout2 = checkout1.split("-")
        checkout3 = "".join(checkout2)
        checkout_int = int(checkout3)

        #check in time

        checkin = tracker.get_slot("check_in").split("-")
        checkin1 = ''.join(checkin)
        checkin_int = int(checkin1)

        if checkout_int > checkin_int:
            dispatcher.utter_message(text="Your checkout date is {}, how many rooms do you need?".format(checkout1))
            return[SlotSet("check_out", checkout1)]
        else:
            dispatcher.utter_message(text="Please enter the date of the checkout greater then check in date.")
            return[ActionExecuted("action_back")]


class Rooms(Action):
    def name(self) -> Text:
        return "action_room"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        rooms = tracker.get_slot("number")
        print(rooms)

        if int(rooms) == 0:
            dispatcher.utter_message(text="number of rooms should be one or more.")
            u = tracker.current_slot_values()
            print(u)
            return[ActionExecuted("action_back")]
        else:
            location = tracker.get_slot("location")
            checkin = tracker.get_slot("check_in")
            checkout = tracker.get_slot("check_out")

            dispatcher.utter_message(text='Ok, so your location of hotel is {}, check in date is {}, check out date is {}, and number of rooms is {}, please affrim to confirm.'\
                .format(location, checkin, checkout, rooms))
            
        return []

        


class SessionID(Action):

    def name(self) -> Text:
        return "action_session_id"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        conversation_id = tracker.sender_id

        dispatcher.utter_message(text="the session id is {}".format(conversation_id))

        return []


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "ACTION_DEFAULT_FALLBACK_NAME"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="my_custom_fallback_template")

        # Revert user message which led to fallback.
        return []


class Location1(Action):

    def name(self) -> Text:
        return "action_location1"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        location0 = tracker.get_slot('location')

        dispatcher.utter_message(text="OK, so you the hotel in {}, please tell me your name?".format(location0))

        return[]

class Name1(Action):

    def name(self) -> Text:
        return "action_name1"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name1 = tracker.get_slot('name')
        dispatcher.utter_message(text='Hi {}, Tell me your check in date?'.format(name1))

        return []


class Combined2(Action):

    def name(self) -> Text:
        return "action_combined1"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        location = tracker.get_slot('location')
        checkIN = tracker.get_slot('time').split("T00:00:00.000+00:00")
        checkIN1 = ("").join(checkIN)

        dispatcher.utter_message(text="OK, You want to book a hotel in {} and will be check in on {}, what is your name?".format(location, checkIN1))

        return [SlotSet('check_in', checkIN1)]


class Name2(Action):

    def name(self) -> Text:
        return "action_name0"

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = tracker.get_slot("name")

        dispatcher.utter_message(text="hi {}, now I only need your check out date.".format(name))

        return []



                
        

