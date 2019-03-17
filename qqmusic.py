import requests
import re



class QQmusic():
    def __init__(self):
        pass

    def first_sid(self):
        for i in range(0,3):
            resp = requests.get('https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date=2018-12-03&topid=4&type=top&song_begin={}&song_num=30&g_tk=5381&jsonpCallback=MusicJsonCallbacktoplist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'.format(i*30)).text
            sid = re.findall(r'"songmid":"(.*?)"', resp)
            return sid


    def save(self, sid_list):
        # sid = '001lxWgP1C4MnJ'
        for sid in sid_list:
            data = '{"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"130979388","songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":20,"cv":0}}'%sid

            pamars = {
                "callback": "getplaysongvkey15782675050806594",
                "g_tk": "5381",
                "jsonpCallback": "getplaysongvkey15782675050806594",
                "loginUin": "0",
                "hostUin": "0",
                "format": "jsonp",
                "inCharset": "utf8",
                "outCharset": "utf-8",
                "notice": "0",
                "platform": "yqq",
                "needNewCode": "0",
                "data": data
                }

            resp = requests.get('https://u.y.qq.com/cgi-bin/musicu.fcg?', params=pamars).text

            result = re.search(r'"purl":"(.*?)"', resp).group(1)
            url = 'http://isure.stream.qqmusic.qq.com/{}'.format(result)
            print(url)

    def run(self):
        sid_list = self.first_sid()
        self.save(sid_list)


if __name__ == '__main__':
    qq = QQmusic()
    qq.run()
