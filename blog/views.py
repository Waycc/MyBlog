from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from blog.models import Post, Comment
from blog import forms
from blog.utils import query_set
from django.db.models import F, Q
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import re

# Create your views here.


class Index(View):

    def get(self, request):
        cid = request.GET.get('cid', '')
        year = request.GET.get('y', '')
        month = request.GET.get('m', '')
        page = request.GET.get('p', '')
        sk = request.GET.get('sk', '')
        filter_dict = {}
        if cid:
            post = Post.objects.filter(category=cid)
            filter_dict['cid'] = cid
        else:
            post = Post.objects.all()
        if year and month:
            if len(str(year)) >= 5:
                post = []
            else:
                post = post.filter(created_time__month=month, created_time__year=year)
                filter_dict['year'] = year
                filter_dict['month'] = month
        if sk:
            post = post.filter(Q(title__contains=sk) | Q(body__contains=sk))
            for i in post:
                body = i.body
                title = i.title
                pattern = r',?(.*%s.{1,12})'%sk
                body = re.findall(pattern, body)
                title_pattern = r'.*%s.*'%sk
                title = re.findall(title_pattern, title)
                if body:
                    excerpt = body[0].replace(sk,'<span style="color:red">%s</span>'%sk)
                    i.excerpt = excerpt
                if title:
                    new_title = title[0].replace(sk,'<span style="color:red">%s</span>'%sk)
                    i.title = new_title
        post = query_set(post, page, 5)
        return render(request, 'index.html', {
            'post_list': post,
            'filter_dict': filter_dict,
            'post_obj_list': post,
            'sk': sk,
        })

    def post(self, request):
        pass


class Detail(View):
    """
    展示文章细节
    """
    def get(self, request, article_id):
        post = Post.objects.filter(id=article_id).first()
        Post.objects.filter(id=article_id).update(view=F('view')+1)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify)
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return render(request, 'detail.html',{'post': post})

    def post(self, request, article_id):
        """
        以post提交是处理评论的
        """
        post = Post.objects.filter(id=article_id).first()
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            name = form.cleaned_data['name']
            if not name:
                name = '无名氏'
            comment = Comment(name=name, text=comment, post=post)
            comment.save()
        url = reverse('blog:article', kwargs={'article_id': article_id})
        return redirect(url)


class Tag(View):

    def get(self, request,tag_id):
        page = request.GET.get('page')
        post = Post.objects.filter(tags=tag_id)
        post = query_set(post, page, 2)
        return render(request, 'index.html', {'post_list':post, "post_obj_list":post})


class About(View):

    def get(self, request):
        return render(request, 'about.html')




