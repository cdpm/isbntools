# -*- coding: utf-8 -*-
"""
Queries the isbndb.org service for metadata
"""

import logging
import re
from isbntools.dev.webquery import query as wquery
from isbntools.dev.data import stdmeta
from isbntools.bouth23 import u
from isbntools.config import apikeys
from isbntools.dev.exceptions import (DataWrongShapeError,
                                      NoDataForSelectorError,
                                      RecordMappingError, NoAPIKeyError)


UA = 'isbntools (gzip)'
SERVICE_URL = 'http://isbndb.com/api/v2/json/%s/book/%s'
PATT_YEAR = re.compile(r'\d{4}')
LOGGER = logging.getLogger(__name__)


def _mapper(isbn, records):
    """
    Mapping canonical <- records
    """
    # canonical:
    # -> ISBN-13, Title, Authors, Publisher, Year, Language
    try:
        # mapping: canonical <- records
        canonical = {}
        canonical['ISBN-13'] = u(isbn)
        # assert isbn == records['isbn13'], "isbn was mungled!"
        canonical['Title'] = records.get('title', u(''))
        authors = [a['name'] for a in records['author_data']]
        canonical['Authors'] = authors
        canonical['Publisher'] = records.get('publisher_name', u(''))
        canonical['Year'] = u('')
        if 'edition_info' in records:
            match = re.search(PATT_YEAR, records['edition_info'])
            if match:
                canonical['Year'] = str(match.group(0))
        canonical['Language'] = records.get('language', u(''))
    except:
        raise RecordMappingError(isbn)
    # call stdmeta for extra cleanning and validation
    return stdmeta(canonical)


def _records(isbn, data):
    """
    Classifies (canonically) the parsed data
    """
    try:
        # put the selected data in records
        records = data['data'][0]
    except:
        try:
            extra = data['error']
            LOGGER.debug('DataWrongShapeError for %s with data %s',
                         isbn, extra)
        except:
            raise DataWrongShapeError(isbn)
        raise NoDataForSelectorError(isbn)

    # map canonical <- records
    return _mapper(isbn, records)


def query(isbn):
    """
    Queries the isbndb.org service for metadata
    """
    if not apikeys.get('isbndb'):
        raise NoAPIKeyError
    data = wquery(SERVICE_URL % (apikeys['isbndb'], isbn), UA)
    return _records(isbn, data)
