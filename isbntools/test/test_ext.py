#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nose.tools import assert_equals, assert_raises
from ..ext import mask, editions, isbn_from_words


# nose tests


def test_mask():
    assert_equals(mask('5852700010'), '5-85270-001-0')
    assert_equals(mask('0330284983'), '0-330-28498-3')
    assert_equals(mask('3796519008'), '3-7965-1900-8')
    assert_equals(mask('4198301271'), '4-19-830127-1')
    assert_equals(mask('2226052577'), '2-226-05257-7')
    assert_equals(mask('6053840572'), '605-384-057-2')
    assert_equals(mask('7301102992'), '7-301-10299-2')
    assert_equals(mask('8085983443'), '80-85983-44-3')
    assert_equals(mask('9056911872'), '90-5691-187-2')
    assert_equals(mask('9500404427'), '950-04-0442-7')
    assert_equals(mask('9800101942'), '980-01-0194-2')
    assert_equals(mask('9813018399'), '981-3018-39-9')
    assert_equals(mask('9786001191251'), '978-600-119-125-1')
    assert_equals(mask('9780321534965'), '978-0-321-53496-5')
    assert_equals(mask('9781590593561'), '978-1-59059-356-1')
    assert_equals(mask('9789993075899'), '978-99930-75-89-9')
    assert_equals(mask('0-330284983'), '0-330-28498-3')
    assert_equals(mask('9791090636071'), '979-10-90636-07-1')
    assert_equals(mask(''), None)


def test_editions():
    assert_equals(len(editions('9780156001311')), 19)
    assert_equals(len(editions('9780151446476')), 19)
    assert_raises(TypeError, len(editions('9780151446476')))


def test_isbn_from_words():
    assert_equals(len(isbn_from_words('old men and sea')), 13)
# flake8: noqa
