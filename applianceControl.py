
##################################
#操作キューデータベースにageとsage操作を格納する
#設定温度は{目標温度 : tTarget}で操作

def tempHigh(tTarget):
    return "下げる"


def tempLow(tTarget):
    return "上げる"

##################################


#######################温度の差を確認
def control(sNumber, tActual, tTarget):
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
