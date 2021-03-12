from django.urls import include, path

from . import views

urlpatterns = [
    path('reg/', views.SignUp.as_view(), name='reg'),
    path("", include("django.contrib.auth.urls")),
]
