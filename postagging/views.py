from django.shortcuts import render
from django.http import HttpResponse
from konlpy.tag import Twitter, Kkma, Komoran


def index(request):
    message = ''
    tagger = ''
    list_of_tagger = ''
    if request.method == 'POST':
        input_sentence = request.POST.get("name", "")
        list_of_tagger = request.POST.getlist("tagger")
        if 'selectall' in list_of_tagger:
            list_of_tagger = ['moara', 'twitter', 'kkma', 'komoran']
            
        if input_sentence != '':
            if 'moara' in list_of_tagger:
                # ======== 모아라 형태소 분석기 ========
                from subprocess import Popen, PIPE, STDOUT
                import os
                import re
                p = Popen(['java', '-jar', 'C:/Users/bessh4/Desktop/mysite/postagging/moara_pos.jar', input_sentence], stdout=PIPE, stderr=STDOUT, shell=True)
                output = [line.decode('cp949') for line in p.stdout]

                print_moara = []
                print_moara2 = []
                for i in output[2:]:
                    if i != "\n":
                        if i != '\r\n':
                            print_moara2.append(i.split(", ")[0][1:] + " / " + i.split(", ")[1])
                            
                string_i = ''
                for i in print_moara2:
                    word_i = i.split('단어음절: ')[1].split(" / ")[0]
                    pos_i = i.split('단어품사: ')[1]
                    if len(re.findall(r'\bRECOMMEND\S+\b', pos_i)) == 0:
                        string_i += word_i + "/" + pos_i + " "
                        
                print_moara = ("모아라", string_i)
            else:
                print_moara = ("모아라", "")
            
            # ======== konlpy 형태소 분석기 ========
            if 'twitter' in list_of_tagger:
                twitter_str = ''
                twitter = Twitter()
                for i in twitter.pos(input_sentence):
                    twitter_str += str(i[0] + "/" + i[1] + " ")
                twitter_message = ("트위터", twitter_str)
            else:
                twitter_message = ("트위터", "")
                
            if 'kkma' in list_of_tagger:
                kkma_str = ''
                kkma = Kkma()
                for i in kkma.pos(input_sentence):
                    kkma_str += str(i[0] + "/" + i[1] + " ")
                kkma_message = ("꼬꼬마", kkma_str)
            else:
                kkma_message = ("꼬꼬마", "")
                
            if 'komoran' in list_of_tagger:
                komoran_str = ''
                komoran = Komoran()
                for i in komoran.pos(input_sentence):
                    komoran_str += str(i[0] + "/" + i[1] + " ")
                komoran_message =  ("코모란", komoran_str)
            else:
                komoran_message = ("코모란", "")
            
            message = [print_moara, twitter_message, kkma_message, komoran_message]
                
        else:
            message = "형태소 분석할 문장을 입력하세요"
        
    context = {'message': message}
    return render(request, 'postagging/index.html', context)