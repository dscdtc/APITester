# -*- coding: utf_8 -*-

import requests

#返回1：URL不能为空 返回2：post方法异常，post_data为空 
#返回3：方法名称不匹配 返回4：服务器无回应，检查下host：port
#返回request方法：

def requests_return(method,url,params):
    if url=='':
        #print("URL不能为空")
        return 1
        
    else: 
        try:   
            if method=='GET':
                if params!='':
                    r=requests.get(url,params)
                else:
                    r=requests.get(url)
                #print r.url
                return r
            elif method=='POST':
                if params!='':
                    r=requests.post(url,params)
                    #print r.url
                    return r
                else:
                    #print("post方法异常，post_data为空")
                    return 2
            else:
                #print("方法名称不对？注意区分大小写")
                return 3
        except:
            #print ("服务器无回应，检查下host：port")
            return 4
    
  