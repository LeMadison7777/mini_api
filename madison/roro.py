import os

FICHIER = "taches.txt"

def charger_taches():
    """Lit le fichier et retourne une liste de tâches."""
    if not os.path.exists(FICHIER):
        return []
    with open(FICHIER, "r", encoding="utf-8") as f:
        return [ligne.strip() for ligne in f if ligne.strip()]

def sauvegarder_taches(taches):
    """Écrit toutes les tâches dans le fichier."""
    with open(FICHIER, "w", encoding="utf-8") as f:
        for t in taches:
            f.write(t + "\n")

def afficher_taches(taches):
    if not taches:
        print("\n📭 Aucune tâche enregistrée.")
    else:
        print("\n=== 📋 Liste des tâches ===")
        for i, t in enumerate(taches, 1):
            print(f"{i}. {t}")

def ajouter_tache(taches):
    tache = input("🆕 Nouvelle tâche : ").strip()
    if tache:
        taches.append(tache)
        sauvegarder_taches(taches)
        print("✅ Tâche ajoutée !")
    else:
        print("⚠️ Impossible d'ajouter une tâche vide.")

def supprimer_tache(taches):
    afficher_taches(taches)
    if not taches:
        return
    choix = input("Numéro de la tâche à supprimer : ").strip()
    if choix.isdigit():
        num = int(choix)
        if 1 <= num <= len(taches):
            taches.pop(num - 1)
            sauvegarder_taches(taches)
            print("❌ Tâche supprimée.")
        else:
            print("⚠️ Numéro invalide.")
    else:
        print("⚠️ Entre un numéro valide.")

def menu():
    taches = charger_taches()
    while True:
        print("\n=== Gestionnaire de tâches ===")
        print("1. ➕ Ajouter une tâche")
        print("2. 📋 Afficher les tâches")
        print("3. ❌ Supprimer une tâche")
        print("4. 🚪 Quitter")
        choix = input("Choisis une option (1/2/3/4) : ").strip()

        if choix == "1":
            ajouter_tache(taches)
        elif choix == "2":
            afficher_taches(taches)
        elif choix == "3":
            supprimer_tache(taches)
        elif choix == "4":
            print("👋 Au revoir !")
            break
        else:
            print("⚠️ Choix invalide.")

# --- Programme principal ---
menu()
# Fin du script