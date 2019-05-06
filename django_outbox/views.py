import base64

from django.http import HttpResponse
from django.views.generic import TemplateView

from .outbox import Outbox


class OutboxTemplateView(TemplateView):
    template_name = 'django_outbox/outbox.html'

    def get_context_data(self, **kwargs):
        context = super(OutboxTemplateView, self).get_context_data(**kwargs)
        context['mails'] = Outbox().all()
        return context


class MailTemplateView(TemplateView):
    """Displays the contents of an e-mail message"""
    template_name = 'django_outbox/mail.html'

    def render_to_response(self, context, **kwargs):
        body = context['body']
        if body.content_type in ["text/html", "text/plain"]:
            return super(MailTemplateView, self).render_to_response(context, **kwargs)
        return HttpResponse(body.content, content_type=body.content_type)

    def get_context_data(self, id, **kwargs):
        context = super(MailTemplateView, self).get_context_data(**kwargs)
        mail = Outbox().get(id)
        index = int(self.request.GET.get('index', 0))
        context['mail'] = mail
        context['body'] = mail.body[index]
        return context
