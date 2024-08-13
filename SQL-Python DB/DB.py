import sqlite3
import datetime

conn = sqlite3.connect('Central.db')
c = conn.cursor()

nomeClient=""
cognomeClient=""

def Create_Table():
 
 c.execute("""CREATE TABLE IF NOT EXISTS ebooks(
             ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
             Titolo VARCHAR,
             Genere VARCHAR,
             Npagine INTEGER,
             URL VARCHAR,
             FOREIGN KEY (Genere) REFERENCES generi(Nome)
    )""")

 c.execute("""CREATE TABLE IF NOT EXISTS utenti(
             ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
             Nome VARCHAR,
             Cognome VARCHAR,
             Password VARCHAR,
             Tipo VARCHAR,
             Indirizzo INTEGER
    )""")

 c.execute("""CREATE TABLE IF NOT EXISTS generi(
             Nome VARCHAR NOT NULL PRIMARY KEY 
    )""")

 c.execute("""CREATE TABLE IF NOT EXISTS preferenze(
             ID_Cliente INTEGER NOT NULL PRIMARY KEY, 
             Nome_Genere VARCHAR NOT NULL,
             FOREIGN KEY (ID_Cliente) REFERENCES utenti(ID),
             FOREIGN KEY (Nome_Genere) REFERENCES generi(Nome)
    )""")

 c.execute("""CREATE TABLE IF NOT EXISTS accessi(
             ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
             ID_Utente INTEGER, 
             ID_Ebook INTEGER,
             Data VARCHAR,
             URL VARCHAR,
             FOREIGN KEY (ID_Utente) REFERENCES utenti(ID),
             FOREIGN KEY (ID_Ebook) REFERENCES ebooks(ID)
    )""")
 

def AddData(q) :
   
   var=q.split(",")
   query="INSERT INTO ebooks (Titolo,Genere,Npagine,URL) VALUES(?,?,?,?);"
   c.execute(query,(var[1],var[2],var[3],var[4]))
   print(c.fetchall())
   conn.commit()
   

def ViewAll(): 

   c.execute("SELECT * FROM ebooks")
   print(c.fetchall())
   conn.commit()

def Delete(q):

   var=q.split(",")
   query="DELETE FROM ebooks WHERE ID=?"
   c.execute(query,var[1])
   print(c.fetchall())
   conn.commit()

def Update(q):

   var=q.split(",")
   query="UPDATE ebooks SET Titolo=?,Genere=?,Npagine=?,URL=? WHERE ID=?;"
   c.execute(query,(var[2],var[3],var[4],var[5],var[1]))
   print(c.fetchall())
   conn.commit()

def Clear():
   c.execute("DELETE FROM ebooks")

def Login_Client(user):
  userSplit=user.split(",")
  query="SELECT * FROM utenti WHERE Nome=? and Cognome=? and Password=? and Tipo='client';"
  if(c.execute(query,(userSplit[1],userSplit[2],userSplit[3]))):
   print("Login Permitted")
   nomeClient=userSplit[1]
   cognomeClient=userSplit[2]
  else:
   print("Access Denied")
   conn.commit()

def Login_Admin(user):
  userSplit=user.split(",")
  query="SELECT * FROM utenti WHERE Nome=? and Cognome=? and Password=? and Tipo='admin';"
  if(c.execute(query,(userSplit[1],userSplit[2],userSplit[3]))):
   print("Login Permitted")
  else:
   print("Access Denied")
   conn.commit()

def AddClient(user):
   userSplit=user.split(",")
   query="INSERT INTO utenti (Nome,Cognome,Password,Tipo,Indirizzo) VALUES(?,?,?,?,?);"
   c.execute(query,(userSplit[1],userSplit[2],userSplit[3],"client",userSplit[4]))
   print("Client Registered")
   conn.commit()

def Rental(titolo):
   titoloSplit=titolo.split(",")

   query="SELECT ID FROM ebooks WHERE Titolo=?;"
   c.execute(query,(titoloSplit[1],))
   IdTitolo="%s"%c.fetchone()
   query2="SELECT ID FROM utenti WHERE Nome=? and Cognome=?;"
   c.execute(query2,(titoloSplit[2],titoloSplit[3]))
   IdUtente="%s"%c.fetchone()
   url="www.rentalEbook/"+titoloSplit[2]+"."+titoloSplit[3]+"/"+titoloSplit[1]
   data = datetime.datetime.now()
   data_ora=data.strftime("%d/%m/%Y, %H:%M:%S")
   query3="INSERT INTO accessi (ID_Utente,ID_Ebook,Data,URL) VALUES(?,?,?,?)"
   c.execute(query3,(IdUtente,IdTitolo,data_ora,url,))
   conn.commit()

def Preference(item):
   itemSplit=item.split(",")
   query="SELECT ID FROM utenti WHERE Nome=? and Cognome=?;"
   c.execute(query,(itemSplit[2],itemSplit[3]))
   IdUtente="%s"%c.fetchone()
   query2="SELECT Nome FROM generi WHERE Nome=?;"
   c.execute(query2,(itemSplit[1],))
   NomeGenere="%s"%c.fetchone()
   query3="INSERT INTO preferenze (ID_Cliente,Nome_Genere) VALUES(?,?)"
   c.execute(query3,(IdUtente,NomeGenere,))
   conn.commit()

