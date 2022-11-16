import pytest


def test_get_metadata_form():
    
     response = requests.get("")
     assert response.status_code == 200