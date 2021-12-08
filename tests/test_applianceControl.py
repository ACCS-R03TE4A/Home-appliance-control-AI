import pytest
import json
#from Home-appliance-Control-AI 
from applianceControl import *


# def test_config():
#     assert not control().testing
#     assert control({'TESTING': True}).testing

@pytest.fixture(scope = 'module', autouse=True)
def scope_module():
    print()
    print(f"-----------------{__name__}のテスト-----------------")
    yield
    print(f"--------------------------------------------------------")
    print()

def test_controlTest_high_1():
    #client = app.test_client()

    response = control("0", 15, 20)
    #applianceControl.control(sNumber, int(tActual), tTarget)

    assert response == "上げる"


def test_controlTest_high_2():
    #client = app.test_client()

    response = control("0", 25, 30)
    #applianceControl.control(sNumber, int(tActual), tTarget)

    assert response == "上げる"


def test_controlTest_low_1():
    #client = app.test_client()

    response = control("0", 25, 20)
    #applianceControl.control(sNumber, int(tActual), tTarget)

    assert response == "下げる"


def test_controlTest_low_2():
    #client = app.test_client()

    response = control("0", 20, 15)
    #applianceControl.control(sNumber, int(tActual), tTarget)

    assert response == "下げる"



def test_controlTest_low_2():
    #client = app.test_client()

    response = control("0", 20, 15)
    #applianceControl.control(sNumber, int(tActual), tTarget)

    assert response == "下げる"



def test_controlTest_true_1():
    #client = app.test_client()

    response = control("0", 20, 20)
    #applianceControl.control(sNumber, int(tActual), tTarget)

    assert response == "tolerance"

def test_controlTest_true_2():
    #client = app.test_client()

    response = control("0", 26, 23)
    #applianceControl.control(sNumber, int(tActual), tTarget)

    assert response == "tolerance"


def test_controlTest_true_3():
    #client = app.test_client()

    response = control("0", 18, 21)
    #applianceControl.control(sNumber, int(tActual), tTarget)

    assert response == "tolerance"



def test_controlTest_outRange_1():
    #client = app.test_client()

    response = control("0", 18, 21)
    #applianceControl.control(sNumber, int(tActual), tTarget)

    assert response == "tolerance"





