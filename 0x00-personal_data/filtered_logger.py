#!/usr/bin/env python3
'''Regex-ing'''
from typing import List, Match, Optional
import re
import logging
import mysql.connector
import os

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''filter the massage that was sent in the record'''
        msg = filter_datum(self._fields, self.REDACTION,
                           record.msg, self.SEPARATOR)
        record.msg = msg
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    '''create a custom looger and return it'''

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()

    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''methode that return mysql connector'''

    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    db_passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    connex = mysql.connector.connect(user=db_user,
                                     password=db_passwd,
                                     host=host,
                                     database=db_name)
    return connex
