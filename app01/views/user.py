from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, NumModelForm, NumEditModelForm


def user_list(request):

    queryset = models.UserInfo.objects.all()
    # for item in data_list:
    #     print(item.id, item.name, item.age, item.account, item.create_time.strftime("%Y-%m-%d"),
    #           item.gender, item.get_gender_display(), item.depart.title)
        ##如果在model里面有 tuple套tuple的格式对应，django会直接写出结果
    page_object = Pagination(request, queryset, page_size=10)

    context = {'queryset': page_object.page_queryset,
               "page_string": page_object.html()}

    return render(request, "user_list.html", context)



############# ModelForm 示例 #############

def user_model_form_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    ## 用户的数据进行校验

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")

    return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    row_data = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        ## 根据id去数据库获取第一行数据
        form = UserModelForm(instance=row_data)  ## 填入之前默认的数据
        return render(request, "user_edit.html", {"form":form})

    form = UserModelForm(data=request.POST, instance=row_data)
    if form.is_valid():
        form.save()
        return redirect("/user/list")
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list")