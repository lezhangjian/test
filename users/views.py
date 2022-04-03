from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from .models import EmailVerifyRecord
from .utils.email_send import send_register_email
from django.contrib.auth.hashers import make_password      # 给密码加密
from .models import UserProfile  # 引入用户模型字段
from django.contrib.auth.decorators import login_required   # 保持登录
from django.contrib.auth import logout                      # 用户退出
from .forms import UserForm, UserProfileForm
# Create your views here.
"""
# django发送邮件需要这两个模块django.db.models import Q    auth.backends import ModelBackend
ModelBackend是Django使用的默认身份验证后端，我们将重写这个类让他支持验证邮箱，它实现了两个必要的方法：
    get_user(user_id) 和 authenticate(request, **credentials
"""
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class MyBackend(ModelBackend):
    """使用邮箱登录注册"""
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):  # 加密明文密码
                return user
        except Exception as e:
            return None


#用户登录
class UsersLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        # username = request.POST['username']  # request.POST[]或request.POST.get()获取数据
        # password = request.POST['password']
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username, password)
            """
             # 与数据库中的用户名和密码比对，django默认保存密码是以哈希形式存储，并不是明文密码，
             这里的password验证默认调用的是User类的check_password方法，以哈希值比较。
            """
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # login方法登录
                login(request, user)
                # 返回登录成功信息
                return HttpResponseRedirect('user_profile')
            else:
                # 返回登录失败信息
                return HttpResponse('登陆失败')


#用户注册
class UsersRegister(View):
    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'users/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            # 让username等于邮箱即可
            new_user.email = form.cleaned_data.get('email')
            new_user.username = form.cleaned_data.get('email')
            try:
                send_register_email(form.cleaned_data.get('email'), 'register')
            except:
                return HttpResponse('邮箱错误！')
            # return HttpResponse('发送邮件')
            new_user.save()
            # 将账户保存到数据库，但是此时账户没有后台的登录权限，需要通过邮箱激活
            return HttpResponseRedirect('login')
        context = {'form': form}
        return render(request, 'users/register.html', context)


# 上面注册的的账户已经在数据库里了，但是不能登录后台，需要激活
class ActiveUser(View):
    # 上面注册的的账户已经在数据库里了，但是不能登录后台，需要激活
    def get(self, request, active_code):
        # active_code这样可拿到前端直接传过来的值
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            email = all_records[0].email
            user = User.objects.get(email=email)
            user.is_staff = True      # 将账户激活起来
            user.save()
            return HttpResponseRedirect('/users/login')
        else:
            return HttpResponse('链接有误！')


class ForgetPassword(View):
    # 点击忘记密码，返回输入邮箱链接
    def get(self, request):
        form = ForgetPwdForm()
        return render(request, 'users/forget_pwd.html', {'form': form})

    def post(self, request):
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            exists = User.objects.filter(email=email).exists()
            if exists:
                # 发送邮件
                send_register_email(email, 'forget')
                return HttpResponse('邮件已经发送请查收！')
            else:
                return HttpResponse('邮箱还未注册，请前往注册！')


class ForGetUrl(View):
    def get(self, request, active_code):
        form = ModifyPwdForm()
        return render(request, 'users/reset_pwd.html', {'form': form})

    def post(self, request, active_code):
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVerifyRecord.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)
            user.username = email
            user.password = make_password(form.cleaned_data.get('password'))   # 对密码进行加密
            user.save()
            return HttpResponse('修改成功')
        else:
            return HttpResponse('修改失败')


class UsersProfile(View):
    # @login_required(login_url='users:login')
    def get(self, request):
        try:
            # 如果用户已经登录了， 会有返回值，且不会报错
            User.objects.get(username=request.user)
            user = User.objects.get(username=request.user)
            return render(request, 'users/user_profile.html', {'user': user})
        except:
            # 用户没有登录，上面的程序报错了，返回登录界面
            return HttpResponseRedirect('/users/login')


class LogoutView(View):
    # 用户退出
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/users/login')


class EditorUsers(View):
    def get(self, request):
        try:
            # 如果用户已经登录了，User.objects.get(username=request.user) 会有返回值，且不会报错
            user = User.objects.get(username=request.user)

        except:
            # 用户没有登录，上面的程序报错了，返回登录界面
            return HttpResponseRedirect('/users/login')

        try:
            userprofile = user.userprofile
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(instance=userprofile)
            # user_profile_form = UserProfileForm()
        except UserProfile.DoesNotExist:  # 这里发生错误说明userprofile无数据
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm()
        return render(request, 'users/editor_users.html', locals())

    def post(self, request):
        try:
            # 如果用户已经登录了，User.objects.get(username=request.user) 会有返回值，且不会报错
            user = User.objects.get(username=request.user)

        except:
            # 用户没有登录，上面的程序报错了，返回登录界面
            return HttpResponseRedirect('/users/login')
        try:
            userprofile = user.userprofile
            form = UserForm(request.POST, instance=user)
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)  # 向表单填充默认数据
            # user_profile_form = UserProfileForm(request.POST, request.FILES)  # 向表单填充默认数据
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                # return redirect('users:user_profile')
                return HttpResponseRedirect('/users/user_profile')
        except UserProfile.DoesNotExist:  # 这里发生错误说明userprofile无数据
            form = UserForm(request.POST, instance=user)  # 填充默认数据 当前用户
            user_profile_form = UserProfileForm(request.POST, request.FILES)  # 空表单，直接获取空表单的数据保存
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值天剑进去，提交保存新的数据
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()
                return HttpResponseRedirect('/users/user_profile')









