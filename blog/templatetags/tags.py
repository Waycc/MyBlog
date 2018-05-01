from ..models import Post, Category, Tag
from django import template
from blog.models import Post
from django.db.models.aggregates import Count
from django.utils.safestring import mark_safe
from blog.utils import return_page_range

register = template.Library()


@register.simple_tag
def recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

# 返回所有同年所有月份的日期
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 分类模板标签
@register.simple_tag
def get_categories():
    # return Category.objects.all()
    # count 接收一个和 Category 相关联的模型参数名（此处是 post，通过外键关联），然后统计 Category 记录的集合中每条记录下与之关联的 Post 记录的行数
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


# 标签云模板标签
@register.simple_tag
def get_tags():
    # return Tag.objects.all()
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def format_time(raw_time):
    formatted_time = raw_time.strftime('%Y{y}%m{m}%d{d} %H:%S').format(y='年', m='月', d='日')
    return formatted_time

@register.simple_tag
def return_page_ele(query_set):
    """
    返回分页标签
    """
    ele = ''
    num_pages = query_set.paginator.num_pages    #总页数
    current_page = query_set.number   # 当前页
    page_range = return_page_range(num_pages,current_page)
    for page in page_range:
        if page == query_set.number:
            ele += '<li class="active" ><span>%s</span></li>' % (page,)
        else:
            ele += '<li><a href="?p=%s">%s</a></li>' % (page,page)
    return mark_safe(ele)
