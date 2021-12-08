import pytest
import json
from flaskr.databases.collection_models.queueOperation import queueOperation
from Home_appliance_control_AI.applianceControl import *

# def test_config():
#     assert not control().testing
#     assert control({'TESTING': True}).testing


@pytest.fixture(scope = 'function', autouse=True)
def scope_function():#いったんmocker抜いた
    #テスト前処理
    #queueOperationを空にする
    queueOperation.objects.all().delete()

    print("setup before session")
    yield
    #テスト後処理

    print("teardown after session")




def test_controlTest_high_1():
    
    control(15, 20)

    operation = queueOperation.objects(appliance="学校のサーキュレータ").order_by("+_id").first()
    x = int.from_bytes(operation.data, "big")
    ope = hex(x)
    operation.delete()

    operation2 = queueOperation.objects(appliance="学校のサーキュレータ").order_by("+_id").first()
    x = int.from_bytes(operation2.data, "big")
    ope2 = hex(x)
    operation2.delete()

    assert ope == "0x17b00ff"
    assert ope2 == "0x17b10ef"



def test_controlTest_high_2():
    #client = app.test_client()

    control(25, 30)
    operation = queueOperation.objects(appliance="学校のサーキュレータ").order_by("+_id").first()
    x = int.from_bytes(operation.data, "big")
    ope = hex(x)
    operation.delete()

    operation2 = queueOperation.objects(appliance="学校のサーキュレータ").order_by("+_id").first()
    x = int.from_bytes(operation2.data, "big")
    ope2 = hex(x)
    operation2.delete()

    assert ope == "0x17b00ff"
    assert ope2 == "0x17b10ef"


def test_controlTest_low_1():
    #client = app.test_client()

    response = control(25, 20)
    operation = queueOperation.objects(appliance="学校のサーキュレータ").order_by("+_id").first()
    x = int.from_bytes(operation.data, "big")
    ope = hex(x)

    operation.delete()

    assert ope == "0x17b00ff"


def test_controlTest_low_2():
    #client = app.test_client()

    response = control(20, 15)
    operation = queueOperation.objects(appliance="学校のサーキュレータ").order_by("+_id").first()
    x = int.from_bytes(operation.data, "big")
    ope = hex(x)

    operation.delete()

    assert ope == "0x17b00ff"




# def test_controlTest_suitable_1():
#     #client = app.test_client()

#     response = control("0", 20, 20)
#     #applianceControl.control(sNumber, int(tActual), tTarget)

#     assert response == "tolerance"

# def test_controlTest_suitable_2():
#     #client = app.test_client()

#     response = control("0", 26, 23)
#     #applianceControl.control(sNumber, int(tActual), tTarget)

#     assert response == "tolerance"


# def test_controlTest_suitable_3():
#     #client = app.test_client()

#     response = control("0", 18, 21)
#     #applianceControl.control(sNumber, int(tActual), tTarget)

#     assert response == "tolerance"



# def test_controlTest_outRange_1():
#     #client = app.test_client()

#     response = control(18, 21)
#     #applianceControl.control(sNumber, int(tActual), tTarget)

#     assert response == "tolerance"





