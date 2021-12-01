from flaskr.databases.collection_models.queueOperation import queueOperation

##################################
#操作キューデータベースに上げと下げ操作を格納する
#設定温度は{目標温度 : tTarget}で操作

def order_save(order):
    queueOperation(
        operation=order
        ).save()

    return order


#温度が閾値より高くなった時の指示
def tempHigh(tTarget):
    order = "下げる",tTarget

    res = order_save(str(order))
    return res
    #return order

#温度が閾値より低くなった時の指示
def tempLow(tTarget):
    order = "上げる",tTarget

    res = order_save(str(order))
    return res
    #return order

##################################


#######################温度の差を確認
def control(tActual, tTarget):
    try: 

        threshold = 3   #目標値から閾値までの絶対値

        tTagetHigh = tTarget + threshold
        tTagetLow = tTarget - threshold

        #######温度比較
        if tActual > tTagetHigh:
            res = tempHigh(tTarget)
        
        elif tActual < tTagetLow:
            res = tempLow(tTarget)
        
        else: #範囲内
            res = "tolerance"
        
    

    except Exception as e:
        print(e)#エラー
        res = "エラー"

    return res

