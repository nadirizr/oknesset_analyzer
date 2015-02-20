from django.db import models

from base import BaseModel


class Party(BaseModel):
  name = models.CharField(max_length=100)
  number_of_seats = models.IntegerField()
  is_coalition = models.BooleanField(default=None)
  resource_uri = models.CharField(max_length=3000)

  def __unicode__(self):
    return (u"%s (%s) [%s], seats: %s" % (
      self.name,
      self.id,
      "coalition" if self.is_coalition else "oposition",
      self.number_of_seats))
