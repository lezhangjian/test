from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.views import View
from .models import Post, Category
from django.core.paginator import Paginator
from django.db.models import Q, F

# Create your views here.
# def index(request):
# 	category_list = Category.objects.all()  # 查询到所有的分类
# 	post_list = Post.objecs.all()   # 查询到所有的文章
# 	context = {'category_list': category_list, 'post_list': post_list}   # 上下文数据
#     return render(request, 'blog/index.html', context)


class Index(View):
	def get(self, request):
		post_list = Post.objects.all()  # 查询到所有的文章,queryset
		post_list = list(post_list)[::-1]
		# 分页方法
		paginator = Paginator(post_list, 3)  # 第二个参数2代表每页显示几个
		page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
		page_obj = paginator.get_page(page_number)
		# page_obj = list(page_obj)
		context = {'post_list': post_list, 'page_obj': page_obj}
		return render(request, 'blog/index.html', context)


class CategoryList(View):
	def get(self, request, category_id):
		# category = get_object_or_404(Category, id=category_id)
		# # 获取当前分类下的所有文章
		# posts = category.post_set.all()
		# context = {'category': category, 'post_list': posts}
		# return render(request, 'blog/list.html', context)

		category = get_object_or_404(Category, id=category_id)
		# 获取当前分类下的所有文章
		posts = category.post_set.all()
		paginator = Paginator(posts, 2)  # 第二个参数2代表每页显示几个
		page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
		page_obj = paginator.get_page(page_number)
		context = {'category': category, 'page_obj': page_obj}
		return render(request, 'blog/list.html', context)


class PostDetail(View):
	def get(self, request, post_id):
		# 文章详情页
		post = get_object_or_404(Post, id=post_id)
		date_prev_post = Post.objects.filter(add_date__lt=post.add_date).last()
		date_next_post = Post.objects.filter(add_date__gt=post.add_date).first()
		context = {'post': post, 'prev_post': date_prev_post, 'next_post': date_next_post}
		return render(request, 'blog/detail.html', context)


class Archives(View):
	def get(self, request, year, month):
		post_list = Post.objects.filter(add_date__year=year, add_date__month=month)
		context = {'post_list': post_list, 'year': year, 'month': month}
		return render(request, 'blog/archives_list.html', context)


class Search(View):
	""" 搜索视图 """
	def get(self, request):
		keyword = request.GET.get('keyword')
		# 没有搜索默认显示所有文章
		if not keyword:
			post_list = Post.objects.all()
		else:
			# 包含查询的方法，用Q对象来组合复杂查询，title__icontains 他两个之间用的是双下划线（__）链接
			post_list = Post.objects.filter(
				Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword))
		paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
		page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
		page_obj = paginator.get_page(page_number)
		context = {
			'page_obj': page_obj
		}
		return render(request, 'blog/index.html', context)





