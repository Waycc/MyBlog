from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator


def query_set(obj_list, page, per_page_num=10):
    """
    返回分页后的对象，用于分页
    """
    paginator = Paginator(obj_list, per_page_num)
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        query_sets = paginator.page(1)
    except EmptyPage:
        query_sets = paginator.page(paginator.num_pages)
    return query_sets


def return_page_range(num_pages, current_page):
    """
    根据页面总页数和当前页码返回需要显示的页码范围，一共显示9个页码，保持当前
    页码处于中间位置
    """
    if current_page < 5 :  # 当前页码小于5时分两种情况，一种是总页码大于10，一种在10以内
        if num_pages<10:
            page_range = range(1,num_pages+1)  # 总页码小于10时，只需要显示1 到总页码数即可
        else:
            page_range = range(1, 10)
    else:
        if current_page > num_pages-5: # 这个代表当前页码与总页码距离小于4了
            if num_pages-8 <= 0:  # 这个代表总页码小于8，无法使当前页码保持在中间位置，不然最后页码值将会超出总页码值
                page_range = range(1,num_pages+1)
            else:
                page_range = range(num_pages-8, num_pages+1)
        else:
            page_range = range(current_page-4, current_page+5)
    return page_range