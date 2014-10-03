from django.test import TestCase
from .models import Entry


class EntryModelTest(TestCase):

   def test_unicode_representation(self):
      entry = Entry(title="My entry title")
      self.assertEqual(unicode(entry), entry.title)

   def test_verbose_name_plural(self):
      self.assertEqual(unicode(Entry._meta.verbose_name_plural), "entries")

class ProjectTests(TestCase):

   def test_homepage(self):
      response = self.client.get('/')
      self.assertEqual(response.status_code, 200)