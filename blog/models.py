from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

class Entry(models.Model):

   title = models.CharField(max_length=500)
   author = models.ForeignKey('auth.User')
   body = models.TextField()
   created_at = models.DateTimeField(auto_now_add=True, editable=False)
   modified_at = models.DateTimeField(auto_now=True, editable=False)
   slug = models.SlugField()

   def __unicode__(self):
       return self.title

   def get_absolute_url(self):
       return reverse('blog.views.entry_detail', kwargs={'pk': self.pk})


   class Meta:
      verbose_name_plural = "entries"


   def save(self, *args, **kwargs):
       self.slug = slugify(self.title)
       super(Entry, self).save(*args, **kwargs)

class Comment(models.Model):

    entry = models.ForeignKey(Entry)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
       return self.body