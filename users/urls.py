from django.urls import path, include

from . import views


urlpatterns = [
    #path('login/', views.LoginView.as_view(template_name='users/authForm.html',), name='login'),
  #  path('register/', register, name="register"),
    path("reg", views.register, name="reg"),
    path("", include("django.contrib.auth.urls"))
]