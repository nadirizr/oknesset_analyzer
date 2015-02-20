from django.db import models

from base import BaseModel
from tag import Tag
from member import Member
from party import Party


class Bill(BaseModel):
  title = models.CharField(max_length=1000)
  full_title = models.CharField(max_length=3000)
  stage = models.CharField(max_length=1000)
  tags = models.ManyToManyField(Tag, through='BillTag')
  proposing_members = models.ManyToManyField(
      Member, through='BillProposingMember', related_name='bills_proposed')

  def proposingParties(self):
    return set([member.party for member in self.proposing_members.all()])

  def __unicode__(self):
      return (u"%s (%s), stage: %s" % (
      self.title,
      self.id,
      self.stage))


class BillProposingMember(BaseModel):
  member = models.ForeignKey(Member)
  bill = models.ForeignKey(Bill)


class BillTag(BaseModel):
  tag = models.ForeignKey(Tag)
  bill = models.ForeignKey(Bill)
