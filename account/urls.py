from django.urls import path
from .views import *
from account.views import *

urlpatterns = [
    path('logout', logout_view, name="logout_view"),

]
