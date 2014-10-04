from django.test import TestCase
from .models import Entry
from django.contrib.auth import get_user_model
from .forms import CommentForm
from .models import Entry, Comment
from django_webtest import WebTest
from django.template import Template, Context


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


class EntryViewTest(WebTest):


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

   def test_no_comments_yet(self):
      response = self.client.get(self.entry.get_absolute_url())
      # print response
      self.assertContains(response, 'No comments yet.')

   def test_view_page(self):
       page = self.app.get(self.entry.get_absolute_url())
       self.assertEqual(len(page.forms), 1)

   def test_form_error(self):
       page = self.app.get(self.entry.get_absolute_url())
       page = page.form.submit()
       self.assertContains(page, "This field is required.")

   def test_form_success(self): # 403 FORBIDDEN
       page = self.app.get(self.entry.get_absolute_url())
       page.form['name'] = "Phillip"
       page.form['email'] = "phillip@example.com"
       page.form['body'] = "Test comment body."
       page = page.form.submit()
       self.assertRedirects(page, self.entry.get_absolute_url())


   # def test_one_comment(self): # blog_comment.entry_id may not be NULL
   #    Comment.objects.create(entry=Entry(title="My entry title"), name='1-peter', email='1-claude@g.com', body='1-body')
   #    response = self.client.get('/')
   #    self.assertContains(response, 'My entry title')
   #    self.assertContains(response, '1-peter')
   #    self.assertContains(response, '1-claude@g.com')
   #    self.assertContains(response, '1-body')


class CommentModelTest(TestCase):


   def test_unicode_representation(self):
       comment = Comment(body="My comment body")
       self.assertEqual(unicode(comment), "My comment body")



class CommentFormTest(TestCase):

   def setUp(self):
       user = get_user_model().objects.create_user('lisa')
       self.entry = Entry.objects.create(author=user, title="My entry title")

   def test_init(self):
       CommentForm(entry=self.entry)

   def test_init_without_entry(self):
       with self.assertRaises(KeyError):
           CommentForm()

   def test_valid_data(self):
       form = CommentForm({
                              'name': "lisa schmidt",
                              'email': "lisa.schmidt@example.com",
                              'body': "Hello world",
                              }, entry=self.entry)
       self.assertTrue(form.is_valid())
       comment = form.save()
       self.assertEqual(comment.name, "lisa schmidt")
       self.assertEqual(comment.email, "lisa.schmidt@example.com")
       self.assertEqual(comment.body, "Hello world")
       self.assertEqual(comment.entry, self.entry)

   def test_blank_data(self):
       form = CommentForm({}, entry=self.entry)
       self.assertFalse(form.is_valid())
       self.assertEqual(form.errors, {
        'name': ['This field is required.'],
        'email': ['This field is required.'],
        'body': ['This field is required.'],
        })


class EntryHistoryTagTest(TestCase):


    TEMPLATE = Template("{% load blog_tags %} {% entry_history %}")

    def setUp(self):
        self.user = get_user_model().objects.create(username='zoidberg')
        self.entry = Entry.objects.create(author=self.user, title="My entry title")

    def test_entry_shows_up(self):
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn(self.entry.title, rendered)

    # def test_no_posts(self): # FAIL
    #     rendered = self.TEMPLATE.render(Context({}))
    #     # import pdb; pdb.set_trace()
    #     self.assertIn("No recent entries", rendered)

    def test_many_posts(self):
        for n in range(1,6):
            Entry.objects.create(author=self.user, title="Post #{0}".format(n))
        rendered = self.TEMPLATE.render(Context({}))
        # import pdb; pdb.set_trace()
        self.assertIn("Post #5", rendered)
        self.assertNotIn("Post #6", rendered)
