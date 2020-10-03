from django.urls import path,include
from .views import *
urlpatterns = [
    path('', Login),
    path('Auth/', Auth),
    path('SignUp/', SignUp),
    path('SignUp/SignUpOTP/', SignUpOTP),
    path('SignUp/SignUpOTP/CreateUser/', CreateUser),
    path('ForgetPassword/', ForgetPassword),
    path('ForgetPassword/CheckUser/', CheckUser),
    path('ForgetPassword/CheckUser/ResetPassword/',ResetPassword),
    path('Dashboard/',include('students.urls')),
    path('ContactLogin/', Contact_Us),
    path('Logout/',Logout)
]