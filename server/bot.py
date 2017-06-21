# -*- coding: utf-8 -*-

from typos import TYPOED_GIOSG_NAMES
from .conf import OPEN_WEATHER_MAP_API_KEY
from datetime import datetime
import requests
import json


GIPHY_SEARCH_URL = 'http://api.giphy.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&limit=1&q='


class Jelpperi(object):

    # Handlers
    def handle_feedback(self):
        return {"message": "Thank you for participating our feedback survey."}

    def handle_giosg_name(self, response_value):
        if response_value == 'wrong':
            payload = self.giosg_name_checker(message=None, cont=True)
            payload['message'] = "That didn't quite hit the mark. Let's try again!"
            correct = False
        else:
            payload = {"message": "Cheers! You have finally learned how to spell quiskue correctly."}
            correct = True
        return payload, correct

    # Getters
    def get_giphy_link(self, search_terms, valid_url):
        """
        Use GiphyAPI:
        https://github.com/Giphy/GiphyAPI
        """
        message = "Have some gif"
        if not valid_url:
            search_term = search_terms.replace(' ', '+')
            response = requests.get(GIPHY_SEARCH_URL+search_term)
            try:
                attachments = [{"title": search_terms, "image_url": json.loads(response.content)['data'][0]['images']['fixed_height']['url']}]
                payload = {"message": message, "attachments": attachments}
            except IndexError:
                message = "Sorry I didn't find any gif for that."
                payload = {"message": message}
        else:
            payload = {"message": message, "attachments": [{"image_url": search_terms}]}
        return payload

    def giosg_name_checker(self, message=None, cont=False):
        if any(typo in message for typo in TYPOED_GIOSG_NAMES if message) or cont:
            actions = [
                {
                    "text": "Giosg",
                    "type": "button",
                    "value": "correct",
                    "style": "success",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                },
                {
                    "text": "quiskue",
                    "type": "button",
                    "value": "wrong",
                    "style": "danger",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                },
                {
                    "text": "geosk OS system",
                    "type": "button",
                    "value": "wrong",
                    "style": "danger",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }
            ]
            attachments = [{
                "text": "So how do you spell Giosg?",
                "actions": actions
            }]
            payload = {"message": "Hello my good sir, it seems that you have mistyped Giosg. I'm here to assist you how to write this shit properly.", "attachments": attachments}
            return payload
        return

    def get_lunch(self):
        now = datetime.now()

        # Get sodexo courses and format them
        response = requests.get(
            "http://www.sodexo.fi/ruokalistat/output/daily_json/101/{}/{}/{}/fi".format(now.year, now.month, now.day)
        )

        # Add Roseway foods
        courses = [{"title": "Roseway", "text": u'Inkkari, kebab, rasvalätty ja leike tänäänkin rosewayssa ruokana', "image_url": "http://www.ravintolaroseway.fi/img/img_food/WP_20140920_0021.jpg"}]
        for course in json.loads(response.content)['courses']:
            courses.append({"title": "Sodexo", "text": course['title_fi'], "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/c/ca/Sodexo.svg/1200px-Sodexo.svg.png"})
        return {"message": "Tänään on ruokana", "attachments": courses}

    def get_covfefe(self):
        covfefe_url = 'https://9779d278c82a9b8468643a400f791860c6ba446c7b0eee59028e849b1d7d72.resindevice.io/'
        response = requests.get(covfefe_url)

        if json.loads(response.content)['attachments']:
            attachments = [{"title": json.loads(response.content)['attachments'][0]['text'], "image_url": json.loads(response.content)['attachments'][0]['image_url']}]
            return {"message": "Current coffeee situtation", "attachments": attachments}
        return

    def get_feedback(self):
        actions = [
            {
                "text": "Yes",
                "type": "button",
                "value": "yes",
                "style": "success",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "I don't know",
                "type": "button",
                "value": "maybe",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "No",
                "type": "button",
                "value": "no",
                "style": "danger",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            }
        ]
        attachments = [{
            "text": "Was this conversation helpful?",
            "actions": actions
        }]
        message = {"message": "We would like to hear your feedback about this conversation", "attachments": attachments}
        return message

    def get_weather_forecast(self, city_name, country_code):
        """
        Returns a message payload for a 5 day weather forecast for the
        given city name and the country code.
        """
        url = "http://api.openweathermap.org/data/2.5/forecast?q={},{}&appid={}".format(
            city_name, country_code, OPEN_WEATHER_MAP_API_KEY,
        )
        response = requests.get(url, headers={"Accept": "application/json"})
        response.raise_for_status()
        results = response.json()
        text = "\n\n".join(
            "**{date}**: {weather} ![{weather}]({icon_url})".format(
                date=datetime.fromtimestamp(result['dt']).strftime("%A at %H"),
                weather=weather['main'],
                icon_url="http://openweathermap.org/img/w/{}.png".format(weather['icon']),
            ) for result in results['list'] for weather in result['weather']
        )
        return {
            "type": "msg",
            "message": "Here's the 5 day weather forecast for {}".format(city_name),
            "attachments": [
                {
                    "text": text,
                }
            ]
        }

    def get_wombat_info(self):
        return {
            "type": "msg",
            "message": "Wikipedia says the following thing about wombats:",
            "attachments": [
                {
                    "title": "Wombat",
                    "title_link_url": "https://en.wikipedia.org/wiki/Wombat",
                    "text": \
                        "**Wombats** are short-legged, muscular [quadrupedal](https://en.wikipedia.org/wiki/Quadruped) "\
                        "[marsupials](https://en.wikipedia.org/wiki/Marsupial) that are native to [Australia](https://en.wikipedia.org/wiki/Australia). "\
                        "They are about 1 m (40 in) in length with small, stubby tails. There are three extant species and they are "\
                        "all members of the [family](https://en.wikipedia.org/wiki/Family_(biology)) **Vombatidae**.\n\n"\
                        "They are not commonly seen, but leave ample evidence of their passage, treating fences as minor "\
                        "inconveniences to be gone through or under, and leaving distinctive cubic [faeces](https://en.wikipedia.org/wiki/Faeces).",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Vombatus_ursinus_-Maria_Island_National_Park.jpg/440px-Vombatus_ursinus_-Maria_Island_National_Park.jpg",
                    "image_link_url": "https://en.wikipedia.org/wiki/Wombat",
                }
            ]
        }
