from django.urls import path
from blockchain import views

app_name = 'blockchain'

urlpatterns = [
    path('',views.index,name='home'),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('signup/',views.signup,name="signup"),
    path('file-upload/',views.user_file_upload,name="user_file_upload"),
    path('user_files/',views.user_files,name="user_files"),
    path('file_details/<int:pk>',views.file_details,name="file_details"),

]
