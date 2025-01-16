# Les bibliothèques à importer
from subprocess import call
from tkinter import ttk, Tk
from tkinter import *
from tkinter import messagebox


# Fonction Ventes
def Ventes():
    root.destroy()
    call(["python", "ventes.py"])

# Fonction Achats
def Achats():
    root.destroy()
    call(["python", "achats.py"])
    
#fonction fournisseur
def Fournisseur() :
    root.destroy()
    call(["python","fournisseur.py"])

# La fenêtre
root = Tk()

root.title("GESTION DES ACHATS")
root.geometry("600x250+400+200")
root.resizable(False, False)
root.configure(background="#CCCCCC")

# Ajouter le titre
lbltitre = Label(root, borderwidth=10, relief=SUNKEN, text="Gestion d'achats", font=("Sans Serif", 25),background="#008080", foreground="white")
lbltitre.place(x=0, y=0, width=600)

# Bouton achats
btn_enregistrer = Button(root, text="ACHATS", font=("Arial", 20), background="#008080",fg="white", command=Achats)
btn_enregistrer.place(x=100, y=100, width=200)

# Bouton ventes
btn_enregistrer = Button(root, text="VENTES", font=("Arial", 20), background="#008080",fg="white", command=Ventes)
btn_enregistrer.place(x=300, y=100, width=200)

#fournisseur
btn_fournisseur = Button(root, text="Fournisseur", font=('Arial', 16), background="#605066", foreground="white", command=Fournisseur)
btn_fournisseur.place(x=10, y=200, width=200)

# Exécution
root.mainloop()
