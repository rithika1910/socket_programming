import socket
from datetime import date
from datetime import timedelta
from PIL import Image
SEPARATOR = ","

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 5001

s.connect((host, port))
lst = [-1, 0, 1, 2, 3]
while True:
    number = int(input("0: View Today's Feedback \n1: Rating Analysis \n2: Performance rate of the week \nEnter option (-1 to break): "))

    if number in lst:
        send_str = str(number)
        if(number == 0):
            date=date.today()
            d1 = date.strftime("%d-%m-%Y")
            print("Today's DATE: "+ str(d1))
            send_str = send_str+SEPARATOR+d1
            s.send(bytes(send_str, 'utf-8'))
            print(s.recv(2048).decode())

        if(number == 1):
            s.send(bytes(send_str, 'utf-8'))
            print(s.recv(2048).decode())
            print("File received...")
            rating=Image.open('rating.png')
            print("File opened..")
            rating.show()

        if(number == 2):
            d1 = date.today()
            d2 = d1 - timedelta(days=7)
            d1 = d1.strftime("%d-%m-%Y")
            d2 = d2.strftime("%d-%m-%Y")
            print("Today's DATE: "+ str(d1))
            print("Last week's DATE: "+str(d2))
            send_str = send_str+SEPARATOR+d1+SEPARATOR+d2
            s.send(bytes(send_str, 'utf-8'))
            print(s.recv(2048).decode())

        if(number == -1):
            break            
    else:
        print("Invalid number!")
    print("\n")
s.close()
