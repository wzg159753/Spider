import json

import math
import websocket
import threading
import time
import requests
from lxml import etree
import logging


logger = logging.getLogger('my_websocket')



def download(url):
    return requests.get(url)

def get_outcome():
    url = 'https://www.betvictor56.com/bv_api/price_it_up_home_component?max_outcomes_per_event=3&max_events_per_sport=10&event_ids_to_exclude=1015843100&exclude_rank_events=true&exclude_game_events=false&sport_ids%5B%5D=100'
    response = download(url).json()['priceItUps'] # [0]['outcomeIds']
    data = []
    lis = [data.extend(i['outcomeIds']) for i in response]
    return data

def get_market():
    uri = 'https://www.betvictor56.com/zh-cn/sport/football'
    resp = download(uri)
    html = etree.HTML(resp.text)
    info = html.xpath('//span[@data-ew_d="1"]/@data-bet')
    lis = list(map(int, info))
    print(len(lis))
    li = '-'.join(html.xpath('//h4[@class="sortable_coupon sports-coupon__title"]/@data-market-id')).split('-')
    return li, lis

def get_five_ids():
    url = 'https://www.betvictor56.com/zh-cn/sport/top_bets/100?event_ids_to_exclude=&exclude_in_running=0'
    data = download(url)
    return [i['outcome_id'] for i in data.json()[:5]]

def get_data():
    markets, markets2 = get_market()
    outcomes = get_outcome()
    five = get_five_ids()

    outcome_ids = ['{"type":"register","address":"/outcome/%s"}' % i for i in outcomes]
    market_ids = ['{"type":"register","address":"/market/%s"}' % i for i in markets]
    # 1
    data = [
        '{"type":"ping"}',
        '{"type":"register","address":"/outcome/66367385100"}',
        '{"type":"register","address":"/outcome/66367385300"}',
        '{"type":"register","address":"/outcome/66375635200"}',
        '{"type":"register","address":"/outcome/66375635400"}',
        '{"type":"register","address":"/outcome/66367576000"}',
        '{"type":"register","address":"/outcome/66367576100"}',
        '{"type":"send","address":"get/outcome","body":{"payload":{"ids":[66367385100,66367385300,66375635200,66375635400,66367576000,66367576100]}},"replyAddress":"43e01853-7d0a-4551-851c-997343480fbc"}',

    ]
    # 2
    for i in market_ids:
        data.append(i)

    # 3
    # 这条数据的ids在页面能找到所有的
    # 数据1
    data.append('{"type":"send","address":"get/outcome","body":{"payload":{"ids": %s}},"replyAddress":"1fd59598-b405-45dd-955e-e23f1dbac15e"}' % str(markets2))
    # data.append('{"type":"send","address":"get/outcome","body":{"payload":{"ids":[66725095600,66725096200,66725096800,66725097400,66725960400,66725960500,66725099700,66725100300,66725100900,66725101100,66725101400,66725101700,66696924700,66696924800,66696924900,66696925100,66696924500,66696924600,66696557300,66696557500,66696556700,66696557000,66696555900,66696556300,66696173600,66696173900,66696174200,66696174500,66696536000,66696536100,66696554200,66696554500,66723859300,66723859400,66696553500,66696554000,66701323100,66701323200,66698582200,66698582300,66698582400,66698582500,66724191500,66724191600,66696181300,66696181700,66696180700,66696181000,66697550700,66697550800,66696197000,66696197400,66696536600,66696536700,66696562200,66696562500,66696561700,66696561900,66696562900,66696563200]}},"replyAddress":"23c6a4f8-dc9b-434b-96cf-84e97373378b"}')
    # print(aa)
    data.append('{"type":"register","address":"/market/undefined"}')
    # 这条数据的ids前五个id在ajax中，ajax请求数据有十条，前五条就是，后几条就是上一条数据（数据1）的ids
    # data.append('{"type":"send","address":"get/outcome","body":{"payload":{"ids":[66725096800,66725011800,66652162700,66727504000,66699127400,66725095600,66725096200,66725096800,66725097400,66725960400,66725960500,66725099700,66725100300,66725100900,66725101100,66725101400,66725101700,66696924700,66696924800,66696924900,66696925100,66696924500,66696924600,66696557300,66696557500,66696556700,66696557000,66696555900,66696556300,66696173600,66696173900,66696174200,66696174500,66696536000,66696536100,66696554200,66696554500,66723859300,66723859400,66696553500,66696554000,66701323100,66701323200,66698582200,66698582300,66698582400,66698582500,66724191500,66724191600,66696181300,66696181700,66696180700,66696181000,66697550700,66697550800,66696197000,66696197400,66696536600,66696536700,66696562200,66696562500,66696561700,66696561900,66696562900,66696563200]}},"replyAddress":"b1fa6677-6f26-4875-99ed-1323f7d3b602"}')
    data.append('{"type":"send","address":"get/outcome","body":{"payload":{"ids": %s}},"replyAddress":"4fb49631-ad78-4c35-be6e-2cf496af8c41"}' % str(five + markets2))

    for i in outcome_ids:
        data.append(i)
    # 上面都是构造的参数，还没看js，
    # 主要就是获取比赛的id 拼接成消息
    # 发送的前六条id不清楚 估计是js里面的，第七条是将前六条的outcome放到payload的ids里面
    # 后面的replyAddress类似uuid 每次都不一样，肯定在js # 暂时不用也可以
    # market在前端都能获取到 就是一个元素的id如li 需要自己清洗一下
    # 然后就是3 添加的ids也是前端里面的
    # 发送完这些还有一些数据  是ajax用普通的http请求发来的 只需要请求那条URL获取outcome_id 然后序列化参数
    ##############################################
    return data

def on_message(ws, message):
    # 不断接受消息，一定要try一下，因为有的数据是空的
    try:
        time.sleep(0.1)
        mg = message[2:-1].replace('\\', '')[1:-1]
        print(mg)
    except:
        print('*'*60)
        print(message)



def on_close(ws):
    ws.close()

def on_open(ws):
    data = get_data()
    def run(data):
        # 首先循环要发送的消息列表，将需要发送的消息发到服务器
        for i in data:
            ws.send(json.dumps(i))

        # 自己写心跳，websocket自带心跳不好用
        while True:
            # 根据前端ws协议的请求间隔
            time.sleep(5)
            # 发送ping
            ws.send(json.dumps('{"type":"ping"}'))

        # ws.close()

    # 开一个线程一直跑，不要阻塞主进程
    t1 = threading.Thread(target=run, args=(data, ))
    t1.start()
    # t1.join()




def on_error(ws, error):
    logger.error(error)

# key不断变化  待解决
header = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'Upgrade',
    'Host': 'dt-rt.com:8444',
    'Origin': 'https://www.betvictor56.com',
    'Pragma': 'no-cache',
    # 'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    'Sec-WebSocket-Key': 'QLQ5G52XtKz0Vv9K5/CEEQ==',
    'Sec-WebSocket-Version': '13',
    'Upgrade': 'websocket',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
}

if __name__ == '__main__':
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        url='wss://dt-rt.com:8444/eventbus/654/4u0a5yvl/websocket',
        on_close=on_close,
        on_error=on_error,
        on_message=on_message,
        header=header
    )
    # 首次连接打开
    ws.on_open = on_open
    # 循环起来
    ws.run_forever()


    # res = get_market()
    # print('{"type":"send","address":"get/outcome","body":{"payload":'+str(res[1])+'},"replyAddress":"1fd59598-b405-45dd-955e-e23f1dbac15e"})')
    # '''"{"type":"send","address":"get/outcome","body":{"payload":{"ids":[66725095600,66725096200,66725096800,66725097400,66725960400,66725960500,66725099700,66725100300,66725100900,66725101100,66725101400,66725101700,66696924700,66696924800,66696924900,66696925100,66696924500,66696924600,66696557300,66696557500,66696556700,66696557000,66696555900,66696556300,66696173600,66696173900,66696174200,66696174500,66696536000,66696536100,66696554200,66696554500,66723859300,66723859400,66696553500,66696554000,66701323100,66701323200,66698582200,66698582300,66698582400,66698582500,66724191500,66724191600,66696181300,66696181700,66696180700,66696181000,66697550700,66697550800,66696197000,66696197400,66696536600,66696536700,66696562200,66696562500,66696561700,66696561900,66696562900,66696563200]}},"replyAddress":"23c6a4f8-dc9b-434b-96cf-84e97373378b"}"'''
    # rl = 'https://www.betvictor56.com/zh-cn/sport/football'
    # res = download(rl)
    # html = etree.HTML(res.text)
    # response = html.xpath('//span[@data-sp="0"]/@data-bet')
    # # print(response)
    # a = list(map(int, response))
    # a = get_five_ids()
    # print(a)

# # """'{"type":"send","address":"get/outcome","body":{"payload":{"ids":[66725095600,66725096200,66725096800,66725097400,66725960400,66725960500,66725099700,66725100300,66725100900,66725101100,66725101400,66725101700,66696924700,66696924800,66696924900,66696925100,66696924500,66696924600,66696557300,66696557500,66696556700,66696557000,66696555900,66696556300,66696173600,66696173900,66696174200,66696174500,66696536000,66696536100,66696554200,66696554500,66723859300,66723859400,66696553500,66696554000,66701323100,66701323200,66698582200,66698582300,66698582400,66698582500,66724191500,66724191600,66696181300,66696181700,66696180700,66696181000,66697550700,66697550800,66696197000,66696197400,66696536600,66696536700,66696562200,66696562500,66696561700,66696561900,66696562900,66696563200]}},"replyAddress":"23c6a4f8-dc9b-434b-96cf-84e97373378b"}'"""
#
#     li = [66756355000,66756326700,66756383300,66756284900,66756302500,66726255100,66726255300,66723333700,66723333800,66723333900,66723334000,66201150900,66201151100,66201151000,66160916000,66160916100,66160915800,66160915900,66160916200,66160916300,66725095900,66725096500,66755765700,66755765800,66725097100,66725097700,66725105800,66725106000,66725105400,66725105600,66725106100,66725106200,66725095500,66725096100,66725096600,66725097200,66725097800,66725098400,66725104100,66725104400,66725105000,66725105200,66725104600,66725104800,66201157500,66201157600,66201157700,66201157800,66201157900,66201158000,66696924700,66696924800,66696924900,66696925100,66696924500,66696924600,66696557300,66696557500,66696556700,66696557000,66696555900,66696556300,66696173600,66696173900,66696174200,66696174500,66696536000,66696536100,66696554200,66696554500,66723859300,66723859400,66696553500,66696554000,66701323100,66701323200,66698582200,66698582300,66698582400,66698582500,66724191500,66724191600,66696181300,66696181700,66696180700,66696181000,66697550700,66697550800,66696197000,66696197400,66696536600,66696536700,66696562200,66696562500,66696561700,66696561900,66696562900,66696563200]
#     print(li)
#     def get_data(a, b, c):
#         d = (b**2-4*a*c)
#         if d >= 0:
#             x = (-b + math.sqrt(d)) / 2*a
#             y = (-b - math.sqrt(d)) / 2*a
#             print(y)
