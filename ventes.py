#Achats
#Les bibliotheque a importer
from subprocess import call
from tkinter import ttk, Tk, Label, Entry, Button
from tkinter import *
from tkinter import messagebox
import pandas as pd
from tkinter import ttk
from tkcalendar import DateEntry




#fonction Imprimer
def imprimer():
    root.destroy()
    call(["python","imprimerVentes.py"])



# Créer un DataFrame vide pour achats 
columns = ['PRODUIT', 'PRIX', 'QUANTITE']
df_achats = pd.DataFrame(columns=columns)

# Créer un DataFrame vide pour ventes
columns = ['CODE_ACHAT', 'CLIENTS', 'TELEPHONE','PRODUIT','PRIX vente','QUANTITE', 'PRIX_TOTALE','DATE_VENTE']
df_ventes = pd.DataFrame(columns=columns)
 # ...



def Ajouter():
    global df_achats
    global df_ventes

    produit = comboproduit.get()
    prix_vente = float(txtPrix_vente.get())
    prix = float(txtPrix.get())
    quantite = int(txtQuantite.get())
    code_achat = int(txtmatricule.get())
    clients = txtclients.get()
    telephone = txttelephone.get()
    prix_totale = prix_vente * quantite
    #  Utiliser get_date() pour obtenir la date sélectionnée
    date_vente_value = date_vente.get_date().strftime('%Y-%m-%d')

    # Vérifier si la matricule est unique
    if code_achat in df_ventes['CODE_ACHAT'].values:
        messagebox.showerror("Erreur", "La matricule doit être unique.")
        return

    # Vérifier le format du numéro de téléphone
    if not (telephone.isdigit() and len(telephone) == 8 and not telephone.startswith('00')):
        messagebox.showerror("Erreur", "Le numéro de téléphone doit contenir 8 chiffres et ne doit pas commencer par '00'.")
        return

    
    # Ajouter la nouvelle vente à la table des ventes
    df_achats = df_achats._append({'PRODUIT': produit, 'PRIX d''achat': prix, 'QUANTITE': quantite}, ignore_index=True)
    df_ventes = df_ventes._append({'CODE_ACHAT': code_achat, 'CLIENTS': clients, 'TELEPHONE': telephone,
                                  'PRODUIT': produit, 'PRIX vente': prix_vente, 'QUANTITE': quantite,
                                  'PRIX_TOTALE': prix_vente * quantite, 'DATE_VENTE': date_vente_value},
                                 ignore_index=True)

    # Mettre à jour la table d'achats dans l'interface
    UpdateTableAchats()
    # Mettre à jour la table des ventes dans l'interface utilisateur
    UpdateTableVentes()
    ViderChampsTexte()



    
    
    #UpdateFichier()

def UpdateTableAchats():
    # Effacer les données actuelles dans la table d'achats
    for row in Table.get_children():
        Table.delete(row)

    # Ajouter les nouvelles données à la table d'achats
    for index, row in df_achats.iterrows():
        Table.insert('', 'end', values=(row['PRODUIT'], row['PRIX d''achat'], row['QUANTITE']))

#def UpdateFichier():
    #df_achats.to_csv('df_achats.csv', index=False)


def UpdateTableVentes():
    #Effacer les données actuelles dans la table d'ventes
    for row in TableVentes.get_children():
        TableVentes.delete(row)

    # Ajouter les nouvelles données à la table d'ventes
    for index, row in df_ventes.iterrows():
        TableVentes.insert('', 'end', values=(row['CODE_ACHAT'], row['Clients'], row['TELEPHONE'], row['PRIX vente'],row['PRODUIT'], row['QUANTITE'],row['DATE_VENTE'],row['PRIX_TOTALE']))


def ViderChampsTexte ():
    # Vider les champs de texte dans la table d'achats
    comboproduit.set('')
    txtPrix.delete(0,END )
    txtPrix_vente.delete(0,END )
    txtQuantite.delete(0, END)
    txtmatricule.delete(0,END)
    txttelephone.delete(0,END)
    txtclients.delete(0,END)
    date_vente.delete(0,END)




def Retour():
    root.destroy()
    call(["python","main.py"])


def Modifier():
    global df_achats
    global df_ventes

    # Obtenir l'élément sélectionné dans la table d'achats
    selection_achat = Table.selection()

    # Vérifier si un élément est sélectionné
    if selection_achat and not df_achats.empty:
        # Utilisez le premier élément sélectionné (peut être ajusté selon vos besoins)
        selected_item = selection_achat[0]

        # Obtenez l'index réel dans le DataFrame en utilisant la valeur de la colonne 'PRODUIT'
        produit_selected = Table.item(selected_item, "values")[0]
        index_achat = df_achats[df_achats['PRODUIT'] == produit_selected].index[0]

        # Afficher les éléments à l'interface
        comboproduit.set(df_achats.at[index_achat, 'PRODUIT'])
        txtPrix.insert(0, str(df_achats.at[index_achat, 'PRIX d''achat']))
        txtQuantite.insert(0, str(df_achats.at[index_achat, 'QUANTITE']))
        txttelephone.insert(0, str(df_ventes.at[index_achat, 'TELEPHONE']))
        txtclients.insert(0, str(df_ventes.at[index_achat, 'CLIENTS']))
        txtPrix_vente.insert(0, str(df_ventes.at[index_achat, 'PRIX vente']))

        # Créer une fonction de mise à jour pour éviter la répétition de code
        def update_data():
            nonlocal index_achat  # Utiliser nonlocal pour accéder à la variable de l'encapsulation parente

            # Mettre à jour les valeurs dans le DataFrame pour la table d'achats
            df_achats.at[index_achat, 'PRODUIT'] = comboproduit.get()
            df_achats.at[index_achat, 'PRIX d''achat'] = float(txtPrix.get())
            df_achats.at[index_achat, 'QUANTITE'] = int(txtQuantite.get())
            

            # Mettre à jour les valeurs dans le DataFrame pour la table des ventes
            produit_vente_index = df_ventes[df_ventes['PRODUIT'] == produit_selected].index
            for vente_index in produit_vente_index:
                df_ventes.at[vente_index, 'PRODUIT'] = comboproduit.get()
                df_ventes.at[vente_index, 'PRIX vente'] = float(txtPrix_vente.get())
                df_ventes.at[vente_index, 'QUANTITE'] = int(txtQuantite.get())
                df_ventes.at[vente_index, 'CLLIENTS'] = txtclients.get()
                df_ventes.at[vente_index, 'TELEPHONE'] = txttelephone.get()
                df_ventes.at[vente_index, 'PRIX_TOTALE'] = df_ventes.at[vente_index, 'QUANTITE'] * float(txtPrix_vente.get())

            # Mettre à jour la table d'achats dans l'interface
            UpdateTableAchats()
            UpdateTableVentes()
            ViderChampsTexte()

            # Désactiver le bouton "Enregistrer" après la mise à jour
            btnModifierEnregistrer.config(state='disabled')

        # Créer un bouton "Enregistrer" et associer la fonction update_data
        btnModifierEnregistrer = Button(root, text="Enregistrer", font=('Arial', 14), background="#605067",
                                        foreground="white", command=update_data)
        btnModifierEnregistrer.place(x=1230, y=198, width=100)


        

def Supprimer():
    global df_achats
    global df_ventes

    # Obtenir l'élément sélectionné dans la table d'achats
    selection_achat = Table.selection()

    # Vérifier si un élément est sélectionné
    if selection_achat and not df_achats.empty:
        # Utilisez le premier élément sélectionné (peut être ajusté selon vos besoins)
        selected_item = selection_achat[0]

        # Obtenez l'index réel dans le DataFrame en utilisant la valeur de la colonne 'PRODUIT'
        produit_selected = Table.item(selected_item, "values")[0]
        index_achat = df_achats[df_achats['PRODUIT'] == produit_selected].index[0]

        # Supprimer la ligne dans le DataFrame pour la table d'achats
        df_achats = df_achats.drop(index_achat)

        # Supprimer les lignes correspondantes dans le DataFrame pour la table des ventes
        produit_vente_index = df_ventes[df_ventes['PRODUIT'] == produit_selected].index
        df_ventes = df_ventes.drop(produit_vente_index)
    UpdateTableAchats()
    UpdateTableVentes()
   


# Fonction pour trier le DataFrame
def Trier():
    global df_achats
    global df_ventes
    tri_type = combotri.get()

    if tri_type == "Prix d''achat Croissant":
        df_achats = df_achats.sort_values(by='PRIX d''achat ', ascending=True)
        df_ventes = df_ventes.sort_values(by='PRIX vente', ascending=True)
    elif tri_type == "Prix d''achat Décroissant":
        df_achats = df_achats.sort_values(by='PRIX d''achat ', ascending=False)
        df_ventes = df_ventes.sort_values(by='PRIX vente', ascending=False)
    elif tri_type == "Quantité Croissante":
        df_achats = df_achats.sort_values(by='QUANTITE', ascending=True)
        df_ventes = df_ventes.sort_values(by='QUANTITE', ascending=True)
    elif tri_type == "Quantité Décroissante":
        df_achats = df_achats.sort_values(by='QUANTITE', ascending=False)
        df_ventes = df_ventes.sort_values(by='QUANTITE', ascending=False)
    elif tri_type == "Ventes les plus récentes":
        df_ventes = df_ventes.sort_values(by='DATE_VENTE', ascending=False)

        # Mettre à jour les tables dans l'interface
    UpdateTableAchats()
    UpdateTableVentes()
    ViderChampsTexte()

    
    # Function to update tables based on product search
def search_product():
    global df_achats
    global df_ventes

    # Get the product to search
    search_product = entry_search.get().upper()  # Convert to uppercase for case-insensitive search

    # Filter DataFrame based on the searched product
    filtered_achats = df_achats[df_achats['PRODUIT'].str.upper().str.contains(search_product, na=False)]
    filtered_ventes = df_ventes[df_ventes['PRODUIT'].str.upper().str.contains(search_product, na=False)]

    # Update tables with filtered data
    UpdateTableAchats(filtered_achats)
    UpdateTableVentes(filtered_ventes)




#la fenetre
root= Tk()

root.title("MENUE ACHATS")
root.geometry("1350x700+0+0")
root.resizable(False,False)
root.configure(background="#D3D3D3")

#Ajouter le titre 
lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="Gestion de ventes", font=("Sans Serif", 25), background="#008080", foreground="white")
lbltitre.place(x=0, y=0, width=1350, height=60) 

#matricule 
lblmatricule = Label(root, text="MATRICULE", font=("Arial", 18), background="#008080", foreground="white")
lblmatricule.place(x=70, y=150, width=150)
txtmatricule = Entry(root, bd=4, font=("Ariel", 14))
txtmatricule.place(x=255, y=150, width=150)

#clients
lblclients = Label(root, text="CLIENTS", font=("Arial", 18), background="#008080", foreground="white")
lblclients.place(x=70, y=200, width=150)
txtclients = Entry(root, bd=4, font=("Ariel", 14))
txtclients.place(x=255, y=200, width=150)



#Numero telephone
lbltelephone = Label(root, text="TELEPHONE", font=("Arial", 18), background="#008080", foreground="white")
lbltelephone.place(x=70, y=250, width=150)
txttelephone = Entry(root, bd=4, font=("Ariel", 14))
txttelephone.place(x=255, y=250, width=300)

#Achats 
lblproduit = Label(root, text="PRODUIT", font=("Arial", 18), background="#008080", foreground="white")
lblproduit.place(x=600, y=110, width=150)
comboproduit = ttk.Combobox(root, font=("Arial", 14))
comboproduit['values'] = ['IPHONE 12', 'IPHONE 11', 'GALAXY S22', 'S10', 'A20', 'NOKIA']
comboproduit.place(x=760, y=110, width=150)


#Prix de vente
lblPrix_vente = Label(root, text="PRIX vente", font=("Arial", 18), background="#008080", foreground="white")
lblPrix_vente.place(x=600, y=200, width=150)
txtPrix_vente = Entry(root, bd=4, font=("Ariel", 14))
txtPrix_vente.place(x=760, y=200, width=150)
#Prix d'achat 
lblPrix= Label(root, text="PRIX d'ACHAT", font=("Arial", 16), background="#008080", foreground="white")
lblPrix.place(x=600, y=155, width=150)
txtPrix = Entry(root, bd=4, font=("Ariel", 14))
txtPrix.place(x=760, y=155, width=150)

#Quantité
lblQuantite = Label(root, text="QUANTITE", font=("Arial", 18), background="#008080", foreground="white")
lblQuantite.place(x=600, y=250, width=150)
txtQuantite = Entry(root, bd=4, font=("Ariel", 14))
txtQuantite.place(x=760, y=250, width=150)

# Créer le bouton "Enregistrer" et le désactiver initialement
btnModifierEnregistrer = Button(root, text="Enregistrer", font=('Arial', 14), background="#605067", foreground="grey", state='disabled')
btnModifierEnregistrer.place(x=1230, y=198, width=100)

# Ajouter le widget DateEntry pour la date de vente
date_label = Label(root, text="Date de vente", font=("Arial", 18), background="#008080", foreground="white")
date_label.place(x=600, y=64, width=150)

date_vente = DateEntry(root, font=("Arial", 14), date_pattern='yyyy-mm-dd')
date_vente.place(x=760, y=64, width=150)


# Fonction pour enregistrer les données dans un fichier
def EnregistrerDansFichier():
    global df_achats
    global df_ventes

    # Enregistrer les DataFrames dans des fichiers CSV
    df_achats.to_csv('achats.csv', index=False)
    df_ventes.to_csv('ventes.csv', index=False)

    # Afficher un message pour indiquer que les données ont été enregistrées
    messagebox.showinfo("Enregistrement", "Les données ont été enregistrées dans les fichiers achats.csv et ventes.csv.")

# Bouton "Enregistrer dans un fichier"
btnEnregistrerFichier = Button(root, text="Enregistrer fichier", font=('Arial', 16), background="#008080", foreground="white", command=EnregistrerDansFichier)
btnEnregistrerFichier.place(x=1000,y=110, width=200)


#Ajouter 
btnenregistrer = Button(root, text="Ajouter", font=('Arial', 16), background="#008080", foreground="white", command=Ajouter)
btnenregistrer.place(x=1000, y=160, width=200)
#Trier
combotri = ttk.Combobox(root, font=("Arial", 14))
combotri['values'] = ['Prix d''achat Croissant', 'Prix d''achat Décroissant', 'Quantité Croissante', 'Quantité Décroissante', 'Ventes les plus récentes']
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
entry_search.place(x=230, y=70, width=200)

# Button rechercher
btn_search = Button(root, text="Rechercher", font=('Arial', 12), background="#605067", foreground="white", command=search_product)
btn_search.place(x=430, y=69, width=100)

#Ajouter le titre 
lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="Gestion de ventes", font=("Sans Serif", 20), background="#001F3F", foreground="white")
lbltitre.place(x=500, y=310, width=800, height=30) 

# Update Table functions now take an optional argument for the filtered DataFrame
def UpdateTableAchats(filtered_df=None):
    # Clear current data in the table
    for row in Table.get_children():
        Table.delete(row)

    # Use filtered DataFrame if provided, otherwise use the entire DataFrame
    df_to_display = filtered_df if filtered_df is not None else df_achats

    # Add new data to the table
    for index, row in df_to_display.iterrows():
        Table.insert('', 'end', values=(row['PRODUIT'], row['PRIX d''achat'], row['QUANTITE']))


def UpdateTableVentes(filtered_df=None):
    # Clear current data in the table
    for row in TableVentes.get_children():
        TableVentes.delete(row)

    # Use filtered DataFrame if provided, otherwise use the entire DataFrame
    df_to_display = filtered_df if filtered_df is not None else df_ventes

    # Add new data to the table
    for index, row in df_to_display.iterrows():
        TableVentes.insert('', 'end', values=(row['CODE_ACHAT'], row['CLIENTS'], row['TELEPHONE'], row['PRIX vente'],
                                              row['PRODUIT'], row['QUANTITE'],row['DATE_VENTE'], row['PRIX_TOTALE']))


#Ajouter le titre 
lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="Gestion d'achats", font=("Sans Serif", 20), background="#001F3F", foreground="white")
lbltitre.place(x=12, y=310, width=400, height=30) 

#Table Achats
Table = ttk.Treeview(root, columns=(1, 2, 3), height=10, show='headings')
Table.place(x=12, y=340, width=400, height=350)
#entete
Table.heading(1, text="PRODUIT")
Table.heading(2,text="PRIX")
Table.heading(3,text="QUANTITE")

#definir les dimensions des colonnes
Table.column(1,width=100)
Table.column(2,width=50)
Table.column(3,width=100)




#Table ventes
TableVentes = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6, 7,8), height=10, show='headings')
TableVentes.place(x=500, y=340, width=800, height=350)

#entete
TableVentes.heading(1, text="CODE_ACHAT")
TableVentes.heading(2,text="CLIENTS")
TableVentes.heading(3,text="TELEPHONE")
TableVentes.heading(4,text="PRIX vente")
TableVentes.heading(5,text="PRODUIT")
TableVentes.heading(6,text="QUANTITE")
TableVentes.heading(7,text="DATE_VENTE")
TableVentes.heading(8,text="PRIX_TOTALE")


#definir les dimensions des colonnes
TableVentes.column(1,width=100)
TableVentes.column(2,width=100)
TableVentes.column(3,width=100)
TableVentes.column(4,width=80)
TableVentes.column(5,width=100)
TableVentes.column(6,width=80)
TableVentes.column(7,width=100)
TableVentes.column(8,width=100)



#Execution
root.mainloop()