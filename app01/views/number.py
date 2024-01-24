from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm, NumModelForm, NumEditModelForm


def num_list(request):





    page = int(request.GET.get('page', '1'))
    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size

    ## 搜索功能 Search Function
    data_dict = {}
    value = request.GET.get("q", "")  ## 这个空字符串表示，有的话就用q, 没有的话就要用空字符串
    if value:
        data_dict["mobile__contains"] = value

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")
    page_object = Pagination(request, queryset, page_size = 20)
    page_queryset = page_object.page_queryset    ## 每个分页



    ## 分页功能
    # total_count = models.PrettyNum.objects.filter(**data_dict).count()
    # total_page = (total_count // page_size) + 1
    page_string = page_object.html()

    return render(request, "num_list.html",
                  {"nums":page_queryset, "value":value, "page_string": page_string})


def num_add(request):
    if request.method == "GET":
        form = NumModelForm()
        return render(request, "num_add.html", {"form":form})

    form = NumModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/num/list")
    return render(request, "num_add.html", {"form": form})


def num_edit(request, nid):
    row_data = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = NumEditModelForm(instance=row_data) ## 填入之前默认的数据
        return render(request, "num_edit.html", {"form": form})

    form = NumEditModelForm(data=request.POST, instance=row_data)
    if form.is_valid():
        form.save()
        return redirect("/num/list")
    return render(request, "num_edit.html", {"form": form})


def num_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/num/list")