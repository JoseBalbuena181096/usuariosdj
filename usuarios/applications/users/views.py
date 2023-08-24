from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import EmailMessage
from .forms import (
    UserRegisterForm, 
    LoginForm,
    UpdatePasswordForm,
    VerificationForm)
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail



# Create your views here.
from django.views.generic import (
    CreateView,
    View
)
from django.views.generic.edit import (
    FormView
)
from .models import User
from .funtions import code_generator


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    # Es la url a la que se tiene que ir al completar el proseso de registro
    success_url = '/'

    def form_valid(self, form):
        # Generamos el codigo
        codigo = code_generator()
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
            codregistro = codigo
        )
        # enviar el codigo al email al usuario
        asunto = 'Confirmacion de email Marte'
        mensaje = 'Código de verificación: ' + codigo
        send_mail(
            asunto,
            mensaje,
            "josebalbuena181096@gmail.com",
            [form.cleaned_data['email'],],
            fail_silently=False,
        )

        # return super(UserRegisterView, self).form_valid(form)
        return HttpResponseRedirect(reverse('users_app:user-verification', kwargs={'pk': usuario.id}))

class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')
    
    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)
    
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
            'users_app:user-login'
            )
        )
        
class UpdatePasswordView(LoginRequiredMixin , FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')
    
    def form_valid(self, form ):
        # Es el susuario que tenemos activo 
        usuario = self.request.user
        # Autenticamos que la contraseña actual es la misma que la de la db
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1']
        )
        if user:
            # Actualizamos la contraseña tomando la nueva desde el formulario
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)

class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')
    
    def get_form_kwargs(self):

        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk':self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self, form):
        # id_user = self.kwargs['pk']
        User.objects.filter(
            id = self.kwargs['pk']
        ).update(
            is_active = True
        )
        return super(CodeVerificationView, self).form_valid(form)