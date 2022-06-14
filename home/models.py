from django.db import models
from django.forms import ModelForm

from numpy import require
# Create your models here.

class Contact(models.Model) :
    name = models.CharField(max_length = 50)
    mail = models.CharField(max_length = 50)
    pnum = models.CharField(max_length = 50)
    msg  = models.TextField()
    
    def __init__(self, name_, mail_, pnum_, msg_) :
        self.name = name_
        self.mail = mail_
        self.pnum = pnum_
        self.msg  =  msg_ 
    
class Document(models.Model) :
    title = models.CharField(max_length = 50)
    pdf   = models.FileField(upload_to = '' )
    
    def __str__(self) :
        return self.title