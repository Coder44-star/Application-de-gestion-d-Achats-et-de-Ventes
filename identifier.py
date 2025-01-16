import tkinter as tk
from tkinter import messagebox
import subprocess
from tkinter import *


# Fonction pour ouvrir la page d'achat
def ouvrir_page_achat():
    subprocess.Popen(["python", "main.py"])  # Remplacez "achat.py" par le nom de votre fichier Python de la page d'achat

# Fonction pour vérifier l'authentification
def verifier_authentification():
    nom_utilisateur = nom_utilisateur_entry.get()
    mot_de_passe = mot_de_passe_entry.get()
    
    # Comparaison avec des informations d'authentification simulées
    if nom_utilisateur == "utilisateur" and mot_de_passe == "motdepasse":
        messagebox.showinfo("Connexion réussie", "Bienvenue sur la page suivante !")
        ouvrir_page_achat()  # Appel pour ouvrir la page d'achat
        root.destroy()
    else:
        messagebox.showerror("Erreur d'authentification", "Nom d'utilisateur ou mot de passe incorrect.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Authentification")
root.geometry("600x250+400+200")
root.resizable(False, False)
root.configure(background="#CCCCCC")



# Ajouter le titre
lbltitre = tk.Label(root, borderwidth=10, relief=SUNKEN, text="Authentification", font=("Sans Serif", 25),background="#008080", foreground="white")
lbltitre.place(x=0, y=0, width=600)


# Création des étiquettes et des champs de saisie pour le nom d'utilisateur et le mot de passe
nom_utilisateur_label = tk.Label(root, text="Nom d'utilisateur:",font=("Arial", 14), background="#008080",fg="white")
nom_utilisateur_label.pack()
nom_utilisateur_label.place(x=50, y=75, width=150)
nom_utilisateur_entry = tk.Entry(root)
nom_utilisateur_entry.pack()
nom_utilisateur_entry.place(x=250, y=77, width=150)

mot_de_passe_label = tk.Label(root, text="Mot de passe:",font=("Arial", 16), background="#008080",fg="white")
mot_de_passe_label.pack()
mot_de_passe_label.place(x=50, y=120, width=150)
mot_de_passe_entry = tk.Entry(root, show="*")
mot_de_passe_entry.pack()
mot_de_passe_entry.place(x=250, y=130, width=150)
# Bouton de connexion
bouton_connexion = tk.Button(root, text="Se connecter", font=("Arial", 16), background="#008080",fg="white", command=verifier_authentification)
bouton_connexion.pack()
bouton_connexion.place(x=230, y=200, width=150)

# Exécution de la boucle principale
root.mainloop()