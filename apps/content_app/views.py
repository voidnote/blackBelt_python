from django.shortcuts import render, redirect
from ..first_app.models import User
from .models import Appt
from django.contrib import messages
from datetime import datetime, date, time


def main(request):
	if not request.session["user_id"]:
		return redirect("login:logout")
	this_user = User.objects.get(id=request.session["user_id"])
	context = {
		"this_user" : this_user,
		"today" : datetime.now().date(),
		"appts_today" : Appt.objects.filter(date=datetime.now().date()).filter(created_by=this_user).order_by('time'),
		"other_appt" : Appt.objects.exclude(date=datetime.now().date()).filter(created_by=this_user).order_by('date'),
	}
	return render(request, "content_app/main.html", context)

def process(request, userid):
	if not request.session["user_id"]:
		return redirect("login:logout")
	if request.method == "POST":
		response_from_models = Appt.objects.createAppt(request.POST, userid)
		if not response_from_models["status"]:
			for error in response_from_models["errorStr"]:
				messages.error(request, error)
			return redirect("content:mainpage")
	return redirect("content:mainpage")


def edit(request, apptid):
	if not request.session["user_id"]:
		return redirect("login:logout")
	this_appt = Appt.objects.get(id=apptid)
	context = {
		"this_appt" : this_appt,
		"this_date" : datetime.strftime(this_appt.date, "%Y-%m-%d"),
		"this_time" : time.strftime(this_appt.time, "%H:%M"),
	}
	return render(request, "content_app/edit.html", context)

def update(request, apptid):
	if not request.session["user_id"]:
		return redirect("login:logout")
	if request.method == "POST":
		response_from_models = Appt.objects.updateAppt(request.POST, apptid)
		if not response_from_models["status"]:
			for error in response_from_models["errorStr"]:
				messages.error(request, error)
			return redirect("content:edit")
	return redirect("content:mainpage")

def delete(request, apptid):
	if not request.session["user_id"]:
		return redirect("login:logout")
	this_appt = Appt.objects.get(id=apptid)
	this_appt.delete()
	return redirect("content:mainpage")
