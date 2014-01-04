from django.conf.urls import patterns, url

from ownYourLife import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/entry-detail/$', views.EntryDetailView.as_view(), name='entry-detail'),
)
