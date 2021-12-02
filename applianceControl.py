from flaskr.databases.collection_models.queueOperation import queueOperation
import traceback
import encodings
import binascii

##################################


def order_save(appliance, protocol, data, size, frequency = None):

    #dataはintで渡されている
    #文字列にして、bytesにしてからDBへ
    data_str = str(data)
    data = binascii.hexlify(data_str.encode('utf-8'))

    if frequency == None:#NEC、家製協
        queueOperation(
        appliance = appliance,
        protocol = protocol,
        data = data,
        size = size
        ).save()

    else:#その他
        queueOperation(
        appliance = appliance,
        protocol = protocol,
        data = data,
        size = size,
        frequency = frequency
        ).save()
    

    print(appliance, protocol, data, size, frequency)

    return "/save"


#家電ごとに変わる(appliance, protocol),
#操作指示ごとに変わる(size, frequency)


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
    
    def getInfo(self, ope):
        return circulator.code[self.name][ope]
    
cir = circulator("学校のサーキュレータ", 3, 64)

#温度が閾値より高くなった時の指示
def tempHigh(tActual,tTargetHigh):
    #電源オフ##########################
    ope = "OFF"

    ##サーキュレータ##
    data = cir.getInfo(ope)
    res = order_save("学校のサーキュレータ", 3, data, 64)
    return res + " <- 電源オフ"

#温度が閾値より低くなった時の指示
def tempLow(tActual,tTargetLow):
    #電源オン##############################
    ope = "ON"
    
    ##サーキュレータ##
    data = cir.getInfo(ope)
    res = order_save("学校のサーキュレータ", 3, data, 64)

    res = res + " <- 電源オン"

    #強中弱#################################
    #指定の温度は適当
    difference = tTargetLow - tActual
    if difference > 3:
        ope = "Low"
    elif difference > 5:
        ope = "Mid"
    else:
        ope = "High"
    
    
    ##サーキュレータ##
    data = cir.getInfo(ope)
    res = res + order_save("学校のサーキュレータ", 3, data, 64)
    
    return res + " <- 強さ設定"


#####################温度の差を確認##########################
def control(tActual, tTarget):
    try: 
        res = None

        threshold = 2   #目標値から閾値までの絶対値

        tTargetHigh = tTarget + threshold
        tTargetLow = tTarget - threshold

        #######温度比較
        if tActual > tTargetHigh:
            res = tempHigh(tActual,tTargetHigh)

            res = res + " <- 温度が高い"
        
        elif tActual < tTargetLow:
            res = tempLow(tActual,tTargetLow)

            res = res + " <- 温度が低い"
        
        else: #範囲内
            res = " <- ちょうどいい"
        
    

    except Exception as e:
        traceback.print_exc()#エラー
        res = "エラー"

    return res

