from django.conf.urls import patterns, url

from webaccount.views import AccountAuthView, AccountEditView, logout_view

urlpatterns = patterns(
    '',
    url(r'^login/$', AccountAuthView.as_view(), name='login_registration'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^profile/$', AccountEditView.as_view(), name='profile'),
)
