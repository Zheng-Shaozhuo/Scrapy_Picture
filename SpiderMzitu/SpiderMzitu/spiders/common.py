# -*- coding: utf-8 -*-
import re
import sys
reload(sys)

import pymysql
import time

from SpiderMzitu.settings import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME, DB_CHARSET

def _query(sql):
    _conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset=DB_CHARSET)
    _cursor = _conn.cursor()

    try:
        _cursor.execute(sql)
        rows = _cursor.fetchall()
        _conn.commit()
        _cursor.close()
        _conn.close()
        return rows
    except:
        _cursor.close()
        _conn.close()
        return []
    pass

def _execute(sql):
    _conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS, db=DB_NAME, charset=DB_CHARSET)
    _cursor = _conn.cursor()

    try:
        _cursor.execute(sql)
        _conn.commit()
        _cursor.close()
        _conn.close()
        return True
    except:
        _cursor.close()
        _conn.close()
        return False

    pass

def _strip(path):
    sys.setdefaultencoding('utf-8')
    try:
        # path = re.sub(r'[？\\*|“<>:/]', '', str(path))
        path = str(path).strip().replace('【', '_').replace('】', '_').replace('？', '_').replace('“', '_').replace('”','_').replace('，', '_')
    except:
        path = int(time.time())
    return path