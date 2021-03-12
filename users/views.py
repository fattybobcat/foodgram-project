from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "reg.html"


# class MyPasswordResetView(PasswordResetView):
#
#   # forcing to use HTML email template (param: html_email_template_name)
#   def form_valid(self, form):
#       opts = {
#           'use_https': self.request.is_secure(),
#           'token_generator': self.token_generator,
#           'from_email': self.from_email,
#           'email_template_name': self.email_template_name,
#           'subject_template_name': self.subject_template_name,
#           'request': self.request,
#          # 'html_email_template_name': 'registration/password_reset_email.html',
#           'extra_email_context': self.extra_email_context,
#       }
#       form.save(**opts)
#       return HttpResponseRedirect(self.get_success_url())