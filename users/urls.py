from django.urls import include, path

from . import views

urlpatterns = [
    path('reg/', views.SignUp.as_view(), name='reg'),
   # path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path("", include("django.contrib.auth.urls")),
]
