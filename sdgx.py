import base64
import requests
import binascii


session = requests.Session()
session.headers = {
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
}

params = {
    "client_id": "online-agency",
    "user_type": "student",
    "response_type": "code",
    "redirect_uri": "http://www.sdgxbys.cn/platform/service/user/login/oauth/student"
}

# resp = session.get(url='http://auth.sdbys.com/oauth2/auth/authorize', params=params)
# print(resp.text)
# print(resp.cookies)
a = "OAXb3WwBfrG6fO3mzo3Pi75NCIvippssB1IBRGG511U4_gph9yELik9QvsyS6j5FmXOBM7hwDszSWUKoSQnlorDklDScc-1a14kxevS1SQv-V0m5bP0iZ06cOgpvbXqI68gpHt6guUu09b91826__YYHKSA-huO3WwqB2nYMo5Qym9cRRYjzMWKgpdN--o35wSU9lC-VV0HvFF7KsEvqeKxmOhsQqDSBsVtodliSTUVglyDvc9FBg5iryC08FOW5OUaMt6CdwHYdJXTmuoaew0VEXiwZEVM8pFDm9QaOrWd3zwvxtHwZRM5xsBb5HnP4Qj1bR_QVtHDhkzpQ3xaoPSfMQwfE59Ke_CWwXKjmFs-7mpKCgLMTw5vpznYJVsI8zgpVv9ttGKJjVry9iB49ftaGKVYODAdZVynlzEYhwXh9C2COwp4mFpJHtLYd18nHja7bxW6KEyaWENwrDKKXrdBOGATrBwkPpywm7ZQ90XIAqLnfNHRQg66JMjsw1bOuhBoMWAmLZszj3ZVvitDJml8lOcDEAJsUTCceRjeEKDQ2DdXLfRznZLm14_BafWUDRENeVB3S-3M7MTu11gAHIw"
img = binascii.a2b_base64(a.encode())
print(img)

# print(base64.urlsafe_b64decode(binascii.a2b_base64(a.encode())))
with open('image/sdgx.png', 'wb') as f:
    f.write(img)