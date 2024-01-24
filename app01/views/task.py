from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from app01 import models
from app01.utils.bootstrap import BootstrapModelForm
from django import forms
from app01.utils.pagination import Pagination


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'
        widgets = {
            "detail": forms.TextInput
        }


def task_list(request):
    """ task list """

    # get all data from database
    queryset = models.Task.objects.all().order_by('-id')

    page_obj = Pagination(request, queryset)


    form = TaskModelForm()
    context = {
        "form": form,
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html(),
    }
    return render(request, "task_list.html", context)



@csrf_exempt
def task_ajax(request):
    print("get:", request.GET)
    print("post:", request.POST)

    data_dict = {"status": True, "data": [11,22,33,44]}
    json_str = json.dumps(data_dict)
    return HttpResponse(json_str)


@csrf_exempt
def task_add(request):
    print("Post:", request.POST)


    ## 1. Verify the data we received(By using ModelForm)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))