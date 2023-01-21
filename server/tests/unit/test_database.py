from website.models import database_request

def test_response():
    assert database_request() == "database_response"