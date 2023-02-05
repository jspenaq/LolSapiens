from backend.lolsapiens.lolsapiens import get_languages

def test_get_languages():
    assert type(get_languages()) is list