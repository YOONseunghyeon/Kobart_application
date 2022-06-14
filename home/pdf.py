import fitz
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

def get_text(path, pdf) :        
    file = extract_pages(path + '/' + pdf)
    return [element.get_text() for page_layout in file for element in page_layout if isinstance(element, LTTextContainer)]

def clean_text(texts) :
    temp = [text.replace('\n', '') for text in texts]
    return [' '.join(t.split()) for t in temp]

def get_clean_text(path, file) :
    return clean_text(get_text(path, file))

def istitle(text) :
    if text.count('.') != 1 :
        return False
    numbers = ['I', 'V', 'X', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    for num in text.split('.')[0] :
        if num not in numbers :
            return False
    return True

def get_title(texts) :
    return [text for text in texts if istitle(text)]

def extract_para(text, start_idx, end_idx) :
    return [text[i] for i in range(start_idx, end_idx)]

def get_title_idx(texts, titles) :
    
    indices = []
    idx     = 0
    for i in range(len(texts)) :
        if texts[i] == titles[idx] :
            idx += 1
            indices.append(i)
            if idx == len(titles) :
                break
    return indices

def get_para(text, title_idx) :
    idx = title_idx.copy()
    idx.append(len(text))
    return [text[idx[i] : idx[i + 1]] for i in range(len(idx) - 1) ]

def paragraph(text, title) :
    idx   = get_title_idx(text, title)
    paras = get_para(text, idx)
    return [' '.join(para) for para in paras]

def slicing(para) :
    temp   = []
    c      = 512
    string = ''
    for text in para.split('.') :
        if len(string) + len(text) > c :
            temp.append(string)
            string = text + '.'
        else :
            string += text + '.'
    temp.append(string)
    return temp

def preprocessing(path, file) :
    ct     = get_clean_text(path, file)
    titles = get_title(ct)
    paras  = paragraph(ct, titles)
    return [slicing(para) for para in paras]

def save_images(path, pdf) :
    
    folder    = 'final/static/img/'
    open_file = fitz.open(path + '/' + pdf)
    for i in range(len(open_file)):
        for img in open_file.getPageImageList(i):
            xref = img[0]
            pix  = fitz.Pixmap(open_file, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.save(folder + "p%s-%s.png" % (i, xref))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.save(fitz.csRGB, pix)
                pix1.save(folder + "p%s-%s.png" % (i, xref))
                pix1 = None
            pix = None
            