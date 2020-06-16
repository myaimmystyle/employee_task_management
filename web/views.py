from django.shortcuts import render

def Login(request):
	return render(request, "login.html")

def Task(request):
	return render(request, "task.html")

def Dashboard(request):
	return render(request, "dashboard.html")