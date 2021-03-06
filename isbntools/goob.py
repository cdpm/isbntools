# -*- coding: utf-8 -*-
"""
Queries the Google Books (JSON API v1) for metadata
"""

import logging
from .dev.webquery import query as wquery
from .dev.data import stdmeta
from .bouth23 import u
from .dev.exceptions import (DataWrongShapeError,
                             NoDataForSelectorError,
                             RecordMappingError)

UA = 'isbntools (gzip)'
SERVICE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn+%s&fields='\
    'items/volumeInfo(title,authors,publisher,publishedDate,language)'\
    '&maxResults=1'
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
        canonical['Title'] = records.get('title', u('')).replace(' :', ':')
        canonical['Authors'] = records.get('authors', [u('')])
        canonical['Publisher'] = records.get('publisher', u(''))
        if 'publishedDate' in records \
           and len(records['publishedDate']) >= 4:
            canonical['Year'] = records['publishedDate'][0:4]
        else:         # pragma: no cover
            canonical['Year'] = u('')
        canonical['Language'] = records.get('language', u(''))
    except:           # pragma: no cover
        raise RecordMappingError(isbn)
    # call stdmeta for extra cleanning and validation
    return stdmeta(canonical)


def _records(isbn, data):
    """
    Classifies (canonically) the parsed data
    """
    try:
        # put the selected data in records
        records = data['items'][0]['volumeInfo']
    except:           # pragma: no cover
        try:
            extra = data['stat']
            LOGGER.debug('DataWrongShapeError for %s with data %s',
                         isbn, extra)
        except:
            raise DataWrongShapeError(isbn)
        raise NoDataForSelectorError(isbn)

    # map canonical <- records
    return _mapper(isbn, records)


def query(isbn):
    """
    Queries the Google Books (JSON API v1)service for metadata
    """
    data = wquery(SERVICE_URL % isbn, UA)
    return _records(isbn, data)
