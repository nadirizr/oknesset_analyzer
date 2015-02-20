from django.db import models

from base import BaseModel
from member import Member
from party import Party
from vote import Vote


class Agenda(BaseModel):
  name = models.CharField(max_length=1000)
  description = models.TextField()
  public_owner_name = models.CharField(max_length=1000)
  members = models.ManyToManyField(Member, through='MemberAgenda')
  parties = models.ManyToManyField(Party, through='PartyAgenda')
  votes = models.ManyToManyField(Vote, through='VoteAgenda')

  def __unicode__(self):
    return u"%s (%s)" % (self.name, self.id)


class VoteAgenda(BaseModel):
  agenda = models.ForeignKey(Agenda)
  vote = models.ForeignKey(Vote)
  score = models.DecimalField(max_digits=6, decimal_places=2)
  importance = models.DecimalField(max_digits=6, decimal_places=2)
  reasoning = models.CharField(max_length=1000)


class PartyAgenda(BaseModel):
  agenda = models.ForeignKey(Agenda)
  party = models.ForeignKey(Party)
  score = models.DecimalField(max_digits=6, decimal_places=2)
  volume = models.DecimalField(max_digits=6, decimal_places=2)


class MemberAgenda(BaseModel):
  agenda = models.ForeignKey(Agenda)
  member = models.ForeignKey(Member)
  score = models.DecimalField(max_digits=6, decimal_places=2)
  volume = models.DecimalField(max_digits=6, decimal_places=2)
