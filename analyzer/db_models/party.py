from django.db import models


class Party(models.Model):
  number_of_seats = models.IntegerField()
  name = models.CharField(max_length=100)
  is_coalition = models.BooleanField()
  resource_uri = models.CharField(max_length=3000)

  @staticmethod
  def from_json(data):
    filtered = {k: v for (k, v) in data.items() if k in Party._meta.get_all_field_names()}
    party = Party.objects.create(**filtered)
    party.save()

    return party

  def __unicode__(self):
    return (u"%s (%s) [%s], seats: %s" % (
      self.name,
      self.id,
      "coalition" if self.is_coalition else "oposition",
      self.number_of_seats))
