import re
from bot import wppbot

bot = wppbot('Luna')
# bot.treina('treino')
bot.inicia('ChatBot Python - Selenium')
bot.saudacao(['Bot: Oi, sou a Luna um chatbot que vai te dar dinheiro!','Bot: Use :: para falar alguam coisa comigo.'])
ultimo_texto = ''



while True:

    texto = bot.escuta()

    if texto != ultimo_texto and re.match(r'^::', texto):

        ultimo_texto = texto
        texto = texto.replace('::', '')
        texto = texto.lower()

        if (texto == 'aprender' or texto == ' aprender' or texto == 'ensinar' or texto == ' ensinar'):
            bot.aprender(texto,'bot: Escreva a pergunta e após o ? a resposta.','bot: Obrigado por ensinar! Agora já sei!','bot: Você escreveu algo errado! Comece novamente..')
        elif (texto == 'noticias' or texto == ' noticias' or texto == 'noticia' or texto == ' noticia' or texto == 'notícias' or texto == ' notícias' or texto == 'notícia' or texto == ' notícia'):
            bot.noticias()
        else:
            bot.responde(texto)