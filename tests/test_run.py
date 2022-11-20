import pytest
from canary_islands_professors_designations.run import format_message


def test_format_message():

    input = {
        'Tenerife': 1,
        'Gran Canaria': 2
    }

    actual = format_message(input)

    expected = """Los llamamientos de biologia para hoy son: 
Tenerife: 1
Gran Canaria: 2
"""

    assert actual == expected

def test_format_message_with_empty_designations():

    input = {}

    actual = format_message(input)

    expected = 'Hoy no han habido llamamientos para biologia'

    assert actual == expected