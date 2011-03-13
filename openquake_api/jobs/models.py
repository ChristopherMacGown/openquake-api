from django.db import models

# Create your models here.

STATUSES = (
    ('complete', 'Complete'),
    ('new', 'New'),
    ('running', 'Running'),
)

class Job(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUSES)
    job_hash = models.CharField(max_length=40, unique=True)
    repository = models.FilePathField()


    def save(self):
        print self.created_at
        print self.updated_at
