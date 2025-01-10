'''Campo Minato'''

import tkinter as k
from tkinter import messagebox
from tkinter import ttk
from random import randrange

window=k.Tk()
window.title("Campo Minato")
griglia_comandi=k.Frame(window, bg="#00ff00")
griglia_comandi.pack(fill="x")
tabellone=k.Frame(window)
tabellone.pack()

opzioni = ["Facile", "Medio", "Difficile"]

rows=8
cols=10
griglia=[]
n_bombe=int(10)
contatore_bandierine=n_bombe
caselle_da_scoprire=rows*cols-n_bombe
secondi=0
started=False
to_end=False
timer_id=None
primo=True

def crea_bottoni(rows, cols, comboboxed):
    global griglia
    codice_colore=0
    if comboboxed:
        for widget in tabellone.winfo_children():
            widget.destroy()
    for r in range(rows):
        codice_colore+=1
        griglia.append([])
        for c in range(cols):
            codice_colore+=1
            bottone=k.Button(tabellone, width=4, height=2, bg=seleziona_colore(codice_colore))
            bottone.grid(row=r, column=c)
            bottone.bind("<Button-1>", scopri_casella)
            bottone.bind("<Button-3>", metti_bandierina)
            dict={
                "Bottone" : bottone,
                "Etichetta" : 0,
                "Scoperta" : False
            }
            griglia[r].append(dict)

def scopri_casella(event):
    global griglia, caselle_da_scoprire, primo
    x = event.widget.grid_info()["row"]
    y = event.widget.grid_info()["column"]
    if griglia[x][y]["Bottone"].cget("text")=="🚩": return
    
    if primo:
        posizioni_escluse=escludi_posizioni(griglia, x, y)
        crea_bombe(griglia, n_bombe, rows, cols, posizioni_escluse)
        crea_numero(griglia)
        primo=False

    scopri_cella(x, y)

def scopri_cella(x, y):
    global griglia, caselle_da_scoprire, started, to_end, secondi
    if griglia[x][y]["Etichetta"]!=0:
        griglia[x][y]["Bottone"].config(text=griglia[x][y]["Etichetta"])
        griglia[x][y]["Bottone"].config(fg=scegli_fg(griglia, x, y))
    else: griglia[x][y]["Bottone"].config(text="")
    if griglia[x][y]["Scoperta"]==False: caselle_da_scoprire-=1
    griglia[x][y]["Scoperta"]=True
    if caselle_da_scoprire==(rows*cols-n_bombe)-1:
        incrementa_tempo()
    
    if griglia[x][y]["Etichetta"]==-1:
        mostra_bombe(griglia, "red")
        to_end=True
        incrementa_tempo()
        k.messagebox.showerror("Sconfitta","Hai perso!!!")
        window.destroy()
    else:
        match griglia[x][y]["Bottone"].cget("bg"):
            case "green":
                griglia[x][y]["Bottone"].config(bg="#AAAAAA")
            case "darkgreen":
                griglia[x][y]["Bottone"].config(bg="grey")
    if caselle_da_scoprire==0:
        mostra_bombe(griglia, "green")
        to_end=True
        incrementa_tempo()
        k.messagebox.showinfo("Vittoria", f"HAI VINTO!!!\nHai impiegato {secondi} secondi")
    if griglia[x][y]["Etichetta"]==0:
        righe=len(griglia)
        colonne=len(griglia[0])
        if x>0 and y>0 and griglia[x-1][y-1]["Scoperta"]==False:
            scopri_cella(x-1, y-1)
        if x>0 and griglia[x-1][y]["Scoperta"]==False:
            scopri_cella(x-1, y)
        if x>0 and y<colonne-1 and griglia[x-1][y+1]["Scoperta"]==False:
            scopri_cella(x-1, y+1)
        if y>0 and griglia[x][y-1]["Scoperta"]==False:
            scopri_cella(x, y-1)
        if y<colonne-1 and griglia[x][y+1]["Scoperta"]==False:
            scopri_cella(x, y+1)
        if x<righe-1 and y>0 and griglia[x+1][y-1]["Scoperta"]==False:
            scopri_cella(x+1, y-1)
        if x<righe-1 and griglia[x+1][y]["Scoperta"]==False:
            scopri_cella(x+1, y)
        if x<righe-1 and y<colonne-1 and griglia[x+1][y+1]["Scoperta"]==False:
            scopri_cella(x+1, y+1)

def metti_bandierina(event):
    global griglia, contatore_bandierine
    x = event.widget.grid_info()["row"]
    y = event.widget.grid_info()["column"]
    if griglia[x][y]["Scoperta"]==True: return
    if griglia[x][y]["Bottone"].cget("text")!="🚩":
        griglia[x][y]["Bottone"].config(text="🚩")
        contatore_bandierine-=1
    else:
        griglia[x][y]["Bottone"].config(text="")
        contatore_bandierine+=1
    counter_bandierine.config(text=f"🚩 {contatore_bandierine}")

def crea_bombe(griglia, n_bombe, rows, cols, posizioni_escluse):
    posizionate=0
    while posizionate != n_bombe:
        r=randrange(rows)
        c=randrange(cols)
        if griglia[r][c]["Etichetta"]!=-1 and (r, c) not in posizioni_escluse:
            griglia[r][c]["Etichetta"]=-1
            posizionate+=1

def crea_numero(griglia):
    righe=len(griglia)
    colonne=len(griglia[0])

    for i in range(righe):
        for j in range(colonne):
            if griglia[i][j]["Etichetta"]!=-1:
                counter=0
                if i>0 and j>0 and griglia[i-1][j-1]["Etichetta"] == -1: counter+=1
                if i>0 and griglia[i-1][j]["Etichetta"] == -1: counter+=1
                if i>0 and j<colonne-1 and griglia[i-1][j+1]["Etichetta"] == -1: counter+=1
                if j>0 and griglia[i][j-1]["Etichetta"] == -1: counter+=1
                if j<colonne-1 and griglia[i][j+1]["Etichetta"] == -1: counter+=1
                if i<righe-1 and j>0 and griglia[i+1][j-1]["Etichetta"] == -1: counter+=1
                if i<righe-1 and griglia[i+1][j]["Etichetta"] == -1: counter+=1
                if i<righe-1 and j<colonne-1 and griglia[i+1][j+1]["Etichetta"] == -1: counter+=1

                griglia[i][j]["Etichetta"] = counter

def mostra_bombe(griglia, colore):
    rows=len(griglia)
    cols=len(griglia[0])
    for r in range(rows):
        for c in range(cols):
            if griglia[r][c]["Etichetta"]!=-1 and griglia[r][c]["Bottone"].cget("text")=="🚩": griglia[r][c]["Bottone"].config(text="❌", bg="red")
            if griglia[r][c]["Etichetta"]==-1:
                griglia[r][c]["Bottone"].config(bg=colore, text="💣")

def scegli_fg(griglia, x, y):
    match griglia[x][y]["Etichetta"]:
        case 1: return "#111111"
        case 2: return "blue"
        case 3: return "green"
        case 4: return "brown"
        case 5: return "orange"
        case 6: return "red"
        case 7: return "purple"
        case 8: return "white"

def incrementa_tempo():
    global secondi, tempo, to_end, timer_id
    started=True
    tempo.config(text=secondi)
    if started and not to_end:
        secondi+=1
        timer_id = window.after(1000, incrementa_tempo)
    else: pass

def selezione_difficolta(event):
    global rows, cols, n_bombe, griglia, caselle_da_scoprire, secondi, to_end, started, timer_id, contatore_bandierine, primo
    if timer_id:
        window.after_cancel(timer_id)
        timer_id=None
    match combobox.get():
        case "Facile":
            rows=8
            cols=10
            n_bombe=10
        case "Medio":
            rows=14
            cols=18
            n_bombe=40
        case "Difficile":
            rows=20
            cols=24
            n_bombe=99
    
    contatore_bandierine=n_bombe
    griglia=[]
    caselle_da_scoprire=rows*cols-n_bombe
    secondi=0
    started=False
    to_end=False
    tempo.config(text=str(secondi))
    counter_bandierine.config(text=f"🚩 {contatore_bandierine}")
    primo=True
    crea_bottoni(rows, cols, True)

def escludi_posizioni(griglia, x, y):
    escluse = []

    for r in range(x-1, x+2):
        for c in range(y-1, y+2):
            if 0<=r<rows and 0<=c<cols:
                escluse.append((r, c))

    return escluse

def seleziona_colore(codice):
    if codice%2==0: return "green"
    else: return "darkgreen"

combobox = ttk.Combobox(griglia_comandi, values=opzioni, state="readonly")
combobox.set(opzioni[0])
combobox.bind("<<ComboboxSelected>>", selezione_difficolta)
combobox.pack(side="left", padx=10)

restart_btn=k.Button(griglia_comandi, text="RESET", border=0, bg="darkgreen", fg="white", font=("arial", 10))
restart_btn.bind("<Button-1>", selezione_difficolta)
restart_btn.pack(side="left", padx=10)

counter_bandierine=k.Label(griglia_comandi, text=f"🚩 {contatore_bandierine}", bg="#00ff00")
counter_bandierine.pack(side="left", padx=10)

tempo=k.Label(griglia_comandi, text=str(secondi), font=("Arial", 20), bg="#00ff00")
tempo.pack(side="right", padx=10)
if started: incrementa_tempo(secondi, tempo)
crea_bottoni(rows, cols, False)

window.mainloop()