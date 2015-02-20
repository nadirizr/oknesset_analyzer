from django.db import models
from flufl.enum import Enum

from base import BaseModel
from bill import Bill
from member import Member


class Vote(BaseModel):
  class Type(Enum):
    PRE = 1
    FIRST = 2
    APPROVAL = 3

  title = models.CharField(max_length=1000)
  full_text = models.TextField()
  summary = models.TextField()
  bill = models.ForeignKey(Bill)
  type = models.IntegerField(choices=Type._enums.items())
  type_description = models.CharField(max_length=1000)
  time = models.DateTimeField()

  def __unicode__(self):
    return (u"%s (%s), type: %s - %s [%s]" % (
      self.title,
      self.id,
      self.Type(self.type),
      self.bill,
      self.time))


class VoteMemberDecision(BaseModel):
  class Decision(Enum):
    FOR = 1
    AGAINST = -1
    ABSTAIN = 0

  member = models.ForeignKey(Member)
  vote = models.ForeignKey(Vote)
  decision = models.IntegerField(choices=Decision._enums.items())

  def __unicode__(self):
    return "%s: %s" % (
            self.member.__unicode__(),
            self.Decision(self.decision))
