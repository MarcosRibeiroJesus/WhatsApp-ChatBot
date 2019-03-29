import os
import time
import re
import requests
import json
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from selenium import webdriver


class wppbot:

    dir_path = '.'
    bot = ChatBot('Ron Obvious')

    # Create a new trainer for the chatbot
    trainer = ChatterBotCorpusTrainer(bot)

    # Train the chatbot based on the english corpus
    trainer.train("chatterbot.corpus.english")
    trainer.train("chatterbot.corpus.portuguese")
    
    def __init__(self, nome_bot):
        print(self.dir_path)
        # self.bot = ChatBot('Luna')
        # trainer = ChatterBotCorpusTrainer(bot)
        # self.chrome = self.dir_path+'\chromedriver'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir="+self.dir_path+"\profile\wpp")
        # self.driver = webdriver.Chrome('/home/mrj/Projects/Python/First/chromedriver',chrome_options=self.options)
        self.driver = webdriver.Chrome(chrome_options=self.options)
        # self.driver = webdriver.Chrome()

    def inicia(self, nome_contato):

        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(25)

        self.caixa_de_pesquisa = self.driver.find_element_by_class_name(
            'jN-F5')

        self.caixa_de_pesquisa.send_keys(nome_contato)
        time.sleep(2)
        print(nome_contato)
        self.contato = self.driver.find_element_by_xpath(
            '//span[@title = "{}"]'.format(nome_contato))
        self.contato.click()
        time.sleep(2)

    def saudacao(self, frase_inicial):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name(
            '_2S1VP')

        if type(frase_inicial) == list:
            for frase in frase_inicial:
                self.caixa_de_mensagem.send_keys(frase)
                time.sleep(1)
                self.botao_enviar = self.driver.find_element_by_class_name(
                    '_35EW6')
                self.botao_enviar.click()
                time.sleep(1)
        else:
            return False

    def escuta(self):
        post = self.driver.find_elements_by_class_name('_3_7SH')
        ultimo = len(post) - 1
        texto = post[ultimo].find_element_by_css_selector(
            'span.selectable-text').text
        return texto

    def aprender(self, ultimo_texto, frase_inicial, frase_final, frase_erro):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name(
            '_2S1VP')
        self.caixa_de_mensagem.send_keys(frase_inicial)
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
        self.botao_enviar.click()
        self.x = True
        while self.x == True:
            texto = self.escuta()

            if texto != ultimo_texto and re.match(r'^::', texto):
                if texto.find('?') != -1:
                    ultimo_texto = texto
                    texto = texto.replace('::', '')
                    texto = texto.lower()
                    texto = texto.replace('?', '?*')
                    texto = texto.split('*')
                    novo = []
                    for elemento in texto:
                        elemento = elemento.strip()
                        novo.append(elemento)

                    self.bot.train(novo)
                    self.caixa_de_mensagem.send_keys(frase_final)
                    time.sleep(1)
                    self.botao_enviar = self.driver.find_element_by_class_name(
                        '_35EW6')
                    self.botao_enviar.click()
                    self.x = False
                    return ultimo_texto
                else:
                    self.caixa_de_mensagem.send_keys(frase_erro)
                    time.sleep(1)
                    self.botao_enviar = self.driver.find_element_by_class_name(
                        '_35EW6')
                    self.botao_enviar.click()
                    self.x = False
                    return ultimo_texto
            else:
                ultimo_texto = texto

    def noticias(self):

        req = requests.get(
            'https://newsapi.org/v2/top-headlines?sources=globo&pageSize=5&apiKey=f6fdb7cb0f2a497d92dbe719a29b197f')
        noticias = json.loads(req.text)

        for news in noticias['articles']:
            titulo = news['title']
            link = news['url']
            new = 'bot: ' + titulo + ' ' + link + '\n'

            self.caixa_de_mensagem.send_keys(new)
            time.sleep(1)

    def responde(self, texto):
        response = self.bot.get_response(texto)
        # if float(response.confidence) > 0.5:
        response = str(response)
        response = 'bot: ' + response
        self.caixa_de_mensagem = self.driver.find_element_by_class_name(
            '_2S1VP')
        self.caixa_de_mensagem.send_keys(response)
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
        self.botao_enviar.click()

    # def treina(self, treino):
    #     for treino in os.listdir('/home/mrj/Projects/Python/First/treino/'):
    #         conversas = trainer.train(
    #         "texto.yml"
    #     )
    #         self.trainer = ChatterBotCorpusTrainer(bot)
    #         self.trainer.train(conversas)

    # def treina():
    #     trainer.train(
    #         "./treino/texto.txt"
    #     )
