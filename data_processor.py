import re
from enum import Enum
import pandas as PD
import os

class Adequacy(Enum):
    Natural = 1 #第一ポジション
    Accomplished = 2 #第二ポジション
    Others = 3#それ以外


class position_dataframe:
    positions_dict = {}
    pdf = PD.DataFrame(columns=list(positions_dict))
    
    def __init__(self):
        self.positions_dict = {"GK":[],"DR":[],"DC":[],"DL":[],"WBR":[],"WBL":[],"DM":[],"MR":[],"MC":[],"ML":[],"AMR":[],"AMC":[],"AML":[],"STC":[]}
        self.pdf = PD.DataFrame(columns=list(self.positions_dict))
    
    def update_info(self,line,num):
        datum = re.split(',',line)
        ad_dict = {"GK":Adequacy.Others,"DR":Adequacy.Others,"DC":Adequacy.Others,"DL":Adequacy.Others,
                   "WBR":Adequacy.Others,"WBL":Adequacy.Others,"DM":Adequacy.Others,"MR":Adequacy.Others,
                   "MC":Adequacy.Others,"ML":Adequacy.Others,"AMR":Adequacy.Others,"AMC":Adequacy.Others,
                   "AML":Adequacy.Others,"STC":Adequacy.Others}
        for data in datum:
            if(re.search("GK",data) != None):
                if(num == 1):
                    ad_dict["GK"] = Adequacy.Natural
                elif(num == 2):
                    ad_dict["GK"] = Adequacy.Accomplished
            if(re.search("DM",data) != None):
                if(num == 1):
                    ad_dict["DM"] = Adequacy.Natural
                elif(num == 2):
                    ad_dict["DM"] = Adequacy.Accomplished 
            #左右が同様の異なるポジションの左右がまとめて記述されている場合の対応を含めて
            if(re.search("L",data) != None):
                if(re.search("D",data) != None):
                    if(num == 1):
                        ad_dict["DL"] = Adequacy.Natural
                    elif(num == 2):
                        ad_dict["DL"] = Adequacy.Accomplished
                if(re.search("WB",data) != None):
                    if(num == 1):
                        ad_dict["WBL"] = Adequacy.Natural
                    elif(num == 2):
                        ad_dict["WBL"] = Adequacy.Accomplished
                if(re.search("AM",data) != None):
                    if(num == 1):
                        ad_dict["AML"] = Adequacy.Natural
                    elif(num == 2):
                        ad_dict["AML"] = Adequacy.Accomplished 
                if((re.search("[^A]M",data) != None) or (re.match("M",data) != None)):
                    if(num == 1):
                        ad_dict["ML"] = Adequacy.Natural
                    elif(num == 2):
                        ad_dict["ML"] = Adequacy.Accomplished

            if(re.search("R",data) != None):
                if(re.search("D",data) != None):
                    if(num == 1):
                        ad_dict["DR"] = Adequacy.Natural
                    elif(num == 2):
                        ad_dict["DR"] = Adequacy.Accomplished
                if(re.search("WB",data) != None):
                    if(num == 1):
                        ad_dict["WBR"] = Adequacy.Natural
                    elif(num == 2):
                        ad_dict["WBR"] = Adequacy.Accomplished
                if(re.search("AM",data) != None):
                    if(num == 1):
                        ad_dict["AMR"] = Adequacy.Natural
                    elif(num == 2):
                        ad_dict["AMR"] = Adequacy.Accomplished
                if((re.search("[^A]M",data) != None) or (re.match("M",data) != None)):
                    if(num == 1):
                        ad_dict["MR"] = Adequacy.Natural
                    elif(num == 2):
                        ad_dict["MR"] = Adequacy.Accomplished
            if(re.search("C",data) != None):
                if(re.search("D",data) != None):
                    if(num == 1):
                        ad_dict["DC"] = Adequacy.Natural
                    elif(num == 2):
                        ad_dict["DC"] = Adequacy.Accomplished
                if(re.search("AM",data) != None):
                    if(num == 1):
                        ad_dict["AMC"] = Adequacy.Natural
                    elif(num == 2):
                        ad_dict["AMC"] = Adequacy.Accomplished
                if((re.search("[^A]M",data) != None) or (re.match("M",data) != None)):
                    if(num == 1):
                        ad_dict["MC"] = Adequacy.Natural
                    elif(num == 2):
                        ad_dict["MC"] = Adequacy.Accomplished
                if(re.search("ST",data) != None):
                    if(num == 1):
                        ad_dict["STC"] = Adequacy.Natural
                    elif(num == 2):
                        ad_dict["STC"] = Adequacy.Accomplished
            
        if(num == 1):
            for k,v in ad_dict.items():
                self.positions_dict[k].append(v)
        elif(num == 2):
            for k,v in ad_dict.items():
                if(v == Adequacy.Accomplished):
                    self.positions_dict[k][-1] = Adequacy.Accomplished
                    
import copy
class playerdata(position_dataframe):
    data_dict = {}
    df = PD.DataFrame(columns=list(data_dict.keys()))
    #何人分のデータが入っているか
    num_of_p = 0
    
    def __init__(self):
        super().__init__()
        self.data_dict = {
            "名前":[], #選手名　〇
            "年齢":[], #年齢　〇
           "ポジション":[], #適性が最高のポジション　〇
            "第2ポジション":[], #サブポジション　〇
            "賃金":[], #給料
            "移籍評価額":[], #市場価値　〇
            "国":[], #国　〇
            "ディビジョン" :[], #プレイしているリーグ　〇
            "クラブ" :[], #プレイしているクラブ　〇
           "冷静":[], #冷静さ　〇
            "予測" :[], #予測力　〇
            "勇敢" :[], #度胸　〇
            "敏捷" :[], #敏捷性　〇
            "飛び" :[], #飛び出し(傾向):GK　〇
            "反応" :[], #反応:GK　〇
            "判断" :[], #判断力　〇
            "積極" :[], #積極性　〇
            "意欲" :[], #意志の強さ　〇
            "集中" :[], #集中力　〇
            "視野" :[], #視野　〇
            "支配" :[], #支配力:GK　〇
            "健康" :[], #基礎体力　〇
            "決力" :[], #決定力　〇
            "空中" :[], #空中戦:GK
            "強さ" :[], #強靭さ　〇
            "奇抜" :[], #奇抜さ　〇
            "加速" :[], #加速力　〇
            "運動" :[], #運動量　〇
            "Lｽﾛｰ" :[], #ロングスロー　〇
            "Lｼｭｰ" :[], #ロングシュート　〇
            "ﾘｰﾀﾞ" :[], #リーダーシップ　〇
            "ﾏｰｸ" :[], #マーキング　〇
            "ﾎﾟｼﾞ" :[], #ポジショニング　〇
            "PK" :[],#PK　〇
            "ﾍｯﾄﾞ" :[],#ヘディング　〇
           "FK" :[],#FK　〇
            "ﾀｯﾁ" :[],#ファーストタッチ　〇
            "ひら" :[],#ひらめき　〇
            "ﾊﾝﾄﾞ" :[],#ハンドリング:GK　〇
            "ﾊﾟﾝﾁ" :[],#パンチング(傾向):GK　〇
            "ﾊﾞﾗ" :[],#バランス　〇
            "ﾊﾟｽ" :[],#パス　〇
            "ﾄﾞﾘﾌﾞ" :[],#ドリブル　〇
            "ﾃｸ" :[],#テクニック　〇
            "ﾁｰﾑ" :[],#チームワーク　〇
            "ﾀｯｸﾙ" :[],#タックル　〇
            "ｽﾛｰ" :[],#スロー:GK　〇
            "ｽﾋﾟ" :[],#スピード　〇
            "ｽﾀﾐﾅ" :[],#スタミナ　〇
            "ｼﾞｬﾝ" :[],#ジャンプ到達点　〇
            "CK" :[],#CK　〇
            "ｺｰﾁ" :[],#コミュニケーション能力:GK　〇　
            "ｸﾛｽ":[] ,#クロス　〇
            "ｷｯｸ" :[],#キック:GK　〇
            "ｵﾌ" :[],#オフザボール　〇
            "1対1":[] ,#1対1:GK　〇　
            "時間" :[], #出場時間　〇
            "勝利" :[], #勝ち数　〇
            "D" :[],#引き分け数　〇
            "敗" :[], #負け数　〇
            "平均" :[],#平均評価　〇
            "情報" :[],
            "推薦" :[]
        }
        self.df = PD.DataFrame(columns=list(self.data_dict.keys()))
        self.num_of_p = 0
        
        self.aliases = {
            "サブポジション":"第2ポジション", 
            "給与":"賃金",
            "市場価値":"移籍評価額", 
            "度胸" :"勇敢",
            "俊敏" :"敏捷", 
            "飛出" :"飛び", 
            "反射" : "反応",
            "意志" :"意欲", 
            "体力" :"健康",
            "決定" :"決力", 
            "空中高" :"空中", 
            "強靭" :"強さ", 
            "Lス" :"Lｽﾛｰ",
            "Lシュート" :"Lｼｭｰ",
            "リーダー" :"ﾘｰﾀﾞ", 
            "マーク" :"ﾏｰｸ", 
            "ポジ" :"ﾎﾟｼﾞ",
            "ヘッド" :"ﾍｯﾄﾞ",
            "1st" :"ﾀｯﾁ",
            "直観" :"ひら",
            "ハンド" :"ﾊﾝﾄﾞ",
            "パンチ" :"ﾊﾟﾝﾁ",
            "バラ" :"ﾊﾞﾗ",
            "パス" :"ﾊﾟｽ",
            "ドリ" :"ﾄﾞﾘﾌﾞ",
            "テク" :"ﾃｸ",
            "チーム" :"ﾁｰﾑ",
            "タク" :"ﾀｯｸﾙ",
            "スロー" :"ｽﾛｰ",
            "スピ" :"ｽﾋﾟ",
            "スタ" :"ｽﾀﾐﾅ",
            "ジャン" :"ｼﾞｬﾝ",
            "コミュ" :"ｺｰﾁ",
            "クロ":"ｸﾛｽ" ,
            "キック" :"ｷｯｸ",
            "オフボ" :"ｵﾌ",
            "分" : "時間", 
            "無" :"D",
        }
        
        self.para_set = set()

        
    
    def order_add(self,data,parameter_order):
        flag = False
        item = ""
        for l in data:
            if(flag == True and l == "<"):
                break
            if(flag == True):
                item += l
            if(l == ">"):
                flag = True
        item = re.sub(r'[\u200b\u200c\u200d\uFEFF]','', item)
        
        if(item in self.para_set):
            parameter_order.append((item,False))
            return
        
        self.para_set.add(item)
        
        if(item in self.data_dict):
            parameter_order.append((item,True))
        elif(item in self.aliases):
            parameter_order.append((self.aliases[item],True))
        else:
            parameter_order.append((item,False))
            
        

    def copy(self):
        # ここで必要なフィールドをコピーして新しいオブジェクトを作成
        new_obj = playerdata()
        new_obj.data_dict = copy.copy(self.data_dict)  # あるいは、self.data_dictを適切にコピーする方法を使用
        return new_obj

    def deepcopy(self):
        # ここで必要なフィールドを深いコピーして新しいオブジェクトを作成
        new_obj = playerdata()
        new_obj.data_dict = copy.deepcopy(self.data_dict)

        return new_obj
    
    def update_info(self,data,num):
        super().update_info(data,num)
        
    #複数の選手データを足して扱う時のための関数
    def sum_ability(self,other):
        for k,v in self.data_dict.items():
            #データが文字列なら処理しない→数値は処理する
            if(not v):
                self.data_dict[k].append(other.data_dict[k][-1])
                continue
            if((type(v[0]) is str) and (type(other.data_dict[k][-1]) is not str)):
                self.data_dict[k][0] = other.data_dict[k][-1]
                continue
            if(type(v[0]) is str):
                continue
            if(type(other.data_dict[k][-1]) is str):
                continue
            self.data_dict[k][0] = self.data_dict[k][0] + other.data_dict[k][-1]
        self.num_of_p += 1
        
    def myteam_init(self):
        self.data_dict = {
            "名前":[], #選手名
           "ポジション":[], #適性が最高のポジション
            "第2ポジション":[], #サブポジション
            "平均" :[],
            "冷静":[], #冷静さ　〇
            "予測" :[], #予測力　〇
            "勇敢" :[], #度胸　〇
            "敏捷" :[], #敏捷性　〇
            "飛び" :[], #飛び出し(傾向):GK　〇
            "反応" :[], #反応:GK　〇
            "判断" :[], #判断力　〇
            "積極" :[], #積極性　〇
            "意欲" :[], #意志の強さ　〇
            "集中" :[], #集中力　〇
            "視野" :[], #視野　〇
            "支配" :[], #支配力:GK　〇
            "健康" :[], #基礎体力　〇
            "決力" :[], #決定力　〇
            "空中" :[], #空中戦:GK
            "強さ" :[], #強靭さ　〇
            "奇抜" :[], #奇抜さ　〇
            "加速" :[], #加速力　〇
            "運動" :[], #運動量　〇
            "Lｽﾛｰ" :[], #ロングスロー　〇
            "Lｼｭｰ" :[], #ロングシュート　〇
            "ﾘｰﾀﾞ" :[], #リーダーシップ　〇
            "ﾏｰｸ" :[], #マーキング　〇
            "ﾎﾟｼﾞ" :[], #ポジショニング　〇
            "PK" :[],#PK　〇
            "ﾍｯﾄﾞ" :[],#ヘディング　〇
           "FK" :[],#FK　〇
            "ﾀｯﾁ" :[],#ファーストタッチ　〇
            "ひら" :[],#ひらめき　〇
            "ﾊﾝﾄﾞ" :[],#ハンドリング:GK　〇
            "ﾊﾟﾝﾁ" :[],#パンチング(傾向):GK　〇
            "ﾊﾞﾗ" :[],#バランス　〇
            "ﾊﾟｽ" :[],#パス　〇
            "ﾄﾞﾘﾌﾞ" :[],#ドリブル　〇
            "ﾃｸ" :[],#テクニック　〇
            "ﾁｰﾑ" :[],#チームワーク　〇
            "ﾀｯｸﾙ" :[],#タックル　〇
            "ｽﾛｰ" :[],#スロー:GK　〇
            "ｽﾋﾟ" :[],#スピード　〇
            "ｽﾀﾐﾅ" :[],#スタミナ　〇
            "ｼﾞｬﾝ" :[],#ジャンプ到達点　〇
            "CK" :[],#CK　〇
            "ｺｰﾁ" :[],#コミュニケーション能力:GK　〇　
            "ｸﾛｽ":[] ,#クロス　〇
            "ｷｯｸ" :[],#キック:GK　〇
            "ｵﾌ" :[],#オフザボール　〇
            "1対1":[] ,#1対1:GK　〇　
        }
        self.df = PD.DataFrame(columns=list(self.data_dict.keys()))
        self.num_of_p = 0
        
    def candidates_init(self):
        self.data_dict = {
            "情報" :[],
            "推薦" :[],
            "名前":[], #選手名
           "ポジション":[], #適性が最高のポジション
            "第2ポジション":[], #サブポジション
            "平均" :[],
            "冷静":[], #冷静さ　〇
            "予測" :[], #予測力　〇
            "勇敢" :[], #度胸　〇
            "敏捷" :[], #敏捷性　〇
            "飛び" :[], #飛び出し(傾向):GK　〇
            "反応" :[], #反応:GK　〇
            "判断" :[], #判断力　〇
            "積極" :[], #積極性　〇
            "意欲" :[], #意志の強さ　〇
            "集中" :[], #集中力　〇
            "視野" :[], #視野　〇
            "支配" :[], #支配力:GK　〇
            "健康" :[], #基礎体力　〇
            "決力" :[], #決定力　〇
            "空中" :[], #空中戦:GK
            "強さ" :[], #強靭さ　〇
            "奇抜" :[], #奇抜さ　〇
            "加速" :[], #加速力　〇
            "運動" :[], #運動量　〇
            "Lｽﾛｰ" :[], #ロングスロー　〇
            "Lｼｭｰ" :[], #ロングシュート　〇
            "ﾘｰﾀﾞ" :[], #リーダーシップ　〇
            "ﾏｰｸ" :[], #マーキング　〇
            "ﾎﾟｼﾞ" :[], #ポジショニング　〇
            "PK" :[],#PK　〇
            "ﾍｯﾄﾞ" :[],#ヘディング　〇
           "FK" :[],#FK　〇
            "ﾀｯﾁ" :[],#ファーストタッチ　〇
            "ひら" :[],#ひらめき　〇
            "ﾊﾝﾄﾞ" :[],#ハンドリング:GK　〇
            "ﾊﾟﾝﾁ" :[],#パンチング(傾向):GK　〇
            "ﾊﾞﾗ" :[],#バランス　〇
            "ﾊﾟｽ" :[],#パス　〇
            "ﾄﾞﾘﾌﾞ" :[],#ドリブル　〇
            "ﾃｸ" :[],#テクニック　〇
            "ﾁｰﾑ" :[],#チームワーク　〇
            "ﾀｯｸﾙ" :[],#タックル　〇
            "ｽﾛｰ" :[],#スロー:GK　〇
            "ｽﾋﾟ" :[],#スピード　〇
            "ｽﾀﾐﾅ" :[],#スタミナ　〇
            "ｼﾞｬﾝ" :[],#ジャンプ到達点　〇
            "CK" :[],#CK　〇
            "ｺｰﾁ" :[],#コミュニケーション能力:GK　〇　
            "ｸﾛｽ":[] ,#クロス　〇
            "ｷｯｸ" :[],#キック:GK　〇
            "ｵﾌ" :[],#オフザボール　〇
            "1対1":[] ,#1対1:GK　〇　
        }
        self.df = PD.DataFrame(columns=list(self.data_dict.keys()))
        self.num_of_p = 0
        
    
    ab_ls = [  
            "冷静", #冷静さ　〇
            "予測" , #予測力　〇
            "勇敢" , #度胸　〇
            "敏捷" , #敏捷性　〇
            "飛び" , #飛び出し(傾向):GK　〇
            "反応" , #反応:GK　〇
            "判断" , #判断力　〇
            "積極" , #積極性　〇
            "意欲" , #意志の強さ　〇
            "集中" , #集中力　〇
            "視野" , #視野　〇
            "支配" , #支配力:GK　〇
            "健康" , #基礎体力　〇
            "決力" , #決定力　〇
            "空中" , #空中戦:GK
            "強さ" , #強靭さ　〇
            "奇抜" , #奇抜さ　〇
            "加速" , #加速力　〇
            "運動" , #運動量　〇
            "Lｽﾛｰ" , #ロングスロー　〇
            "Lｼｭｰ" , #ロングシュート　〇
            "ﾘｰﾀﾞ" , #リーダーシップ　〇
            "ﾏｰｸ" , #マーキング　〇
            "ﾎﾟｼﾞ" , #ポジショニング　〇
            "PK" ,#PK　〇
            "ﾍｯﾄﾞ" ,#ヘディング　〇
           "FK" ,#FK　〇
            "ﾀｯﾁ" ,#ファーストタッチ　〇
            "ひら" ,#ひらめき　〇
            "ﾊﾝﾄﾞ" ,#ハンドリング:GK　〇
            "ﾊﾟﾝﾁ" ,#パンチング(傾向):GK　〇
            "ﾊﾞﾗ" ,#バランス　〇
            "ﾊﾟｽ" ,#パス　〇
            "ﾄﾞﾘﾌﾞ" ,#ドリブル　〇
            "ﾃｸ" ,#テクニック　〇
            "ﾁｰﾑ" ,#チームワーク　〇
            "ﾀｯｸﾙ" ,#タックル　〇
            "ｽﾛｰ" ,#スロー:GK　〇
            "ｽﾋﾟ" ,#スピード　〇
            "ｽﾀﾐﾅ" ,#スタミナ　〇
            "ｼﾞｬﾝ" ,#ジャンプ到達点　〇
            "CK" ,#CK　〇
            "ｺｰﾁ",#コミュニケーション能力:GK　〇　
            "ｸﾛｽ" ,#クロス　〇
            "ｷｯｸ" ,#キック:GK　〇
            "ｵﾌ" ,#オフザボール　〇
            "1対1" ,#1対1:GK　〇　
    ]
    #データが能力値であるかどうかを調べる
    def _isability(self,data):
        return data in self.ab_ls
    
import re
#リーグの種類を全て格納する配列

#単位を数値に変換する関数
def unit_conversion(unit,num):
    if(unit == "日"):
        return 1
    elif(unit == "週"):
        return num
    elif(unit == "ヶ月"):
        return num * 4
    if(unit == "K"):
        return num * 1000
    elif(unit == "M"):
        return num * 1000000
    elif(unit == "B"):
        return num * 1000000000
    elif(unit == "億" or unit == "HM"):
        return num * 100000000
    elif(unit == "万" or unit == "TT"):
        return num * 10000

#選手のデータを、適切な形に書き直して格納
def make_data(pdlist,line,abnum,parameter_order):
    #ディビジョンの検出
    
    if(not parameter_order[abnum][1]):
        return
    
    para_name = parameter_order[abnum][0]

    if(para_name == "ディビジョン"):
        ele = re.sub(r'(</?td>)|\s','',line)
        pdlist.data_dict[para_name].append(ele)
        return
    if(para_name == "ポジション"):
        ele = re.sub(r'(</?td>)|\s','',line)
        pdlist.update_info(ele,1)
    if(para_name == "サブポジション"):
        ele = re.sub(r'(</?td>)|\s','',line)
        pdlist.update_info(ele,2)
        
    res0 = re.search(r'\d?\d',line) #完全判明能力値
    res1 = re.search(r'(\d)*\d\.\d(\d)*',line) #小数値
    res2 = re.search(r'1?\d-1?\d',line) #未判明能力値
    res3 = re.search(r'<td>-</td>',line) #完全未判明能力値
    res4 = re.search(r'(\d?\d?\d?,?)*\d?\d?\d,\d\d\d',line) #4桁以上の給与の検出
    res5 = re.search(r'(¥|£|€)\d?(\.)?\d?(\.)?\d(K|M|B|万|億|(HM)|(TT))?',line) #市場価値の検出2
    res6 = re.search(r'(¥|£|€)\d{1,3}(,\d{3})*(\.\d+)?(万|億|K|M|B|(HM)|(TT))?\s*-\s*(¥|£|€)?\d{1,3}(,\d{3})*(\.\d+)?(万|億|K|M|B|(HM)|(TT))?',line) #市場価値の検出
    res7 = re.search(r'\d?\d( 日| 週| ヶ月)? - \d?\d (日|週|ヶ月)',line) #負傷状況の検出
    if(res7 != None):
        ele = res7.group(0)
        infos = re.split(" - ",ele)
        if(re.search(r"日|週|ヶ月",infos[0]) == None):
            info1 = int(re.search(r"\d?\d",infos[0]).group(0))
            info2 = int(re.search(r"\d?\d",infos[1]).group(0))
            info3 = re.search(r"日|週|ヶ月",infos[1]).group(0)
            pdlist.data_dict[para_name].append(unit_conversion(info3,(info1+info2)/2))
            return
        if(re.search(r"日|週|ヶ月",infos[0]) != None):
            info1 = int(re.search(r"\d?\d",infos[0]).group(0))
            info2 = int(re.search(r"\d?\d",infos[1]).group(0))
            info3 = re.search(r"日|週|ヶ月",infos[0]).group(0)
            info4 = re.search(r"日|週|ヶ月",infos[1]).group(0)
            min_w = unit_conversion(info3,info1)
            max_w = unit_conversion(info4,info2)
            pdlist.data_dict[para_name].append((min_w + max_w)/2)
            return
    if(res6 != None):
        ele = res6.group(0).replace(',', '')
        infos = re.split(" - ",ele)
        if(re.search(r"(TT)|(HM)|K|M|B|万|億",infos[0]) == None):
            info1 = float(re.search(r"\d?(\.)?\d?(\.)?\d",infos[0]).group(0))
            info2 = float(re.search(r"\d?(\.)?\d?(\.)?\d",infos[1]).group(0))
            if(re.search(r"(TT)|(HM)|K|M|B|万|億",infos[1])):
                info3 = re.search(r"(TT)|(HM)|K|M|B|万|億",infos[1]).group(0)
                pdlist.data_dict[para_name].append(unit_conversion(info3,(info1+info2)/2))
            else:
                pdlist.data_dict[para_name].append((info1+info2)/2)
            return
        if(re.search(r"(TT)|(HM)|K|M|B|万|億",infos[0]) != None):
            info1 = float(re.search(r"\d?(\.)?\d?(\.)?\d",infos[0]).group(0))
            info2 = float(re.search(r"\d?(\.)?\d?(\.)?\d",infos[1]).group(0))
            info3 = re.search(r"(TT)|(HM)|K|M|B|万|億",infos[0]).group(0)
            info4 = re.search(r"(TT)|(HM)|K|M|B|万|億",infos[1]).group(0)
            min_w = unit_conversion(info3,info1)
            max_w = unit_conversion(info4,info2)
            pdlist.data_dict[para_name].append((min_w + max_w)/2)
            return
    if(res5 != None):
        ele = res5.group(0)
        #print(ele)
        if(re.search(r"(TT)|(HM)|K|M|B|万|億",ele) == None):
            info = float(re.search(r"\d?(\.)?\d?(\.)?\d",ele).group(0))
            pdlist.data_dict[para_name].append(info)
            return
        else:
            info1 = float(re.search(r"\d?(\.)?\d?(\.)?\d",ele).group(0))
            info2 = re.search(r"(TT)|(HM)|K|M|B|万|億",ele).group(0)
            value = unit_conversion(info2,info1)
            pdlist.data_dict[para_name].append((value))
            return
    if(res4 != None):
        ele = res4.group(0)
        #print(ele)
        pdlist.data_dict[para_name].append(int(ele.replace(',' , '')))
        return
    if(res3 != None):
        pdlist.data_dict[para_name].append(0)
        return
    if(res2 != None):
        ele = res2.group(0)
        #print(ele)
        numls = re.findall(r'1?\d',ele)
        median = (int(numls[0]) + int(numls[1])) / 2
        pdlist.data_dict[para_name].append(median)
        return
    if(res1 != None):
        ele = res1.group(0)
        #print(ele)
        pdlist.data_dict[para_name].append(float(ele))
        return
    if(res0 != None):
        ele = res0.group(0)
        #print(ele)
        pdlist.data_dict[para_name].append(int(ele))
        return
    ele = re.sub(r'(</?td>)|\s','',line)
    pdlist.data_dict[para_name].append(ele)

#ファイルから選手データを読み込む関数
def make_pdlist(filename,pdlist,leagues):
    f = open(filename, 'r', encoding='UTF-8')
    line = f.readline()
    flag1 = False
    pd = playerdata()
    parameter_order = []
    
    #能力値の順番を調べる
    while line:
        if(len(line) < 5):
            line = f.readline()
            continue
        if(flag1):
            pd.order_add(line,parameter_order)
        if(line[0]+line[1]+line[2] == "<tr"):
            flag1 = True
        if(line[0]+line[1]+line[2]+line[3]+line[4] == "</tr>"):
            line = f.readline()
            break
        line = f.readline()
        
    pnum = 0
    while line:
        
        if(line[0]+line[1]+line[2] == "<tr"):
            abnum = 0
            line = f.readline() 
        elif(line[0]+line[1]+line[2]+line[3]+line[4] == "</tr>"):
            line = f.readline()
            #リーグデータの処理
            if("ディビジョン" in pdlist.data_dict and pdlist.data_dict["ディビジョン"][-1] not in leagues):
                leagues.append(pdlist.data_dict["ディビジョン"][-1])
            continue
        if(re.match(r"</table>",line) != None):
            break
        make_data(pdlist,line,abnum,parameter_order)
        abnum += 1
        line = f.readline()
        line = f.readline()
    f.close()

def make_Mypdlist(filename,pdlist):
    f = open(filename, 'r', encoding='UTF-8')
    line = f.readline()
    flag1 = False
    pd = playerdata()
    parameter_order = []
    
    #能力値の順番を調べる
    while line:
        if(len(line) < 5):
            line = f.readline()
            continue
        if(flag1 == True):
            pd.order_add(line,parameter_order)
        if(line[0]+line[1]+line[2] == "<tr"):
            flag1 = True
        if(line[0]+line[1]+line[2]+line[3]+line[4] == "</tr>"):
            line = f.readline()
            break
        line = f.readline()  
        
    pnum = 0
    while line:
        if(line[0]+line[1]+line[2] == "<tr"):
            abnum = 0
            line = f.readline() 
        elif(line[0]+line[1]+line[2]+line[3]+line[4] == "</tr>"):
            line = f.readline()
            continue
        if(re.match(r"</table>",line) != None):
            break
        make_data(pdlist,line,abnum,parameter_order)
        abnum += 1
        line = f.readline()
        line = f.readline()
    f.close()
    
def make_newdf(pdlist):
    #選手データをDataFrame=pdの形にする
    for k,v in pdlist.data_dict.items():
        pdlist.df[k] = v
    #ポジションデータをDataFrame=pdfの形にする
    for k,v in pdlist.positions_dict.items():
        pdlist.pdf[k] = v
    #pdとpdfを連結
    return PD.concat([pdlist.df, pdlist.pdf], axis=1)

#ヒープソートを行う関数
def heap_sort(lst):
    n = len(lst)
    for i in range(n//2-1, -1, -1):
        heapify(lst, i, n)

    for i in range(n-1, 0, -1):
        lst[0], lst[i] = lst[i], lst[0]
        heapify(lst, 0, i)
        
    return lst

def heapify(lst, i, heap_size):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < heap_size and lst[left][1] > lst[largest][1]:
        largest = left

    if right < heap_size and lst[right][1] > lst[largest][1]:
        largest = right

    if largest != i:
        lst[largest], lst[i] = lst[i], lst[largest]
        heapify(lst, largest, heap_size)
        
#そのリーグが含まれるかどうか 含まれるならインデックスを返す
def contain_league(name,ls):
    for i in range(len(ls)):
        if(ls[i][0] == name):
            return i
    return -1
    


#ポジションごとに選手データを振り分け、ポジション名の文字データと対応させた辞書を返す関数
def split_by_position(df,adequacy):
    ab_ls = playerdata().ab_ls
    if(adequacy == Adequacy.Natural):
        GK_df = df.loc[(df['GK'] == Adequacy.Natural),ab_ls+["平均"]]
        DR_df = df.loc[(df['DR'] == Adequacy.Natural),ab_ls+["平均"]]
        DC_df = df.loc[(df['DC'] == Adequacy.Natural),ab_ls+["平均"]]
        DL_df = df.loc[(df['DL'] == Adequacy.Natural),ab_ls+["平均"]]
        WBR_df = df.loc[(df['WBR'] == Adequacy.Natural),ab_ls+["平均"]]
        WBL_df = df.loc[(df['WBL'] == Adequacy.Natural),ab_ls+["平均"]]
        DM_df = df.loc[(df['DM'] == Adequacy.Natural),ab_ls+["平均"]]
        MR_df = df.loc[(df['MR'] == Adequacy.Natural),ab_ls+["平均"]]
        MC_df = df.loc[(df['MC'] == Adequacy.Natural),ab_ls+["平均"]]
        ML_df = df.loc[(df['ML'] == Adequacy.Natural),ab_ls+["平均"]]
        AMR_df = df.loc[(df['AMR'] == Adequacy.Natural),ab_ls+["平均"]]
        AMC_df = df.loc[(df['AMC'] == Adequacy.Natural),ab_ls+["平均"]]
        AML_df = df.loc[(df['AML'] == Adequacy.Natural),ab_ls+["平均"]]
        STC_df = df.loc[(df['STC'] == Adequacy.Natural),ab_ls+["平均"]]
    elif(adequacy == Adequacy.Accomplished):
        GK_df = df.loc[((df['GK'] == Adequacy.Natural) | (df['GK'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        DR_df = df.loc[((df['DR'] == Adequacy.Natural) | (df['DR'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        DC_df = df.loc[((df['DC'] == Adequacy.Natural) | (df['DC'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        DL_df = df.loc[((df['DL'] == Adequacy.Natural) | (df['DL'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        WBR_df = df.loc[((df['WBR'] == Adequacy.Natural) | (df['WBR'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        WBL_df = df.loc[((df['WBL'] == Adequacy.Natural) | (df['WBL'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        DM_df = df.loc[((df['DM'] == Adequacy.Natural) | (df['DM'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        MR_df = df.loc[((df['MR'] == Adequacy.Natural) | (df['MR'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        MC_df = df.loc[((df['MC'] == Adequacy.Natural) | (df['MC'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        ML_df = df.loc[((df['ML'] == Adequacy.Natural) | (df['ML'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        AMR_df = df.loc[((df['AMR'] == Adequacy.Natural) | (df['AMR'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        AMC_df = df.loc[((df['AMC'] == Adequacy.Natural) | (df['AMC'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        AML_df = df.loc[((df['AML'] == Adequacy.Natural) | (df['AML'] == Adequacy.Accomplished)),ab_ls+["平均"]]
        STC_df = df.loc[((df['STC'] == Adequacy.Natural) | (df['STC'] == Adequacy.Accomplished)),ab_ls+["平均"]]
    else:
        GK_df=DR_df=DC_df=DL_df=WBR_df=WBL_df=DM_df=MR_df=MC_df=ML_df=AMR_df=AMC_df=AML_df=STC_df=df
    result = {"GK":GK_df,"DR":DR_df,"DC":DC_df,"DL":DL_df,"WBR":WBR_df,"WBL":WBL_df,"DM":DM_df,"MR":MR_df,"MC":MC_df,"ML":ML_df,"AMR":AMR_df,"AMC":AMC_df,"AML":AML_df,"STC":STC_df}
    return result

def listing_players(dataframe,position,num,budget,age,adequacy,models,posi_dict):
    pre_posi_dict = split_by_position(dataframe,adequacy)#能力値とポジションごとに分ける.
    predf = pre_posi_dict[position]
    predf = predf.loc[:,posi_dict[position].columns]
    #欠損値の補完
    predf = predf.fillna(predf.mean())
    x = predf.drop("平均",axis = 1)
    model = models[position]
    pred = model.predict(x)
    index_of_predf = predf.index
    res_df = dataframe.loc[index_of_predf]
    res_df['予測評価'] = pred
    res_df = res_df.sort_values(by='予測評価',ascending=False)
    res_df = res_df[res_df['移籍評価額'].apply(lambda x: type(x) is not str) & res_df['年齢'].apply(lambda x: type(x) is not str)]
    res_df = res_df[(res_df['移籍評価額'] <= budget) & (res_df['年齢'] <= age)]