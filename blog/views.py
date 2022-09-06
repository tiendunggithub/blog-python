from django.shortcuts import render, get_object_or_404
from .models import Blog
from django.views.generic import(
    ListView
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.http import JsonResponse, HttpResponse
import csv
from taggit.models import Tag
from django.db.models import Count
import random

def all_blogs(request, tag_slug=None):
    blogs_list = Blog.objects.filter(status=1)
    #pagination
    paginator = Paginator(blogs_list, 6)
    pageNumber = request.GET.get('page') 
    blogs = paginator.get_page(pageNumber)
    nums = "a" * blogs.paginator.num_pages
    #tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        blogs = blogs_list.filter(tags__in = [tag])
        paginator = Paginator(blogs, 6)
        page = request.GET.get('page') 
        blogs = paginator.get_page(pageNumber)
        nums = "a" * blogs.paginator.num_pages

    return render(request, 'blog/all_blogs.html', {'blogs':blogs, 'nums':nums, 'tag':tag})

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    #also like
    all_blog = list(Blog.objects.exclude(id=blog_id))
    like_blog =random.sample(all_blog, 3)

    #similar
    blog_tag_id = Blog.tags.values_list('id', flat=True)
    similar_blog = Blog.objects.filter(tags__in = blog_tag_id, status=1).exclude(id = blog.id)
    similar_blog = similar_blog.annotate(same_tags=Count('tags')).order_by('-same_tags')[:3]

    return render(request, 'blog/detail.html', {'blog':blog,'like_blog': like_blog, 'similar_blog': similar_blog})

# def best_blogs(request):
#     best_blogs = Blog.objects.filter(is_best=True)
#     paginator = Paginator(best_blogs, 1)
#     pageNumber = request.GET.get('page') 
#     try:
#         blogs = paginator.page(pageNumber)
#     except PageNotAnInteger:
#         # Nếu page_number không thuộc kiểu integer, trả về page đầu tiên
#         blogs = paginator.page(1)
#     except EmptyPage:
#         # Nếu page không có item nào, trả về page cuối cùng
#         blogs = "a" * paginator.page(paginator.num_pages) 
#     return render(request, 'blog/best_blogs.html',{'blogs': blogs})

def best_blogs(request):
    best_blogs = Blog.objects.filter(is_best=True)
    paginator = Paginator(best_blogs, 3)
    pageNumber = request.GET.get('page') 
    blogs = paginator.get_page(pageNumber)
    nums = "a" * blogs.paginator.num_pages
    return render(request, 'blog/best_blogs.html',{'blogs': blogs, 'nums': nums})
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = Blog.objects.filter(title__contains = searched)
        return render(request, 'blog/search.html',{'searched': searched, 'blogs': blogs})
    else:
        return render(request, 'blog/search.html',{})

#xuất file csv
def blog_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; encoding=utf-8; filename = blog.csv'
    #create csv write
    writer = csv.writer(response)

    blogs = Blog.objects.all()
    #add column csv
    writer.writerow(['Title', 'Image', 'Slug', 'Author', 'Create_On', 'Is_Best', 'Description', 'Status'])
    for blog in blogs:
        writer.writerow([blog.title, blog.image, blog.slug, blog.author, blog.created_on, blog.is_best, blog.description, blog.status])
    
    return response


# def load_more(request):
#     blogs=Blog.objects.all()
#     blogs_json=serializers.serialize('blog',blogs)
#     return JsonResponse(
#         {'blogs':blogs_json
#     })