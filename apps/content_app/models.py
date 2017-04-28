from __future__ import unicode_literals
from django.db import models
from ..first_app.models import User
from datetime import datetime, date



class ApptManager(models.Manager):
    def createAppt(self, postData, userid):
        errorStr = []
        timeError = 0
        this_user = User.objects.get(id=userid)

        if len(postData['task']) < 1:
            errorStr.append("Task name can't be empty")
        if len(postData['date']) < 1:
            errorStr.append("Date can't be empty")
            timeError += 1
        if len(postData['time']) < 1:
            errorStr.append("Time can't be empty")
            timeError += 1
        
        if timeError == 0:
            appt_date = datetime.strptime(postData["date"], "%Y-%m-%d").date()
            if appt_date < datetime.now().date():
                errorStr.append("Task date must be in the future")
            # QUERY THE DB FOR EXISTING APPOINTMENTS
        if Appt.objects.filter(date=postData['date']).filter(time=postData['time']).filter(created_by=this_user):
            errorStr.append("You already have an appointment at this time")

        response_to_views = {}
        if errorStr:
            response_to_views['status'] = False
            response_to_views['errorStr'] = errorStr
        else:
            appt = self.create(task = postData["task"], created_by = this_user, date = postData["date"], time = postData["time"])
            response_to_views['status'] = True
            response_to_views['appt_obj'] = appt
        return response_to_views

    def updateAppt(self, postData, apptid):
        errorStr = []
        timeError = 0
        this_appt = Appt.objects.get(id=apptid)

        if len(postData['task']) < 1:
            errorStr.append("Task name can't be empty")
        if len(postData['date']) < 1:
            errorStr.append("Date can't be empty")
            timeError += 1
        if len(postData['time']) < 1:
            errorStr.append("Time can't be empty")
            timeError += 1
        
        if timeError == 0:
            appt_date = datetime.strptime(postData["date"], "%Y-%m-%d").date()
            appt_time = datetime.strptime(postData["time"], "%H:%M").time()
            # check to see if they edited the date
            if this_appt.date != postData["date"]:
                # check to see if date is in the future
                if appt_date < datetime.now().date():
                    errorStr.append("Task date must be in the future")

        this_appt.task = postData["task"]
        this_appt.status = postData["status"]
        this_appt.date = postData["date"]
        this_appt.time = postData["time"]
        this_appt.save()
        
        response_to_views = {}
        if errorStr:
            response_to_views['status'] = False
            response_to_views['errorStr'] = errorStr
        else:
            response_to_views['status'] = True
            response_to_views['appt_obj'] = this_appt

        return response_to_views

class Appt(models.Model):
  task = models.TextField(max_length=1000)
  created_by = models.ForeignKey(User, related_name="my_appts")
  date = models.DateField()
  time = models.TimeField()
  status = models.TextField(max_length=1000, default="pending")
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  objects = ApptManager()
  def __str__(self):
    return self.task