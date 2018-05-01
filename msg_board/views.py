from django.shortcuts import render, redirect
from django.views import View
from blog.forms import CommentForm
from msg_board.models import MsgBoardModel
from django.urls import reverse


class MsgBoard(View):

    def get(self, request):
        messages = MsgBoardModel.objects.all()
        return render(request,'msgboard.html', {'messages': messages})

    def post(self, request):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data['comment']
            name = comment_form.cleaned_data['name']
            if not name:
                name = '无名氏'
            comment = MsgBoardModel(name=name, text=comment)
            comment.save()
        url = reverse('msgboard:msgboard')
        return redirect(url)
