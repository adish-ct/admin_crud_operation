from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from user_app.models import Customer
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user_app import views
from django.views.decorators.cache import cache_control
from django.contrib.admin.views.decorators import staff_member_required



# Create your views here.

@cache_control(no_cache=True, no_store=True)
@login_required(login_url='admin_log_in')
def admin_home(request):
    if 'email' in request.session:
        my_user = Customer.objects.all()
        context = {
            'users': my_user
        }
        return render(request, 'adminDash.html', context)
    else:
        return redirect(admin_log_in)


@cache_control(no_cache=True, no_store=True)
def admin_log_in(request):
    if 'username' in request.session:
        return redirect('home')
    if 'email' in request.session:
        return redirect(admin_home)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user:
                if user.is_superuser:
                    request.session['email'] = username
                    login(request, user)
                    return redirect(admin_home)
                else:
                    messages.error(request, "Sorry, Invalid credentials please try again with admin credentials only")
                    return redirect(admin_log_in)
            else:
                messages.error(request, "Login with admin credentials only")
                return redirect('admin_log_in')
        return render(request, 'adminLogin.html')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='admin_log_in')
def admin_add_user(request):
    if 'email' in request.session:
        if request.method == 'POST':
            name = request.POST.get('name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            c_password = request.POST.get('c_password')

            exist_username = User.objects.filter(username=username)
            if exist_username.exists():
                messages.error(request, 'username already taken')
                return redirect(admin_home)
            if password == c_password:
                my_user = User.objects.create_user(username=username, password=password, email=email)
                my_user.save()
                new_user = Customer(name=name, user_name=username, email=email)
                new_user.save()
                return redirect(admin_home)
            else:
                messages.error(request, 'password not matching try again..')
                return redirect(admin_home)
        else:
            return redirect(admin_log_in)
    else:
        return redirect(admin_log_in)
    return render(request, 'adminDash.html')


@cache_control(no_cache=True, no_store=True)
def admin_update(request, id):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        user = Customer(
            id=id,
            name=name,
            user_name=username,
            email=email
        )
        user.save()
    return redirect(admin_home)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='admin_log_in')
def admin_delete_user(request, id):
    if 'email' in request.session:
        my_user = get_object_or_404(Customer, id=id)
        user = User.objects.filter(id=id)
        my_user.delete()
        user.delete()
        return redirect(admin_home)
    else:
        return redirect(admin_log_in)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='admin_log_in')
def admin_logout(request):
    if 'email' in request.session:
        if request.method == 'POST':
            logout(request)
            return redirect('log_in')
        return redirect('admin_home')
    else:
        return redirect('admin_home')


@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='admin_log_in')
def admin_search(request):
    if request.method == 'POST':
        search_name = request.POST['search']
        search_query = Customer.objects.filter(user_name__icontains=search_name)
        context = {
            'users': search_query
        }
        return render(request, 'adminDash.html', context)

    return redirect('admin_home')