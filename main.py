#!/usr/bin/env python
# -*- coding: utf-8 -*-

#接口测试
#参考文档：https://www.bstester.com/2015/08/interface-test-automation-scheme-details
####http://blog.csdn.net/iloveyin/article/details/21444613
#仅适用于定义好的case模板
try:
    import xlrd
except:
    os.system('pip install -U xlrd')
    import xlrd
try:
    import xlwt
except:
    os.system('pip install -U xlwt')
    import xlwt

import sys,os
sys.path.append("..\\")
reload(sys)
sys.setdefaultencoding('utf-8')
from public import *
from xlutils.copy import copy
import re
import time
import ConfigParser
import json

import base64
import rsa
pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(b"""-----BEGIN PUBLIC KEY-----               
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC75wr1oiN8lZ+18GngYMzEejUv
wIhqVrs3Ek15igModCkFozENLpWKfkvF9byG3XmFDO2QbV8WVLY/laFKo1yyS9DE
XAoQLgUPwqyTJ9CaBEyLrYG+RkXpp/MYDgp7wO1/Oi+Oa0pRRWVAHco9sUz4RX4q
wdYSa8fjeVt7TckkUQIDAQAB
-----END PUBLIC KEY-----""")

correlationDict = {}

#打开testcase文档，运行完毕，更新关联字典，结果另存为resultfile.xls文档   

def excel_data(casefile,resultfile,host_port):
    
    pass_yes='Y'
    pass_no='N'
    run_yes='Y'
    run_no='N'
    
    try:
        book = xlrd.open_workbook(casefile)
        #,formatting_info=True)
        api_sheet = book.sheet_by_index(0)
        nrows = api_sheet.nrows
        #print (nrows)
        write_book=copy(book)
        write_sheet=write_book.get_sheet(0)
        logger.info('Load casefile succeed!!')
    except Exception as e:
        logger.error(u"打开用例文件出错:%s" % e) 
    
#    try:
    for i in range(0,nrows):
        #根据active一列确定是否执行此用例
        
        if api_sheet.cell(i,16).value !='Y':
            continue
            
        methodd=api_sheet.cell(i,8).value
        request_data_type=api_sheet.cell(i,9).value
        #！！！！！！！！！！！！！！！！！！！！记得要改！！！通用的版本要求把host_port从配置文件读取
        num = api_sheet.cell(i,0).value
        urll=host_port+api_sheet.cell(i,10).value
        #urll=api_sheet.cell(i,10).value
        paralist=api_sheet.cell(i,11).value.replace('\n','').replace('\r','')
        pre_code=api_sheet.cell(i,13).value
        check_point=api_sheet.cell(i,14).value
        correlation = api_sheet.cell(i,15).value.replace('\n','').replace('\r','').split(';')
        
        ###参数化或者关联，总之就是替换关联字段里面存在的key的值
        for key in correlationDict:
            if urll.find(key) > 0:
                request_url = request_url.replace(key,str(correlationDict[key]))
            if paralist.find(key) > 0:
                paralist = paralist.replace(key,str(correlationDict[key]))
        
        
        
        if request_data_type == 'form':
            
            #1.将excel中参数字符串转换成字典 2.字典转换成json 3.josn使用RSA公钥加密 4.加密后使用base64转码 5.构造formdata param=*****
            
            """###paralist='sdg=""'这种情况会报错，也就是参数或者值为空，不能转换成字典 ,待解决…………………… 
            File "main.py", line 68, in excel_data
            dicdata1=eval('dict(%s)' % paralist)
            File "<string>", line 1
            SyntaxError: keyword can't be an expression
            """
            dicdata1=eval('dict(%s)' % paralist)
            
            #print (dicdata1)
            request_data=json.dumps(dicdata1)
            #print (request_data)
            try:
                rsalist = rsa.encrypt(request_data, pubkey)
            except:
                logger.error(u'用例【%s】RSA encrypt error!!!' % num)
                continue
            base64list = base64.b64encode(rsalist)
            request_data={'param':base64list}
            #print (formdata)
            #rr=requests_return(methodd,urll,formdata) 
            
            #print(urll)
            #print(request_data)
            rr=httprequest.requests_return(methodd,urll,request_data)

            
        elif request_data_type == 'data':
            request_data = paralist.encode('utf-8')
            rr=httprequest.requests_return(methodd,urll,request_data)
            # print rr.url
            #print rr.text
            #rr_resopen=rr.getresponse()
            #resp = rr_resopen.read()
            #resp=rr.text
            
        elif request_data_type == 'File':
            dataFile = paralist
            if not os.path.exists(dataFile):
                logger.error(u'用例【%s】请检查[Request Data]字段%s是否存在!' % (num, paralist))
                continue
            fopen = open(dataFile,'rb')
            data = fopen.read()
            fopen.close()
            request_data = '''
------WebKitFormBoundaryDf9uRfwb8uzv1eNe
Content-Disposition:form-data;name="file";filename="%s"
Content-Type:
Content-Transfer-Encoding:binary

%s
------WebKitFormBoundaryDf9uRfwb8uzv1eNe--
    ''' % (os.path.basename(dataFile),data)
        
            rr=httprequest.requests_return(methodd,urll,request_data)
            #print rr.url
            #print rr.text
            #rr_resopen=rr.getresponse()
            #resp = rr_resopen.read()
            #resp=rr.text

       
        if rr in {1,2,3,4}:
            logger.error(str(rr)+u'用例【%s】运行失败，请检查用例文档' % num)
            write_sheet.write(i,17,run_yes)
            write_sheet.write(i,18,pass_no)
            write_sheet.write(i,19,str(rr))
            continue

        #print rr.url
        #resp = rr.text
        #resp = resp.replace('\n','').replace('\r','').replace(' ','')
        try: 
            msg = json.loads(rr)["msg"]
            print (msg)
        except: 
            msg = str(rr)
    
        if rr.status_code==pre_code and re.search(check_point,rr.text):
            
            #处理返回的json，同关联对比，将关联参数添加到参数字典
            #将返回的json处理为字典，json中有相同的key回出问题，也不能使用value(1)的形式匹配--待解决再说吧
            for j in range(len(correlation)):
                param = correlation[j].split('=')
                if len(param) == 2:
                    if param[1] == '' or not re.search(r'^\[',param[1]) or not re.search(r'\]$',param[1]):
                        logger.error(u'用例【%s】关联参数设置有误，请检查[Correlation]字段中%s是否正确！！！' % (num,correlation))
                        continue
                    value = msg
                    #print (value)
                    for key in param[1][1:-1].split(']['):
                        try:
                            temp = value[int(key)]
                        except:
                            try:
                                temp = value[key]
                            except:
                                break
                        value = temp
                    correlationDict[param[0]] = value
                #print (correlationDict)
        
            #将运行结果写入excel
            write_sheet.write(i,17,run_yes)
            write_sheet.write(i,18,pass_yes)
            write_sheet.write(i,19,msg)
        else:
            write_sheet.write(i,17,run_yes)
            write_sheet.write(i,18,pass_no)
            write_sheet.write(i,19,msg)
    
    write_book.save(resultfile)
    logger.info('Creat %s succeed!!!' % os.path.basename(resultfile))
    # except Exception as e:
        # logger.error(u'生成xls测试结果失败:%s' % e)
        # #print (correlationDict)
 
#根据生成结果的resultfile文档，生成并保存XML测试报告，用于后面发送email或者上传

def createxmlreport(resultfile,savefile):
    try:
        book2 = xlrd.open_workbook(resultfile,formatting_info=True)
        xml_sheet = book2.sheet_by_index(0)
        nrows1 = xml_sheet.nrows
    except Exception as e:
        return False, u'读取结果文档错误：%s' % e

    html = '<html><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><body>接口自动化扫描，异常接口用例列表如下：' + '</p><table><tr><th style="width:100px;">用例ID</th><th style="width:50px;">接口地址</th><th style="width:200px;">参数列表</th><th>用例描述</th><th>用例结果</th></tr>'

    try:
        for i in range(0,nrows1):
            if xml_sheet.cell(i,18).value =='N':
                case_id=unicode(xml_sheet.cell(i,0).value)
                request_para=unicode(xml_sheet.cell(i,11).value)
                request_api=unicode(xml_sheet.cell(i,10).value)
                request_src=unicode(xml_sheet.cell(i,12).value)
                request_result=unicode(xml_sheet.cell(i,19).value)
                html=html+'<tr><td>' + case_id+ '</td><td>' + request_api+ '</td><td>'+ request_para+ '</td><td>'  +request_src+ '</td><td>'+request_result+ '</td></tr>'
        html = html + '</table></body></html>' 
        #print(html)

        f = open(savefile,'w')
        message = html

        f.write(message)
        f.close()
        return True, 'Creat %s succeed!!!' % os.path.basename(savefile)
    
    except Exception as e:
        return False, u'生成html报告失败：%s' % e

        
        
        
        
if __name__=="__main__":

    #生成测试结果文档
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    reportfile_log = 'log\\requet_test '+now+'.log'
    reportfile_xls ='result\\testcasereport '+now+'.xls'
    reportfile_html='result\\HTML\\htmlreport '+now+'.html'    

    #执行日志记录 1 ~ 加载配置文件
    global logger
    logger = log.Logger(logfile=reportfile_log, loglevel=0, logger='Loading_Config').getlog()
    try:
        #读取配置文件中的相关参数
        config_file_path='cofig\\main_test.ini'
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        #对字典进行初始化赋值
        env = cf.get("Login", "env")
        un = cf.get("Login", "un")
        pw = cf.get("Login", "pw")
        
        correlationDict['${userToken}'] = get_token.token(env,un,pw)
        #读取相关的用例参数
        case_file = cf.get("testcase", "case_file")
        host_port=cf.get("run_environment","host_port")
        #读取相关的发送邮件参数
        if_sendemail=cf.get("send_email","if_sendemail")
        sender=cf.get("send_email","sender")
        receiver=cf.get("send_email","receiver")
        mailToCc=cf.get("send_email","mailToCc")
        smtpserver=cf.get("send_email","smtpserver")
        username=cf.get("send_email","username")
        password=cf.get("send_email","password")
    except Exception as e:
        logger.error(e)

    #执行日志记录 2 ~用例执行
    logger = log.Logger(logfile=reportfile_log, loglevel=0, logger=os.path.basename(case_file)).getlog()
    #执行接口访问，记录生成结果xls文档
    excel_data(case_file,reportfile_xls,host_port)
    #根据结果xls文档，生成HTML测试报告
    result,msg = createxmlreport(reportfile_xls,reportfile_html)
    if result:
        logger.info(msg)
    else:
        logger.error(msg)
    
    if if_sendemail=='1':
        
        subject = u'接口测试报告'
        msg_text=reportfile_html
        msg_type='file'
        atti_file=reportfile_xls
        resultt,msgg = send_email.sendMail(sender,smtpserver,username,password,subject,receiver,mailToCc,msg_text,msg_type,atti_file)
        if resultt:
            logger.info(msgg)
        else:
            logger.error(msgg)
