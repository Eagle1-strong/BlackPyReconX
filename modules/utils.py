# modules/utils.py

import os
import shutil

def clear_outputs():
    """
    Supprime et recrée le dossier outputs.
    """
    try:
        if os.path.exists("outputs"):
            shutil.rmtree("outputs")
        os.makedirs("outputs", exist_ok=True)
    except Exception as e:
        return f"Erreur suppression des outputs : {e}"
    return "✔️ Outputs nettoyés avec succès."
