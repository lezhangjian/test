from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    USER_GENDER_TYPE = (
        ('male', '男'),
        ('female', '女'),
    )
    desc = models.TextField('个人简介', max_length=200, blank=True, default='')
    gexing = models.CharField('个性签名', max_length=100, blank=True, default='')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')     # 一对一字段
    nike_name = models.CharField('昵称', max_length=50, blank=True, default='')
    birthday = models.DateField('生日', null=True, blank=True)                            # 时间字段
    gender = models.CharField('性别', max_length=6, choices=USER_GENDER_TYPE, default='male')  # 选择框，默认男性
    address = models.CharField('地址', max_length=100, blank=True, default='')
    image = models.ImageField(upload_to='images/%Y/%m', default='images/default.png', max_length=100,
                              verbose_name='用户头像')
    """
    图片字段，字段必须定义`upload_to`选项， 这个选项用来指定用于上传文件的`MEDIA_ROOT`的子目录
    例如我们在最开始配置settings.py的时候配置了`MEDIA_ROOT = os.path.join(BASE_DIR, 'media')`，那么我们这里设置了`upload_to='images/%Y/%m'`, `upload_to`的`'%Y /%m /%d'`部分是`strftime()`格式; '%Y'是四位数年份，`%m`是两位数月份，`%d`是两位数日期。 如果您在2020年1月15日上传文件，它将保存在目录`/media/images/2020/01`中
    """
    class Meta:
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username


class EmailVerifyRecord(models.Model):
    """邮箱验证记录"""
    SEND_TYPE_CHOICES = (
        ('register', '注册'),
        ('forget', '找回密码'),
    )

    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, max_length=10, default='register')
    send_time = models.DateTimeField('时间', auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code










