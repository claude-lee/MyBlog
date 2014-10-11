from django.conf.urls import patterns, include, url

from django.contrib import admin

from myblog import views
# from blog.models import Entry

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^'+'blogger'+'/', include('blog.urls')),
    #url(r'^', include('blog.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


