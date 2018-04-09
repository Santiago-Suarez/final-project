from google.appengine.ext import ndb

class Message(ndb.Model):
    sender_name = ndb.StringProperty()
    sender_email = ndb.StringProperty()
    receiver_name = ndb.StringProperty()
    receiver_email = ndb.StringProperty()
    text = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)
