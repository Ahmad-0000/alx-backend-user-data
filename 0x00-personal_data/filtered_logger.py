#!/usr/bin/env python3
"""
Obfuscation
"""
import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscation 'fileds' values in 'message'"""
    for field in fields:
        message = re.sub(f'{field}=[^{separator}]*',
                         f'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formation and obfuscation"""
        record.msg = filter_datum(self.fields, '***', record.msg, ';')
        output = logging.Formatter.format(self, record)
        return output 
