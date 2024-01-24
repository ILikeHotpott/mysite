from io import BytesIO
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from app01.utils.bootstrap import BootstrapForm
from app01.utils.encrypt import md5
from app01 import models
from app01.utils.code import check_code



class LoginForm(BootstrapForm):
    username = forms.CharField(
        label="username",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}, render_value=True),
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

    if request.session.get("info"):
        return redirect("/admin/list")

    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})


    form = LoginForm(data=request.POST)
    if form.is_valid():
        ## verification successful, get user's username and password
        # {'username': 'liuyitong1210', 'password': '5ade17bc8f36b021bc6749fc47c4d3e7'}

        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("image_code", "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "Incorrect code")
            return render(request, "login.html", {"form": form})


        # go to database and verify it
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()

        # if the input is incorrect
        if not admin_object:
            form.add_error("password", "Incorrect username or password")
            return render(request, "login.html", {"form": form})

        ## if the input is correct
        ## generate random string, write into the cookie and session
        request.session["info"] = {"id": admin_object.id, "username": admin_object.username}

        ## session can save the info for 7 days
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/admin/list")

    return render(request, "login.html", {"form": form})

def image_code(request):

    img, code_string = check_code()

    ## write the code to session
    request.session["image_code"] = code_string
    print(request.session)
    ## the code would expire in 60 seconds
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, "PNG")
    stream.getvalue()

    return HttpResponse(stream.getvalue(), content_type="image/png")



def logout(request):
    """ logout """
    request.session.clear()

    return redirect("/login/")
