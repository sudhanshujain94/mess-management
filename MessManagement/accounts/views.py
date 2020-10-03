from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from random import randint
from .models import Contact_Us_Login
OTP = randint(1000, 9999)
EnterUser = ''
first_name = ''
last_name = ''
email = ''
username = ''
password = ''
confirm_password = ''


def Login(request):
    return render(request, 'Login.html')


def SignUp(request):
    return render(request, 'SignUp.html')


def SignUpOTP(request):
    global first_name,last_name,username,email,password,confirm_password
    first_name = request.POST.get('FIRST NAME', default='NOT VALID').upper()
    last_name = request.POST.get('LAST NAME', default='NOT VALID').upper()
    username = request.POST.get('USERNAME', default='NOT VALID').upper()
    try:
        if len(username) != 10 or (int(username[0:2]) < 16 and int(username[0:2]) > 19) or username[2:5] != 'EGJ' or int( username[7:10] ) > 400 :
            messages.error(request,'Invalid Roll No')
            return HttpResponseRedirect('/SignUp/')
    except:
        messages.error(request, 'Invalid Roll No')
        return HttpResponseRedirect('/SignUp/')
    email = request.POST.get('EMAIL', default='NOT VALID')
    if '@' not in email or '.com' != email[-4:]:
        messages.error(request, 'Invalid E-Mail ID')
        return HttpResponseRedirect('/SignUp/')
    password = request.POST.get('PASSWORD', default='NOT VALID')
    confirm_password = request.POST.get('CONFIRM PASSWORD', default='NOT VALID')
    if first_name=='NOT VALID' or last_name == "NOT VALID" or email == 'NOT VALID' or password == 'NOT VALID':
        messages.error(request, 'Complete all Entries')
        return HttpResponseRedirect('/SignUp/')
    if password == confirm_password:
        if len(password) < 8:
            messages.error(request, 'Password Length is Insufficient')
        global OTP
        try:
            user = User.objects.get(username=username)
            messages.error(request, 'Roll No Already Exist')
            return HttpResponseRedirect('/SignUp/')
        except :
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email ID Already Exist')
                return HttpResponseRedirect('/SignUp/')
            else:
                OTP = randint(1000,9999)
                print(OTP)
                return render(request,"Sign Up OTP.html")
    else:
        return HttpResponse("""<meta http-equiv="refresh" content = "0;url='/SignUp/' " /><title>Password MisMatch</title><script>alert('Password MisMatch')</script>""")



def CreateUser(request):
    global OTP
    Enter_OTP = int(request.POST.get("OTP",default='0'))
    if OTP == Enter_OTP:
        global first_name,last_name,username,email,password,confirm_password
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = True
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        first_name = last_name = username = email = password = confirm_password = ''
        return HttpResponse("""<meta http-equiv="refresh" content = "0;url='/'" /><title>Account Created</title><script>alert('Account Created')</script>""")
    else:
        messages.error(request,'Invalid OTP')
        return render(request,'Sign Up OTP.html')



def Auth(request):
    logout(request)
    username = request.POST.get('USERNAME', default='NOT VALID').upper()
    password = request.POST.get('PASSWORD', default='NOT VALID')
    try:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            return HttpResponseRedirect('/Dashboard/')
        else:
            return HttpResponse("""<meta http-equiv="refresh" content = "0;url='/'" /><title>Invalid Account</title><script>alert('Invalid Creditials')</script>""")
    except:
        return HttpResponse("""<meta http-equiv="refresh" content = "0;url='/'" /><title>Error</title><script>alert('Somethong Went Wrong')</script>""")


def ForgetPassword(request):
    return render(request, 'Forget Password.html')


def CheckUser(request):
    global EnterUser
    EnterUser = request.POST.get('USERNAME', default='NOT VALID').upper()
    email = request.POST.get('EMAIL', default='NOT VALID')
    try:
        user = User.objects.get(username = EnterUser)
        print(user.email)
        global OTP
        OTP = randint(1000,9999)
        print(OTP)
        return render(request,'OTP Forget Password.html', {'user': (user.first_name + ' ' + user.last_name)})
    except:
            messages.error(request, 'Invalid Roll No')
            return HttpResponseRedirect('/ForgetPassword/')


def ResetPassword(request):
    Enter_OTP = int(request.POST.get('OTP',default = 0000))
    password = request.POST.get('PASSWORD', default='NOT VALID')
    confirm_password = request.POST.get('CONFIRM PASSWORD', default='NOT VALID')
    global OTP
    if Enter_OTP != OTP:
        messages.error(request,'Invalid OTP, Enter Again')
        return HttpResponseRedirect('/ForgetPassword/CheckUser/')
    elif password != confirm_password:
        messages.error(request,'Password MisMatch')
        return HttpResponseRedirect('/ForgetPassword/CheckUser/')
    else:
        global EnterUser
        user = User.objects.get(username=EnterUser)
        user.set_password(password)
        user.save()
        return HttpResponse("""<meta http-equiv="refresh" content = "0;url=http://127.0.0.1:8000/" /><title>Password Saved</title><script>alert('Password Saved')</script>""")


def Contact_Us(request):
    username = request.POST.get('USERNAME', default='NOT VALID').upper()
    try:
        if len(username) != 10 or (int(username[0:2]) < 16 and int(username[0:2]) > 19) or username[2:5] != 'EGJ' or int(username[7:10]) > 400:
            return HttpResponse('''<meta http-equiv="refresh" content="0;url='/' " ><title>Invalid Roll No</title>"<script>alert('Invalid Roll No')</script>''')
    except:
        return HttpResponse('''<meta http-equiv="refresh" content="0;url='/' " ><title>Invalid Roll No</title>"<script>alert('Invalid Roll No')</script>''')
    email = request.POST.get('EMAIL', default='NOT VALID')
    if '@' not in email or '.com' != email[-4:]:
        return HttpResponse(
            '''<meta http-equiv="refresh" content="0;url='/' " ><title>Invalid Email ID</title>"<script>alert('Invalid Email ID')</script>''')
    description = request.POST.get('DESCRIPTION', default='NOT VALID')
    if description == 'NOT VALID':
        return HttpResponse(
            '''<meta http-equiv="refresh" content="0;url='/' " ><title>Message is Empty</title>"<script>alert('Message is Empty')</script>''')
    try:
        Contact_Us_Login(roll_no=username, email=email, description=description).save()
        return HttpResponse('''<meta http-equiv="refresh" content="0;url='/' " ><title>Saved</title>"<script>alert('We will Contact you in 24 hrs')</script>''')
    except:
        return HttpResponse('''<meta http-equiv="refresh" content="0;url='/' " ><title>Error</title>"<script>alert('This Roll No has already Registered Sent the Data')</script>''')


def Logout(request):
    global EnterUser
    EnterUser=''
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse('''<meta http-equiv="refresh" content="0;url='/' " ><title>Logout</title>"<script>alert('You have Logged Out Successfully')</script>''')
    else:
        return HttpResponse('''<meta http-equiv="refresh" content="0;url='/' " ><title>Logout</title>"<script>alert('You Were Not Logged In, Please Login For More Functionality ')</script>''')
