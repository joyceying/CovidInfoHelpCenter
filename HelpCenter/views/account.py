from django.shortcuts import render, HttpResponse, redirect
from django import forms
from io import BytesIO

from HelpCenter.utils.code import check_code
from HelpCenter import models
from HelpCenter.utils.bootstrap import BootStrapForm
from HelpCenter.utils.encrypt import md5


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="username",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="code",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "code error")
            return render(request, 'login.html', {'form': form})

        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "username or password error")
            # form.add_error("username", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}

        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/index/")

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """


    img, code_string = check_code()

    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销 """

    request.session.clear()

    return redirect('/login/')
