from tkinter import *
import os.path
import shutil
import time
from pathlib import Path
from datetime import timedelta, datetime

def recuperer():
    global get_path
    get_path=entree.get()
    # chemin defini :
    global path
    path = Path(get_path)
    entree.delete(0, END)
    print(get_path)

def recuperer2():
    global get_numb
    get_numb=entree2.get()
    # je determine les jours a soustraire a ma date actuelle
    global removed_days
    removed_days = timedelta(days=int(get_numb))
    # je soustraie à la date actuelle les jours defini dans removed_days
    global present_days_less_removed_days
    present_days_less_removed_days = present_day - removed_days
    entree2.delete(0, END)
    print(get_numb)

def lancer():
    # je parcours tous les elements dans le chemin
    for i in path.iterdir():
        if i.is_file():
            # La méthode os.path.getmtime() est utilisée pour obtenir l’heure de la dernière last_modification_epoch_path du chemin spécifié.
            last_modification_epoch_path = os.path.getmtime(i)
            # ctime() convertit un temps exprimé en secondes depuis l'époque en une chaîne représentant l'heure locale.
            last_modification_epoch_path_local_time = time.ctime(last_modification_epoch_path)

            # recupere last_modification_epoch_path_local_time en objet datetime
            last_modification_epoch_path_datetime = datetime.strptime(last_modification_epoch_path_local_time,
                                                                      "%a %b %d %H:%M:%S %Y")

            # #si la date de last_modification_epoch_path du fichier est inferieur a la date actuelle moins le nombre de jour defini dans "removed_days", on supprime le fichier.
            if last_modification_epoch_path_datetime < present_days_less_removed_days:
                shutil.move(i, trie_dir)

    # ajout des elements a supprimé dans une liste
    for i in trie_dir.iterdir():
        unlink_files.append(i)

    global window2
    window2 = Tk()
    # titre de l'app
    window2.title("confirmation de suppression")
    # taille de la fenetre
    window2.geometry("720x480")
    # logo
    window2.iconbitmap("data/Hermes-Embleme.ico")
    # couleur fond
    window2.config(background="#f37021")
    # taille min de la fenetre
    window2.minsize(width=1080, height=480)
    window2.maxsize(width=1280, height=480)

    #frame de window2
    frame_window2=Frame(window2,width=1920, height=1080, bg="#f37021")
    frame_window2.pack(expand=True)

    # frame des bouttons de window2
    frame_boutton_window2 = Frame(window2, bg="#f37021", bd=1)
    frame_boutton_window2.pack(expand=True)

    title = Label(frame_window2, text="LISTE DES FICHIERS A SUPPRIMER :", font=("sanchezregular", 20), bg="#f37021",
                  fg="black")
    title.pack(side=TOP)

    scrollbar = Scrollbar(frame_window2)
    scrollbar.pack(side=RIGHT, fill=Y)

    label_scroll=Listbox(frame_window2, width=100, font=("sanchezregular", 20), bg="#f37021", fg="black", yscrollcommand=scrollbar.set)

    for i in unlink_files:
        label_scroll.insert(END, i)
    label_scroll.pack(expand=True)
    scrollbar.config(command=label_scroll.yview)

    cancel_button = Button(frame_boutton_window2, width=7, text="annuler", font=("sanchezregular", 20), bg="#f37021", fg="black", command=cancel)
    cancel_button.grid(row=0, column=0)

    confirm_button=Button(frame_boutton_window2, width=7, text="confirmer", font=("sanchezregular", 20), bg="#f37021", fg="black", command=confirm)
    confirm_button.grid(row=0, column=1)

def confirm():
    # verifie si le fichier est vide ou non, si oui il l'ouvre et ajoute les fichiers qui seront supprimés
    if os.path.getsize(txt_file_path)==0:
        with open(txt_file_path, "w") as f:
            f.write(f"{str(present_day)} : {unlink_files}")
    else:
        # si le fichier contient deja des données, enregistre les données presentes dans la variable 'data'
        with open(txt_file_path, "r") as f:
            data = f.read()
        # ajoute les données existantes (data) + les nouvelles données à supprimer
        with open(txt_file_path, "w") as f:
            f.write(f"{str(data)}\n{str(present_day)} : {unlink_files}")
    # suppression des fichiers contenus dans le dosier 'fichiers_triés'
    for i in trie_dir.iterdir():
        print(f"{i.name} supprimé")
        i.unlink()
        #remet la liste vide pour une utilisation continue
        unlink_files.clear()
    window2.destroy()

def cancel():
    print("Vous quittez le programme, les fichiers ne seront pas supprimés.")
    # les fichiers sont re-transférés dans le dossier d'orgine
    for i in trie_dir.iterdir():
        shutil.move(i, path)
    # remet la liste vide pour une utilisation continue
    unlink_files.clear()
    window2.destroy()

#current path
txt_path=Path.cwd()
#création d'un fichier json pour stocker les fichiers supprimés
txt_file_path= txt_path / "fichiers_supprimés.txt"
txt_file_path.touch(exist_ok=True)

#creation du dossier des fichiers triés
trie_dir=txt_path/"fichiers_triés"
trie_dir.mkdir(exist_ok=True)

#je recupere la date actuelle
present_day=datetime.now()

#liste qui recupere tous les dossier a supprimer
unlink_files=[]

###---INTERFACE TKINTER---###

window=Tk()

#titre de l'app
window.title("Gestionnaire de fichier")
#taille de la fenetre
window.geometry("1280x720")
#logo
window.iconbitmap("data/Hermes-Embleme.ico")
#couleur fond
window.config(background="#f37021")
#taille min de la fenetre
window.minsize(width=720, height=480)

#creer une frame 1
frame=Frame(window, bg="#f37021", bd=1, highlightthickness=1)
#afficher la frame
frame.pack(side=TOP)

#creer une frame 2
frame2=Frame(window, bg="#f37021", bd=1, highlightthickness=1)
frame2.pack(expand=True)

#creation dimage
canvas=Canvas(frame, width=180, height=130, bg="#f37021", bd=0, highlightthickness=0)
image=PhotoImage(file="data/logo_hermes.gif").zoom(10).subsample(30)
canvas.create_image(10,10, anchor=NW, image=image)
canvas.pack()

#créé un label
label_path=Label(frame2, text="Chemin du dossier à parcourir :\n(exemple : C:/Users/Guillaume/Documents/data)",font=("sanchezregular", 20), bg="#f37021", fg="black", bd=0, highlightthickness=0)
label_path.pack()

#creer un champs d'entree
value_str=StringVar()
value_str.set("C:/Users/Guillaume/Documents/data")
entree=Entry(frame2, textvariable=value_str, width=30, font=("sanchezregular", 20))
entree.pack(ipady=4)

# creer un boutton valider
valider_button=Button(frame2, text="valider", font=("sanchezregular", 20), bg="#f37021", fg="black", command=recuperer)
valider_button.pack()

#créé un label pour le nombre de jour
label_jour=Label(frame2, text="Suppression des fichiers au-delà de :",font=("sanchezregular", 20), bg="#f37021", fg="black", bd=0, highlightthickness=0)
label_jour.pack()

#creer un champs d'entree
value_int=StringVar()
entree2=Entry(frame2, textvariable=value_int, width=8, font=("sanchezregular", 20))
entree2.pack(ipady=4)

# creer un boutton valider
valider_button2=Button(frame2, text="valider", font=("sanchezregular", 20), bg="#f37021", fg="black", command=recuperer2)
valider_button2.pack()

# creer un boutton pour lancer la suppression
valider_button2=Button(window, text="Lancer le programme", font=("sanchezregular", 20), bg="#f37021", fg="black", command=lancer)
valider_button2.pack(side=BOTTOM)


window.mainloop()