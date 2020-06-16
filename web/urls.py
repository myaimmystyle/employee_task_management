from django.urls import path
from .views import *

urlpatterns = [
	path('',Login),
	path('task/',Task),
	path('dashboard/',Dashboard)
]