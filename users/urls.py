from django.urls import path
from .views import UsersLogin, UsersRegister, ActiveUser, ForgetPassword, ForGetUrl, UsersProfile, LogoutView, EditorUsers

app_name = 'users'   # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [
    path('login', UsersLogin.as_view(), name='login'),
    path('register', UsersRegister.as_view(), name='register'),
    path('active/<active_code>', ActiveUser.as_view(), name='active_pwd_url'),
    path('forget', ForgetPassword.as_view(), name='forget_pwd_url'),
    # active_code这样可拿到前端直接传过来的值
    path('forget_pwd_url/<active_code>', ForGetUrl.as_view(), name='forget_pwd_url'),
    path('user_profile', UsersProfile.as_view(), name='user_profile'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('editer_user', EditorUsers.as_view(), name='editer_user'),
]