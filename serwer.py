from socket import *
import json

s = socket(AF_INET, SOCK_STREAM) #utworzenie gniazda
s.bind(('', 8888)) #dowiazanie do portu 8888
s.listen(5)


while 1:
    client,addr = s.accept() # odebranie polaczenia
    with open('todolist.json') as json_file:
        json_data = json.load(json_file)
    while 1:

        print ('Polaczenie z ', addr)
        tm = client.recv(1024)  # odbior danych (max 1024 bajtów)
        if not tm:
            print("Polaczenie zakonczone")
            break
        elif tm.decode() == "TYPE_SHOW_TASK":
            data = json.dumps(json_data).encode('utf-8')
            client.sendall(data)
            print("show")
        elif tm.decode() == "TYPE_ADD_TASK_JSON":
            new_id = int(json_data['liczba_zadan'])+1
            client.send(str.encode(str(new_id)))
            data = client.recv(1024)
            templist = json_data['zadania']
            b = b''
            b += data
            d = json.loads(b.decode('utf-8'))
            templist.append(d)
            json_data['zadania'] = templist
            json_data['liczba_zadan']=new_id
            print(data.decode())
            print("add")
        elif tm.decode() == "TYPE_DELETE_TASK":
            id = client.recv(1024)
            stan = "NIE USUNIETO"
            print(id.decode())
            licznik = 0;
            for element in json_data['zadania']:
                if element["id"] == int(id.decode()):
                    print("try")
                    licznik+=1
                    break
            json_data['zadania'].pop(licznik)
            client.send(stan.encode())
            print("delete")
        elif tm.decode() == "TYPE_SHOW_TASK_BY_PRIORITY":
            priorytet = client.recv(1024)
            templist = []
            for element in json_data['zadania']:
                if element["priorytet"] == int(priorytet.decode()):
                    templist.append(element)
            data = json.dumps(templist).encode('utf-8')
            client.sendall(data)
            print("show priority")

    with open('todolist.json', 'w') as outfile:
        json.dump(json_data, outfile)
    client.close()