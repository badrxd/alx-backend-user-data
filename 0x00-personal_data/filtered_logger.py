#!/usr/bin/env python3
'''Regex-ing'''
from typing import List, Match, Optional
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''function that returns the log message obfuscated'''
    for e in fields:
        pattern = r'{}=(.*?){}'.format(e, separator)
        message = re.sub(
            re.search(pattern, message).group(1), redaction, message)
    return message
