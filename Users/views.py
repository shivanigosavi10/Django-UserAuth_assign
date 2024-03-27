from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .helper import send_forgot_password_mail
# Create your views here.

@api_view(['POST'])
def register(request):
    context={}
    if request.method == "POST":
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        name=request.POST["uname"]
        email=request.POST["email"]
        upass1=request.POST["upass"]
        upass2=request.POST["ucom"]
        if fname=='' or lname=='' or name=='' or email=='' or upass1=='':            
            context['errmsg']="Feild cannot be empty!!!"
            return render(request,'register.html',context)
        elif upass1 != upass2:
            context['errmsg']="Password and Confirm password not matched!!!"
            return render (request, 'register.html',context)
        else:
            try:
              u=User.objects.create( first_name=fname, last_name=lname, username=name, email=email,password=upass1)
              u.set_password(upass1)
              u.save()
              context['success']="Successfully registered"
              return render(request,"register.html",context)
            except Exception:
                context['errmsg']="Username already Exist"
                return render(request, "register.html", context)
    else:
        return render(request, "register.html")
    
    
@api_view(['POST'])
def user_login(request):
     context={}
     if request.method=="POST":
            user_name=request.POST['uname']
            pwd=request.POST['pass']
            if user_name=='' or pwd=='':
                context['errmsg']="field can not be empty"
                return render(request,"login.html",context)
            else:
                u=authenticate(username=user_name,password=pwd)
                if u is not None:
                    login(request,u)
                    print(request.user.is_authenticated)
                    context['success']="Successfully registered"
                    return HttpResponseRedirect('/home/')
                else:
                    context['errmsg']="Invalid username and password!!"
                    return render(request,"login.html",context)
                
     else:
         return render(request,"login.html")
     
def home(request):
     return render(request,"home.html")

@api_view(['POST'])
def ChangePassword(request, token):
    context ={}
    try:
        profile_obj = User(forgot_password_token = token)

        print(profile_obj)

    except Exception as e:
        print(e)
    return render(request, 'reset_password.html')


import uuid
@api_view(['POST'])
def forgot_password(request):
    try:
        if request.method == 'POST':
           username = request.POST.get('uname')

           if not User.objects.filter(username=username).first():
                messages.success(request, 'No User Found this username.')
                return render('/forgot_password')
           
           user_obj = User.ob.get(username = username)
           token = str(uuid.uuid4())
           send_forgot_password_mail(user_obj, token)
           messages.success(request, 'An email is send.')
           return render('/forgot_password')

    except Exception as e:
        print(e)
        return render(request, 'forgot_password.html')