from django import forms
import re


class CommentForm(forms.Form):
    name = forms.CharField(max_length=30, required=False, error_messages={
        'max_length': '你的名字太长了哦',
    })
    comment = forms.CharField(widget=forms.Textarea,error_messages={
        'required': '亲，请输入内容',
    })

    def clean_name(self):
        name = self.cleaned_data['name']
        name = self.check_script(name)
        return name

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        comment = self.check_script(comment)
        return comment

    # 用来替换表单中的script标签
    def check_script(self, val):
        script = re.compile(r'<script>')
        if script.findall(val):
            val = script.sub('&ltscript&gt',val)
            val = re.sub(r'</script>', '&lt/script&gt', val)
        return val