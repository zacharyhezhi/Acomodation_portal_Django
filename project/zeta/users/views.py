# users/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import UpdateView

from .forms import CustomUserCreationForm

from users.models import CustomUser

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

def profile(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    return render(request, 'users/profile.html', {'customuser':user})

class EditProfile(UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'about', 'location', 'neighbourhood']
    template_name = 'users/edit-profile.html'
    
    def get_form(self, form_class=None):
        form = super(EditProfile, self).get_form(form_class)
        for field in form.fields:
            form.fields[field].required = False
        return form
    
    def get_object(self):
        user_id = None
        if self.request.user.is_authenticated \
           and self.kwargs['user_id'] == self.request.user.id:
            user_id = self.kwargs['user_id']
        return get_object_or_404(CustomUser, pk=user_id)

    def get_success_url(self):
        return reverse('users:profile', kwargs={'user_id':self.kwargs['user_id']})
