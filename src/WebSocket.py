# -*- coding: utf-8 -*-
import asyncio
import chardet
import websockets
import json
from Function import *
######################################## 全局变量 ########################################
numbers = {
    1: login_verification,
    2: insert_roadbasic,
    3: get_roadlist,
    4: get_roadinfo,
    5: get_roadNo,
    6: insert_dailyreport,
    7: insert_flatreport,
    8: insert_damagereport,
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
        # print(type(data))
        print(data)

        ################################## 解析前端信息 ##################################
        obj = json.loads(data)
        # print(obj)

        ################################## 处理前端需求 ##################################
        info = Fuction_Map(obj['OT'],obj)
        # print(info)

        ################################## 返回结果信息 ##################################
        msg = json.dumps(info,ensure_ascii=False)
        # print(msg)
        await websocket.send(msg)





#########################################################################################
if __name__ == '__main__':
    # server = websockets.serve(Process, '127.0.0.1', 4200)
    server = websockets.serve(Process, '10.180.130.93', 4200)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

