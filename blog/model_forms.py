from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError

from blog.models import UserInfo

widget_username_reg = widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名（不少于2个字符）'})
widget_username_login = widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'})
widget_password = widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码（不少于6个字符）'})
widget_password_login = widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'})
widget_r_password = widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '确认密码'})
widget_email = widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': '邮箱'})
error_messages = {'required': '请输入内容', 'invalid': '请输入正确的邮箱格式'}


class UserFormReg(forms.Form):
    """
    forms组件格式校验：
    注册功能
    """
    username_reg = forms.CharField(error_messages=error_messages, min_length=2, max_length=32, label='&#xe62f;',
                                   widget=widget_username_reg)
    password_reg = forms.CharField(error_messages=error_messages, min_length=6, max_length=32, label='&#xe627;',
                                   widget=widget_password)
    r_password_reg = forms.CharField(error_messages=error_messages, min_length=6, max_length=32, label='&#xe627;',
                                     widget=widget_r_password)
    email_reg = forms.EmailField(error_messages=error_messages, label='&#xe631;', widget=widget_email)

    def clean_username_reg(self):
        """ 检测用户名是否被注册过 """
        val = self.cleaned_data.get('username_reg')
        obj = UserInfo.objects.filter(username=val)
        if not obj:
            return val
        else:
            raise ValidationError('用户名已经被注册！')

    def clean(self):
        """ 检测两次密码输入是否一致 """
        pwd = self.cleaned_data.get('password_reg')
        r_pwd = self.cleaned_data.get('r_password_reg')
        if pwd and r_pwd:
            if pwd == r_pwd:
                return self.cleaned_data
            else:
                raise ValidationError('两次密码输入不一致')
        else:
            return self.cleaned_data


class UserFormLogin(forms.Form):
    """
    forms组件格式校验：
    登录功能
    """
    username_login = forms.CharField(error_messages=error_messages, max_length=32, label='&#xe62f;',
                                     widget=widget_username_login)
    password_login = forms.CharField(error_messages=error_messages, max_length=32, label='&#xe627;',
                                     widget=widget_password_login)
