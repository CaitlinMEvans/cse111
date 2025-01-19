from names import make_full_name, extract_family_name, extract_given_name
import pytest

def test_make_full_name():
    # Test for normal names
    assert make_full_name("Harry", "Potter") == "Potter;Harry"
    assert make_full_name("Hermione", "Granger") == "Granger;Hermione"
    # Test for hyphenated names
    assert make_full_name("Albus", "Dumbledore-Smith") == "Dumbledore-Smith;Albus"
    # Test for long names
    assert make_full_name("Sirius", "Black") == "Black;Sirius"

def test_extract_family_name():
    # Test for normal names
    assert extract_family_name("Potter;Harry") == "Potter"
    assert extract_family_name("Granger;Hermione") == "Granger"
    # Test for hyphenated names
    assert extract_family_name("Dumbledore-Smith;Albus") == "Dumbledore-Smith"
    # Test for long names
    assert extract_family_name("Black;Sirius") == "Black"

def test_extract_given_name():
    # Test for normal names
    assert extract_given_name("Potter;Harry") == "Harry"
    assert extract_given_name("Granger;Hermione") == "Hermione"
    # Test for hyphenated names
    assert extract_given_name("Dumbledore-Smith;Albus") == "Albus"
    # Test for long names
    assert extract_given_name("Black;Sirius") == "Sirius"
