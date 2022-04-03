from django import forms
from django.contrib.auth.models import User    # 注册只需要修改django提供的已有的字段就行
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'
    }))
    # widget = forms.PasswordInput() 密码输入，需要保密处理

    def clean_password(self):
        """清理前端输入的数据"""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username == password:
            raise forms.ValidationError('密码不能与用户名一样！')
        return password


class RegisterForm(forms.ModelForm):
    # username = forms.CharField(label='用户名', max_length=32, widget=forms.TextInput(attrs={
    #     'class': 'input', 'placeholder': '用户名/邮箱'
    # }))
    email = forms.EmailField(label='邮箱', min_length=3, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '邮箱'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'}))
    password1 = forms.CharField(label='再次密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '再次密码'}))

    class Meta:
        model = User
        # 使用django提供的字段
        # fields = ('username', 'password')
        fields = ('email', 'password')

    def clean_email(self):
        # 对前端传来的email字段进行筛选
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError("邮箱已经存在！")
        return email

    def clean_password1(self):
        # 对前端传来的password1字段进行筛选
        data = self.cleaned_data
        password = data['password']
        password1 = data['password1']
        if password != password1:
            raise forms.ValidationError('两次输入的密码不一致，请修改!')
        return password


class ForgetPwdForm(forms.Form):
    """ 填写邮箱地址表单 """
    email = forms.EmailField(label='请输入注册邮箱地址', min_length=4, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))


class ModifyPwdForm(forms.Form):
    """修改密码"""
    password = forms.CharField(label='输入新密码', min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'input',
                                                                 'placeholder': '输入新密码'}))


class UserForm(forms.ModelForm):
    """ User模型的表单，只允许修改email一个数据，用户名不允许修改 """
    class Meta:
        model = User
        fields = ('email',)


class UserProfileForm(forms.ModelForm):
    """ UserProfile的表单 """
    class Meta:
        """Meta definition for UserInfoform."""
        model = UserProfile
        fields = ('nike_name','desc', 'gexing', 'birthday',  'gender', 'address', 'image')







