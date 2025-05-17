from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# accounts/views.py
from django.shortcuts import render, redirect
from accounts.forms import UserRegistrationForm, LoginForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required 

def homepage(request):
    return render (request, 'accounts/homepage.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("CLEANED DATA:", form.cleaned_data)
            form.save()
            return redirect('accounts:login')  # Or wherever you want
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)
    
    def get_success_url(self):
        user = self.request.user
        
        # Check if user is a driver
        if hasattr(user, 'driver'):
            return reverse_lazy('shipper:freight-search')  # URL name for driver's freight search
        
        # Check if user is a carrier/shipper
        elif hasattr(user, 'shipper'):
            return reverse_lazy('shipper:freight-list')

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'accounts/logout.html', {
        'message': 'You have been successfully logged out.'
    })