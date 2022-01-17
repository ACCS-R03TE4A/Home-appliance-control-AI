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

#温度が閾値より高くなった時の指示
def tempHigh(tActual,tTargetHigh):

    #電源オフ
    queueOperation.objects(appliance="学校のサーキュレータ").delete()

    if cir.status == 1:
        ope = "OFF"

        cir.status = 0
        ##サーキュレータ##
        data = cir.getInfo(ope)
        order_save("学校のサーキュレータ", 3, data, 64)


        ##リレーモジュール##
        res = requests.get("http://192.168.59.129/off")
    

#温度が閾値より低くなった時の指示
def tempLow(tActual,tTargetLow):
    #電源オン
    queueOperation.objects(appliance="学校のサーキュレータ").delete()

    if cir.status == 0:
        ope = "ON"

        
        cir.status = 1
        
        ##サーキュレータ##
        data = cir.getInfo(ope)
        order_save("学校のサーキュレータ", 3, data, 64)
 

        ##リレーモジュール##
        res = requests.get("http://192.168.59.129/on")

    #強中弱
    difference = tTargetLow - tActual
    if difference > 3:
        ope = "Low"
    elif difference > 5:
        ope = "Mid"
    else:
        ope = "High"
    
    ##サーキュレータ##
    data = cir.getInfo(ope)
    order_save("学校のサーキュレータ", 3, data, 64)

#####################温度の差を確認##########################
def control(tActual, tTarget):
    try: 
        res = None

        threshold = 0   #目標値から閾値までの絶対値

        tTargetHigh = tTarget + threshold
        tTargetLow = tTarget - threshold

        #温度比較
        if tActual > tTargetHigh:
            tempHigh(tActual,tTargetHigh)


        
        elif tActual < tTargetLow:
            tempLow(tActual,tTargetLow)
        

        print("response",res)


        

        
    
    except Exception as e:
        traceback.print_exc()#エラー

