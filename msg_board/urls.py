from django.urls import path
from msg_board import views
from django.conf.urls import url

app_name = 'msgboard'

urlpatterns = [
    path(r'msgboard/', views.MsgBoard.as_view(), name='msgboard'),
]