import json
import sys

from pprint import pprint
from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine, context_manager

engine = IntentDeterminationEngine()

pandora_keyword = [
    "pandora"
]

pronoun_keyword = [
    "he",
    "she",
    "they",
    "them"
]

where_keyword = [
    "in town",
    "here"
]

day_keyword = [
    "Saturday",
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

for kw in pandora_keyword:
    engine.register_entity(kw, "PandoraKeyword")

for kw in pronoun_keyword:
    engine.register_entity(kw, "ProNounKeyword")

for kw in where_keyword:
    engine.register_entity(kw, "WhereKeyword")

engine.register_entity("when", "WhenKeyword")
engine.register_entity("next", "NextKeyword")

engine.register_regex_entity("play (?P<Artist>.*) on")

pandora_intent = IntentBuilder("PandoraIntent")\
    .require("PandoraKeyword")\
    .require("Artist")\
    .build()

engine.register_intent_parser(pandora_intent)

concert_intent = IntentBuilder("ConcertIntent")\
    .link_one_of("Artist", "ProNounKeyword")\
    .require("WhenKeyword")\
    .optionally("NextKeyword")\
    .require("WhereKeyword")\
    .build()

engine.register_intent_parser(concert_intent)

engine.register_entity("weather", "WeatherKeyword")
for kw in day_keyword:
    engine.register_entity(kw, "DayKeyword")

weather_intent = IntentBuilder("WeatherIntent")\
    .require("DayKeyword", "mycroft_response")\
    .build()

engine.register_intent_parser(weather_intent)

if __name__ == "__main__":
    print "*"*100
    utterance = "Hey mycroft, play taylor swift on pandora"
    for intent in engine.determine_intent(utterance, num_results=1):
        if intent.get('confidence') > 0:
            print "utterance:", utterance
            print(json.dumps(intent, indent=4))
            intent['mycroft_response'] = ""

    print "*"*100
    utterance = "Hey mycroft, when is she in town next?"
    for intent in engine.determine_intent(utterance, num_results=1):
        if intent.get('confidence') > 0:
            print "utterance:", utterance
            print(json.dumps(intent, indent=4))
            intent['mycroft_response'] = "TaySway will be in your area this Saturday night."

    print "*"*100
    utterance = "hey mycroft, what's the weather going to be like?"
    for intent in engine.determine_intent(utterance, num_results=1):
        if intent.get('confidence') > 0:
            print "utterance:", utterance
            print(json.dumps(intent, indent=4))
            intent['mycroft_response'] = "It will be 67 degrees with a 9pm sunset this saturday."

    pprint(context_manager.history)