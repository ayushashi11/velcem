import os
from dotenv import load_dotenv
load_dotenv()
def test_KEY():
    assert os.getenv("KEY") is not None
def test_TOKEN():
    assert os.getenv("TOKEN") is not None
def test_GUILD():
    assert os.getenv("GUILD") is not None
def test_MID():
    assert os.getenv("MID") is not None
def test_NCID():
    assert os.getenv("NCID") is not None
def test_DBID():
    assert os.getenv("DBID") is not None
