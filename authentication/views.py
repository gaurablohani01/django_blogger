from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


def register_page(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1= request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not User.objects.filter(username= username).exists():
            if not User.objects.filter(email = email).exists():
                if not first_name.lower() in password1.lower() or last_name.lower() in password1.lower(): 
                    if password1 == password2:
                        user= User.objects.create(first_name= first_name, last_name=last_name, username=username, email=email)
                        user.set_password(password1)
                        user.save()
                        messages.success(request, f'User has been created successfully')
                        return redirect('register')
                    else:
                        messages.warning(request, f'Password should be same')
                        return redirect('register')
                else:
                    messages.warning(request, f'Password should not contain their first or last name')
                    return redirect('register')
            else:
                messages.warning(request, f'Email already exists')
                return redirect('register')
        else:
            messages.warning(request, f'Username already exists')
            return redirect('register')
    context={
        'title': "Register"
    }
    return render(request, "register.html", context=context)

def login_page(request):
    try:
        if request.method=="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username= username, password=password)

            if User.objects.filter(username=username).exists():
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Successfully login')
                    return redirect('home')
                else:
                    messages.warning(request, f'Invalid  password')
                    return redirect('login')
            else:
                messages.warning(request, f'Invalid username or password')
                return redirect('login')
        context={
            'title': "Login"
        }
        return render(request, "login.html", context=context)
    except Exception as e:
        messages.warning(request, f'{e}')

def logout_page(request):
    try:
        logout(request)
        messages.success(request, f'Logout successfully')
        return redirect('login')
    except Exception as e:
        messages.error(request, f'{e}')