import socket
import _thread as thread
import os
import string
import datetime
import matplotlib.pyplot as plt
from numpy.lib.utils import info
import pandas as pd
import numpy as np
import sys
FORMAT = "utf-8"
SIZE = 2048
FILE ="SalesFile.csv"
file = pd.read_csv(FILE)

SEPARATOR = " "
print("****This is a SERVER program****")
print("--------------------------------")

df = pd.read_csv('customer_care.csv',index_col=0)

def feedback_today(conn_socket, date):
    new_df = df.loc[df['DATE'] == date]
    new_df.to_csv('today_feedback.csv',index=False)
    conn_socket.send(bytes(new_df.to_string(), 'utf-8'))
    try:
        pass
    except:
        conn_socket.send(b"Operation failed!")

def rating_analysis(conn_socket):
    y=list(df["RATING"].value_counts())
    x=[5,4,3,2,1]
    plt.bar(x,y,color='r')
    plt.title("CUSTOMER RATING")
    plt.xlabel("Stars")
    plt.ylabel("Number of customers")
    plt.savefig('rating.png', dpi=300, bbox_inches='tight')
    conn_socket.send(bytes('rating.png', 'utf-8'))
    try:
        pass
    except:
        conn_socket.send(b"Operation failed!")

def week_performance(conn_socket, d1,d2):
    week=[]
    fd=open("Week_performance.txt",'w')
    fd.write("Last week's DATE (from): "+ str(d1) + "\nToday's DATE (to): "+str(d2))
    d1 = datetime.datetime.strptime(d1, '%d-%m-%Y')
    d2 = datetime.datetime.strptime(d2, '%d-%m-%Y')
    step = datetime.timedelta(days=1)
    while d2 <= d1:
        week.append(d2.strftime("%d-%m-%Y"))
        d2 += step
    new_df= df.loc[df['DATE'].isin(week)]
    perc= ((new_df['RATING'].sum())/(5*len(new_df)))*100
    info= "\nMEAN : "+ str(round(new_df['RATING'].mean(axis=0),3)) + "\nMAX : "+ str(new_df['RATING'].max()) + "\nMIN : "+ str(new_df['RATING'].min()) + "\n\t***WEEK'S PERFORMANCE RATE*** : "+str(round(perc,3))+"%"
    fd.write(info)
    fd.close()
    conn_socket.send(bytes(info, 'utf-8'))
    try:
        pass
    except:
        conn_socket.send(b"Operation failed!")

def salesAnalysis(conn):
    try:
        yr = list(sorted(set(file["Year"])))
        a=list(file.groupby(['Year'])['Number'].max())
        b=list(file.groupby(['Year'])['Number'].min())
        x = np.arange(len(yr))  
        width = 0.35  

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2,a, width, label='Max')
        rects2 = ax.bar(x + width/2, b, width, label='Min')
        
        ax.set_ylabel('Client Count')
        ax.set_xlabel('Year')
        ax.set_xticks(x)
        ax.set_xticklabels(yr)
        ax.set_title('Sales Analysis')
        ax.legend()
        fig.tight_layout()
        plt.show()
        op = plt.savefig("Sales.jpg")
        conn.send(bytes("[Successful] Sales Log Generated ",FORMAT))
    except:
        conn.send(bytes("[Fail] Error",FORMAT))
    
def revenue(conn):
    try:
        file['NetRevenue'].fillna((file["Number"] * 99), inplace=True)
        file.to_csv(FILE, index=False)
        conn.send(bytes(FILE,FORMAT))
    except:
        conn.send(bytes("[Fail] Error",FORMAT))


def addAttr(conn,dataSet):
    try:
        fname = os.path.basename(dataSet)
        fileNew = pd.read_csv(fname)
        tempFile=pd.concat([file,fileNew], axis = 1)
        tempFile.to_csv(FILE, index=False)       
        conn.send(bytes(FILE,FORMAT))
    except:
        conn.send(bytes("[Fail] Error",FORMAT))  


#***SOCKET CONNECTION***

def on_new_client(clientsocket, addr, host):
    while True:
        msg = clientsocket.recv(1024).decode()
        args = msg.split(SEPARATOR)

        if(args[0] == "-1"):
            break
        elif(args[0] == "0"):
            feedback_today(clientsocket, args[1])
        elif(args[0] == "1"):
            rating_analysis(clientsocket)
        elif(args[0] == "2"):
            week_performance(clientsocket, args[1], args[2]) 
        elif(args[0] == "3"):
            salesAnalysis(clientsocket)
        elif(args[0] == "4"):
            revenue(clientsocket)
        elif(args[0] == "5"):
            addAttr(clientsocket, args[1])
          
    clientsocket.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 5001                # Reserve a port for your service.

print('Server started!')
print('Waiting for customer care...\n')

s.bind((host, port))        # Bind to the port
s.listen()

while True:
    c, addr = s.accept()     # Establish connection with client.
    print("Connected to a customer care : "+ str(addr[0]))
    thread.start_new_thread(on_new_client, (c, addr, host))
s.close()
