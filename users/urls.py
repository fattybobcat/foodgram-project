from django.urls import path, include

from . import views


urlpatterns = [
    path('reg/', views.SignUp.as_view(), name='reg'),
    path("", include("django.contrib.auth.urls")),
]
