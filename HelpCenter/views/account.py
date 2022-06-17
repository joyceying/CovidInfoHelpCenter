from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from io import BytesIO

from django.core.exceptions import ValidationError

from HelpCenter.utils.code import check_code
from HelpCenter import models
from HelpCenter.utils.bootstrap import BootStrapForm
from HelpCenter.utils.encrypt import md5

from HelpCenter.utils.bootstrap import BootStrapModelForm
from HelpCenter.utils.encrypt import md5


class LoginForm(BootStrapForm):
    name = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="验证码",
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
        # 验证成功，获取到的用户名和密码
        # {'username': 'wupeiqi', 'password': '123',"code":123}
        # {'username': 'wupeiqi', 'password': '5e5c3bad7eb35cba3638e145c830c35f',"code":xxx}

        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        # admin_object = models.Admin.objects.filter(username=xxx, password=xxx).first()
        user_object = models.User.objects.filter(**form.cleaned_data).first()
        if not user_object:
            form.add_error("password", "用户名或密码错误")
            # form.add_error("username", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': user_object.id, 'name': user_object.name}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/index/")

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())



class UserModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="confirm password",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.User
        fields = ["name", 'password', "confirm_password","Email","DOB","age"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("the password it not same")
        # 返回什么，此字段以后保存到数据库就是什么。
        return confirm

def registe(request):
    """注册新用户"""
    title = "please registe below"
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'change.html', {'form': form, "title": title})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/login/')

    return render(request, 'change.html', {'form': form, "title": title})


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect('/home/')





