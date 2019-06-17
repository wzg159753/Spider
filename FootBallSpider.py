import time
import json
import logging
import threading

import requests
import websocket
from lxml import etree

logger = logging.getLogger('football')

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


class GetData(object):
    """
    获取ws要发送的数据
    """

    def _get_data(self, markets=None, markets2=None, outcomes=None, five=None):
        """
        构造要send的数据
        :return:
        """
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

        if markets[0]:
            market_ids = ['{"type":"register","address":"/market/%s"}' % i for i in markets]
            for i in market_ids:
                data.append(i)

        # 3
        # 这条数据的ids在页面能找到所有的
        # 数据1
        if markets2:
            data.append(
                '{"type":"send","address":"get/outcome","body":{"payload":{"ids": %s}},"replyAddress":"1fd59598-b405-45dd-955e-e23f1dbac15e"}' % str(markets2))
        # data.append('{"type":"send","address":"get/outcome","body":{"payload":{"ids":[66725095600,66725096200,66725096800,66725097400,66725960400,66725960500,66725099700,66725100300,66725100900,66725101100,66725101400,66725101700,66696924700,66696924800,66696924900,66696925100,66696924500,66696924600,66696557300,66696557500,66696556700,66696557000,66696555900,66696556300,66696173600,66696173900,66696174200,66696174500,66696536000,66696536100,66696554200,66696554500,66723859300,66723859400,66696553500,66696554000,66701323100,66701323200,66698582200,66698582300,66698582400,66698582500,66724191500,66724191600,66696181300,66696181700,66696180700,66696181000,66697550700,66697550800,66696197000,66696197400,66696536600,66696536700,66696562200,66696562500,66696561700,66696561900,66696562900,66696563200]}},"replyAddress":"23c6a4f8-dc9b-434b-96cf-84e97373378b"}')
        # print(aa)
        data.append('{"type":"register","address":"/market/undefined"}')
        # 这条数据的ids前五个id在ajax中，ajax请求数据有十条，前五条就是，后几条就是上一条数据（数据1）的ids
        # data.append('{"type":"send","address":"get/outcome","body":{"payload":{"ids":[66725096800,66725011800,66652162700,66727504000,66699127400,66725095600,66725096200,66725096800,66725097400,66725960400,66725960500,66725099700,66725100300,66725100900,66725101100,66725101400,66725101700,66696924700,66696924800,66696924900,66696925100,66696924500,66696924600,66696557300,66696557500,66696556700,66696557000,66696555900,66696556300,66696173600,66696173900,66696174200,66696174500,66696536000,66696536100,66696554200,66696554500,66723859300,66723859400,66696553500,66696554000,66701323100,66701323200,66698582200,66698582300,66698582400,66698582500,66724191500,66724191600,66696181300,66696181700,66696180700,66696181000,66697550700,66697550800,66696197000,66696197400,66696536600,66696536700,66696562200,66696562500,66696561700,66696561900,66696562900,66696563200]}},"replyAddress":"b1fa6677-6f26-4875-99ed-1323f7d3b602"}')
        if five:
            data.append(
                '{"type":"send","address":"get/outcome","body":{"payload":{"ids": %s}},"replyAddress":"4fb49631-ad78-4c35-be6e-2cf496af8c41"}' % str(five + markets2))

        outcome_ids = ['{"type":"register","address":"/outcome/%s"}' % i for i in outcomes]
        if outcome_ids:
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
        print(len(data))
        # print(outcomes)
        return data

    def download(self, url, params=None, **kwargs):
        return requests.get(url, params=params)

    def _get_outcome(self):
        """
        获取第三条长数据之后的id 构成数据发送
        :return:
        """
        params = {
            'max_outcomes_per_event': '3',
            'max_events_per_sport': '10',
            'event_ids_to_exclude': '',
            'exclude_rank_events': 'true',
            'exclude_game_events': 'false',
            'sport_ids[]': '100'
        }
        url = 'https://www.betvictor56.com/bv_api/price_it_up_home_component'
        response = self.download(url, params).json()['priceItUps']  # [0]['outcomeIds']
        data = []
        lis = [data.extend(i['outcomeIds']) for i in response]
        return data

    def _get_market(self):
        """
        获取第一条长数据和第二条长数据之间的id 14..... 构成数据发送
        :return:
        """
        uri = 'https://www.betvictor56.com/zh-cn/sport/football'
        resp = self.download(uri)
        html = etree.HTML(resp.text)
        # 将span标签的date-bet属性解析，就是单条的"{"type":"register","address":"/outcome/66871921200"}"里面的outcome，爬取全部[16871921200, .....]
        # 用map函数将列表中的字符串转为int
        info = html.xpath('//span[@data-ew_d="1"]/@data-bet')
        lis = list(map(int, info))
        # 一定要将字符串列表转化为int列表
        # 获取"{"type":"register","address":"/market/148697737"}" 里面的market  用split将其分割成列表 [148697737, .....]
        select = '//select[@id="Selector"]/@data-unique-key'
        path = '//h4[@class="sortable_coupon sports-coupon__title"]/@data-market-id | //div[@class="single_markets"]//h4/@data-market-id'
        # li = list(map(int, '-'.join(html.xpath(path)).split('-')))
        li = self.market_id(html, path, '-')
        ids = self.market_id(html, select, six='_', offset=1)
        id_list = li+ids
        # 返回
        return id_list, lis

    def market_id(self, html, path, six=None, offset=None, end=None):
        """
        获取market的不规则id
        :param html:
        :param path:
        :param six:
        :param offset:
        :param end:
        :return:
        """
        info = html.xpath(path)
        if info:
            ids = list(map(int, six.join(info).split(six)[offset:end]))
        else:
            ids = []
        return ids


    def get_five_ids(self):
        """
        获取第三条长数据的前五条
        在ajax请求中
        :return:
        """
        url = 'https://www.betvictor56.com/zh-cn/sport/top_bets/100?event_ids_to_exclude=&exclude_in_running=0'
        data = self.download(url)
        return [i['outcome_id'] for i in data.json()[:5]]

    def run(self):
        five = self.get_five_ids() # 五个id
        mar1, mar2 = self._get_market()
        out_id = self._get_outcome()
        # data = self._get_data(markets=mar1, markets2=mar2, outcomes=out_id, five=five)
        return {
            'five': five,
            'markets': mar1,
            'markets2': mar2,
            'outcomes': out_id
        }


class FootWebSocket(websocket.WebSocketApp):
    def __init__(self):
        # 重写init，，将参数传入
        info = dict(
            url='wss://dt-rt.com:8444/eventbus/654/4u0a5yvl/websocket',
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message,
            header=header
        )

        # 复用父类init将参数传入
        super().__init__(**info)

    def on_open(self):
        """
        打开ws连接，发送数据
        :return:
        """
        # get_market方法是获取market的id的方法
        info = GetData()
        data = info.run()
        # 获取要发送的数据
        data = info._get_data(**data)

        def run(data):
            # 首先循环要发送的消息列表，将需要发送的消息发到服务器
            # 只发送一次，发送完成后就开始心跳检测
            print(data)
            for i in data:
                ws.send(json.dumps(i))

            # 自己写心跳，websocket自带心跳不好用
            while True:
                # 根据前端ws协议的请求间隔
                time.sleep(5)
                # 发送ping心跳   这里可以异常捕获一下  因为有时候连接失败
                # websocket._exceptions.WebSocketConnectionClosedException: Connection is already closed.
                # 网站也是重新发送了websocket请求  data变化一下再创建ws连接
                try:
                    ws.send(json.dumps('{"type":"ping"}'))
                except Exception as e:
                    logger.error(e)
                    # 第二次请求发送的数据不一样 就是重新发送一次请求 但是发送的数据不一样
                    ws.run_forever()

            # ws.close()

        # 开一个线程一直跑，不要阻塞主线程，一直跑下去
        t1 = threading.Thread(target=run, args=(data,))
        t1.start()
        # t1.join()

    def on_close(self):
        """
        关闭ws连接
        :return:
        """
        ws.close()

    def on_message(self, message):
        """
        接收服务端返回的消息，并处理
        :param message: 返回的数据
        :return:
        """
        # 接收的数据清洗时可能会出错  异常捕获
        try:
            time.sleep(0.1) # 可有可无
            mg = message[2:-1].replace('\\', '')[1:-1] # 消息是一个不规则的字符串，要自己清洗
            if mg:
                print("接受消息：{}".format(mg))
            else:
                print('h')
        except Exception as e:
            logger.warning(e) # 偶尔会返回一个h

    def on_error(self, error):
        """
        当ws报错时触发的方法
        :param error:
        :return:
        """
        logger.error(error)


if __name__ == '__main__':
    url = 'https://www.betvictor56.com/bv_api/price_it_up_home_component'

    websocket.enableTrace(True)
    ws = FootWebSocket()
    ws.run_forever()
    # data = GetData()
    # print(data.run())

