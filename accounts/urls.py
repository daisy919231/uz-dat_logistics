from django.urls import path
from accounts import views
app_name='accounts'
urlpatterns=[
    path('register/', views.register_view, name='register'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('home/', views.homepage, name='homepage'),
    path('logout/', views.user_logout, name='logout'),
]