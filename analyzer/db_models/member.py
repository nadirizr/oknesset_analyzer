from django.db import models

from base import BaseModel
from party import Party


class Member(BaseModel):
  name = models.CharField(max_length=300)
  party = models.ForeignKey(Party)
  role = models.CharField(max_length=1000)
  img_url = models.URLField()
  is_current = models.BooleanField(default=None)
  resource_uri = models.CharField(max_length=3000)

  def __unicode__(self):
    return (u"%s (%s)  %s" % (
        self.name,
        self.id,
        " [current]" * self.is_current))
