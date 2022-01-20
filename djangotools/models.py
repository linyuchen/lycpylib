from django.db import models


class BaseModel(models.Model):
    """模型抽象基类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        # 说明是一个抽象基类
        abstract = True


def object_convert(origin: models.Model, new_object: models.Model):
    for f in origin._meta.fields:
        k = f.attname
        if k == "id":
            continue
        if hasattr(new_object, k):
            v = getattr(origin, k, None)
            setattr(new_object, k, v)
