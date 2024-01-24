from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.encrypt import md5
from django import forms
from app01.utils.bootstrap import BootstrapModelForm


def admin_list(request):
    """ Administrator list """

    ## check if the user has already logged in
    ## if logged in, to the admin list, if not, redirect to the login page

    # info_dict = request.session["info"]
    # print(info_dict)
    # print(info_dict["id"])
    # print(info_dict["username"])

    data_dict = {}
    search_data = request.GET.get("q", "")  ## 这个空字符串表示，有的话就用q, 没有的话就要用空字符串
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.Admin.objects.filter(**data_dict)

    page_object = Pagination(request, queryset)
    context = {
        "queryset": queryset,
        "page_string": page_object.html(),
        "search_data": search_data,
    }
    return render(request, "admin_list.html", context)






class AdminModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data["password"]
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise forms.ValidationError("Inconsistent password")
        return confirm


def admin_add(request):
    """ Administrator add"""
    title = "Add an administrator"

    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"title": title, "form": form})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")

    return render(request, "change.html", {"title": title, "form": form})



class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


def admin_edit(request, nid):
    """ Administrator Edit """

    ## object / None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        # return render(request, "error.html", {"msg": "Data doesn't exist"})
        return redirect("/admin/list")

    title = "Edit Administrator"

    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, "change.html", {"form": form,
                                               "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")

    return render(request, "change.html", {"form": form,
                                           "title": title})


def admin_delete(request, nid):
    """ Administrator Delete """

    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list")


class AdminResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        ## password cannot be the same as the previous one
        exist = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exist:
            raise ValidationError("Password cannot be the same as the previous one")

        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise forms.ValidationError("Inconsistent password")
        return confirm


def admin_reset(request, nid):
    """ Reset Password"""

    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        # return render(request, "error.html", {"msg": "Data doesn't exist"})
        return redirect("/admin/list/")

    title = "Reset Password - {}".format(row_object.username)

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"title": title, "form": form})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")

    return render(request, "change.html", {"title": title, "form": form})
