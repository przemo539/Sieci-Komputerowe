from socket import *
import os
import time
import json
serwer = socket(AF_INET, SOCK_STREAM) #utworzenie gniazda
serwer.connect(('localhost', 8888)) # nawiazanie polaczenia


choice = -100000
while True:
    os.system("cls")
    print(" 1.Wyswietl liste zadan \n 2.Dodaj zadanie \n 3.Usun zadanie\n 4.Wyswielt liste z danym priorytetem\n 5.Koniec programu")


    if choice == 1:
        print("LISTA ZADAN:")
        serwer.send("TYPE_SHOW_TASK".encode())
        data = serwer.recv(1024)
        b = b''
        b += data
        d = json.loads(b.decode('utf-8'))
        for tmp in d["zadania"]:
            print("ID: "+str(tmp["id"]))
            print("PRIORYTET: "+str(tmp["priorytet"]))
            print("OPIS: "+tmp["opis"]+"\n")
    elif choice == 2:
        print("TWORZENIE ZADANIA: ")
        print("Podaj priorytet(1-10):")
        priorytet = input()
        print("Opis zadania:")
        opis = input()
        serwer.send("TYPE_ADD_TASK_JSON".encode())  # wyslanie naglowka
        id = serwer.recv(1024)  # odbiorid
        json_data = {'id': int(id.decode()), 'priorytet': int(priorytet), 'opis': opis }
        data = json.dumps(json_data).encode('utf-8')
        serwer.sendall(data)

        if int(id.decode()) > 0:
            print('\n\nDODANO POPRAWNIE ZADANIE O ID: ', id.decode())
        else:
            print('\n\nPRZEPRASZAMY WYSTAPIL BLAD')
    elif choice == 3:
        serwer.send("TYPE_DELETE_TASK".encode())
        print("PODAJ ID ZADANIA DO USUNIECIA:")
        id = input()
        serwer.send(id.encode())
        stan = serwer.recv(1024)
        print(stan.decode())
    elif choice == 4:
        print("PODAJ PRIORYTET DO WYSWIETLENIA:")
        priorytet = input()
        serwer.send("TYPE_SHOW_TASK_BY_PRIORITY".encode())
        serwer.send(priorytet.encode())
        json_data = serwer.recv(1024)
        b = b''
        b += json_data
        data = json.loads(b.decode('utf-8'))
        #print(data)
        print("ZADANIA Z PRIORYTETEM: "+priorytet)
        for element in data:
            print("ID: " + str(element["id"]))
            print("PRIORYTET: " + str(element["priorytet"]))
            print("OPIS: " + element["opis"] + "\n")
    if choice == 5:
        print("Dziekujemy za uzywanie programu!")
        break
    elif ((choice > 5 or choice < 0) and choice !=-100000):
        print("Niepoprawny wybor")
    choice = input("\nWybierz:")
    try: choice=int(choice)
    except: choice=-10


serwer.close()
