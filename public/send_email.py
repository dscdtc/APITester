#!/usr/bin/env python3  
#coding: utf-8  
import smtplib  
import os
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.header import Header
import email

##发送邮件方法，邮件形式以HTML展示（效果好，抛弃text的形式）
##msg_text：邮件正文（字符串或者文件路径）
##msg_type：邮件正文的形式 text file
##atti_file：附件，多个附件以,分隔
##receiver mailToCc ：发送，抄送地址，多个地址以,分隔
def sendMail(sender,smtpserver,username,password,subject,receiver,mailToCc,msg_text,msg_type,atti_file):
    
    msg = MIMEMultipart()
    
    if msg_type=='file':
        try:
            f=open(msg_text,'rb')
            msg_text=f.read()
            f.close()
        except Exception as e:
            return False, u"打开文件出错:%s" % e

    elif msg_type=='text':
        msg_text=msg_text
    else:
        return False, u"正文类型不正确，正确的类型有 text ，file"
    
    msg_text = MIMEText(msg_text,_subtype='html',_charset="utf-8")  
    msg.attach(msg_text)
    
    #构造附件
    if atti_file != "":
        for tmp_attachment_file_name in atti_file.split(","):  
            contype = 'application/octet-stream'  
            maintype, subtype = contype.split('/', 1)
            try:
                file_data = open(tmp_attachment_file_name.encode("utf-8"), 'rb')  
                file_msg = email.MIMEBase.MIMEBase(maintype, subtype)  
                file_msg.set_payload(file_data.read())  
                file_data.close( )  
                email.Encoders.encode_base64(file_msg)  
                basename = os.path.basename(tmp_attachment_file_name)  
                file_msg.add_header('Content-Disposition', 'attachment', filename = basename.encode("utf-8"))  
                msg.attach(file_msg) 
            except Exception as e:
                return False, u"添加附件出错:%s" % e

    #sender= ("%s<"+sender+">") % (Header(username,'utf-8'),)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg['Cc'] = mailToCc
    #print(msgRoot['Cc'])
    try:
        smtp = smtplib.SMTP()  
        smtp.connect(smtpserver)  
        smtp.login(username, password) 
        smtp.sendmail(sender,receiver.split(',')+mailToCc.split(','),msg.as_string())
        #smtp.starttls()#加密SMTP会话，实际上就是先创建SSL安全连接，然后再使用SMTP协议发送邮件
        #smtp.set_debuglevel(1)   # 打印出和SMTP服务器交互的所有信息
        return True, ('Email has send out !!')
    except Exception as e:
        return False, "Failed to send email:%s" % e
    finally:
        smtp.quit()
    
if __name__=="__main__":
    
    sender = 'lixinxin.jk0801@163.com'
    receiver = 'lixinxin@icloudcity.cn,907044350@qq.com'
    mailToCc = '924940668@qq.com,907044350@qq.com'
    smtpserver = 'smtp.163.com'  
    username = 'lixinxin.jk0801@163.com'  
    password = '20081626xiaohui'  
    subject = u'接口测试报告'
    msg_text = 'C:\\Users\\admin\\Desktop\\002.html'
    msg_type = 'file'
    #atti_file='C:\\Users\\admin\\Desktop\\1.txt,C:\\Users\\admin\\Desktop\\3.py'
    atti_file=''
    sendMail(sender,smtpserver,username,password,subject,receiver,mailToCc,msg_text,msg_type,atti_file)