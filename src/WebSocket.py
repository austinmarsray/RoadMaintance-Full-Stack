# -*- coding: utf-8 -*-
import asyncio
import websockets
import json
from Function import *
from Deal import *

######################################## 全局变量 ########################################
numbers = {
    1:  login_verification,
    2:  insert_roadbasic,
    3:  get_roadlist,
    4:  get_roadinfo,
    5:  get_roadNo,
    6:  insert_dailyreport,
    7:  insert_flatreport,
    8:  insert_damagereport,
    9:  get_dayilyplan,
    10: get_roadno_and_regularno,
    11: insert_regularreport,
    12: get_regularplan,
    13: generate_tables,
    14: get_statistic,
    15: get_roadlist_and_conservationlevel,
    16: delete_roadbasicinfo,
}
######################################## 辅助函数 ########################################
def Fuction_Map(x,obj):
    method = numbers.get(x)
    if method:
        return method(obj)

######################################## 进程函数 ########################################
async def Process(websocket,path):
    while True:
        ################################## 接受前端信息 ##################################
        data = await websocket.recv()
        signalprint()
        print('recv: '+data)

        ################################## 解析前端信息 ##################################
        obj = json.loads(data)
        # print(obj)

        ################################## 处理前端需求 ##################################
        info = Fuction_Map(obj['OT'],obj)
        # print(info)

        ################################## 返回结果信息 ##################################
        msg = json.dumps(info,ensure_ascii=False)
        await websocket.send(msg)
        signalprint()
        print('send: ' + msg)


#########################################################################################
if __name__ == '__main__':
    try:
        signalprint()
        print("服务器已启动。")
        file = open('warning.txt', 'r')
        com.Warning_List = eval(file.read())
        file.close()

        server = websockets.serve(Process, '127.0.0.1', 4200)
        # server = websockets.serve(Process, '10.180.180.191', 4200)
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        file = open('warning.txt', 'w')
        file.write(str(com.Warning_List))
        file.close()
        print("服务器已暂停。")