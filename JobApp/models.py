from django.db import models
from django.conf import settings
# Create your models here.
class JobDb(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.CharField(max_length=50)
    job_type= models.CharField(max_length=100)
    experience_required = models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ApplicationDb(models.Model):
    job = models.ForeignKey(JobDb,on_delete=models.CASCADE)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE)
    applied_at =models.DateTimeField(auto_now_add=True)

