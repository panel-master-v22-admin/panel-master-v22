import datetime

def generer_facture():
    # --- Informations de la Pharmacie ---
    pharmacie_nom = "PHARMACIE DE LA SANTÉ"
    pharmacie_adresse = "123 Rue de la République, 75001 Paris"
    pharmacie_tel = "01 23 45 67 89"

    # --- Saisie des informations client ---
    print("--- Création d'une nouvelle facture ---")
    nom_client = input("Nom du client : ")
    date_actuelle = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    num_facture = f"FAC-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"

    panier = []
    continuer = True

    while continuer:
        print("\nAjout d'un produit :")
        nom_prod = input("Nom du médicament/produit : ")
        dosage = input("Dosage (ex: 500mg) : ")
        quantite = int(input("Quantité : "))
        prix_unit = float(input("Prix unitaire (€) : "))
        tva_taux = float(input("Taux TVA (%) (ex: 2.1 ou 5.5) : "))

        total_ligne = quantite * prix_unit
        panier.append({
            'nom': nom_prod,
            'dosage': dosage,
            'quantite': quantite,
            'prix_u': prix_unit,
            'tva': tva_taux,
            'total': total_ligne
        })

        choix = input("Ajouter un autre produit ? (o/n) : ").lower()
        if choix != 'o':
            continuer = False

    # --- Calculs totaux ---
    total_ht = sum(item['total'] for item in panier)
    total_tva = sum(item['total'] * (item['tva'] / 100) for item in panier)
    total_ttc = total_ht + total_tva

    # --- Construction du contenu de la facture ---
    contenu = []
    contenu.append("="*45)
    contenu.append(pharmacie_nom.center(45))
    contenu.append(pharmacie_adresse.center(45))
    contenu.append(f"Tél: {pharmacie_tel}".center(45))
    contenu.append("="*45)
    contenu.append(f"Facture N° : {num_facture}")
    contenu.append(f"Date       : {date_actuelle}")
    contenu.append(f"Client     : {nom_client}")
    contenu.append("-" * 45)
    
    # En-tête du tableau
    contenu.append(f"{'Désignation':<18} {'Qté':>3} {'P.U':>7} {'TTC':>8}")
    contenu.append("-" * 45)

    for item in panier:
        ligne = f"{item['nom'][:12]} ({item['dosage']})".lower().capitalize()
        contenu.append(f"{ligne:<18} {item['quantite']:>3} {item['prix_u']:>7.2f} {item['total']:>8.2f}")

    contenu.append("-" * 45)
    contenu.append(f"{'TOTAL HT :':<30} {total_ht:>10.2f} €")
    contenu.append(f"{'TOTAL TVA :':<30} {total_tva:>10.2f} €")
    contenu.append(f"{'TOTAL TTC À PAYER :':<30} {total_ttc:>10.2f} €")
    contenu.append("-" * 45)
    contenu.append("Merci de votre confiance !")
    contenu.append("Conservez cette facture pour votre mutuelle.")
    contenu.append("="*45)

    # --- Sauvegarde dans un fichier texte ---
    nom_fichier = f"facture_{num_facture}.txt"
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write("\n".join(contenu))

    print(f"\nLa facture a été générée avec succès : {nom_fichier}")

if __name__ == "__main__":
    generer_facture()
