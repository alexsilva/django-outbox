import re
from email.parser import Parser
from os import path, listdir

from django.conf import settings
from django.utils.timezone import localtime


class Outbox(object):
    
    def __init__(self):
        self._parser = Parser()

    def all(self):
        try:
            return list(reversed(
                    [self._message_from_file(filepath) 
                    for filepath in listdir(self.maildirectory)]))
        except OSError:
            return []

    def get(self, id):
        return self._message_from_file(id)

    def _message_from_file(self, filepath):
        abspath = path.join(self.maildirectory, filepath)
        with open(abspath) as f:
            message = self._parser.parse(f)
            return self._convert_message(filepath, message)

    def _convert_message(self, filepath, message):
        if message.is_multipart():
            body = []
            for submessage in message.get_payload():
                body.append((
                    submessage.get_content_type(),
                    (submessage.get_filename(None), self._clear_content(submessage.get_payload()))
                ))
        else:
            body = [(
                message.get_content_type(),
                (message.get_filename(None), self._clear_content(message.get_payload()))
            )]

        return Mail(
                filepath,
                message.get('Subject'), 
                message.get('From'), 
                message.get('To'), 
                message.get('Date'),
                message.get_content_type(),
                body)

    def _clear_content(self, content):
        return re.sub(r'\n-+', '', content)

    @property
    def maildirectory(self):
        return settings.EMAIL_FILE_PATH


class Mail(object):

    def __init__(self, id, subject, from_address, to, when, content_type, body):
        self._id = id
        self._subject = subject
        self._from_address = from_address
        self._to = to
        self._when = when
        self._content_type = content_type
        self._body = body

    @property
    def id(self):
        return self._id

    @property
    def subject(self):
        return self._subject

    @property
    def body(self):
        return self._body

    @property
    def from_address(self):
        return self._from_address

    @property
    def to(self):
        return self._to

    @property
    def when(self):
        return self._when

    @property
    def when_local(self):
        try:
            from dateutil import parser
            return localtime(parser.parse(self.when))
        except ImportError:
            return self.when

    @property
    def content_type(self):
        return self._content_type
