from django.http import HttpResponse
from django.shortcuts import render
from .form import UploadForm, Document
from .kobart import Kobart
from .sts import Sts
from .ptt import save_images, preprocessing, \
    get_clean_text, slicing, set_figure, make_pdf

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

def get_para_list(word, pp) :
    para_list = []
    if word == '' :
        para_list = set([p[0] for p in pp])
    else :
        para_list = set([p[0] for p in pp for text in p[1] if word in text])
    return para_list

def get_output(para_sum, result, string):
    temp = []
    sentences = [string[idx] for idx in result]
    
    for sentence in sentences :
        for para in para_sum :
            if sentence in para[1] :
                temp.append((para[0], sentence))
    return temp
      
def get_post(request) :
    img_path = 'final\static\img'
    path     = 'media'
    files    = os.listdir(path)
    kobart   = Kobart()
    sts      = Sts()
    
    if request.method == 'POST' :
        text = request.POST['text']
        word = request.POST['word']
        line = int(request.POST['line'])
        sts.set_line(line)

        try :   ## pdf
            pdf = request.FILES['pdf']
            if pdf.name not in files :
                doc       = Document()
                doc.title = pdf.name
                doc.pdf   = pdf
                doc.save()
                save_images(path, doc.title)
            pp        = preprocessing(path + '/' + pdf.name)
            img_list  = set_figure(pp, img_path)
            para_list = get_para_list(word, pp)
    
            para_sum  = kobart.para_summary(pp, para_list) # 문단별 요약
            string    = [text for texts in para_sum for text in texts[1]]
            
            sts.set_corpus(string)      # sts    
            query     = kobart.summary(''.join(string))
            result    = sts.similarity(query)
            output    = get_output(para_sum, result, string)
            context   = make_dict(' '.join(get_clean_text(path + '/' + pdf.name)), ' '.join([text[1] for text in output]), os.listdir(img_path))
            make_pdf(output, img_list, 'final/static/pdf/new_' + pdf.name) 
            
        except :  ## text
            pp = slicing(text)
            string = ''
            for p in pp :
                string += kobart.summary(p)
            context = make_dict(word, string, [])
            
    else :
        uf = UploadForm
        context = make_dict('text', 'summ', [])
    return render(request, 'result.html', context)

    