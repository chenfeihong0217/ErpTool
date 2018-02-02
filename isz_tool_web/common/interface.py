# -*- coding:utf8 -*-

import collections
from common.base import *
import requests
import json
from common.base import consoleLog
import re



def myRequest(interfaceURL ,data=None, needCookie=True, contentType='application/json', method='post',Value=False):
    """
    接口请求方法
    :param url:
    :param data:
    :param needCookie:
    :param contentType:
    :param method:
    :param returnValue:
    :return:
    """
    headers = {
        'content-type' : contentType,
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    cookie = eval(get_conf('cookieInfo', 'cookies'))

    if method == 'get':
        if needCookie:
            try:
                request = requests.get(interfaceURL, headers=headers,cookies=cookie)
            except BaseException as e:
                return e
        else:
            try:
                request = requests.get(interfaceURL, headers=headers)
            except BaseException as e:
                return  e

    if method == 'post':
        if needCookie:
            try:
                request = requests.post(interfaceURL, data=json.dumps(eval(data)), headers=headers, cookies=cookie)
            except BaseException as e:
                return e
        else:
            try:
                request = requests.post(interfaceURL, data=json.dumps(eval(data)), headers=headers)
            except BaseException as e:
                return e

    if method == 'put':
        if needCookie:
            try:
                request = requests.put(interfaceURL, data=json.dumps(eval(data)), headers=headers, cookies=cookie)
            except BaseException as e:
                return e
        else:
            try:
                request = requests.put(interfaceURL, data=json.dumps(eval(data)), headers=headers)
            except BaseException as e:
                return e

    result = json.loads(request.text)
    if Value:
        return result
    elif request.status_code is not 200 or result['code'] is -1:
        msg = result['msg'].encode('utf-8')
        return ((u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s') % (interfaceURL, data, msg.decode('utf-8')))
    else:
        return result["code"]



def get_cookie():
    user, pwd = get_conf('loginUser', 'user'), get_conf('loginUser', 'pwd')
    "get_cookie"
    needClient = None
    # 默认登录不使用客户端，如果报错，则赋值给needClient为True，然后调用客户端的登录接口进行校验
    url = 'http://isz.ishangzu.com/isz_base/LoginController/login.action'
    data = {
        'user_phone': user, 'user_pwd': pwd, 'auth_code': '', 'LechuuPlatform': 'LECHUU_CUSTOMER',
        'version': '1.0.0'
    }
    headers = {
        'content-type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    result = json.loads(response.text)
    if result['msg'] == '登录成功' or result['msg'] == u'非生产环境,不做校验！':
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        set_conf('cookieInfo', cookies=str(cookies))
        return result['msg']
    elif u'密码错误' in result['msg']:
        return  result['msg']
    elif "账号不存在" in result['msg']:
        return result['msg']
    else:
        needClient = True
    if needClient:
        from common.getAuthKey import getAuthKey
        auth_key = getAuthKey()
        # 检查授权
        url = 'isz_base/LoginAuthController/checkLoginAuth.action'
        data ={'auth_key': auth_key}
        result = myRequest(url, data, needCookie=False)
        if u'授权成功' in result['msg']:
            auth_code = result['obj']['authList'][0]['auth_code']
            authTag = result['obj']['authTag']
        else:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            raise u'客户端登录第一步：检查授权失败'

        # 检查用户名密码
        url = 'isz_base/LoginController/checkUserPassWord.action'
        data = {
            'auth_code': auth_key,
            'authTag': authTag,
            'user_phone': user, 'user_pwd': pwd
        }
        result = myRequest(url, data, needCookie=False)
        if u'用户名密码正确' not in result['msg']:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            raise u'客户端登录第二步：检查用户名密码失败'

        # 获取短信验证码
        url = 'isz_base/LoginController/getVerificationCode.action'
        data = {
            'authTag': authTag,
            'mobile': user
        }
        result = myRequest(url, data, needCookie=False)
        if result['msg'] != 'ok' and u'验证码发送过于频繁' not in result['msg']:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            raise u'客户端登录第三步：获取短信验证码失败'

        # 验证码登录
        url = 'isz_base/LoginController/checkVerificationCode.action'
        data = {
            'auth_code': auth_key,
            'authTag': authTag,
            'user_phone': user,
            'user_pwd': pwd,
            'verificationCode': '0451'
        }
        # 判断是否是开发部，然后决定验证码是默认的0451还是从数据库查最新收到的
        if myRequest(url, data, needCookie=False):
            sql = "select * from sys_department_flat where dept_id=(SELECT dep_id from sys_department where dep_name = '技术开发中心') and child_id=(" \
                  "SELECT dep_id from sys_user where user_phone = '%s' and user_status = 'INCUMBENCY')" % user
            if get_count(sql) == 0:
                content = searchSQL("SELECT content from sms_mt_his where destPhone = '%s' ORDER BY create_time desc limit 1" % user)[0]
                sms_code = re.findall('验证码：(.*?)，', content.encode('utf-8'))[0]
                data['verificationCode'] = sms_code
        headers = {
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
        }
        url = 'http://isz.ishangzu.com/isz_base/LoginController/checkVerificationCode.action'
        response = requests.post(url, data=json.dumps(data), headers=headers)
        result = json.loads(response.text)
        if result['msg'] == 'ok':
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
            print (cookies)
            set_conf('cookieInfo', cookies=cookies)
        else:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            raise u'客户端登录第四步：验证码登录失败'








