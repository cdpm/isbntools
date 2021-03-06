# -*- coding: utf-8 -*-
"""
Queries the worldcat.org service for related ISBNs
"""

import logging
from ast import literal_eval
from .dev.webquery import query as wquery
from .dev.exceptions import DataWrongShapeError, NoDataForSelectorError

LOGGER = logging.getLogger(__name__)
UA = 'isbntools (gzip)'
SERVICE_URL = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s?'\
              'method=getEditions&format=python'


def _editions(isbn, data):
    """
    Returns the records from the parsed response
    """
    try:
        # put the selected data in records
        records = [ib['isbn'][0] for ib in data['list']]
    except:    # pragma: no cover
        try:
            extra = data['stat']
            LOGGER.debug('DataWrongShapeError for %s with data %s',
                         isbn, extra)
        except:
            raise DataWrongShapeError(isbn)
        raise NoDataForSelectorError(isbn)
    return records


def query(isbn):
    """
    Queries the worldcat.org service for metadata
    """
    data = wquery(SERVICE_URL % isbn, UA, parser=literal_eval)
    return _editions(isbn, data)
