#!/usr/bin/env python3
"""
Obfuscation
"""
import re
import logging
from typing import List
import os
import MySQLdb


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password',)


def main():
    """Main function
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    str_row = ""
    fields = {
            0: "name",
            1: "email",
            2: "phone",
            3: "ssn",
            4: "password",
            5: "ip",
            6: "last_login",
            7: "user_agent",
        }
    obfuscated = ["name", "email", "phone", "ssn", "password"]
    for row in cursor.fetchall():
        i = 0
        while i < 8:
            str_row += " " + fields[i] + "=" + str(row[i]) + ";"
            i += 1
        str_row = str_row[1:]
        record = logging.LogRecord("user_data", logging.INFO, None, None, str_row, None, None)
        formatter = RedactingFormatter(obfuscated)
        print(formatter.format(record))
    cursor.close()
    db.close()
        

def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscation 'fileds' values in 'message'"""
    for field in fields:
        message = re.sub(f'{field}=[^{separator}]*',
                         f'{field}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    """Returns a Logger class object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> "<class 'mysql.connector.connection.MySQLConnection'>":
    """Returns a connection object to a database
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', default='root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', default='')
    host = os.getenv('PERSONAL_DATA_DB_HOST', default='localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')
    return MySQLdb.connect(
            user=user, passwd=password, db=db, host=host, port=3306)


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

if __name__ == "__main__":
    main()
