#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nose.tools import assert_equals
from ..core import (_check_digit10, _check_digit13, _check_structure10,
    _check_structure13, is_isbn10, is_isbn13, to_isbn10, to_isbn13,
    canonical, clean, notisbn, get_isbnlike, get_canonical_isbn)
from ..data.data4tests import ISBNs


# nose tests

def test__check_digit10():
    assert_equals(_check_digit10('082649752'), '7')
    assert_equals(_check_digit10('585270001'), '0')
    assert_equals(_check_digit10('08264975X'), None)
    assert_equals(_check_digit10('08264975'), None)


def test__check_digit13():
    assert_equals(_check_digit13('978082649752'), '9')
    assert_equals(_check_digit13('97808264975'), None)
    assert_equals(_check_digit13('97808264975X'), None)


def test__check_structure10():
    assert_equals(_check_structure10('0826497527'), True)
    assert_equals(_check_structure10('0826497X27'), True) # isbnlike!
    assert_equals(_check_structure10('0826497XI7'), False)


def test__check_structure13():
    assert_equals(_check_structure13('9780826497529'), True)
    assert_equals(_check_structure13('978082649752X'), False)


def test_is_isbn10():
    assert_equals(is_isbn10('0826497527'), True)
    assert_equals(is_isbn10('0826497520'), False)
    assert_equals(is_isbn10('954430603X'), True)


def test_is_isbn13():
    assert_equals(is_isbn13('9780826497529'), True)
    assert_equals(is_isbn13('9791090636071'), True)
    assert_equals(is_isbn13('9780826497520'), False)


def test_to_isbn10():
    assert_equals(to_isbn10('9780826497529'), '0826497527')
    assert_equals(to_isbn10('9780826497520'), '0826497527')  # ISBN13 not valid
    assert_equals(to_isbn10('9790826497529'), None)
    assert_equals(to_isbn10('97808264975X3'), None)


def test_to_isbn13():
    assert_equals(to_isbn13('0826497527'), '9780826497529')
    assert_equals(to_isbn13('0826497520'), '9780826497529')  # ISBN10 not valid
    assert_equals(to_isbn13('08X6497527'), None)


def test_clean():
    assert_equals(clean(' 978.0826.497529'), '9780826497529')
    assert_equals(clean('ISBN: 9791090636071'), 'ISBN 9791090636071')
    assert_equals(clean('978,0826497520'), '9780826497520')


def test_notisbn():
    assert_equals(notisbn('0826497527'), False)
    assert_equals(notisbn('0826497520'), True)
    assert_equals(notisbn('9780826497529', level='strict'), False)
    assert_equals(notisbn('9426497529', level='strict'), True)
    assert_equals(notisbn('978082649752', level='strict'), True)
    assert_equals(notisbn('978082649752', level='loose'), True)
    assert_equals(notisbn('9780826400001', level='loose'), False)
    assert_equals(notisbn('9780826400001', level='strict'), True)
    assert_equals(notisbn('9780826400001', level='badlevel'), None)
    assert_equals(notisbn('978 9426497529'), True)
    assert_equals(notisbn('9789426497529'), True)
    assert_equals(notisbn('979 10 9063607 1'), False)
    assert_equals(notisbn('9780826497520'), True)


def test_get_isbnlike():
    assert_equals(len(get_isbnlike(ISBNs)), 79)
    assert_equals(len(get_isbnlike(ISBNs, 'normal')), 79)
    assert_equals(len(get_isbnlike(ISBNs, 'strict')), 69)
    assert_equals(len(get_isbnlike(ISBNs, 'loose')), 81)
    assert_equals(get_isbnlike(ISBNs, 'e'), None)


def test_get_canonical_isbn():
    assert_equals(get_canonical_isbn('0826497527', output='bouth'),
                  '0826497527')
    assert_equals(get_canonical_isbn('0826497527'), '0826497527')
    assert_equals(get_canonical_isbn('0826497527', output='isbn10'),
                  '0826497527')
    assert_equals(get_canonical_isbn('0826497527', output='isbn13'),
                  '9780826497529')
    assert_equals(get_canonical_isbn('ISBN 0826497527', output='isbn13'),
                  '9780826497529')
    assert_equals(get_canonical_isbn('ISBN 0826497527', output='NOOPTION'),
                  None)
    assert_equals(get_canonical_isbn('0826497520'), None)
    assert_equals(get_canonical_isbn('9780826497529'), '9780826497529')
    assert_equals(get_canonical_isbn('9780826497520'), None)


def test_canonical():
    assert_equals(canonical('ISBN 9789720404427'), '9789720404427')
    assert_equals(canonical('ISBN-9780826497529'), '9780826497529')
    assert_equals(canonical('ISBN9780826497529'), '9780826497529')
    assert_equals(canonical('isbn9780826497529'), '9780826497529')
    assert_equals(canonical('isbn 0826497527'), '0826497527')

# flake8: noqa
