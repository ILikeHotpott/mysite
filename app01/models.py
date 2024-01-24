from django.db import models

# Create your models here.

class Admin(models.Model):
    """  Administrator model. """

    username = models.CharField(verbose_name="username", max_length=32)
    password = models.CharField(verbose_name="password", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    # 部门表
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    # 员工表
    name = models.CharField(verbose_name="Name", max_length=16)
    password = models.CharField(verbose_name="Password", max_length=32)
    age = models.IntegerField(verbose_name="Age")
    account = models.DecimalField(verbose_name="Account", max_digits=10, decimal_places=2, default=0)

    create_time = models.DateField(verbose_name="Entry Time")
    # 1. 有约束
    # - to， 与哪张表关联
    # - to_field, 表中的哪一列关联
    # 2. Django自动
    # - 写的depart
    # - 自动生成数据depart_id
    # 3. 部门表被删除
    # ### 3.1 级联删除
    # depart = models.ForeignKey(to="Department", to_field="id", verbose_name="", on_delete=models.CASCADE)
    # ### 3.2 置空
    depart = models.ForeignKey(to="Department", to_field="id", verbose_name="Department", null=True, on_delete=models.SET_NULL)

    #在Django中做约束
    gender_choice = ((1, "Male"), (2, "Female") )
    gender = models.SmallIntegerField(verbose_name="Gender", choices=gender_choice)


class PrettyNum(models.Model):
    mobile = models.CharField(verbose_name="Phone Number", max_length=11)
    # 想要允许为null, 在参数中加上 null=True, blank=True
    price = models.IntegerField(verbose_name="Price")
    level_choices = (
        (1, "Level 1"),
        (2, "Level 2"),
        (3, "Level 3"),
        (4, "Level 4"),
        (5, "Level 5"),
    )
    level = models.SmallIntegerField(verbose_name="Level", choices=level_choices, default=1)

    status_choices = (
        (1, "Occupied"),
        (2, "Not occupied")
    )
    status = models.SmallIntegerField(verbose_name="Status", choices=status_choices, default=2)


class Task(models.Model):
    """ Task """

    level_choices = (
        (1, "High"),
        (2, "Medium"),
        (3, "Low"),
    )
    levels = models.SmallIntegerField(verbose_name="Level", choices=level_choices, default=1)
    title = models.CharField(verbose_name="Title", max_length=64)
    detail = models.TextField(verbose_name="Detail")

    user = models.ForeignKey(verbose_name="Person in charge", to=Admin, on_delete=models.CASCADE)

class Order(models.Model):
    """ Order """
    oid = models.CharField(verbose_name="Order ID", max_length=64)
    title = models.CharField(verbose_name="Title", max_length=64)
    price = models.IntegerField(verbose_name="Price")

    status_choices = (
        (1, 'Not yet paid'),
        (2, 'Already paid'),
    )

    status = models.SmallIntegerField(verbose_name="Status", choices=status_choices, default=1)
    admin = models.ForeignKey(verbose_name="Administrator", to=Admin, on_delete=models.CASCADE)