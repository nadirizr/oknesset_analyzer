from django.db import models

from base import BaseModel
from party import Party


class Member(BaseModel):
  name = models.CharField(max_length=300)
  is_current = models.BooleanField(default=None)
  img_url = models.URLField()
  resource_uri = models.CharField(max_length=3000)
  party = models.ForeignKey(Party)

  @classmethod
  def from_json(cls, data, party):
    data["party"] = party
    return super(Member, cls).from_json(data)

  def __unicode__(self):
    return (u"%s (%s)  %s" % (
        self.name,
        self.id,
        " [current]" * self.is_current))

class SkippedMember(BaseModel):
  pass
