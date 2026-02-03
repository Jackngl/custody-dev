# Logo de l'intégration

Pour que le logo s'affiche dans l'interface Home Assistant (pas seulement dans HACS), il faut le soumettre au dépôt officiel `brands` de Home Assistant.

## Fichiers disponibles

- `custom_components/custody_schedule/icon.png` - Icône PNG pour l'intégration (256×256)
- `custom_components/custody_schedule/logo.png` - Logo PNG pour l'intégration
- `custom_components/custody_schedule/icon.svg.bak` - Fichier source SVG de l’icône (à convertir en PNG si besoin)
- `custom_components/custody_schedule/logo.svg.bak` - Fichier source SVG du logo (à convertir en PNG si besoin)
- `icon.png` - Icône à la racine pour HACS

## Soumettre le logo au dépôt brands

1. Aller sur https://github.com/home-assistant/brands
2. Suivre les instructions pour ajouter votre intégration
3. Créer un dossier `custom_integrations/custody_schedule/`
4. Ajouter les fichiers `icon.png` et `logo.png` (convertir depuis SVG)
5. Créer un pull request

## Format requis

- **icon.png** : 256x256 pixels, format PNG
- **logo.png** : Format paysage, hauteur minimale 128 pixels

## Conversion SVG vers PNG

Vous pouvez convertir le SVG en PNG avec :
- Inkscape : `inkscape icon.svg --export-filename=icon.png --export-width=256 --export-height=256`
- ImageMagick : `convert -background none -size 256x256 icon.svg icon.png`
- En ligne : https://cloudconvert.com/svg-to-png

