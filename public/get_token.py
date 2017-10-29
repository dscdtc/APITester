# -*- coding: utf_8 -*-

import json
import httprequest

def token(env,un,pw):
    params = {
    'operate':'csblogin',
    'model.user_account':un,
    'model.user_pwd':pw,
    'model.clientid':'0603013f993',
    'model.mobiletype':'1',
    'model.sessionId':'e2fcb00b-5ab5-4df9-8d34-0e18abe0bbf6'
    }
    resp = httprequest.requests_return('POST',env,params)
    
    if resp in range (5):
        logger.error("Get token failed... \n  server_error")
    else:
        try:
            return json.loads(resp.text)["model.token"]
        except:
            logger.error("Get token failed... \n  login_error")
#'''dump和dumps（从Python生成JSON），load和loads（解析JSON成Python的数据类型）dump和dumps的唯一区别是dump会生成一个类文件对象，dumps会生成字符串，同理load和loads分别解析类文件对象和字符串格式的JSON'''