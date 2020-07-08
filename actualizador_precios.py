from MercadoLibre_bot import MercadoLibreBot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
import smtplib
import time

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}



class PriceUpdater(object):
    def __init__(self, spreadsheet_name):
        self.item_col = 1
        self.precio_col = 2
        self.imagen_url_col = 3
        self.nombre_produc_col = 4


        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive.file',
                 'https://www.googleapis.com/auth/drive']

        creds = ServiceAccountCredentials.from_json_keyfile_name('cliente.json', scope)

        client = gspread.authorize(creds)
        self.sheet = client.open(spreadsheet_name).sheet1

    def process_items_list(self):
        items = self.sheet.col_values(self.item_col)[1:]
        print(len(items))
        print(" Articulos para buscar....")
        MercadoLibre_bot = MercadoLibreBot(items)
        precios, urls, nombres = MercadoLibre_bot.search_items()

        for j in range(len(precios)):

            self.sheet.update_cell(j+2, self.precio_col, precios[j])
            self.sheet.update_cell(j + 2, self.imagen_url_col, urls[j])
            self.sheet.update_cell(j + 2, self.nombre_produc_col, nombres[j])

        print("Hoja de Calculo Actualizada")


def menu():
    print("-------------------------------------------------------------------------------------------------------------")
    print("TRABAJO FINAL RECUPERACION AVANZADA DE INFORMACIÓN")
    print("")
    print ("Selecciona una opción")
    print ("\t1 - primera opción: Realizar la busqueda, comparacion y almacenamiento de 15 articulos en Mercado Libre")
    print ("\t2 - segunda opción: Monitoreo de un articulo de Mercado Libre con Alerta")
    print ("\t9 - salir")
    print("-------------------------------------------------------------------------------------------------------------")


while True:
    # Mostramos el menu
    menu()

    # solicituamos una opción al usuario
    opcionMenu = input("inserta un numero valor >> ")

    if opcionMenu == "1":
        print("")
        input("Has pulsado la opción 1...\npulsa una tecla para continuar")
        price_updater = PriceUpdater("Productos")
        price_updater.process_items_list()
    elif opcionMenu == "2":
        print("")
        input("Has pulsado la opción 2...\npulsa una tecla para continuar")
        URL = input("Pega url de algun articulo de Mercado Libre:   ")
        def chek_price():
            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.find("title").text
            price = soup.find('span', class_='price-tag ui-pdp-price__part').text

            print("\n"+price)
            print(title+"\n")
            send_mail()

        def send_mail():
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login('gastonruiz957@gmail.com', 'mhlyljedvrhdwjka')
            subject = 'PRECIO ACTUAL DE TU PRODUCTO!'
            body = 'Mira el siguiente Link ' + URL
            msg = f"Subject: {subject}\n\n{body}"
            server.sendmail(
                'gastonruiz957@gmail.com',
                'gastonruiz96@yahoo.com',
                msg
            )
            print('EMAIL HA SIDO ENVIADO')
            server.quit()


        #while(True):
        chek_price()
           # time.sleep(60*60)
    elif opcionMenu == "9":
        break
    else:
        print("")
        input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")






