#libraries
import streamlit as st
from PIL import Image
from io import BytesIO
import requests
import pandas as pd
import altair as alt
#import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import datetime
import numpy as np
#https://stackoverflow.com/questions/65577892/error-message-http-not-defined-api-import-python
import urllib3
from urllib3 import request
# json data
import json
#SMTP
import smtplib
import time
import email
#import openai

from datetime import datetime
from datetime import date
import pytz
datetime_br= datetime.now(pytz.timezone('America/Sao_Paulo'))
#t = datetime_br.strftime('%d:%m:%Y %H:%M:%S')
t = datetime_br.strftime('%d:%m:%Y %H:%M')

def mailSEND(CC, ASSUNTO, Mensagem):
    ################# SMTP SSL ################################
    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as smtp_ssl:
        # print("Connection Object : {}".format(smtp_ssl))

        ######### Log In to mail account ############################
        #print("\nLogging In.....")
        resp_code, response = smtp_ssl.login(user="prof.massaki@gmail.com", password="makchgxvssjzogky")

        #print("Response Code : {}".format(resp_code))
        #print("Response      : {}".format(response.decode()))

        ################ Send Mail ########################
        #print("\nSending Mail..........")

        message = email.message.EmailMessage()

        message["From"] = "prof.massaki@gmail.com"
        message["To"] = ["massakiigarashi2+ayypihj49agm7qwz6k3w@boards.trello.com", ]
        message["cc"] = [CC,]
        message["Bcc"] = ["backupdomassaki@gmail.com", ]

        message["Subject"] =  ASSUNTO

        #body = '''
        #Olá,
        #Este é um e-mail teste do WebappSEG.
        #Obrigado pela atenção,
        #Prof. Massaki
        #'''
        body = "Obrigado por contribuir com sua ideia. A seguir Conteúdo relacionado pesquisado no ChatGPT3: " + Mensagem
        message.set_content(body)

        ### Send Message
        response = smtp_ssl.send_message(msg=message)
        #print("List of Failed Recipients : {}".format(response))
        return "OK"

#def GPT3(assuntoBUSCA):
    #openai.api_key = "....."
    #MODEL = "gpt-3.5-turbo"
    #CONTENT = "Pesquise inovações relacionadas a " + assuntoBUSCA
    #response = openai.ChatCompletion.create(model=MODEL, messages=[{"role": "user", "content": CONTENT}])
    #return response.choices[0].message.content

def Graph(wordcloud, wordfreq,wordlist):
    plt.imshow(wordcloud);
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    #st.pyplot()
    wordcloud.to_file("Nuvem_de_Palavras_Ideacao.png")

    st.header("Nuvem de Palavras das IDEIAS:")
    st.pyplot() #Este método faz exibirt a nuvem de palavras
    st.set_option('deprecation.showPyplotGlobalUse', False)
    chart_data = pd.DataFrame(wordfreq,wordlist)
    st.bar_chart(chart_data)
    
http = urllib3.PoolManager()
rD = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vRUgDjGeiyn2AXcZKsB5v8YzJE3iL7AWboi4L_Zrn9heRi1PKAGVhSaG4-OapTNduwOLc6XxDw0KKrB/pub?gid=689726290&single=true&output=csv')
dataD = rD.content
dfD = pd.read_csv(BytesIO(dataD), index_col=0)
NregD = len(dfD)

st.title("WebApp GESTÃO DE INOVAÇÃO")
# eliminar as colunas com valores ausentes
summary = dfD.dropna(subset=['Mensagem'], axis=0)['Mensagem']
# concatenar as palavras
all_summary = " ".join(s for s in summary)
# lista de stopword
stopwords = set(STOPWORDS)
stopwords.update(["de", "ao", "o", "nao", "para", "da", "meu", "em", "você", "ter", "um", "ou", "os", "ser", "só"])
# gerar uma wordcloud
wordcloud = WordCloud(stopwords=stopwords,
                      background_color="white",
                      width=1600, height=800).generate(all_summary)

wordlist = all_summary.split()
wordfreq = []
for w in wordlist:
    wordfreq.append(wordlist.count(w))

#st.info("Lista\n" + str(wordlist) + "\n")
#st.info("Frequências\n" + str(wordfreq) + "\n")
#st.info("Pares\n" + str(list(zip(wordlist, wordfreq))))


form = st.form('FormularioCADASTRO')
IDEIA = form.text_input('Sua ideia:')
NOME = form.text_input('NOME')
MAIL = form.text_input('e-mail')
link = 'https://docs.google.com/forms/d/e/1FAIpQLScSYzAW0ze2ChpreG0PZqdxf45wTJMwCqr92LeupYm8z0QTyg/formResponse?&submit=Submit?usp=pp_url&entry.1680586862='
link += str(IDEIA)+'&entry.158598808=X'+'&entry.1211796870='+str(NOME)+'&entry.472409006='+str(MAIL)
submit = form.form_submit_button('✔️ ENVIAR')
if submit:
    r = http.request('GET', link)
    #st.info(r.status)        
    #resp = GPT3(IDEIA)    
    #confirmaENVIO = mailSEND(MAIL, NOME + "(" + str(t) + "): " + IDEIA, resp)
    confirmaENVIO = mailSEND(MAIL, NOME + "(" + str(t) + "): " + IDEIA)
    if confirmaENVIO=="OK":
        st.success("Envio confirmado!")
    Graph(wordcloud, wordfreq,wordlist)
    #st.success("A seguir, um conteúdo de pesquisa realizada com sua ideia no ChatGPT3. Isto talvez possa lhe ajudar no desenvolvimento de sua ideia! " + resp)


st.info("Desenvolvido por: Equipe FabLab / Prof. Massaki de O. Igarashi")
