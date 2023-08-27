# Car Meter Detector

## Description du projet

Le projet `car-meter-detector.py` utilise la bibliothèque OpenCV pour détecter et suivre des plaques d'immatriculation dans une séquence d'images. Lorsqu'une plaque est détectée à moins d'une distance prédéfinie
, un ensemble de photos est copié dans un dossier spécifique pour une analyse ultérieure.

## Dépendances

- Python 3.x
- OpenCV (`cv2`)
- Glob
- Shutil
- OS

## Installation

1. Cloner le dépôt

    ```bash
    git clone [URL du dépôt]
    ```

2. Installer les dépendances

    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

Exécutez le script Python `car-meter-detector.py` en vous assurant que vous avez une séquence d'images dans le même dossier que le script.

    ```bash

    python car-meter-detector.py

## Fonctionnalités

- Détection de plaques d'immatriculation en utilisant la détection de contours.
- Calcul de la distance à la plaque d'immatriculation basé sur des mesures réelles et la distance focale.
- Copie d'un ensemble de photos dans un dossier spécifique lorsqu'une plaque est détectée à moins d'une certaine distance.

## Comment ça marche

- Le script utilise la méthode de détection de contours d'OpenCV pour localiser des plaques d'immatriculation.
- Il utilise ensuite les propriétés de la géométrie des lentilles pour estimer la distance de la plaque.
- Enfin, si la distance est en dessous d'une limite prédéfinie, un ensemble de photos est copié dans un dossier cible.

## Contribution

Pour contribuer au projet :

1. Forker le projet
2. Créer votre branche (`git checkout -b ma-nouvelle-fonctionnalité`)
3. Commit vos changements (`git commit -m 'Ajouter une nouvelle fonctionnalité'`)
4. Push à la branche (`git push origin ma-nouvelle-fonctionnalité`)
5. Créer une nouvelle Pull Request

## Auteurs

- [William A](https://github.com/grevoka/)

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE.md](LICENSE.md) pour plus d'informations.

