from django.test import TestCase
from .models import Entry
from django.contrib.auth import get_user_model
from .forms import CommentForm
from .models import Entry, Comment


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


class HomePageTests(TestCase):

   def setUp(self):
       self.user = get_user_model().objects.create(username='some_user')

   def test_one_entry(self):
       Entry.objects.create(title='1-title', body='1-body', author=self.user)
       response = self.client.get('/')
       self.assertContains(response, '1-title')
       self.assertContains(response, '1-body')

   def test_two_entries(self):
       Entry.objects.create(title='1-title', body='1-body', author=self.user)
       Entry.objects.create(title='2-title', body='2-body', author=self.user)
       response = self.client.get('/')
       self.assertContains(response, '1-title')
       self.assertContains(response, '1-body')
       self.assertContains(response, '2-title')

   def test_no_blog_entries(self):
       response = self.client.get('/')
       self.assertContains(response, 'There are no blog entries yet.')


class EntryViewTest(TestCase):


   def setUp(self):
       self.user = get_user_model().objects.create(username='some_user')
       self.entry = Entry.objects.create(title='1-title', body='1-body', author=self.user)

   def test_basic_view(self):
       response = self.client.get(self.entry.get_absolute_url())
       self.assertEqual(response.status_code, 200)

   def test_get_absolute_url(self):
       entry = Entry.objects.create(title="My entry title", author=self.user)
       self.assertIsNotNone(entry.get_absolute_url())

   def test_title_in_entry(self):
       response = self.client.get(self.entry.get_absolute_url())
       self.assertContains(response, self.entry.title)

   def test_body_in_entry(self):
       response = self.client.get(self.entry.get_absolute_url())
       self.assertContains(response, self.entry.body)

   #def test_one_comment(self):
   #    Comment.objects.create(entry=Entry(title="My entry title"), name='1-peter', email='1-claude@g.com', body='1-body')
   #    response = self.client.get('/')
   #    self.assertContains(response, 'My entry title')
   #    self.assertContains(response, '1-peter')
   #    self.assertContains(response, '1-claude@g.com')
   #    self.assertContains(response, '1-body')

   #def test_no_comments_yet(self):
   #    response = self.client.get('/')
   #    self.assertContains(response, 'No comments yet.')

class CommentModelTest(TestCase):


   def test_unicode_representation(self):
       comment = Comment(body="My comment body")
       self.assertEqual(unicode(comment), "My comment body")



class CommentFormTest(TestCase):

   def setUp(self):
       user = get_user_model().objects.create_user('zoidberg')
       self.entry = Entry.objects.create(author=user, title="My entry title")

   def test_init(self):
       CommentForm(entry=self.entry)

   def test_init_without_entry(self):
       with self.assertRaises(KeyError):
           CommentForm()

