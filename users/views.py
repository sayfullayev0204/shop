from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,LoginForm
from django.contrib.auth import authenticate, login,logout



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)  # EmailBackend handles email
            if user is not None:
                login(request, user)  # Correct usage of login()
                messages.success(request, "Siz tizimga muvaffaqiyatli kirdingiz!")
                return redirect('home')  # Adjust to your home URL name
            else:
                messages.error(request, "Email yoki parol xato.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Hisob {email} uchun yaratildi! Endi tizimga kirishingiz mumkin.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
from .models import Profile

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profilingiz muvaffaqiyatli yangilandi!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
@login_required
def logout_view(request):
    logout(request)  # Foydalanuvchini tizimdan chiqaradi
    messages.success(request, "Siz tizimdan muvaffaqiyatli chiqdingiz!")
    return redirect('home')  # Chiqqandan so'ng bosh sahifaga yo'naltirish

