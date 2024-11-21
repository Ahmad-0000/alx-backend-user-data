#!/usr/bin/env python3
"""
Obfuscation
"""
import re


def filter_datum(fields, redaction, message, separator):
    """Obfuscation 'fileds' values in 'message'"""
    for field in fields:
        message = re.sub(f'{field}=[^{separator}]*', f'{field}={redaction}', message)
    return message
