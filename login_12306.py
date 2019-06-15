import base64
import requests
from datetime import datetime




class Login12306(object):

    def __init__(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://kyfw.12306.cn/otn/resources/login.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
            # "Cookie": "RAIL_EXPIRATION=1560787641484; RAIL_DEVICEID=ePNYLFXq-2lSGfT8ZQDzr3NNs0GHsKmCQyw7vR3I8hGrcd03vDpXNsdgyzcH5SywJ3zm_9jGgltuz_0GYT5qz3rm8hwhDasM5L62_vkBrYJX3awQOy-Ylsi0M78I9o6EqYz0PfG0abIoExZtxkJ8mTzyg2zCyVtm; _passport_session=f53f3964ce834fbda52cdab3b7b392749283; _passport_ct=4eaedaf668904183a9c6fe8ef7b4ea68t2436; RAIL_EXPIRATION=1560787641484; RAIL_DEVICEID=ePNYLFXq-2lSGfT8ZQDzr3NNs0GHsKmCQyw7vR3I8hGrcd03vDpXNsdgyzcH5SywJ3zm_9jGgltuz_0GYT5qz3rm8hwhDasM5L62_vkBrYJX3awQOy-Ylsi0M78I9o6EqYz0PfG0abIoExZtxkJ8mTzyg2zCyVtm; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2019-06-14; _jc_save_toDate=2019-06-14; _jc_save_wfdc_flag=dc; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=2246574346.24610.0000; BIGipServerpassport=770179338.50215.0000"
        }
        self.session = requests.Session()
        self.session.headers = headers

    def get_time(self):
        return int(datetime.now().timestamp() * 1000)

    def get_x_y(self, args):

        x_y = {
            '1': '40,40',
            '2': '110,46',
            '3': '180,42',
            '4': '250,45',
            '5': '42,100',
            '6': '112,101',
            '7': '181,103',
            '8': '249,106',
        }
        x_y_list = []
        for i in args:
            x_y_list.append(x_y.get(i))
        return ','.join(x_y_list)

    def download(self, url, params=None, data=None, active='get'):
        response = None
        if active == 'get':
            response = self.session.get(url, params=params)
        elif active == 'post':
            response = self.session.post(url, data=data)

        return response

    def get_verify_image(self):
        params = {
            'login_site': 'E',
            'module': 'login',
            'rand': 'sjrand',
            str(self.get_time()): 'callback: jQuery19108518562441080331_{}'.format(str(self.get_time())),
            '_': str(self.get_time())
        }
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image64'
        result = self.download(url, params=params)
        image = result.json()['image']
        data = base64.urlsafe_b64decode(image.encode())
        with open('image/img_12306.jpg', 'wb') as f:
            f.write(data)

    def captcha_check(self, li):
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        params = {
            "callback": "jQuery19105560178401069158_{}".format(str(self.get_time())),
            "answer": li,
            "rand": "sjrand",
            "login_site": "E",
            "_": str(self.get_time())
        }
        response = self.download(url, params=params)
        return response.text

    def login(self, answer):
        data = {
            "username": "1231651",
            "password": "wzg159753",
            "appid": "otn",
            "answer": answer
        }
        url = 'https://kyfw.12306.cn/passport/web/login'
        resp = self.download(url, data=data, active='post')
        resp.encoding = 'UTF-8'
        print(resp.url)
        print(resp.text)


    def run(self):
        self.get_verify_image()
        please = input('please enter num:')
        li = please.split()
        args = self.get_x_y(li)
        check = self.captcha_check(args)
        print(args)
        print(check)
        # self.login(li)


if __name__ == '__main__':
    login = Login12306()
    login.run()

#
# def get_x_y(args):
#         x_y = {
#             '1': '40,40',
#             '2': '110,46',
#             '3': '180,42',
#             '4': '250,45',
#             '5': '42,100',
#             '6': '112,101',
#             '7': '181,103',
#             '8': '249,106',
#         }
#         x_y_list = []
#         for i in args:
#             x_y_list.append(x_y.get(i))
#         return ','.join(x_y_list)
#
#
# def get_time():
#     return int(datetime.now().timestamp() * 1000)
#
# session = requests.Session()
# session.headers = headers = {
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#             "Referer": "https://kyfw.12306.cn/otn/resources/login.html",
#             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
#             # "Cookie": "RAIL_EXPIRATION=1560787641484; RAIL_DEVICEID=ePNYLFXq-2lSGfT8ZQDzr3NNs0GHsKmCQyw7vR3I8hGrcd03vDpXNsdgyzcH5SywJ3zm_9jGgltuz_0GYT5qz3rm8hwhDasM5L62_vkBrYJX3awQOy-Ylsi0M78I9o6EqYz0PfG0abIoExZtxkJ8mTzyg2zCyVtm; _passport_session=f53f3964ce834fbda52cdab3b7b392749283; _passport_ct=4eaedaf668904183a9c6fe8ef7b4ea68t2436; RAIL_EXPIRATION=1560787641484; RAIL_DEVICEID=ePNYLFXq-2lSGfT8ZQDzr3NNs0GHsKmCQyw7vR3I8hGrcd03vDpXNsdgyzcH5SywJ3zm_9jGgltuz_0GYT5qz3rm8hwhDasM5L62_vkBrYJX3awQOy-Ylsi0M78I9o6EqYz0PfG0abIoExZtxkJ8mTzyg2zCyVtm; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromDate=2019-06-14; _jc_save_toDate=2019-06-14; _jc_save_wfdc_flag=dc; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=2246574346.24610.0000; BIGipServerpassport=770179338.50215.0000"
#         }
#
#
# params = {
#         'login_site': 'E',
#         'module': 'login',
#         'rand': 'sjrand',
#         str(get_time()): 'callback: jQuery19108518562441080331_1560501053906',
#         '_': str(get_time())
#     }
#
#
#
# url = 'https://kyfw.12306.cn/passport/captcha/captcha-image64'
# result = session.get(url, params=params)
# image = result.json()['image']
# data = base64.urlsafe_b64decode(image.encode())
# with open('image/img_12306.jpg', 'wb') as f:
#     f.write(data)
#
# please = input('please enter num:')
# args = please.split()
# li = get_x_y(args)
#
# url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
# params = {
#     "callback": "jQuery19105560178401069158_{}".format(str(get_time())),
#     "answer": li,
#     "rand": "sjrand",
#     "login_site": "E",
#     "_": str(get_time())
# }
# session.params = params
# response = session.get(url, params=params)
# print(response.text)

