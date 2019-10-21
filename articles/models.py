from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):

    JOB_STATUS = [
        ('CREATED', 'Job Created By Employer'),
        ('ACCEPTED', 'Job Accepted By Employee'),
        ('COMPLETED', 'Job Completed By Employee'),
    ]

    employer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Job_Creator')
    title = models.CharField(max_length=120)
    content = models.TextField()
    budget = models.IntegerField()
    post_date = models.DateTimeField(auto_now_add=True)
    job_status = models.CharField(
        max_length=8,
        choices=JOB_STATUS,
        default='CREATED',
    )
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='Freelancer')

    def __str__(self):
        return self.title
