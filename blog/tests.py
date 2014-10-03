from django.test import TestCase
from .models import Entry


class EntryModelTest(TestCase):

   def test_unicode_representation(self):
      entry = Entry(title="My entry title")
      self.assertEqual(unicode(entry), entry.title)
