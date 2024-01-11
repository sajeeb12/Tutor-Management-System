from django.urls import path
from .views import loginuser,logoutuser,registration,change_password,userProfile,ownerprofile

app_name='session'
urlpatterns=[
   path('login/',loginuser,name="login"), 
   path('logout/',logoutuser,name="logout"),
   path('signup/',registration,name="signup"),
   path('password/',change_password,name="password"),
   path('userpro/',userProfile,name="userProfile"),
   path('ownerprofile/',ownerprofile,name="ownerprofile"),
]