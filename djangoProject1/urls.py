"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import depart, user, number, admin, account, task, order
from django.shortcuts import redirect

urlpatterns = [

    # Department
    # path("admin/", admin.site.urls),
    path("depart/list/", depart.depart_list),
    path("depart/add/", depart.depart_add),
    path("depart/delete/", depart.depart_delete),
    path("depart/<int:nid>/edit/", depart.depart_edit),

    # User
    path("user/list/", user.user_list),
    path("user/model/form/add/", user.user_model_form_add),
    path("user/<int:nid>/edit/", user.user_edit),
    path("user/<int:nid>/delete/", user.user_delete),

    # Number
    path("num/list/", number.num_list),
    path("num/add/", number.num_add),
    path("num/<int:nid>/edit/", number.num_edit),
    path("num/<int:nid>/delete/", number.num_delete),

    # Admin
    path("admin/list/", admin.admin_list),
    path("admin/add/", admin.admin_add),
    path("admin/<int:nid>/edit/", admin.admin_edit),
    path("admin/<int:nid>/delete/", admin.admin_delete),
    path("admin/<int:nid>/reset/", admin.admin_reset),

    # Login
    path("login/", account.login),
    path("logout/", account.logout),
    path("image/code/", account.image_code),

    # Task
    path("task/list/", task.task_list),
    path("task/ajax/", task.task_ajax),
    path("task/add/", task.task_add),

    path('', lambda request: redirect('/login/'), name='root_redirect'),

    ## Order
    path("order/list/", order.order_list),
]
