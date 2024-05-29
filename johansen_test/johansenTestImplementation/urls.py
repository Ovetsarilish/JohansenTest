from django.urls import path
from . import views

urlpatterns = [
    path('johansenTestImplementation/', views.fun_met, name='johansenTestImplementation'),
]
