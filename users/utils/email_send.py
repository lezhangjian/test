from users.models import EmailVerifyRecord
from django.core.mail import send_mail
import random
import string

"""
EmailVerifyRecord是我们创建邮箱验证记录的类。

send_mail是django默认为我们封装的邮件发送方法，这个封装方法可以加快邮件的发送，也可以在开发时测试发送邮件，在不支持 SMTP 的平台上支持发送邮件。
# 这是send_mail方法的一些参数
send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None):
random是python提供的模块，生成随机字符串

string是python提供的字符串模块，这里用来生成字符串
"""


def random_str(randomlength=8):
    # 生成a-z,A-Z,0-9左右的字符
    chars = string.ascii_letters + string.digits
    # 从a-zA-Z0-9生成指定数量的随机字符
    strcode = ''.join(random.sample(chars, randomlength))
    return strcode


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str()
    email_record.code = code
    email_record.email = email
    print('>>>>>>>>>>>', email)
    email_record.send_type = send_type
    email_record.save()

    # 验证码保存之后，我们就要把带有验证码的链接发送到注册时的邮箱！
    if send_type == 'register':
        email_title = '博客的注册激活链接'
        email_body = '请点击下面链接激活你的账号：http://upclzj.work:8080/users/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, '1079011291@qq.com', [email])
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = '博客密码重置链接'
        email_body = '请点击以下链接修改密码：http://upclzj.work:8080/users/forget_pwd_url/{0}'.format(code)

        send_status = send_mail(email_title, email_body, '1079011291@qq.com', [email])
        if send_status:
            pass