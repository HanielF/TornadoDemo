import tornado.web
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
import os
import datetime
import asyncio
import tornado.escape
import tornado.ioloop
import tornado.locks
import tornado.web
import os.path
import uuid

from tornado.options import define, options, parse_command_line




# 视图类
class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("Hello World")


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"],
            }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)


class MessageBuffer(object):
    def __init__(self):
        # cond is notified whenever the message cache is updated
        self.cond = tornado.locks.Condition()
        self.cache = []
        self.cache_size = 200

    def get_messages_since(self, cursor):
        """Returns a list of messages newer than the given cursor.
        ``cursor`` should be the ``id`` of the last message received.
        """
        results = []
        for msg in reversed(self.cache):
            if msg["id"] == cursor:
                break
            results.append(msg)
        results.reverse()
        return results

    def add_message(self, message):
        self.cache.append(message)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size :]
        self.cond.notify_all()


# Making this a non-singleton is left as an exercise for the reader.
global_message_buffer = MessageBuffer()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=global_message_buffer.cache)


class MessageNewHandler(tornado.web.RequestHandler):
    """Post a new message to the chat room."""

    def post(self):
        message = {"id": str(uuid.uuid4()), "body": self.get_argument("body")}
        # render_string() returns a byte string, which is not supported
        # in json, so we must convert it to a character string.
        message["html"] = tornado.escape.to_unicode(
            self.render_string("message.html", message=message)
        )
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        global_message_buffer.add_message(message)


class MessageUpdatesHandler(tornado.web.RequestHandler):
    """Long-polling request for new messages.
    Waits until new messages are available before returning anything.
    """

    async def post(self):
        cursor = self.get_argument("cursor", None)
        messages = global_message_buffer.get_messages_since(cursor)
        while not messages:
            # Save the Future returned here so we can cancel it in
            # on_connection_close.
            self.wait_future = global_message_buffer.cond.wait()
            try:
                await self.wait_future
            except asyncio.CancelledError:
                return
            messages = global_message_buffer.get_messages_since(cursor)
        if self.request.connection.stream.closed():
            return
        self.write(dict(messages=messages))

    def on_connection_close(self):
        self.wait_future.cancel()
