#!/usr/bin/env python3
'''Regex-ing'''
from typing import List, Match, Optional
import re
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''function that returns the log message obfuscated'''
    for e in fields:
        message = re.sub(e+'=(.*?)'+separator,
                         e+"="+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        msg = filter_datum(self._fields, self.REDACTION,
                           record.msg, self.SEPARATOR)
        record.msg = msg
        return super(RedactingFormatter, self).format(record)
