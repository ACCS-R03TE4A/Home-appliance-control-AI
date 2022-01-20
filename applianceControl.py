from flaskr.databases.collection_models.queueOperation import queueOperation
import traceback
import encodings
from datetime import datetime
from bson import ObjectId
import requests


##################################

def order_save(appliance, protocol, data, size, frequency = None):

    #dataはintで渡されている
    #文字列にして、bytesにしてからDBへ
    

    # data_str = str(data)
    # data = binascii.hexlify(data_str.encode('utf-8'))
    data = data.to_bytes(8, "big")

    if frequency == None:#NEC、家製協
        print(queueOperation(
        appliance = appliance,
        protocol = protocol,
        data = data,
        size = size
        ).save())

    else:#その他
        print(queueOperation(
        appliance = appliance,
        protocol = protocol,
        data = data,
        size = size,
        frequency = frequency
        ).save())
    
    print(appliance, protocol, data, size, frequency)

class circulator:
    code = {
        "学校のサーキュレータ":{
            "ON" : 0x17B00FF,
            "OFF" : 0x17B00FF,
            "Low" : 0x17B08F7,
            "Mid" : 0x17B30CF,
            "High" : 0x17B10EF,
            "Shake" : 0x17B906F
        }
    }
    def __init__(self, name, prot, size):
        self.name = name
        self.prot = prot
        self.size = size
        self.status = 0
    
    def getInfo(self, ope):
        return circulator.code[self.name][ope]

cir = circulator("学校のサーキュレータ", 3, 64)

#####サーキュレータ#####
def tempHigh_cir():
    if cir.status == 1:
        ope = "OFF"
        cir.status = 0
        ##サーキュレータ##
        data = cir.getInfo(ope)
        order_save("学校のサーキュレータ", 3, data, 64)

def tempLow_cir(tActual,tTargetLow):
    #電源オン
    if cir.status == 0: #停止中：0,起動中：1
        ope = "ON"
        cir.status = 1
        ##サーキュレータ##
        data = cir.getInfo(ope)
        order_save("学校のサーキュレータ", 3, data, 64)
    
    #強中弱の設定
    difference = tTargetLow - tActual
    if difference > 5:
        ope = "High"
    elif difference > 3:
        ope = "Mid"
    else:
        ope = "Low"


    # if difference > 3:
    #     ope = "Low"
    # elif difference > 5:
    #     ope = "Mid"
    # else:
    #     ope = "High"

    data = cir.getInfo(ope)
    order_save("学校のサーキュレータ", 3, data, 64)
#####

#####リレーモジュール
def tempHigh_relay():
    requests.get("http://192.168.59.129/off")

def tempLow_relay():
    requests.get("http://192.168.59.129/on")
#####



#空調家電による近辺温度の変化を学習するメソッド
def transition_learn():
    pass
#



def deviceControl(way,tActual,tTargetLow):
    #way    0:HIGH  
    #       1:LOW    
    if way == 0 :
        tempHigh_cir()
        tempHigh_relay()
    
    elif way == 1:
        tempLow_cir(tActual,tTargetLow)
        tempLow_relay()

#####################温度の差を確認##########################
def control(tActual, tTarget):
    try: 
        #サーキュレータの操作指示の初期化
        queueOperation.objects(appliance="学校のサーキュレータ").delete()
        way = None
        threshold = 0   #閾値の絶対値
        tTargetHigh = tTarget + threshold
        tTargetLow = tTarget - threshold

        #温度比較
        if tActual > tTargetHigh:
            way = 0
        
        elif tActual < tTargetLow:
            way = 1
        
        deviceControl(way,tActual, tTarget)

    except Exception as e:
        traceback.print_exc()#エラー

