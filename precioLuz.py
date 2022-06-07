import requests
import logging
import os
from telegram import (ParseMode)
from telegram.ext import (Updater, CommandHandler)
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

headers = {
    "Accept" : "application/json",
    "Content-Type" : "application/json"
}


def allPrice():
    url = "https://api.preciodelaluz.org/v1/prices/all?zone=PCB"
    res = requests.request("GET", url, headers=headers)
    return res.json()

def minPrice():
    url = "https://api.preciodelaluz.org/v1/prices/min?zone=PCB"
    res = requests.request("GET", url, headers=headers)
    return res.json()

def maxPrice():
    url = "https://api.preciodelaluz.org/v1/prices/max?zone=PCB"
    res = requests.request("GET", url, headers=headers)    
    return res.json()

def avgPrice():
    url = "https://api.preciodelaluz.org/v1/prices/avg?zone=PCB"
    res = requests.request("GET", url, headers=headers)
    return res.json()

def nowPrice():
    url = "https://api.preciodelaluz.org/v1/prices/now?zone=PCB"
    res = requests.request("GET", url, headers=headers)
    return res.json()

def bestPrice():
    url = "https://api.preciodelaluz.org/v1/prices/cheapests?zone=PCB&n=2"
    res = requests.request("GET", url, headers=headers)
    return res.json()

def cheapPrice():
    url = "https://api.preciodelaluz.org/v1/prices/cheapests?zone=PCB&n=2"
    res = requests.request("GET", url, headers=headers)
    return res.json()

def getBeautifulHours(horas):

    hours = {'start':"", 'end':""}

    separador = horas.find("-")

    start = horas[0:separador]
    end = horas[separador:len(horas)]
    end = end.replace("-", "")
    start = start + ":00"
    end = end + ":00"

    hours["end"] = end
    hours["start"] = start

    return hours


def resume():
    media = avgPrice()
    maximo = maxPrice()
    minimo = minPrice()
    
    horasCaras = getBeautifulHours(maximo["hour"])
    horasBaratas = getBeautifulHours(minimo["hour"])


    msg = "El precio medio de la luz hoy será de %s €. La hora más cara será de %s a %s y costará %s €. La hora más barata será de %s a %s y costará %s €." % (media["price"], horasCaras["start"], horasCaras["end"], maximo["price"], horasBaratas["start"], horasBaratas["end"], minimo["price"])

    return msg

def getResume(update, context):
    update.message.reply_text(resume())

def getMax(update, context):
    maximo = maxPrice()
    horasCaras = getBeautifulHours(maximo["hour"])

    msg = "Hoy la luz será más cara de %s a %s y costará %s €" % (horasCaras["start"], horasCaras["end"], maximo["price"])
    update.message.reply_text(msg)

def getMin(update, context):
    minimo = minPrice()
    horasCaras = getBeautifulHours(minimo["hour"])

    msg = "Hoy la luz será más cara de %s a %s y costará %s €" % (horasCaras["start"], horasCaras["end"], minimo["price"])
    update.message.reply_text(msg)

def getAvg(update, context):
    avg = avgPrice()
    
    msg = "Hoy el precio será de %s el %s" % ( avg["price"], avg["units"])
    update.message.reply_text(msg)

def getNow(update, context):
    ahora = nowPrice()
    horas = getBeautifulHours(ahora["hour"])

    msg = "El precio ahora y hasta las %s será de %s€ el %s " % (horas["end"], ahora["price"], ahora["units"])
    update.message.reply_text(msg)

def bestHours():
    menorPrecio = cheapPrice()
    franjas = []

    for precios in menorPrecio: 
        horario = getBeautifulHours(precios["hour"])
        franja = {'start': horario["start"], 'end': horario["end"], 'price': precios["price"], 'units':precios["units"] }
        franjas.append(franja)
        
    return franjas

def getCheap(update, context):
    best = bestHours()

    for i in best:
        msg = "Hoy la luz será más barata entre las %s y las %s. El precio será de %s el %s \n" % (i["start"], i["end"], i["price"], i["units"])        
        update.message.reply_text(msg)

def getAllPrice(update, context):
    tarifas = allPrice()
    horas = tarifas.keys()

    horarios = []
    precios = []

    #Enviamos un mensaje con el precio de cada hora
    for h in horas: 
        tarifa = tarifas[h]        
        hora = getBeautifulHours(tarifa["hour"])
        
        s = hora["start"]
        separador = s.find(":")
        s = s[0:separador]
        horarios.append(int(s))
        precios.append(tarifa["price"])
        msg += "A las  %s el precio será de %s el %s \n" % (hora["start"], tarifa["price"], tarifa["units"])
        
    
    update.message.reply_text(msg)
    
    #Generamos la grafica y la enviamos
    fig, ax = plt.subplots()  
    ax.plot(horarios, precios)
    ax.set(xlabel='Horas', ylabel='Precio (€)',
       title='Evolución del precio de la luz hoy %s ' % tarifa["date"])
    ax.grid()
    plt.savefig('hoy.png')
    plt.show()

    update.message.reply_photo(photo=open('hoy.png', 'rb'))


def main():    
    TOKEN = os.environ["TELEGRAM_TOKEN"]
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Comandos a los que va a responder nuestro bot
    dp.add_handler(CommandHandler('resumen',    getResume))
    dp.add_handler(CommandHandler('maximo',     getMax))
    dp.add_handler(CommandHandler('minimo',     getMin))
    dp.add_handler(CommandHandler('media',      getAvg))
    dp.add_handler(CommandHandler('mejores',    getCheap))
    dp.add_handler(CommandHandler('hoy',    getAllPrice))

    # En caso de error
    dp.add_error_handler(error_callback)

    #Arrancar el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("Bot inicializado")
    main()