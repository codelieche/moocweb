# _*_ coding:utf-8 _*_
from random import Random

from django.core.mail import send_mail

from account.models import EmailVerifyRecord
from moocweb.settings import EMAIL_FROM

def random_str(randomlength=8):
    '''生成随机字符串'''
    s = ''
    chars = 'ABCEFGHIJKLMNOPQRSTUVWXYZabcefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        s += chars[random.randint(0,length)]
    return s

def send_register_email(email, send_type='register'):
    '''发送注册邮件函数'''
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # 先把邮件保存到数据库，然后发送邮件给用户

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "mooc在线注册激活链接"
        email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/" \
                     "active{0}".format(email_record.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
        

