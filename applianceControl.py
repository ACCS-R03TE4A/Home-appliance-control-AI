from flaskr.databases.collection_models.queueOperation import queueOperation

##################################
#操作キューデータベースに上げと下げ操作を格納する
#設定温度は{目標温度 : tTarget}で操作

#指示をdbに保存
#後でちゃんとdbの構造を見ながら書く
def order_save(order):
    queueOperation("ここに入れる値をいろいろ書く").save()


#温度が閾値より高くなった時の指示
def tempHigh(tTarget):
    return "下げる"

#温度が閾値より低くなった時の指示
def tempLow(tTarget):
    return "上げる"

##################################


#######################温度の差を確認
#sNumberいる？
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

    return res

########################################
