import datetime
import os

FICHIER = "journal.txt"

def ajouter_note():
    note = input(" Écris ta note :\n> ")
    if note.strip():
        with open(FICHIER, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            f.write(note + "\n\n")
        print(" Note ajoutée avec succès !")
    else:
        print(" Impossible d'enregistrer une note vide.")

def lire_notes():
    if not os.path.exists(FICHIER):
        print(" Aucune note enregistrée pour le moment.")
        return
    print("\n  VOS NOTES \n")
    with open(FICHIER, "r", encoding="utf-8") as f:
        print(f.read())

def menu():
    while True:
        print("\n Journal Personnel du Madison ")
        print("1.  Ajouter une note ✏️")
        print("2.  Lire toutes les notes 🗒️")
        print("3.  Quitter ❌")

        choix = input("Choisis une option (1/2/3) : ").strip()
        if choix == "1":
            ajouter_note()
        elif choix == "2":
            lire_notes()
        elif choix == "3":
            print("Au revoir !")
            break
        else:
            print("⚠️ Choix invalide, réessaie.")

# --- Programme principal ---
menu()
# Fin du script