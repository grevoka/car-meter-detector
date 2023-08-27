import cv2
import os
import glob
import shutil

# Constantes
LARGEUR_REELLE_PLAQUE = 520  # en mm
LIMITE_DISTANCE = 3.11  # en mm
DOSSIER_CIBLE = 'distance_3.15'
DEBUT_COPIE = "output_0224.jpg"
FIN_COPIE = "output_0526.jpg"
copie_demarree = False

# Estimation de la distance focale
d_eq = 16  # Supposons que vous utilisez le mode "Superview"
s = 6.4  # Largeur approximative du capteur 1/1.9"
d_35mm = 43.3  # Diagonale d'un capteur plein format (35mm)
DISTANCE_FOCAL = (d_eq * s) / d_35mm  # en mm

derniere_distance = None

def detecter_plaque(image, liste_fichiers):
    global derniere_distance, copie_demarree

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 220, 255)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 2000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

            if len(approx) == 4 and cv2.isContourConvex(approx):
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w)/h

                if 2 <= aspect_ratio <= 4.5:
                    cv2.drawContours(image, [approx], -1, (0, 255, 0), 3)

                    # Calcul de la distance à la plaque
                    distance = (LARGEUR_REELLE_PLAQUE * DISTANCE_FOCAL) / w

                    # Vérification du changement de distance
                    if derniere_distance is not None:
                        if abs(derniere_distance - distance) > 5:
                            print("Changement de distance suspect détecté!")
                            continue

                    derniere_distance = distance

                    if distance < LIMITE_DISTANCE and not copie_demarree:
                        index_debut = liste_fichiers.index(os.path.join(os.path.dirname(liste_fichiers[0]), DEBUT_COPIE))
                        index_fin = liste_fichiers.index(os.path.join(os.path.dirname(liste_fichiers[0]), FIN_COPIE))
                        
                        for i in range(index_debut, index_fin + 1, 30):  # Copie tous les 30 frames
                            fichier_source = liste_fichiers[i]
                            nom_fichier = os.path.basename(fichier_source)
                            fichier_destination = os.path.join(DOSSIER_CIBLE, nom_fichier)
                            shutil.copy2(fichier_source, fichier_destination)
                            print(f"Copie de {nom_fichier} vers {DOSSIER_CIBLE}")

                        copie_demarree = True
                        print("Copie des photos terminée.")

                    print(f"Distance détectée: {distance:.2f} mm")
                    position_distance = (int(image.shape[1] - 450), 60)
                    cv2.putText(image, f"Distance: {distance:.2f} mm", position_distance, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

    return image

def lire_sequence_photos(dossier):
    pattern = os.path.join(dossier, "output_*.jpg")
    liste_fichiers = sorted(glob.glob(pattern), key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

    if not liste_fichiers:
        print("Aucun fichier trouvé!")
        return

    index = 0
    vitesse = 100
    facteur_vitesse = "x1"
    saut_images = 1

    while True:
        image = cv2.imread(liste_fichiers[index])
        image = detecter_plaque(image, liste_fichiers)

        hauteur, largeur = image.shape[:2]
        image_reduite = cv2.resize(image, (int(largeur * 0.25), int(hauteur * 0.25)))

        position_frame = (int(0.65*largeur*0.25), 30)
        position_vitesse = (int(0.80*largeur*0.25), 60)
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        cv2.putText(image_reduite, f"Frame: {index+1}/{len(liste_fichiers)}", position_frame, font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image_reduite, facteur_vitesse, position_vitesse, font, 0.5, (255, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('Image', image_reduite)

        key = cv2.waitKey(vitesse) & 0xFF

        if key == ord('A') or key == ord('a'):
            index += saut_images
            if index >= len(liste_fichiers):
                index = 0
        elif key == ord('B') or key == ord('b'):
            index -= saut_images
            if index < 0:
                index = len(liste_fichiers) - 1
        elif key == ord('1'):
            vitesse = 100
            saut_images = 1
            facteur_vitesse = "x1"
        elif key == ord('2'):
            vitesse = 50
            saut_images = 2
            facteur_vitesse = "x2"
        elif key == ord('3'):
            vitesse = 25
            saut_images = 3
            facteur_vitesse = "x3"
        elif key == 27:
            break

    cv2.destroyAllWindows()

if not os.path.exists(DOSSIER_CIBLE):
    os.makedirs(DOSSIER_CIBLE)

dossier_photos = os.path.dirname(os.path.abspath(__file__))
lire_sequence_photos(dossier_photos)
