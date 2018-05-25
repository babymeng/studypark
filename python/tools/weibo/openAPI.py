#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib.request
import urllib.response
import urllib.error
import urllib.parse
import random
import socket
import redis
import base64
from hashlib import sha1

'''访问平台接口'''

# 存储token及secret的redis
token_redis_address = {"host":"rs20605.hebe.grid.sina.com.cn", "port":20605}
token_redis_address_bak = {"host":"rs20605.hebe.grid.sina.com.cn", "port":20605}

token_key = "TOKEN_981203697_frontend_token"
secret_key = "TOKEN_981203697_frontend_secret"

# token的全局存储字典
g_token_dict = {token_key: "", secret_key: "", "ts": 0}
g_token_duration = 900

# 用户及密码
auth_user = "13715190361"
auth_passwd = "gnuzfl5677o"

# 获取token
def get_token():
    try:
        current_ts = int(time.time())
        time_past = current_ts - g_token_dict["ts"]
        if time_past <= g_token_duration + random.randint(1, 100):
            return g_token_dict[token_key], g_token_dict[secret_key]

        mget_key = [token_key, secret_key]
        try:
            host = token_redis_address["host"]
            port = token_redis_address["port"]
            db = redis.Redis(host, port, socket_timeout = 0.02)
            token_result = db.mget(mget_key)
        except Exception as e:
            try:
                host = token_redis_address_bak["host"]
                port = token_redis_address_bak["port"]
                db = redis.Redis(host, port, socket_timeout = 0.02)
                token_result = db.mget(mget_key)
            except Exception as e:
                print("connect token redis error: %s" % str(e))
                return g_token_dict[token_key], g_token_dict[secret_key]

        if token_result == None or len(token_result) <= 0:
            return g_token_dict[token_key], g_token_dict[secret_key]

        g_token_dict[token_key] = token_result[0]
        g_token_dict[secret_key] = token_result[1]
        g_token_dict["ts"] = int(time.time())
        return g_token_dict[token_key], g_token_dict[secret_key]
    except Exception as e:
        print("get_token Error: %s" % str(e))
        return g_token_dict[token_key], g_token_dict[secret_key]

# 生成加密头
def generate_header(type, user=auth_user, passwd=auth_passwd, uid=None):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    if type == "BaseAuth":
        b64str = base64.encodestring('%s:%s' % (user, passwd))[:-1]
        headers["Authorization"] = "Basic %s" % b64str
    elif type == "Tauth2":
        token, sign = get_token()
        token_str = urllib.request.quote(token)                 # 对token使用urlencode编码

        import hmac
        param = "uid=%s" % str(uid)                     # 更换uid
        h = hmac.new(sign, digestmod=sha1)              # 使用sha1进行签名
        h.update(param.encode('utf-8'))

        sign_sha = base64.b64encode(h.digest())         # 对签名后的请求参数使用base64编码
        sign_str = urllib.request.quote(sign_sha)               # 对编码后的签名使用urlencode编码

        authorization_value = 'TAuth2 token="%s", param="%s", sign="%s"' % (token_str, param, sign_str)
        headers["Authorization"] = authorization_value
        

    return headers


# 无授权GET方式访问http
def read_url_by_GET(url, connect_time_out = 2, read_time_out = 2):
    result = ""
    try:
        socket.setdefaulttimeout(connect_time_out)

        headers = generate_header("NoAuth", None)
        req = urllib.request.Request(url = url, headers = headers)

        result = urllib.request.urlopen(req, timeout = read_time_out).read()

    except urllib.error.HTTPError as e:        # HTTP错误，由服务器返回的错误，比如403,404之类
        result = e.read()
    except urllib.error.URLError as e:         # URL错误，比如地址不存在，超时等
        print("read_url_by_GET error.URLError: %s %s" % (url, e.reason))
    except Exception as e:
        print("read_url_by_GET Error: %s %s" % (url, str(e)))

    return result


# 无授权POST方式访问http
def read_url_by_POST(url, param, connect_time_out = 0.2, read_time_out = 0.5):
    result = ""
    try:
        socket.setdefaulttimeout(connect_time_out)

        headers = generate_header("NoAuth", None)
        req = urllib.request.Request(url = url, headers = headers)
        req_param = urllib.urlencode(param)

        result = urllib.request.urlopen(req, req_param, timeout = read_time_out).read()

    except urllib.error.HTTPError as e:        # HTTP错误，由服务器返回的错误，比如403,404之类
        result = e.read()
    except urllib.error.URLError as e:         # URL错误，比如地址不存在，超时等
        print("read_url_by_POST error.URLError: %s %s %s" % (url, req_param, e.reason))
    except Exception as e:
        print("read_url_by_POST Error: %s %s" % (url, str(e)))

    return result

# 无授权POST方式访问http
def read_url_by_POST2(url, data, connect_time_out = 0.2, read_time_out = 0.5):
    result = ""
    try:
        socket.setdefaulttimeout(connect_time_out)

        headers = generate_header("NoAuth", None)
        req = urllib.request.Request(url = url, headers = headers)

        result = urllib.request.urlopen(req, data, timeout = read_time_out).read()

    except urllib.error.HTTPError as e:        # HTTP错误，由服务器返回的错误，比如403,404之类
        result = e.read()
    except urllib.error.URLError as e:         # URL错误，比如地址不存在，超时等
        print("read_url_by_POST error.URLError: %s %s %s" % (url, data, e.reason))
    except Exception as e:
        print("read_url_by_POST Error: %s %s" % (url, str(e)))

    return result



# Tauth2授权GET方式访问http，适用于需要伪登录的情况
def read_url_by_GET_with_Tauth(url, uid, connect_time_out = 2, read_time_out = 5):
    result = ""
    try:
        socket.setdefaulttimeout(connect_time_out)

        headers = generate_header("Tauth2", uid = uid)
        req = urllib.request.Request(url = url, headers = headers)

        result = urllib.request.urlopen(req, timeout = read_time_out).read()

    except urllib.error.HTTPError as e:        # HTTP错误，由服务器返回的错误，比如403,404之类
        result = e.read()
    except urllib.error.URLError as e:         # URL错误，比如地址不存在，超时等
        print("read_url_by_GET_with_Tauth error.URLError: %s %s %s" % (url, uid, e.reason))
    except Exception as e:
        print("read_url_by_GET_with_Tauth Error: %s %s" % (url, str(e)))

    return result


# Tauth2授权POST方式访问http，适用于需要伪登录的情况
def read_url_by_POST_with_Tauth(url, uid, param, connect_time_out = 0.2, read_time_out = 0.5):
    result = ""
    try:
        socket.setdefaulttimeout(connect_time_out)

        headers = generate_header("Tauth2", uid = uid)
        req = urllib.request.Request(url = url, headers = headers)
        req_param = urllib.urlencode(param)

        result = urllib.request.urlopen(req, req_param, timeout = read_time_out).read()

    except urllib.error.HTTPError as e:        # HTTP错误，由服务器返回的错误，比如403,404之类
        result = e.read()
    except urllib.error.URLError as e:         # URL错误，比如地址不存在，超时等
        print("read_url_by_POST_with_Tauth error.URLError: %s %s %s %s" % (url, uid, req_param, e.reason))
    except Exception as e:
        print("read_url_by_POST_with_Tauth Error: %s %s" % (url, str(e)))

    return result


# Tauth2授权POST方式访问http，适用于需要伪登录的情况
def read_url_by_POST2_with_Tauth(url, uid, data, connect_time_out = 0.2, read_time_out = 0.5):
    result = ""
    try:
        socket.setdefaulttimeout(connect_time_out)

        headers = generate_header("Tauth2", uid = uid)
        req = urllib.request.Request(url = url, headers = headers)

        result = urllib.request.urlopen(req, data, timeout = read_time_out).read()

    except urllib.error.HTTPError as e:        # HTTP错误，由服务器返回的错误，比如403,404之类
        result = e.read()
    except urllib.error.URLError as e:         # URL错误，比如地址不存在，超时等
        print("read_url_by_POST2_with_Tauth error.URLError: %s %s %s %s" % (url, uid, req_param, e.reason))
    except Exception as e:
        print("read_url_by_POST2_with_Tauth Error: %s %s" % (url, str(e)))

    return result



# Tauth2授权POST方式带文件访问http，适用于需要伪登录的情况
def read_url_by_POST_with_Tauth_forFile(url, uid, req_param, connect_time_out = 0.2, read_time_out = 0.5):
    result = ""
    try:
        socket.setdefaulttimeout(connect_time_out)

        headers = generate_header("Tauth2", uid = uid)

        from poster.encode import multipart_encode
        from poster.streaminghttp import register_openers
        register_openers()
        datagen, headers = multipart_encode(req_param)
        req = urllib.request.Request(url, datagen, headers)

        result = urllib.request.urlopen(req, req_param, timeout = read_time_out).read()

    except urllib.error.HTTPError as e:        # HTTP错误，由服务器返回的错误，比如403,404之类
        result = e.read()
    except urllib.error.URLError as e:         # URL错误，比如地址不存在，超时等
        print("read_url_by_POST_with_Tauth_forFile error.URLError: %s %s %s %s" % (url, uid, req_param, e.reason))
    except Exception as e:
        print("read_url_by_POST_with_Tauth_forFile Error: %s %s" % (url, str(e)))

    return result


# BaseAuth授权GET方式访问http，适用于需要登录的情况
def read_url_by_GET_with_passwd(url, user = auth_user, passwd = auth_passwd, connect_time_out = 0.2, read_time_out = 0.5):
    result = ""
    try:
        socket.setdefaulttimeout(connect_time_out)

        headers = generate_header("BaseAuth", user, passwd)
        req = urllib.request.Request(url = url, headers = headers)

        result = urllib.request.urlopen(req, timeout = read_time_out).read()

    except urllib.error.HTTPError as e:        # HTTP错误，由服务器返回的错误，比如403,404之类
        result = e.read()
    except urllib.error.URLError as e:         # URL错误，比如地址不存在，超时等
        print("read_url_by_GET_with_passwd error.URLError: %s %s" % (url, e.reason))
    except Exception as e:
        print("read_url_by_GET_with_passwd Error: %s %s" % (url, str(e)))

    return result


# BaseAuth授权POST方式访问http，适用于需要登录的情况
def read_url_by_POST_with_passwd(url, param, user = auth_user, passwd = auth_passwd, connect_time_out = 0.2, read_time_out = 0.5):
    result = ""
    try:
        socket.setdefaulttimeout(connect_time_out)

        headers = generate_header("BaseAuth", user, passwd)
        req = urllib.request.Request(url = url, headers = headers)
        req_param = urllib.urlencode(param)

        result = urllib.request.urlopen(req, req_param, timeout = read_time_out).read()

    except urllib.error.HTTPError as e:        # HTTP错误，由服务器返回的错误，比如403,404之类
        result = e.read()
    except urllib.error.URLError as e:         # URL错误，比如地址不存在，超时等
        print("read_url_by_POST_with_passwd error.URLError: %s %s %s" % (url, req_param, e.reason))
    except Exception as e:
        print("read_url_by_POST_with_passwd Error: %s %s" % (url, str(e)))

    return result

# BaseAuth授权POST方式访问http，适用于需要登录的情况
def read_url_by_POST2_with_passwd(url, param, user = auth_user, passwd = auth_passwd, connect_time_out = 0.2, read_time_out = 0.5):
    result = ""
    try:
        socket.setdefaulttimeout(connect_time_out)

        headers = generate_header("BaseAuth", user, passwd)
        req = urllib.request.Request(url = url, headers = headers)

        result = urllib.request.urlopen(req, param, timeout = read_time_out).read()

    except urllib.error.HTTPError as e:        # HTTP错误，由服务器返回的错误，比如403,404之类
        result = e.read()
    except urllib.error.URLError as e:         # URL错误，比如地址不存在，超时等
        print("read_url_by_POST_with_passwd error.URLError: %s %s %s" % (url, req_param, e.reason))
    except Exception as e:
        print("read_url_by_POST_with_passwd Error: %s %s" % (url, str(e)))

    return result



if __name__ == "__main__":
    print(generate_header("BaseAuth", None))
    print(generate_header("BaseAuth", user="xiiatuuo@foxmail.com", passwd="user_recom"))


