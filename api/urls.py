from django.urls import path
from .views import *

urlpatterns = [
	path('login',Login.as_view()),
	path('task',Task.as_view()),
	path('comment',Comment.as_view()),
	path('notification',Notification.as_view())
]