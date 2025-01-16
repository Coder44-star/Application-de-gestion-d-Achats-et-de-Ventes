#Achats
#Les bibliotheque a importer
from subprocess import call
from tkinter import ttk, Tk, Label, Entry, Button
from tkinter import *
from tkinter import messagebox
import pandas as pd

#fonction Imprimer
def imprimer():
    root.destroy()
    call(["python","imprimerAchats.py"])

# Créer un DataFrame vide pour achats
columns = ['CODE_ACHAT', 'FOURNISSEUR', 'TELEPHONE','PRODUIT','PRIX','QUANTITE', 'PRIX_tOTALE']
df_achats = pd.DataFrame(columns=columns)

def Ajouter():
    global df_achats
    produit = comboproduit.get()
    prix = float(txtPrix.get())
    quantite = int(txtQuantite.get())
    code_achat = int(txtmatricule.get())
    fournisseur = txtfournisseur.get()
    telephone = txttelephone.get()
    prix_totale = prix * quantite

    # Vérifier si la matricule est unique
    if code_achat in df_achats['CODE_ACHAT'].values:
        messagebox.showerror("Erreur", "La matricule doit être unique.")
        return

    # Vérifier le format du numéro de téléphone
    if not (telephone.isdigit() and len(telephone) == 8 and not telephone.startswith('00')):
        messagebox.showerror("Erreur", "Le numéro de téléphone doit contenir 8 chiffres et ne doit pas commencer par '00'.")
        return

    # Ajouter les données dans le DataFrame
    
    df_achats = df_achats._append({'CODE_ACHAT': code_achat, 'FOURNISSEUR': fournisseur, 'TELEPHONE': telephone,
                                  'PRODUIT': produit, 'PRIX': prix, 'QUANTITE': quantite, 'PRIX_tOTALE': prix_totale},
                                 ignore_index=True)

    # Mettre à jour la table d'achats dans l'interface
    UpdateTableAchats()
    ViderChampsTexte()


    
    
    #UpdateFichier()


#def UpdateFichier():
    #df_achats.to_csv('df_achats.csv', index=False)


def UpdateTableAchats():
    #Effacer les données actuelles dans la table d'ventes
    for row in TableAchats.get_children():
        TableAchats.delete(row)

    # Ajouter les nouvelles données à la table d'ventes
    for index, row in df_achats.iterrows():
        TableAchats.insert('', 'end', values=(row['CODE_ACHAT'], row['FOURNISSEUR'], row['TELEPHONE'], row['PRIX'],row['PRODUIT'], row['QUANTITE'],row['PRIX_tOTALE']))

def ViderChampsTexte ():
    # Vider les champs de texte dans la table d'achats
    comboproduit.set('')
    txtPrix.delete(0,END )
    txtQuantite.delete(0, END)
    txtmatricule.delete(0,END)
    txttelephone.delete(0,END)
    txtfournisseur.delete(0,END)





def Retour():
    root.destroy()
    call(["python","main.py"])


def Modifier():
    global df_achats, btnModifierEnregistrer

    # Obtenir l'élément sélectionné dans la table d'achats
    selection_achat = TableAchats.selection()

    # Vérifier si un élément est sélectionné
    if selection_achat and not df_achats.empty:
        # Utilisez le premier élément sélectionné (peut être ajusté selon vos besoins)
        selected_item = selection_achat[0]

        # Obtenez l'index réel dans le DataFrame en utilisant la valeur de la colonne 'PRODUIT'
        produit_selected = TableAchats.item(selected_item, "values")[4]
        index_achat = df_achats[df_achats['PRODUIT'] == produit_selected].index[0]

        # Afficher les éléments à l'interface
        comboproduit.set(df_achats.at[index_achat, 'PRODUIT'])
        txtPrix.insert(0, str(df_achats.at[index_achat, 'PRIX']))
        txtQuantite.insert(0, str(df_achats.at[index_achat, 'QUANTITE']))
        txtfournisseur.insert(0, str( df_achats.at[index_achat, 'FOURNISSEUR']))
        txttelephone.insert(0, str(df_achats.at[index_achat, 'TELEPHONE']))

        # Activer le bouton "Enregistrer" après la sélection
        btnModifierEnregistrer.config(state='normal')

        # Créer une fonction de mise à jour pour éviter la répétition de code
        def update_data():
            nonlocal index_achat  # Utiliser nonlocal pour accéder à la variable de l'encapsulation parente

            # Mettre à jour les valeurs dans le DataFrame pour la table d'achats
            df_achats.at[index_achat, 'PRODUIT'] = comboproduit.get()
            df_achats.at[index_achat, 'PRIX'] = float(txtPrix.get())
            df_achats.at[index_achat, 'FOURNISSEUR'] = txtfournisseur.get()
            df_achats.at[index_achat, 'TELEPHONE'] = int(txttelephone.get())
            df_achats.at[index_achat, 'QUANTITE'] = int(txtQuantite.get())

            # Mettre à jour la table d'achats dans l'interface
            UpdateTableAchats()
            ViderChampsTexte()

            # Désactiver le bouton "Enregistrer" après la mise à jour
            btnModifierEnregistrer.config(state='disabled')

        # Créer un bouton "Enregistrer" et associer la fonction update_data
        btnModifierEnregistrer = Button(root, text="Enregistrer", font=('Arial', 14), background="#605067",
                                        foreground="white", command=update_data)
        btnModifierEnregistrer.place(x=1230, y=198, width=100)
        btnModifierEnregistrer.config(state='normal')  # Activer le bouton initialement

def Supprimer():
    global df_achats, btnModifierEnregistrer

    # Obtenir l'élément sélectionné dans la table d'achats
    selection_achat = TableAchats.selection()

    # Vérifier si un élément est sélectionné
    if selection_achat and not df_achats.empty:
        # Utilisez le premier élément sélectionné (peut être ajusté selon vos besoins)
        selected_item = selection_achat[0]

        # Obtenez l'index réel dans le DataFrame en utilisant la valeur de la colonne 'PRODUIT'
        produit_selected = TableAchats.item(selected_item, "values")[4]
        index_achat = df_achats[df_achats['PRODUIT'] == produit_selected].index[0]

        # Supprimer la ligne dans le DataFrame pour la table d'achats
        df_achats = df_achats.drop(index_achat)

    UpdateTableAchats()
    ViderChampsTexte()


# Fonction pour trier le DataFrame
# Fonction de tri en fonction du choix de l'utilisateur
def Trier():
    global df_achats
    tri_type = combotri.get()

    if tri_type == "Prix Croissant":
        df_achats = df_achats.sort_values(by='PRIX', ascending=True)
    elif tri_type == "Prix Décroissant":
        df_achats = df_achats.sort_values(by='PRIX', ascending=False)
    elif tri_type == "Quantité Croissante":
        df_achats = df_achats.sort_values(by='QUANTITE', ascending=True)
    elif tri_type == "Quantité Décroissante":
        df_achats = df_achats.sort_values(by='QUANTITE', ascending=False)
    elif tri_type == "Code Achat Croissant":
        df_achats = df_achats.sort_values(by='CODE_ACHAT', ascending=True)
    elif tri_type == "Code Achat Décroissant":
        df_achats = df_achats.sort_values(by='CODE_ACHAT', ascending=False)

    # Mettre à jour les tables dans l'interface
    UpdateTableAchats()
    ViderChampsTexte()

    # Function to update tables based on product search
def search_product():
    global df_achats
    
    # Get the product to search
    search_product = entry_search.get().upper()  # Convert to uppercase for case-insensitive search

    # Filter DataFrame based on the searched product
    filtered_achats = df_achats[df_achats['PRODUIT'].str.upper().str.contains(search_product, na=False)]
    
    # Update tables with filtered data
    UpdateTableAchats(filtered_achats)
    




#la fenetre
root= Tk()

root.title("MENUE ACHATS")
root.geometry("1350x700+0+0")
root.resizable(False,False)
root.configure(background="#D3D3D3")

#Ajouter le titre 
lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="Gestion d'achats", font=("Sans Serif", 25), background="#008080", foreground="white")
lbltitre.place(x=0, y=0, width=1350, height=60) 

#matricule 
lblmatricule = Label(root, text="MATRICULE", font=("Arial", 18), background="#008080", foreground="white")
lblmatricule.place(x=70, y=150, width=150)
txtmatricule = Entry(root, bd=4, font=("Ariel", 14))
txtmatricule.place(x=255, y=150, width=150)

#fournisseur
lblfournisseur = Label(root, text="FOURNISSEUR ", font=("Arial", 18), background="#008080", foreground="white")
lblfournisseur.place(x=50, y=200, width=200)
txtfournisseur = Entry(root, bd=4, font=("Ariel", 14))
txtfournisseur.place(x=255, y=200, width=300)



#Numero telephone
lbltelephone = Label(root, text="TELEPHONE", font=("Arial", 18), background="#008080", foreground="white")
lbltelephone.place(x=70, y=250, width=150)
txttelephone = Entry(root, bd=4, font=("Ariel", 14))
txttelephone.place(x=255, y=250, width=300)

#Achats 
lblproduit = Label(root, text="PRODUIT", font=("Arial", 18), background="#008080", foreground="white")
lblproduit.place(x=600, y=150, width=150)
comboproduit = ttk.Combobox(root, font=("Arial", 14))
comboproduit['values'] = ['IPHONE 12', 'IPHONE 11', 'GALAXY S22', 'S10', 'A20', 'NOKIA']
comboproduit.place(x=760, y=150, width=150)


#Prix
lblPrix = Label(root, text="PRIX", font=("Arial", 18), background="#008080", foreground="white")
lblPrix.place(x=600, y=200, width=150)
txtPrix = Entry(root, bd=4, font=("Ariel", 14))
txtPrix.place(x=760, y=200, width=150)

#Quantité
lblQuantite = Label(root, text="QUANTITE", font=("Arial", 18), background="#008080", foreground="white")
lblQuantite.place(x=600, y=250, width=150)
txtQuantite = Entry(root, bd=4, font=("Ariel", 14))
txtQuantite.place(x=760, y=250, width=150)

# Créer le bouton "Enregistrer" et le désactiver initialement
btnModifierEnregistrer = Button(root, text="Enregistrer", font=('Arial', 14), background="#605067", foreground="grey", state='disabled')
btnModifierEnregistrer.place(x=1230, y=198, width=100)


# Fonction pour enregistrer les données dans un fichier
def EnregistrerDansFichier():
    global df_achats
    
    # Enregistrer les DataFrames dans des fichiers CSV
    df_achats.to_csv('achats.csv', index=False)
    
    # Afficher un message pour indiquer que les données ont été enregistrées
    messagebox.showinfo("Enregistrement", "Les données ont été enregistrées dans les fichiers achats.csv ")

# Bouton "Enregistrer dans un fichier"
btnEnregistrerFichier = Button(root, text="Enregistrer fichier", font=('Arial', 16), background="#008080", foreground="white", command=EnregistrerDansFichier)
btnEnregistrerFichier.place(x=1000,y=110, width=200)


#Ajouter 
btnenregistrer = Button(root, text="Ajouter", font=('Arial', 16), background="#008080", foreground="white", command=Ajouter)
btnenregistrer.place(x=1000, y=160, width=200)
#Trier
combotri = ttk.Combobox(root, font=("Arial", 14))
combotri['values'] = ['Prix Croissant', 'Prix Décroissant', 'Quantité Croissante', 'Quantité Décroissante', 'Code Achat Croissant', 'Code Achat Décroissant']
combotri.place(x=50, y=72, width=100)
btnTrier = Button(root, text="Trier", font=('Arial', 12), background="#605067", foreground="white", command=Trier)
btnTrier.place(x=155, y=70, width=45)

#Modifier
btnenregistrer = Button(root, text="Modifier", font=('Arial', 16), background="#008080", foreground="white", command=Modifier)
btnenregistrer.place(x=1000, y=210, width=200)


#Supprimer
btnenregistrer = Button(root, text="Supprimer", font=('Arial', 16), background="#008080", foreground="white", command=Supprimer)
btnenregistrer.place(x=1000, y=260, width=200)

#Retour
btnenregistrer = Button(root, text="Retour", font=('Arial', 16), background="#605067", foreground="white", command=Retour)
btnenregistrer.place(x=1230, y=260, width=100)


#Imprimer
btnenregistrer = Button(root, text="Imprimer", font=('Arial', 16), background="#605067", foreground="white", command=imprimer)
btnenregistrer.place(x=1230, y=140, width=100)

#Ajouter le titre
lblTitreTable = Label(root, borderwidth=3, relief=SUNKEN, text='TABLE', font=("Sans Serif", 18), background="#008080", foreground="white")
# Entry for searching products
entry_search = Entry(root, bd=4, font=("Ariel", 14))
entry_search.place(x=290, y=70, width=200)

# Button rechercher
btn_search = Button(root, text="Rechercher", font=('Arial', 14), background="#605067", foreground="white", command=search_product)
btn_search.place(x=493, y=66, width=120)


# Update TableAchats functions now take an optional argument for the filtered DataFrame
def UpdateTableAchats(filtered_df=None):
    # Clear current data in the table
    for row in TableAchats.get_children():
        TableAchats.delete(row)

    # Use filtered DataFrame if provided, otherwise use the entire DataFrame
    df_to_display = filtered_df if filtered_df is not None else df_achats

    # Add new data to the table
    for index, row in df_to_display.iterrows():
        TableAchats.insert('', 'end', values=(row['CODE_ACHAT'], row['FOURNISSEUR'], row['TELEPHONE'], row['PRIX'],
                                              row['PRODUIT'], row['QUANTITE'], row['PRIX_tOTALE']))





#TableAchats achats
TableAchats = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6, 7), height=10, show='headings')
TableAchats.place(x=12, y=330, width=1320, height=350)

#entete
TableAchats.heading(1, text="CODE_ACHAT")
TableAchats.heading(2,text="FOURNISSEUR")
TableAchats.heading(3,text="TELEPHONE")
TableAchats.heading(4,text="PRIX")
TableAchats.heading(5,text="PRODUIT")
TableAchats.heading(6,text="QUANTITE")
TableAchats.heading(7,text="PRIX_TOTALE")


#definir les dimensions des colonnes
TableAchats.column(1,width=100)
TableAchats.column(2,width=150)
TableAchats.column(3,width=150)
TableAchats.column(4,width=80)
TableAchats.column(5,width=100)
TableAchats.column(6,width=80)
TableAchats.column(7,width=100)


#Execution
root.mainloop()