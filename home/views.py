from django.http import HttpResponse
from django.shortcuts import render
from .form import UploadForm, Document
from .kobart import Kobart
from .pdf import save_images, preprocessing, get_clean_text

import os
# Create your views here.

def index(request) :
    return render(request, 'index.html')

def about(request) :
    return render(request, 'about.html')

def contact(request) :
    return render(request, 'contact.html')

def summary(request) :
    return render(request, 'summary.html')

def make_dict(text, summary, imgs) :
    return { 'text'    : text,
             'summary' : summary,
             'img'     : imgs
            }

def get_post(request) :
    img_path = 'final\static\img'
    path     = 'media'
    files    = os.listdir(path)
    kobart   = Kobart()
    
    if request.method == 'POST' :
        text = request.POST['text']
        word = request.POST['word']
        line = int(request.POST['line'])

        try :
            pdf = request.FILES['pdf']
            if pdf.name not in files :
                doc       = Document()
                doc.title = pdf.name
                doc.pdf   = pdf
                doc.save()
                save_images(path, doc.title)
            pp = preprocessing(path, pdf.name)
            string = ''
            for p in pp :
                string += kobart.summary(p[0])
                
            context = make_dict(get_clean_text(path, pdf.name), string, os.listdir(img_path))
        except :
            context = make_dict(text, kobart.summary(text), [])
            
    else :
        uf = UploadForm
        context = make_dict('text', 'summ', [])
    return render(request, 'result.html', context)

    