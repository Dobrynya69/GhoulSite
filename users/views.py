import random
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth import get_user_model, login
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *
from django.core.mail import send_mail
from .utils import email_activation_token

class ActivateEmailSendView(LoginRequiredMixin, View):
    template_name = 'users/email_send.html'

    def get(self, request, *args, **kwargs):
        token = email_activation_token.make_token(request.user)
        uid64 = force_str(urlsafe_base64_encode(force_bytes(request.user.pk)))
        url = 'http://127.0.0.1:8000' + reverse_lazy('activate_email', kwargs={'uidb64': uid64, 'token': token})

        send_mail('Email activation from "Find your ghoul"', 
                  f'Hello {request.user.first_name}! Now you can activate your email, just follow the link: {url}', 
                  'djangoemailsends@gmail.com', [request.user.email,], 
                  fail_silently=False)
        return render(request=request, template_name=self.template_name)


class ActivateEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and email_activation_token.check_token(user, token):
            user.active_email = True
            user.save()
            login(request, user)
            return redirect('email_success')
        else:
            return redirect('email_error')


class ActivateEmailSuccessView(TemplateView):
    template_name = 'users/email_success.html'
    extra_context = {'title': 'Email success'}


class ActivateEmailErrorView(TemplateView):
    template_name = 'users/email_error.html'
    extra_context = {'title': 'Email error'}

class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=kwargs['pk'])
        return render(request=request, template_name='users/detail.html', context={'form': CustomUserChangeForm(), 'user': user})

    def post(self, request, *args, **kwargs):
        user = request.user
        user.first_name = request.POST['name']
        user.save()
        return redirect(reverse_lazy('user_detail', kwargs={'pk': user.pk}))

    def test_func(self):
        owner = get_user_model().objects.get(pk=self.kwargs['pk'])
        return self.request.user == owner