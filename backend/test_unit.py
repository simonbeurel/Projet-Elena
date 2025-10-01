import backend.util 
import pytest

print("UNIT TESTS")

def test_useless():
    assert 1==1

def test_retrieve_id_from_name_mongo():
    playername = "swiatek iga"
    result = backend.util.get_id_from_name_mongo(playername)
    assert result == "jNyZsXZe"
    
def test_retrieve_name_from_id_mongo():
    player_id = "vVcA2087"
    result = backend.util.get_name_from_id_mongo(player_id)
    assert result == "alison riske amritraj"