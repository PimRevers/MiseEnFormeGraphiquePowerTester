from PIL import Image
import os

def png_to_ico(source_png, output_ico):
    if not os.path.exists(source_png):
        print(f"Erreur : Le fichier {source_png} est introuvable.")
        return

    try:
        # Ouverture de l'image PNG
        img = Image.open(source_png)
        
        # On définit les tailles standards pour un exécutable Windows
        # 256px est crucial pour les grands affichages et éviter le flou
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Sauvegarde au format ICO avec toutes les variantes de taille
        img.save(output_ico, format='ICO', sizes=sizes)
        
        print(f"Succès ! '{output_ico}' a été généré avec {len(sizes)} variantes de tailles.")
        
    except Exception as e:
        print(f"Une erreur est survenue lors de la conversion : {e}")

if __name__ == "__main__":
    # Remplace par les noms de tes fichiers
    nom_image_source = "ptit LOGO-DEEP-CONCEPT fc.png"
    nom_icone_finale = "logo.ico"
    
    png_to_ico(nom_image_source, nom_icone_finale)