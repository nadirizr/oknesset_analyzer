from django.db import models

from base import BaseModel


class Tag(BaseModel):
  name = models.CharField(max_length=300)

  def __unicode__(self):
    return u"%s (%s)" % (self.name, self.id)
