# 📊 Guide Dashboard - Calendrier de garde

[🇫🇷 Version française](README_DASHBOARD_GARDE.fr.md) | [🇬🇧 English version](README_DASHBOARD_GARDE.md)

Ce guide fournit une vue Lovelace dédiée **Calendrier de garde** avec :
- une version proche maquette (vue globale),
- une version **multi-enfants** plus lisible (couleurs distinctes par enfant).

---

## 📋 Table des matières

1. [Prérequis](#prérequis)
2. [Exemple 1 - Vue globale proche maquette](#exemple-1---vue-globale-proche-maquette)
3. [Exemple 2 - Multi-enfants avec couleurs dédiées](#exemple-2---multi-enfants-avec-couleurs-dédiées)
4. [Checklist lisibilité](#checklist-lisibilité)

---

## ✅ Prérequis

- Intégration Custody configurée.
- Entités disponibles pour chaque enfant (`calendar.*`, `sensor.*`, `binary_sensor.*`).
- Cartes custom installées si utilisées (`mushroom`).

---

## Exemple 1 - Vue globale proche maquette

```yaml
title: Calendrier de garde
path: calendrier-garde
icon: mdi:calendar-month
type: sections
max_columns: 2
sections:
  - title: Vue globale
    cards:
      - type: custom:mushroom-title-card
        title: CALENDRIER DE GARDE
        subtitle: Custody Schedule
      - type: custom:mushroom-chips-card
        chips:
          - type: template
            content: Maman
            icon: mdi:account
            icon_color: blue
          - type: template
            content: Papa
            icon: mdi:account
            icon_color: amber
      - type: calendar
        title: Planning
        entities:
          - entity: calendar.lucas_calendar
      - type: entities
        title: Upcoming events
        entities:
          - entity: sensor.lucas_next_arrival
            name: Prochaine arrivée
            icon: mdi:calendar-clock
          - entity: sensor.lucas_next_departure
            name: Prochain départ
            icon: mdi:calendar-arrow-right
          - entity: sensor.lucas_days_remaining
            name: Jours restants
            icon: mdi:timer-outline
```

---

## Exemple 2 - Multi-enfants avec couleurs dédiées

Principe : une couleur fixe par enfant + une section dédiée par enfant.

Palette d'exemple :
- Lucas : `blue`
- Emma : `green`
- Noah : `deep-purple`

```yaml
title: Calendrier de garde
path: calendrier-garde
icon: mdi:calendar-month
type: sections
max_columns: 2
sections:
  - title: Légende enfants
    cards:
      - type: custom:mushroom-chips-card
        chips:
          - type: template
            content: Lucas
            icon: mdi:account-child
            icon_color: blue
          - type: template
            content: Emma
            icon: mdi:account-child
            icon_color: green
          - type: template
            content: Noah
            icon: mdi:account-child
            icon_color: deep-purple

  - title: Lucas
    cards:
      - type: custom:mushroom-template-card
        primary: Lucas
        secondary: "Couleur repère: bleu"
        icon: mdi:account-child
        icon_color: blue
      - type: entities
        entities:
          - entity: binary_sensor.lucas_presence
            name: Présence
          - entity: sensor.lucas_current_period
            name: Période actuelle
          - entity: sensor.lucas_days_remaining
            name: Jours restants
      - type: calendar
        title: Planning Lucas
        entities:
          - entity: calendar.lucas_calendar

  - title: Emma
    cards:
      - type: custom:mushroom-template-card
        primary: Emma
        secondary: "Couleur repère: vert"
        icon: mdi:account-child
        icon_color: green
      - type: entities
        entities:
          - entity: binary_sensor.emma_presence
            name: Présence
          - entity: sensor.emma_current_period
            name: Période actuelle
          - entity: sensor.emma_days_remaining
            name: Jours restants
      - type: calendar
        title: Planning Emma
        entities:
          - entity: calendar.emma_calendar

  - title: Noah
    cards:
      - type: custom:mushroom-template-card
        primary: Noah
        secondary: "Couleur repère: violet"
        icon: mdi:account-child
        icon_color: deep-purple
      - type: entities
        entities:
          - entity: binary_sensor.noah_presence
            name: Présence
          - entity: sensor.noah_current_period
            name: Période actuelle
          - entity: sensor.noah_days_remaining
            name: Jours restants
      - type: calendar
        title: Planning Noah
        entities:
          - entity: calendar.noah_calendar
```

---

## Checklist lisibilité

- Garder une couleur fixe par enfant dans toutes les cartes.
- Répéter le prénom dans le titre de section et le titre du calendrier.
- Éviter deux couleurs visuellement proches sur un même écran.
- Vérifier le contraste en thème clair et thème sombre.

