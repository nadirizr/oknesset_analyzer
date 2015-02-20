import json
import time
import traceback
import urllib
from collections import Iterator
from progressbar import ProgressBar
from analyzer.db_models.member import Member
from analyzer.db_models.party import Party

DOMAIN = 'http://oknesset.org'
BASE_URL = '/api/v2?format=json'


class JsonResource:
  @staticmethod
  def _get_json_data(url, max_tries=10, wait_between_retries=5):
    url = DOMAIN + url
    tries = 0
    exc = None
    while tries <= max_tries:
      try:
        cm = urllib.urlopen(url)
        data = json.load(cm)
        return data
      except IOError, e:
        exc = e
      except ValueError, e:
        exc = e

      time.sleep(wait_between_retries)
      tries += 1
      print "Retrying... (%d/%d)" % (tries, max_tries)
    else:
      print "--> URL = '%s'" % url
      if exc:
        print "IO ERROR:"
        print exc

    raise IOError("Too many IOErrors, aborting")


class ResourceFactory(JsonResource):
  def __init__(self):
    self.resources_json = self._get_json_data(BASE_URL)

  def create(self, name):
    if name not in self.resources_json:
      raise Exception('Resource not found')

    return Resource(self.resources_json[name]['list_endpoint'])


class Resource(JsonResource, Iterator):
  def __init__(self, url):
    self.data = self._get_json_data(url)
    self.current = 0

  def next(self):
    if self.current >= len(self):
      raise StopIteration

    if self.current >= self._end_of_page():
      self._next_page()

    self.current += 1
    return self.data['objects'][self.current-1]

  def _next_page(self):
    self.data = self._get_json_data(DOMAIN + self.data['meta']['next'])

  def _end_of_page(self):
    return self.data['meta']['offset'] + self.data['meta']['limit']

  def __len__(self):
    return self.data['meta']['total_count']

  @staticmethod
  def get(name):
    Resource.factory = ResourceFactory()
    return Resource.factory.create(name)


class OKnessetCrawler:
  def __init__(self):
    self.parties = {party.id: party for party in Party.objects.all()}
    self.members = {member.id: member for member in Member.objects.all()}

  def populate_all(self):
    self.populate_parties()
    self.populate_members()

  def populate_parties(self):
    self._populate_resource('party', self.parties, self.populate_party)

  def populate_party(self, item):
    return Party.from_json(item)

  def populate_members(self):
    self._populate_resource('member', self.members, self.populate_member)

  def populate_member(self, item):
    member = Member.from_json(item)
    return member

  @staticmethod
  def _populate_resource(resource, container, populator):
    print '='*80
    print 'Fetching %s...' % resource
    data = Resource.get(resource)
    progress = ProgressBar()
    for item in progress(data):
      if item['id'] in container:
        continue
      try:
        model = populator(item)
        container[model.id] = model
      except Exception, e:
        print e
        traceback.print_exc()
        raise e
