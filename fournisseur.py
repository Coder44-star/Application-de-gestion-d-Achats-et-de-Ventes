#Les bibliotheque a importer
from subprocess import call
from tkinter import ttk, Tk, Label, Entry, Button
from tkinter import *
from tkinter import messagebox
import pandas as pd
import random
global df_fournisseur

#fonction Imprimer
def imprimer():
    root.destroy()
    call(["python","imprimerfournisseur.py"])

# Créer un DataFrame vide pour fournisseur
columns = ['CODE','NOM', 'PRENOM','ADRESSE','MAIL','TELEPHONE']
df_fournisseur = pd.DataFrame(columns=columns)

def Ajouter():
    global df_fournisseur

    # Générer un nombre aléatoire entre 1 et 100
    nombre_aleatoire1 = random.randint(10, 999999)
    nombre_aleatoire2 = random.randint(20, 100)


# Créer la chaîne de caractères
    code = nombre_aleatoire2 *nombre_aleatoire1
    nom = txtnom.get()
    prenom = txtprenom.get()
    adresse=txtADRESSE.get()
    mail=txtMAIL.get()
    telephone = txtTELEPHONE.get()

    # Vérifier le format du numéro de téléphone
    if not (telephone.isdigit() and len(telephone) == 8 and not telephone.startswith('00')):
        messagebox.showerror("Erreur", "Le numéro de téléphone doit contenir 8 chiffres et ne doit pas commencer par '00'.")
        return

    # Ajouter les données dans le DataFrame
    
    df_fournisseur = df_fournisseur._append({'CODE': code, 'NOM': nom, 'PRENOM': prenom,
                                  'ADRESSE': adresse, 'MAIL':mail, 'TELEPHONE': telephone},
                                 ignore_index=True)

    # Mettre à jour la table d'achats dans l'interface
    UpdateTablefournisseur()
    ViderChampsTexte()


    
    
    #UpdateFichier()


#def UpdateFichier():
    #df_fournisseur.to_csv('df_fournisseur.csv', index=False)


def UpdateTablefournisseur():
    #Effacer les données actuelles dans la table d'ventes
    for row in Tablefournisseur.get_children():
        Tablefournisseur.delete(row)

    # Ajouter les nouvelles données à la table d'ventes
    for index, row in df_fournisseur.iterrows():
        Tablefournisseur.insert('', 'end', values=(row['CODE'], row['NOM'], row['PRENOM'], row['ADRESSE'],row['MAIL'], row['TELEPHONE']))

def ViderChampsTexte():
    # Vider les champs de texte dans la table d'achats
    
    txtADRESSE.delete(0,END )
    txtTELEPHONE.delete(0, END)
    txtnom.delete(0,END)
    txtprenom.delete(0,END)
    txtMAIL.delete(0,END)





def Retour():
    root.destroy()
    call(["python","main.py"])


def Modifier():
    global df_fournisseur

    # Obtenir l'élément sélectionné dans le tableau d'achats
    selection_fournisseur = Tablefournisseur.selection()

    # Vérifier si un élément est sélectionné
    if selection_fournisseur and not df_fournisseur.empty:
        # Utilisez le premier élément sélectionné (peut être ajusté selon vos besoins)
        selected_item = selection_fournisseur[0]
     # Obtenez l'index réel dans le DataFrame en utilisant la valeur de la colonne 'MAIL'
        NOM_selected = Tablefournisseur.item(selected_item, "values")[1]
        index_fournisseur = df_fournisseur[df_fournisseur['NOM'] == NOM_selected].index[0]

        # Afficher les éléments à l'interface
        txtnom.insert(0, str(df_fournisseur.at[index_fournisseur, 'NOM']))
        
        txtprenom.insert(0, str(df_fournisseur.at[index_fournisseur, 'PRENOM']))
        
        txtADRESSE.insert(0, str(df_fournisseur.at[index_fournisseur, 'ADRESSE']))
        
        txtMAIL.insert(0, str(df_fournisseur.at[index_fournisseur, 'MAIL']))
        
        txtTELEPHONE.insert(0, str(df_fournisseur.at[index_fournisseur, 'TELEPHONE']))
        
        # Créer une fonction de mise à jour pour éviter la répétition de code
        def update_data():
            nonlocal index_fournisseur  # Utiliser nonlocal pour accéder à la variable de l'encapsulation parente

            # Mettre à jour les valeurs dans le DataFrame pour la table d'achats
            df_fournisseur.at[index_fournisseur, 'NOM'] = txtnom.get()
            df_fournisseur.at[index_fournisseur, 'PRENOM'] = txtprenom.get()
            df_fournisseur.at[index_fournisseur, 'ADRESSE'] = txtADRESSE.get()
            df_fournisseur.at[index_fournisseur, 'MAIL'] = txtMAIL.get()
            df_fournisseur.at[index_fournisseur, 'TELEPHONE'] = txtTELEPHONE.get()

            # Mettre à jour la table d'achats dans l'interface
            UpdateTablefournisseur()
            ViderChampsTexte()



         # Créer un bouton "Enregistrer" et associer la fonction update_data
        btnModifierEnregistrer = Button(root, text="Enregistrer", font=('Arial', 14), background="#605067",foreground="white", command=update_data)
        btnModifierEnregistrer.place(x=1230, y=198, width=100)
        
        
# Fonction pour trier le DataFrame
def Trier():
    global df_fournisseur
    tri_type = combotri.get()

    if tri_type == "code Croissant":   
        df_fournisseur = df_fournisseur.sort_values(by='CODE', ascending=True)
        
    elif tri_type == "code Décroissant": 
        df_fournisseur = df_fournisseur.sort_values(by='CODE', ascending=False)
       
        # Mettre à jour les tables dans l'interface
    UpdateTablefournisseur()
    ViderChampsTexte()


    # Function to update tables based on product search
def search_product():
    global df_fournisseur

    # Get the product to search
    search_product = entry_search.get().upper()  # Convert to uppercase for case-insensitive search

    # Filter DataFrame based on the searched product
    filtered_fournisseur = df_fournisseur[df_fournisseur['NOM'].str.upper().str.contains(search_product, na=False)]
    
    # Update tables with filtered data
    UpdateTablefournisseur(filtered_fournisseur)
    









def Supprimer():
    global df_fournisseur


    # Obtenir l'élément sélectionné dans la table d'achats
    selection_fournisseur = Tablefournisseur.selection()

    # Vérifier si un élément est sélectionné
    if selection_fournisseur and not df_fournisseur.empty:
        # Utilisez le premier élément sélectionné (peut être ajusté selon vos besoins)
        selected_item = selection_fournisseur[0]

        # Obtenez l'index réel dans le DataFrame en utilisant la valeur de la colonne 'MAIL'
        MAIL_selected = Tablefournisseur.item(selected_item, "values")[1]
        index_achat = df_fournisseur[df_fournisseur['NOM'] == MAIL_selected].index[0]

        # Supprimer la ligne dans le DataFrame pour la table d'achats
        df_fournisseur = df_fournisseur.drop(index_achat)


    
    UpdateTablefournisseur()
    ViderChampsTexte()

def search_product():
    global df_fournisseur
    
    # Get the product to search
    search_product = entry_search.get().upper()  # Convert to uppercase for case-insensitive search

    # Filter DataFrame based on the searched product
    filtered_achats = df_fournisseur[df_fournisseur['TELEPHONE'].str.upper().str.contains(search_product, na=False)]
    
    # Update tables with filtered data
    UpdateTablefournisseur(filtered_achats)
    




#la fenetre
root= Tk()

root.title("MENUE ACHATS")
root.geometry("1350x700+0+0")
root.resizable(False,False)
root.configure(background="#D3D3D3")

#Ajouter le titre 
lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="Gestion fournisseurs", font=("Sans Serif", 25), background="#008080", foreground="white")
lbltitre.place(x=0, y=0, width=1350, height=60) 

#NOM
lblnom= Label(root, text="NOM", font=("Arial", 18), background="#008080", foreground="white")
lblnom.place(x=70, y=150, width=150)
txtnom= Entry(root, bd=4, font=("Ariel", 14))
txtnom.place(x=255, y=150, width=150)

#prenom
lblprenom = Label(root, text="PRENOM ", font=("Arial", 18), background="#008080", foreground="white")
lblprenom.place(x=50, y=200, width=200)
txtprenom = Entry(root, bd=4, font=("Ariel", 14))
txtprenom.place(x=255, y=200, width=300)



#ADRESSE
lblADRESSE = Label(root, text="ADRESSE", font=("Arial", 18), background="#008080", foreground="white")
lblADRESSE.place(x=70, y=250, width=150)
txtADRESSE = Entry(root, bd=4, font=("Ariel", 14))
txtADRESSE.place(x=255, y=250, width=300)

#MAIL
lblMAIL = Label(root, text="MAIL", font=("Arial", 18), background="#008080", foreground="white")
lblMAIL.place(x=600, y=150, width=150)
txtMAIL = Entry(root, bd=4, font=("Ariel", 14))
txtMAIL.place(x=760, y=150, width=230)


#TELEPHONE
lblTELEPHONE = Label(root, text="TELEPHONE", font=("Arial", 18), background="#008080", foreground="white")
lblTELEPHONE.place(x=600, y=200, width=150)
txtTELEPHONE = Entry(root, bd=4, font=("Ariel", 14))
txtTELEPHONE.place(x=760, y=200, width=150)

#Trier
combotri = ttk.Combobox(root, font=("Arial", 14))
combotri['values'] = ['CODE Croissant', 'CODE Décroissant']
combotri.place(x=50, y=72, width=100)
btnTrier = Button(root, text="Trier", font=('Arial', 12), background="#605067", foreground="white", command=Trier)
btnTrier.place(x=155, y=70, width=45)
# Créer le bouton "Enregistrer" et le désactiver initialement
btnModifierEnregistrer = Button(root, text="Enregistrer", font=('Arial', 14), background="#605067", foreground="grey", state='disabled')
btnModifierEnregistrer.place(x=1230, y=198, width=100)


# Fonction pour enregistrer les données dans un fichier
def EnregistrerDansFichier():
    global df_fournisseur
    
    # Enregistrer les DataFrames dans des fichiers CSV
    df_fournisseur.to_csv('fournisseur.csv', index=False)
    
    # Afficher un message pour indiquer que les données ont été enregistrées
    messagebox.showinfo("Enregistrement", "Les données ont été enregistrées dans les fichiers fournisseur.csv ")

# Bouton "Enregistrer dans un fichier"
btnEnregistrerFichier = Button(root, text="Enregistrer fichier", font=('Arial', 16), background="#008080", foreground="white", command=EnregistrerDansFichier)
btnEnregistrerFichier.place(x=1000,y=110, width=200)


#Ajouter 
btnenregistrer = Button(root, text="Ajouter", font=('Arial', 16), background="#008080", foreground="white", command=Ajouter)
btnenregistrer.place(x=1000, y=160, width=200)

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


# Update Table functions now take an optional argument for the filtered DataFrame
def UpdateTablefournisseur(filtered_df=None):
    # Clear current data in the table
    for row in Tablefournisseur.get_children():
        Tablefournisseur.delete(row)

    # Use filtered DataFrame if provided, otherwise use the entire DataFrame
    df_to_display = filtered_df if filtered_df is not None else df_fournisseur

    # Add new data to the table
    for index, row in df_to_display.iterrows():
        Tablefournisseur.insert('', 'end', values=(row['CODE'], row['NOM'], row['PRENOM'], row['ADRESSE'],
                                              row['MAIL'], row['TELEPHONE']))





#Table achats
Tablefournisseur = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6), height=10, show='headings')
Tablefournisseur.place(x=12, y=330, width=1220, height=350)

#entete
Tablefournisseur.heading(1, text="CODE")
Tablefournisseur.heading(2,text="NOM")
Tablefournisseur.heading(3,text="PRENOM")
Tablefournisseur.heading(4,text="ADRESSE")
Tablefournisseur.heading(5,text="MAIL")
Tablefournisseur.heading(6,text="TELEPHONE")


#definir les dimensions des colonnes
Tablefournisseur.column(1,width=100)
Tablefournisseur.column(2,width=150)
Tablefournisseur.column(3,width=150)
Tablefournisseur.column(4,width=80)
Tablefournisseur.column(5,width=100)
Tablefournisseur.column(6,width=80)


#Execution
root.mainloop()