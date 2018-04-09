#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Message
from google.appengine.api import users
from google.appengine.api import urlfetch
import json
import hmac


template_dir = os.path.join(os.path.dirname(__file__), "templates") #crea directorio para incluir templates
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)#inicializa Jinja


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logged_in = True
            logout_url = users.create_logout_url("/")
            params = {"logged_in": logged_in, "logout_url": logout_url, "user": user}
            return self.redirect_to("inbox")

        else:
            logged_in = False
            login_url = users.create_login_url("/")
            params = {"logged_in": logged_in, "login_url": login_url, "user": user}
            return self.render_template("hello.html", params=params)

class WriteHandler(MainHandler):
    def get(self):
        return self.render_template("write.html")

    def post(self):
        user = users.get_current_user()
        se = user.email()
        sn = self.request.get("sender_name")
        rn = self.request.get("receiver_name")
        re = self.request.get("receiver_email")
        t = self.request.get("email_text")


        msg = Message(sender_name=sn, sender_email=se, receiver_name=rn, receiver_email=re, text=t)
        msg.put()
        return self.redirect_to("inbox")

class InboxHandler(MainHandler):
    def get(self):
        url = "http://api.openweathermap.org/data/2.5/weather?q=Malaga,es&units=metric&appid=0cc6e3d89bd2a71c507f04a5ef33882c"
        result = urlfetch.fetch(url)
        weather_info = json.loads(result.content)
        user = users.get_current_user()
        inbox = Message.query(Message.receiver_email == user.email()).fetch()
        params = {"emails": inbox, "title": "Inbox", "weather_info": weather_info}
        return self.render_template("inbox.html", params=params)


class SentHandler(MainHandler):
    def get(self):
        url = "http://api.openweathermap.org/data/2.5/weather?q=Malaga,es&units=metric&appid=0cc6e3d89bd2a71c507f04a5ef33882c"
        result = urlfetch.fetch(url)
        weather_info = json.loads(result.content)
        user = users.get_current_user()
        sent = Message.query(Message.sender_email == user.email()).fetch()
        params = {"emails": sent, "title": "Sent", "weather_info": weather_info}
        return self.render_template("inbox.html", params = params)


class WeatherHandler(MainHandler):
    def get(self):
        url = "http://api.openweathermap.org/data/2.5/weather?q=Malaga,es&units=metric&appid=0cc6e3d89bd2a71c507f04a5ef33882c"
        result = urlfetch.fetch(url)
        weather_info = json.loads(result.content)
        params = {"weather_info": weather_info}
        self.render_template("weather.html", params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/inbox', InboxHandler, name ="inbox"),
    webapp2.Route('/sent', SentHandler, name ="sent"),
    webapp2.Route('/write', WriteHandler),
    webapp2.Route('/weather', WeatherHandler),
], debug=True)

#ninjaprojectmalaga@gmail.com
#Pythonisos18
