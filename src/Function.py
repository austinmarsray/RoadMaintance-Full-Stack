# -*- coding: utf-8 -*-
import ComVar as com
import hashlib
import time
######################################## 辅助函数 ########################################
def encode(pwd):
    h = hashlib.md5()
    h.update(bytes(pwd, encoding='utf-8'))
    pwd_store = h.hexdigest()
    return pwd_store

def generate_tokens():
    #######暂时########
    token = "LHX123"
    com.Tokens.append(token)
    return token

def create_id():
    h = hashlib.md5()
    h.update(bytes(str(time.time()), encoding='utf-8'))
    return h.hexdigest()[8:-8]

##################################### 处理函数-登陆验证 #####################################
def login_verification(obj):
    cursor = com.conn.cursor()
    cursor.execute('select * from Users where LoginName=? and LoginPwd=?',(obj['LoginName'],encode(obj['LoginPwd'])))
    row = cursor.fetchone()
    if row == None:
        info = {'result': 0}
    else:
        token = generate_tokens()
        info = {'result': 1, 'name': row.UserName, 'ID': row.UserNo, 'AuthorityLevel': row.AuthorityLevel, 'Token':token}
    return info


################################## 处理函数-录入道路基本信息 ##################################
def insert_roadbasic(obj):
    if obj['Token'] in com.Tokens:
        try:
            cursor = com.conn.cursor()
            cursor.execute('''
                            insert into RoadBasicSheet(RoadNo,RoadName,RoadLevel,ConservationLevel,RoadLength,
                             RoadWidth,RoadSquare,RoadType,RoadStart,RoadEnd,RoadDirection,LaneNum,Speed,SurfaceLevel,
                             AADT,TranLevel,BuildDate,SurfaceThick,InnerType,InnerThick,DesignCom,BuildCom,ManageCom)
                             values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                          ''',(obj['RoadNo'],obj['RoadName'],com.R_RoadLevel_[obj['RoadLevel']],com.R_ConservationLevel_[obj['ConservationLevel']],
                               obj['RoadLength'],obj['RoadWidth'],obj['RoadSquare'],com.R_RoadType_[obj['RoadType']],obj['RoadStart'],
                               obj['RoadEnd'],obj['RoadDirection'],obj['LaneNum'],obj['Speed'],com.R_SurfaceLevel_[obj['SurfaceLevel']],
                               obj['AADT'],com.R_TranLevel_[obj['TranLevel']],obj['BuildDate'],obj['SurfaceThick'],
                               com.R_InnerType_[obj['InnerType']],obj['InnerThick'],obj['DesignCom'],obj['BuildCom'],obj['ManageCom'])
                          )
            cursor.commit()
            info = {'result':1} #执行成功
        except Exception as e:
            print(e)
            info = {'result':0} #执行失败
    else:
        info = {'result':-1}    #没有权限

    return info


#################################### 处理函数-获取道路列表 ####################################
def get_roadlist(obj):
    roadlist = []
    if obj['Token'] in com.Tokens:
        try:
            cursor = com.conn.cursor()
            rows = cursor.execute('select RoadNo,RoadName,RoadLevel,ConservationLevel,RoadType from RoadBasicSheet')

            for x in rows:
                dict_tmp = {"RoadNo":x.RoadNo , "RoadName":x.RoadName , "RoadLevel":com._RoadLevel_[x.RoadLevel] ,
                            "ConservationLevel":com._ConservationLevel_[x.ConservationLevel] , "RoadType":com._RoadType_[x.RoadType]}
                roadlist.append(dict_tmp)
            print(roadlist)
            info = {'result':1 , 'info':roadlist} #执行成功

        except Exception as e:
            print(e)
            info = {'result':0} #执行失败
    else:
        info = {'result':-1}    #没有权限

    return info


################################## 处理函数-获取道路基本信息 ##################################
def get_roadinfo(obj):
    if obj['Token'] in com.Tokens:
        try:
            cursor = com.conn.cursor()
            cursor.execute('''select RoadNo,RoadName,RoadLevel,ConservationLevel,RoadLength,RoadWidth,
                             RoadSquare,RoadType,RoadStart,RoadEnd,RoadDirection,LaneNum,Speed,SurfaceLevel,
                             AADT,TranLevel,BuildDate,SurfaceThick,InnerType,InnerThick,DesignCom,BuildCom,ManageCom 
                             from RoadBasicSheet where RoadNo=?''',obj['RoadNo'])
            rows = cursor.fetchall()
            for row in rows:
                info = {'result':1 ,
                        "RoadNo":row.RoadNo , "RoadName":row.RoadName , "RoadLevel":com._RoadLevel_[row.RoadLevel],
                        "ConservationLevel":com._ConservationLevel_[row.ConservationLevel] , "RoadLength":row.RoadLength,
                        "RoadWidth":row.RoadWidth , "RoadSquare":row.RoadSquare , "RoadType":com._RoadType_[row.RoadType] ,
                         "RoadStart":row.RoadStart , "RoadEnd":row.RoadEnd , "RoadDirection":row.RoadDirection , "LaneNum":row.LaneNum ,
                         "Speed":row.Speed , "SurfaceLevel":com._SurfaceLevel_[row.SurfaceLevel], "AADT":row.AADT ,
                         "TranLevel":com._TranLevel_[row.TranLevel] ,  "BuildDate":row.BuildDate.strftime('%Y-%m-%d') , "SurfaceThick":row.SurfaceThick , "InnerType":com._InnerType_[row.InnerType] ,
                        "InnerThick":row.InnerThick , "DesignCom":row.DesignCom , "BuildCom":row.BuildCom , "ManageCom":row.ManageCom ,
                        } #执行成功
        except Exception as e:
            print(e)
            info = {'result':0} #执行失败
    else:
        info = {'result':-1}    #没有权限

    return info


#################################### 处理函数-获取道路编号 ####################################
def get_roadNo(obj):
    if obj['Token'] in com.Tokens:
        try:
            cursor = com.conn.cursor()
            cursor.execute('''select RoadNo from RoadBasicSheet where RoadName=?''', obj['RoadName'])
            row = cursor.fetchone()
            info = {'result': 1,"RoadNo": row.RoadNo}  # 执行成功
        except Exception as e:
            print(e)
            info = {'result': 0}  # 执行失败
    else:
        info = {'result': -1}  # 没有权限

    return info


################################### 处理函数-录入日常巡查表 ###################################
def insert_dailyreport(obj):
    if obj['Token'] in com.Tokens:
        try:
            DailyReportNo=create_id()
            cursor = com.conn.cursor()
            cursor.execute('''
                            insert into DailyReport(DailyReportNo,RoadNo,RoadName,ReportDate,
                            DamageType,IsDamageBad,UserNo,DamageDescription)
                             values(?,?,?,?,?,?,?,?)
                          ''',(DailyReportNo,obj['RoadNo'],obj['RoadName'],obj['ReportDate'],
                            obj['DamageType'],obj['IsDamageBad'],obj['UserNo'],obj['DamageDescription']))
            cursor.commit()
            info = {'result':1} #执行成功
        except Exception as e:
            print(e)
            info = {'result':0} #执行失败
    else:
        info = {'result':-1}    #没有权限

    return info


############################### 处理函数-录入道路平整度检测记录表 ##############################
def insert_flatreport(obj):
    if obj['Token'] in com.Tokens:
        try:
            FlatReportNo=create_id()
            cursor = com.conn.cursor()
            cursor.execute('''
                            insert into FlatReport(FlatReportNo,RoadNo,RoadName,IRI,
                            ReportDate,UserNo,Description)
                            values(?,?,?,?,?,?,?)
                          ''',(FlatReportNo,obj['RoadNo'],obj['RoadName'],obj['IRI'],
                               obj['ReportDate'],obj['UserNo'],obj['Description']))
            cursor.commit()
            info = {'result':1} #执行成功
        except Exception as e:
            print(e)
            info = {'result':0} #执行失败
    else:
        info = {'result':-1}    #没有权限

    return info


############################### 处理函数-录入道路损坏情况记录表 ###############################
def insert_damagereport(obj):
    if obj['Token'] in com.Tokens:
        try:
            DamageReportNo=create_id()
            cursor = com.conn.cursor()
            cursor.execute('''
                            insert into DamageReport(DamageReportNo,RoadNo,RoadName,CheckLength,
                            CheckWidth,DamageType,DamageLength,DamageWidth, DamageDepth, 
                            DamageSquare,UserNo,ReportDate)
                            values(?,?,?,?,?,?,?,?,?,?,?,?)
                          ''',(DamageReportNo,obj['RoadNo'],obj['RoadName'],obj['CheckLength'],
                            obj['CheckWidth'],obj['DamageType'],obj['DamageLength'],obj['DamageWidth'],
                            obj['DamageDepth'],obj['DamageSquare'],obj['UserNo'],obj['ReportDate']))
            cursor.commit()
            info = {'result':1} #执行成功
        except Exception as e:
            print(e)
            info = {'result':0} #执行失败
    else:
        info = {'result':-1}    #没有权限

    return info


