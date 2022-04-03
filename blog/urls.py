from django.urls import path
from .views import Index, CategoryList, PostDetail, Search, Archives

app_name = 'blog'   # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('category_list/<int:category_id>/', CategoryList.as_view(), name='category_list'),
    path('post/<int:post_id>/', PostDetail.as_view(), name='post_detail'),
    path('search/', Search.as_view(), name='search'),
    path('archives/<int:year>/<int:month>/', Archives.as_view(), name='archives'),

]