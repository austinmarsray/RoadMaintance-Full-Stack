# -*- coding: utf-8 -*-
import ComVar as com
from Deal import *
import hashlib
import time,datetime
import re
######################################## 辅助函数 ########################################
def encode(pwd):
    h = hashlib.md5()
    h.update(bytes(pwd, encoding='utf-8'))
    pwd_store = h.hexdigest()
    return pwd_store

def generate_tokens(x):
    h = hashlib.md5()
    h.update(bytes(x, encoding='utf-8'))
    token = h.hexdigest()[8:-8]
    com.Tokens.append(token)
    return token

def create_id():
    h = hashlib.md5()
    h.update(bytes(str(time.time()), encoding='utf-8'))
    return h.hexdigest()[8:-8]

def create_id2(key):
    h = hashlib.md5()
    h.update(bytes(key+str(time.time()), encoding='utf-8'))
    return h.hexdigest()

##################################### 处理函数-登陆验证 #####################################
def login_verification(obj):
    cursor = com.conn.cursor()
    cursor.execute('select * from Users where LoginName=? and LoginPwd=? and IsShow=1',(obj['LoginName'],encode(obj['LoginPwd'])))
    row = cursor.fetchone()
    if row == None:
        info = {'result': 0}
    else:
        token = generate_tokens(obj['LoginName'])
        info = {'result': 1, 'UserName': row.UserName, 'UserNo': row.UserNo, 'AuthorityLevel': row.AuthorityLevel, 'Token':token}
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
            rows = cursor.execute('select RoadNo,RoadName,RoadLevel,ConservationLevel,RoadType from RoadBasicSheet where IsShow=1')

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
                             from RoadBasicSheet where RoadNo=? and IsShow=1''',obj['RoadNo'])
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
            cursor.execute('''select RoadNo,RoadType from RoadBasicSheet where RoadName=? and IsShow=1''', obj['RoadName'])
            row = cursor.fetchone()
            info = {'result': 1,"RoadNo": row.RoadNo, "RoadType": com._RoadType_[row.RoadType]}  # 执行成功
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
                            DamageType,IsDamageBad,UserNo,DamageDescripe)
                             values(?,?,?,?,?,?,?,?)
                          ''',(DailyReportNo,obj['RoadNo'],obj['RoadName'],obj['ReportDate'],
                               com._DamageType_[obj['DamageType']],obj['IsDamageBad'],obj['UserNo'],obj['DamageDescription']))
            cursor.commit()
            if obj['IsDamageBad']==True:
                com.Warning_List.append((obj['RoadNo'],obj['RoadName']))

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
                            ReportDate,UserNo,Description,RegularNo)
                            values(?,?,?,?,?,?,?,?)
                          ''',(FlatReportNo,obj['RoadNo'],obj['RoadName'],obj['IRI'],
                               obj['ReportDate'],obj['UserNo'],obj['Description'],obj['RegularNo']))
            cursor.execute("update RegularReport set FlatReportNo=? where RegularNo=?",(FlatReportNo,obj['RegularNo']))
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
                            UserNo,ReportDate,RegularNo)
                            values(?,?,?,?,?,?,?,?,?,?,?,?)
                          ''',(DamageReportNo,obj['RoadNo'],obj['RoadName'],obj['CheckLength'],
                            obj['CheckWidth'],com._DamageType_[obj['DamageType']],obj['DamageLength'],obj['DamageWidth'],
                            obj['DamageDepth'],obj['UserNo'],obj['ReportDate'],obj['RegularNo']))
            cursor.commit()
            info = {'result':1} #执行成功
        except Exception as e:
            print(e)
            info = {'result':0} #执行失败
    else:
        info = {'result':-1}    #没有权限

    return info


################################## 处理函数-获取每日巡查计划 ##################################
def get_dayilyplan(obj):
    plan = []
    if obj['Token'] in com.Tokens:
        Today = datetime.date.today()
        Begin = datetime.date(2020, 6, 24)
        Intervals = (Today - Begin).days

        cursor = com.conn.cursor()
        cursor.execute('''select RoadNo,RoadName,ConservationLevel from RoadBasicSheet where ConservationLevel in (1,?) and IsShow=1''',Intervals)
        rows = cursor.fetchall()

        for row in rows:
            dict_tmp = {'RoadNo':row.RoadNo , 'RoadName':row.RoadName ,
                        'ConservationLevel': com._ConservationLevel_[row.ConservationLevel]}
            plan.append(dict_tmp)

        info = {'result':1 , 'info':plan} #执行成功
    else:
        info = {'result':-1}    #没有权限

    return info


############################## 处理函数-获取道路编号和定期检查编号 ##############################
def get_roadno_and_regularno(obj):
    if obj['Token'] in com.Tokens:
        try:
            cursor = com.conn.cursor()
            cursor.execute('''select RoadNo,RoadType from RoadBasicSheet where RoadName=? and IsShow=1''', obj['RoadName'])
            tmp = cursor.fetchone()
            RoadNo,RoadType = tmp.RoadNo,com._RoadType_[tmp.RoadType]
            cursor.execute("select RegularNo from RegularReport where RoadNo=? and IsFinished=0",RoadNo)
            RegularNo = cursor.fetchone().RegularNo
            info = {'result': 1,"RoadNo": RoadNo,"RegularNo": RegularNo,"RoadType":RoadType}  # 执行成功
        except Exception as e:
            print(e)
            info = {'result': 0}  # 执行失败
    else:
        info = {'result': -1}  # 没有权限

    return info


#################################### 处理函数-录入定期检查 ####################################
def insert_regularreport(obj):
    if obj['Token'] in com.Tokens:
        try:
            RegularReportNo=create_id()
            cursor = com.conn.cursor()
            cursor.execute('''
                            insert into RegularReport(RegularNo,RegularName,RoadNo,StartDate,EndDate)
                            values(?,?,?,?,?)
                          ''',(RegularReportNo,obj['RegularName'],obj['RoadNo'],obj['StartDate'],obj['EndDate']))
            cursor.commit()
            info = {'result':1} #执行成功
        except Exception as e:
            print(e)
            info = {'result':0} #执行失败
    else:
        info = {'result':-1}    #没有权限

    return info


################################## 处理函数-获取定期巡查计划 ##################################
def get_regularplan(obj):
    plan = []
    if obj['Token'] in com.Tokens:
        cursor = com.conn.cursor()
        cursor.execute("select * from RegularReport where IsFinished=0")
        rows = cursor.fetchall()

        for row in rows:
            cursor.execute("select RoadName from RoadBasicSheet where RoadNo=?",row.RoadNo)
            RoadName = cursor.fetchone().RoadName
            dict_tmp = {'RegularNo':row.RegularNo , 'RegularName':row.RegularName ,
                        'RoadNo':row.RoadNo , 'RoadName':RoadName}
            plan.append(dict_tmp)

        info = {'result':1 , 'info':plan} #执行成功
    else:
        info = {'result':-1}    #没有权限

    return info


################################## 处理函数-生成调查表和评价表 #################################
def generate_statisticsdetail(RegularNo):
    for x in com.DamageType_List:
        cursor = com.conn.cursor()
        cursor.execute("select * from DamageReport where RegularNo=? and DamageType=?",(RegularNo,x))
        rows = cursor.fetchall()
        square,density,k=0,0,0
        for row in rows:
            k = k+1
            square += row.DamageSquare
            density += row.DamageSquare/(row.CheckLength*row.CheckWidth)
        if k>0:
            density = density/k
            cursor.execute('''select * from DamageStandard where DamageType=? and 
                              ((DamageDensityCeil>? and DamageDensityFloor<=?) or (DamageDensityCeil=? and DamageDensityFloor=?))
                            ''',(x,density,density,density,density))
            tmp = cursor.fetchone()
            if tmp!=None:
                deduction = tmp.DamageDeduction
                DetailNo = create_id2(x)
                cursor.execute('''insert into StatisticsDetaill(DetailNo,DamageType,RegularNo,DamageSquare,DamageDensity,DamageDeduction)
                                  values(?,?,?,?,?,?)''',(DetailNo,x,RegularNo,square,density,deduction))
                cursor.commit()

def generate_RoadEvaluation(RegularNo,RoadNo):
    EvaluationNo=create_id2('RoadEvaluation')

    cursor = com.conn.cursor()
    cursor.execute("select RoadLevel from RoadBasicSheet where RoadNo=?",RoadNo)
    Level = cursor.fetchone().RoadLevel

    #######IRI RQI
    cursor.execute("select IRI from RegularReport RR join FlatReport FR on RR.RegularNo=FR.RegularNo where RR.RegularNo=?",RegularNo)
    IRI = cursor.fetchone().IRI
    RQI = 4.98 - 0.34*IRI
    RQI_Level = RQI_Rank(RQI,Level)

    #######PCI
    Sum = float()
    list_sum = [[0 for i in range(5)] for j in range(3)]
    Type_Deduction = {}
    cursor.execute("select DamageType,DamageDeduction from StatisticsDetaill where RegularNo=? and DamageDeduction!=0", RegularNo)
    rows = cursor.fetchall()
    for row in rows:
        Type_Deduction[row.DamageType] = row.DamageDeduction

    for p in range(1,3):
        for q in range(1, 5):
            reObj = re.compile('000%d%d[1-5]000' %(p,q))
            for key in Type_Deduction.keys():
                if (reObj.match(key)):
                    list_sum[p][q] += Type_Deduction[key]
    for p in range(1, 3):
        for q in range(1, 5):
            reObj = re.compile('000%d%d[1-5]000' % (p, q))
            for key in Type_Deduction.keys():
                if (reObj.match(key)):
                    u = Type_Deduction[key] / list_sum[p][q]
                    Sum += Type_Deduction[key]*(3*(u**3) - 5.5*(u**2) + 3.5*u)
    PCI = 100 - Sum
    PCI_Level = PCI_Rank(PCI,Level)

    #######PQI
    if Level in (1,2):
        w1, w2 = 0.6, 0.4
    else:
        w1, w2 = 0.4, 0.6
    PQI = 20*w1*RQI + PCI*w2
    PQI_Level = PQI_Rank(PQI,Level)


    cursor.execute('''insert into RoadEvaluation(EvaluationNo,RegularNo,RoadNo,EvaluationDate,RQI,RQILevel,PCI,PCILevel,PQI,PQILevel) 
                      values(?,?,?,?,?,?,?,?,?,?)''',(EvaluationNo,RegularNo,RoadNo,datetime.date.today(),RQI,RQI_Level,PCI,PCI_Level,PQI,PQI_Level))
    cursor.execute('''update RegularReport set EvaluationNo=? where RegularNo=?''',(EvaluationNo,RegularNo))
    cursor.commit()

def generate_tables(obj):
    if obj['Token'] in com.Tokens:
        try:
            cursor = com.conn.cursor()
            cursor.execute("select * from RegularReport where RegularNo=?",obj['RegularNo'])
            row = cursor.fetchone()

            generate_statisticsdetail(obj['RegularNo'])
            generate_RoadEvaluation(obj['RegularNo'],row.RoadNo)

            cursor.execute("update RegularReport set IsFinished=1 where RegularNo=?",obj['RegularNo'])
            cursor.commit()

            info = {'result':1} #执行成功
        except Exception as e:
            print(e)
            info = {'result':0} #执行失败
    else:
        info = {'result':-1}    #没有权限

    return info


#################################### 处理函数-获取统计数据 ###################################
def get_statistic(obj):
    if obj['Token'] in com.Tokens:
        try:
            cursor = com.conn.cursor()
            List = []

            ####道路类型####
            cursor.execute("select RoadType,count(*) as Num  from RoadBasicSheet group by RoadType,IsShow having IsShow=1")
            rows = cursor.fetchall()
            if rows:
                l = []
                for row in rows:
                    dict_tmp = {'RoadType':com._RoadType_[row.RoadType],'Num':row.Num}
                    l.append(dict_tmp)
                List.append(l)
                type_info = {'state':1, 'detail':List[0]}
            else:
                type_info = {'state':0}

            ####道路等级####
            cursor.execute("select RoadLevel,count(*) as Num  from RoadBasicSheet group by RoadLevel,IsShow having IsShow=1")
            rows = cursor.fetchall()
            if rows:
                l = []
                for row in rows:
                    dict_tmp = {'RoadLevel':com._RoadLevel_[row.RoadLevel],'Num':row.Num}
                    l.append(dict_tmp)
                List.append(l)
                level_info = {'state':1, 'detail':List[1]}
            else:
                level_info = {'state':0}

            ####养护等级####
            cursor.execute("select ConservationLevel,count(*) as Num  from RoadBasicSheet group by ConservationLevel,IsShow having IsShow=1")
            rows = cursor.fetchall()
            if rows:
                l = []
                for row in rows:
                    dict_tmp = {'ConservationLevel': com._ConservationLevel_[row.ConservationLevel], 'Num': row.Num}
                    l.append(dict_tmp)
                List.append(l)
                con_level_info = {'state':1, 'detail':List[2]}
            else:
                con_level_info = {'state':0}

            ####RQI####
            cursor.execute('''select tmp.RQILevel,count(*) as Num from 
                                (select RE.* from RoadBasicSheet RBS 
                                join RoadEvaluation RE on RBS.RoadNo=RE.RoadNo 
                                where RBS.IsShow=1 and RE.IsShow=1) as tmp
                                group by tmp.RQILevel,tmp.EvaluationDate
                                having tmp.EvaluationDate=max(tmp.EvaluationDate)''')
            rows = cursor.fetchall()
            t = [row.RQILevel for row in rows]
            d = {}
            for row in rows:
                d[row.RQILevel]=row.Num
            if rows:
                l = []
                for i in range(1,5):
                    if i in t:
                        dict_tmp = {'RQIlevel':com.Rank[i],'Num':d[i]}
                    else:
                        dict_tmp = {'RQIlevel': com.Rank[i], 'Num': 0}
                    l.append(dict_tmp)
                List.append(l)
                RQIlevel_info = {'state':1, 'detail':List[3]}
            else:
                RQIlevel_info = {'state':0}

            ####PCI####
            cursor.execute('''select tmp.PCILevel,count(*) as Num from 
                                (select RE.* from RoadBasicSheet RBS 
                                join RoadEvaluation RE on RBS.RoadNo=RE.RoadNo 
                                where RBS.IsShow=1 and RE.IsShow=1) as tmp
                                group by tmp.PCILevel,tmp.EvaluationDate
                                having tmp.EvaluationDate=max(tmp.EvaluationDate)''')
            rows = cursor.fetchall()
            t = [row.PCILevel for row in rows]
            d = {}
            for row in rows:
                d[row.PCILevel] = row.Num
            if rows:
                l = []
                for i in range(1, 5):
                    if i in t:
                        dict_tmp = {'PCIlevel': com.Rank[i], 'Num': d[i]}
                    else:
                        dict_tmp = {'PCIlevel': com.Rank[i], 'Num': 0}
                    l.append(dict_tmp)
                List.append(l)
                PCIlevel_info = {'state':1,'detail':List[4]}
            else:
                PCIlevel_info = {'state':0}

            ####PQI####
            cursor.execute('''select tmp.PQILevel,count(*) as Num from 
                                (select RE.* from RoadBasicSheet RBS 
                                join RoadEvaluation RE on RBS.RoadNo=RE.RoadNo 
                                where RBS.IsShow=1 and RE.IsShow=1) as tmp
                                group by tmp.PQILevel,tmp.EvaluationDate
                                having tmp.EvaluationDate=max(tmp.EvaluationDate)''')
            rows = cursor.fetchall()
            t = [row.PQILevel for row in rows]
            d = {}
            for row in rows:
                d[row.PQILevel] = row.Num
            if rows:
                l = []
                for i in range(1, 5):
                    if i in t:
                        dict_tmp = {'PQIlevel': com.Rank[i], 'Num': d[i]}
                    else:
                        dict_tmp = {'PQIlevel': com.Rank[i], 'Num': 0}
                    l.append(dict_tmp)
                List.append(l)
                PQIlevel_info = {'state':1,'detail':List[5]}
            else:
                PQIlevel_info = {'state':0}


            info = {'result':1 ,'type_info':type_info, 'level_info':level_info, 'con_level_info':con_level_info,
                    'RQIlevel_info':RQIlevel_info, 'PCIlevel_info':PCIlevel_info, 'PQIlevel_info':PQIlevel_info}
        except Exception as e:
            print(e)
            info = {'result':0} #执行失败
    else:
        info = {'result':-1}    #没有权限

    return info



############################### 处理函数-获取道路列表以及养护等级 ###############################
def get_roadlist_and_conservationlevel(obj):
    if obj['Token'] in com.Tokens:
        try:
            L = []
            cursor = com.conn.cursor()
            cursor.execute('''select RoadNo,RoadName,ConservationLevel,RoadStart from RoadBasicSheet where IsShow=1''')
            rows = cursor.fetchall()
            for row in rows:
                dict_tmp = {"RoadNo": row.RoadNo,"RoadName":row.RoadName,'ConservationLevel': row.ConservationLevel
                    ,"RoadStart":row.RoadStart}
                L.append(dict_tmp)

            info = {'result': 1, 'info':L}  # 执行成功
        except Exception as e:
            print(e)
            info = {'result': 0}  # 执行失败
    else:
        info = {'result': -1}  # 没有权限

    return info


################################## 处理函数-删除道路基本信息 ##################################
def delete_roadbasicinfo(obj):
    if obj['Token'] in com.Tokens:
        try:
            cursor = com.conn.cursor()
            cursor.execute("update RoadBasicSheet set IsShow=0 where RoadNo=?",obj['RoadNo'])
            cursor.commit()
            info = {'result':1} #执行成功
        except Exception as e:
            print(e)
            info = {'result':0} #执行失败
    else:
        info = {'result':-1}    #没有权限

    return info