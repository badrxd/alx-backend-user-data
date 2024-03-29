#!/usr/bin/env python3
'''Regex-ing'''
from typing import List, Match, Optional
import re
import logging
from mysql.connector import connection
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


def get_db() -> connection.MySQLConnection:
    '''returns a connector to the database'''
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    return connection.MySQLConnection(
        host=host,
        username=db_username,
        password=db_password,
        database=db_name
    )


def main() -> None:
    '''function obtain a database connection using get_db and
    retrieve all rows in the users table and display each row under
    a filtered format'''
    logger = get_logger()
    db_connex = get_db()
    cursor = db_connex.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for cu in cursor.fetchall():
        text = ""
        for i in range(len(cu)):
            text += "{}={};".format(fields[i], cu[i])
        logger.info(msg=text)
    cursor.close()
    db_connex.close()


if __name__ == "__main__":
    main()
