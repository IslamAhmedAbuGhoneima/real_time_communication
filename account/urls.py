from django.urls import path
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from . import views
app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html',
                                     form_class=LoginForm), name='login'),
    path('create_user/', views.creat_user, name='creat_user'),
    path('logout/', views.logout_user, name='logout'),

]
