from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import LoginForm, UserRegistrationForm, \
    UserEditForm, ProfileEditForm
from .models import Profile


def account_menu(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile', kwargs={'username': request.user.username}))
    return render(request, 'account/account_menu.html')


@transaction.atomic  # Data will be saved atomically
def register_view(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST, request.FILES)

        if register_form.is_valid():
            try:
                new_user = register_form.save(commit=False)  # Without saving to the DB.
                new_user.set_password(register_form.cleaned_data['password'])  # Encrypt password.
                new_user.save()
                Profile.objects.get_or_create(  # The profile will be created only once for each user.
                    user=new_user,
                    defaults={
                        'image': register_form.cleaned_data.get('image'),
                        'date_of_birth': register_form.cleaned_data.get('date_of_birth')
                    }
                )
                messages.success(request, 'Your account has been successfully created!')
                return redirect(reverse('register_done', args=[new_user.id]))

            except Exception as e:
                messages.error(request, f'Error creating account: {e}')
        else:
            for field, error_list in register_form.errors.items():
                for error in error_list:
                    messages.error(request, f'{register_form.fields[field].label}: {error}')
    else:
        register_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'register_form': register_form})


def register_done(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Fetch the user by ID or return 404 if not found
    return render(request, 'account/register_done.html', {'new_user': user})


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile', kwargs={'username': request.user.username}))
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request,
                                username=login_form.cleaned_data['username'],
                                password=login_form.cleaned_data['password'])
            if user is not None:
                if user.is_active:  # if the account is blocked or deactivated
                    login(request, user)
                    messages.success(request, 'You are logged in successfully.')
                    return redirect(reverse('profile', kwargs={'username': user.username}))
                else:
                    messages.error(request, 'Disabled account')
            else:
                messages.error(request, 'Invalid login or password')
    else:
        login_form = LoginForm()
    return render(request, 'account/login.html', {'login_form': login_form})


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'account/profile.html', {'user': user})


@login_required
@transaction.atomic
def edit_view(request, username):
    user = get_object_or_404(User, username=username)  # Load user by username
    if request.method == 'POST':
        # Initialize forms with data from the request
        forms = {
            'user_edit_form': UserEditForm(instance=request.user, data=request.POST),
            'profile_edit_form': ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        }
        # Check if both forms are valid
        if all(form.is_valid() for form in forms.values()):
            try:
                # Save data from both forms
                for form in forms.values():
                    form.save()
                messages.success(request, 'Profile updated successfully')
            except Exception as e:
                # Handle potential errors during saving
                messages.error(request, f'An error occurred while saving: {str(e)}')
            return redirect(reverse_lazy('profile', kwargs={'username': username}))
        else:
            # Error message if form data is invalid
            messages.error(request, 'Error updating your profile')
    else:
        # Initialize forms for GET request
        forms = {
            'user_edit_form': UserEditForm(instance=request.user),
            'profile_edit_form': ProfileEditForm(instance=request.user.profile)
        }
    return render(request, 'account/edit.html', {'user': user, **forms})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out of your account.')
    return redirect(reverse('account_menu'))
