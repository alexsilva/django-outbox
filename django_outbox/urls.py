from django.conf.urls import url

from django_outbox.views import OutboxTemplateView, MailTemplateView

urlpatterns = [
    url(r'^$', OutboxTemplateView.as_view(), name='outbox'),
    url(r'^(?P<id>.+)/$', MailTemplateView.as_view(), name='mail'),
]
