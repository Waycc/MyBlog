from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    """
    分类，每篇文章都有一个对应的分类
    """
    # 分类名字段
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    '''
    标签表，每篇文章都有多个对应的标签
    '''

    # 标签名字段
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章表
    """
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField()

    # 文章摘要字段
    excerpt = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    view = models.PositiveIntegerField(default=0)

    class Meta:
        # 默认倒序排序
        ordering = ['-created_time']


class Comment(models.Model):
    """
    评论数据表，用于存放名称，评论内容，评论时间及对应的文章
    """
    name = models.CharField(max_length=100)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)  # 把 created_time 指定为当前时间

    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.text[:20]