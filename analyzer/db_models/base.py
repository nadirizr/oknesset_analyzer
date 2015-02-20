from django.db import models


class BaseModel(models.Model):
  @classmethod
  def from_json(cls, data):
    if "id" in data:
      cls.objects.filter(id=data["id"]).delete()

    filtered = { k: v for (k, v) in data.items()
                 if k in cls._meta.get_all_field_names() }
    instance = cls.objects.create(**filtered)
    instance.save()
    return instance

  class Meta:
    abstract = True
