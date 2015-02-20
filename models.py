from django.db import models


class Party(models.Model):
  name = models.CharField()
  is_coalition = models.BooleanField()
  number_of_seats = models.IntegerField()
  resource_uri = models.CharField()

  def __unicode__(self):
    return (u"%s (%s) [%s], seats: %d" % (
      self.name,
      self.id,
      "coalition" if self.is_coalition else "oposition",
      self.number_of_seats))

class Member(models.Model):
  name = models.CharField()
  party = models.ForeignKey(Party)
  role = models.CharField()
  img_url = models.URLField()
  is_current = models.BooleanField()
  resource_uri = models.CharField()

  def __unicode__(self):
    return (u"%s (%s)  %s" % (
        self.name,
        self.id,
        " [current]" * self.is_current))

class Tag(models.Model):
  name = models.CharField(max_length=200)

  def __unicode__(self):
    return u"%s (%s)" % (self.name, self.id)

class Bill(models.Model):
  title = models.CharField()
  full_title = models.CharField()
  stage = models.CharField()
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

class BillProposingMember(models.Model):
  member = models.ForeignKey(Member)
  bill = models.ForeignKey(Bill)

class BillTag(models.Model):
  tag = models.ForeignKey(Tag)
  bill = models.ForeignKey(Bill)

class Vote(models.Model):
  title = models.CharField()
  full_text = models.CharField()
  summary = models.CharField()
  bill = models.ForeignKey(Bill)
  type = models.IntegerField()
  type_description = models.CharField()
  time = models.DateTimeField()

  def __unicode__(self):
    return (u"%s (%s) - %s [%s]" % (
      self.title,
      self.id,
      self.bill,
      self.time))

class Agenda(models.Model):
  name = models.CharField(max_length=1000)
  description = models.TextField()
  img_url = models.URLField()
  owner = models.CharField(max_length=200)
  members = models.ManyToManyField(Member, through='MemberAgenda')
  parties = models.ManyToManyField(Party, through='PartyAgenda')
  votes = models.ManyToManyField(Vote, through='VoteAgenda')

  def __unicode__(self):
    return u"%s (%s)" % (self.name, self.id)

class VoteAgenda(models.Model):
  agenda = models.ForeignKey(Agenda)
  vote = models.ForeignKey(Vote)
  score = models.DecimalField(max_digits=6, decimal_places=2)
  reasoning = models.CharField(max_length=1000)

class VoteMemberDecision(models.Model):
  member = models.ForeignKey(Member)
  vote = models.ForeignKey(Vote)
  decision = models.CharField(max_length=100)

  def __unicode__(self):
    return "%s: %s" % (self.member.__unicode__(), self.decision)

class PartyAgenda(models.Model):
  agenda = models.ForeignKey(Agenda)
  party = models.ForeignKey(Party)
  score = models.DecimalField(max_digits=6, decimal_places=2)
  volume = models.DecimalField(max_digits=6, decimal_places=2)

class MemberAgenda(models.Model):
  agenda = models.ForeignKey(Agenda)
  member = models.ForeignKey(Member)
  score = models.DecimalField(max_digits=6, decimal_places=2)
  volume = models.DecimalField(max_digits=6, decimal_places=2)
