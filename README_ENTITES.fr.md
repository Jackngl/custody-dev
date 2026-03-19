# 📊 Guide des Entités - Custody

[🇫🇷 Version française](README_ENTITES.fr.md) | [🇬🇧 English version](README_ENTITES.md)

Ce guide explique toutes les entités créées par l'intégration **Custody** et comment les utiliser dans vos dashboards et automations Home Assistant.

---

## 📋 Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Entités disponibles](#entités-disponibles)
3. [Utilisation dans les dashboards](#utilisation-dans-les-dashboards)
4. [Exemples d'automations](#exemples-dautomations)
5. [Attributs disponibles](#attributs-disponibles)

---

## 🎯 Vue d'ensemble

L'intégration **Custody** crée automatiquement plusieurs entités pour chaque enfant configuré :

- **1 Binary Sensor** : Statut de présence
- **1 Calendar** : Calendrier complet
- **1 Device Tracker** : Suivi de présence (utilisable dans l'entité Personne)
- **9 Capteurs** : Informations détaillées sur la garde et les vacances

Toutes les entités sont préfixées par le **slug du prénom de l’enfant** : minuscules, espaces remplacés par des underscores (ex. « Sarah-Léa » → `sarah_lea`). Remplacez `{enfant}` dans les exemples par ce slug.

---

## 📦 Entités disponibles

### 1. Binary Sensor : Présence

**Nom de l'entité** : `binary_sensor.{enfant}_presence`  
**Nom affiché** : `{Enfant} Présence`

#### Description
Indique si l'enfant est actuellement en garde (garde classique ou vacances scolaires).

#### États
- **`on`** : L'enfant est actuellement en garde
- **`off`** : L'enfant n'est pas en garde actuellement
- **`unavailable`** : Données non disponibles

#### Attributs disponibles
- `child_name` : Nom de l'enfant
- `custody_type` : Type de garde classique configuré
- `next_arrival` : Prochaine arrivée (ISO format)
- `next_departure` : Prochain départ (ISO format)
- `vacation_name` : Nom des vacances en cours (si applicable)
- `next_vacation_name` : Nom des prochaines vacances
- `next_vacation_start` : Début des prochaines vacances (ISO format)
- `next_vacation_end` : Fin des prochaines vacances (ISO format)
- `days_until_vacation` : Jours jusqu'aux prochaines vacances
- `school_holidays_raw` : Liste complète des vacances scolaires

#### 🏠 Comportement en Mode Garde Complète
Si la **gestion de la garde est désactivée** :
- `custody_type` : Devient `None`.
- `next_arrival` : Devient `None` (forcé).
- `next_departure` : Devient `None` (forcé).
- `vacation_name` : Affiche la période de vacances complète sans découpage.
- **Sensors** : Les capteurs correspondants afficheront `unknown` ou `None`.


#### Utilisation
- **Dashboard** : Afficher un indicateur visuel de présence
- **Automation** : Déclencher des actions quand l'enfant arrive/part

---

### 2. Calendar : Calendrier complet

**Nom de l'entité** : `calendar.{enfant}_calendar`  
**Nom affiché** : `{Enfant} Calendrier`

#### Description
Calendrier complet affichant tous les événements de garde (weekends/semaines et vacances scolaires).

#### Caractéristiques
- Affiche tous les événements de garde classique (weekends, semaines)
- Affiche tous les événements de vacances scolaires
- Distinction visuelle entre garde classique et vacances scolaires
- Compatible avec les vues calendrier de Home Assistant

#### Types d'événements
1. **Garde normale** : Weekends et semaines de garde classique
2. **Vacances scolaires** : Périodes de vacances (Noël, Hiver, Printemps, Toussaint, Été)

#### Utilisation
- **Dashboard** : Intégrer dans une carte calendrier
- **Automation** : Utiliser les événements pour déclencher des actions
- **Vue calendrier** : Visualiser le planning complet

---

### 3. Device Tracker : Suivi de présence

**Nom de l'entité** : `device_tracker.{enfant}_tracker`  
**Nom affiché** : `{Enfant} Suivi`

#### Description
Dispositif de suivi basé sur la présence de l'enfant (garde classique ou vacances scolaires). Cette entité peut être utilisée dans l'entité **Personne** de Home Assistant pour créer un suivi de présence complet.

#### États
- **`home`** : L'enfant est actuellement en garde (présent)
- **`not_home`** : L'enfant n'est pas en garde actuellement (absent)
- **`unavailable`** : Données non disponibles

#### Attributs disponibles
- `child_name` : Nom de l'enfant
- `source` : Source du suivi (`custody_schedule`)
- `is_present` : État de présence (booléen)

#### Utilisation
- **Personne Home Assistant** : Associer ce device tracker à une personne pour le suivi de présence
- **Dashboard** : Afficher le statut de présence dans les cartes de personne
- **Automation** : Déclencher des actions basées sur la présence/absence
- **Zones** : Compatible avec le système de zones de Home Assistant

#### Configuration d'une Personne
1. Aller dans **Paramètres** → **Personnes et zones**
2. Cliquer sur **Créer une personne**
3. Nommer la personne (ex: "Sarah-Léa")
4. Dans **Dispositifs de suivi**, sélectionner `device_tracker.{enfant}_tracker`
5. Ajouter une photo si souhaité
6. Sauvegarder

#### Avantages
- ✅ Intégration native avec le système de Personnes de Home Assistant
- ✅ Mise à jour automatique toutes les 15 minutes
- ✅ Historique des changements de statut
- ✅ Utilisable dans les automations et les dashboards
- ✅ Compatible avec les zones personnalisées

---

### 4. Sensor : Prochaine arrivée

**Nom de l'entité** : `sensor.{enfant}_next_arrival`  
**Nom affiché** : `{Enfant} Prochaine arrivée`

#### Description
Date et heure de la prochaine arrivée de l'enfant (garde classique ou vacances).

#### Format
- **État** : Objet Timestamp (Home Assistant gère automatiquement l'affichage selon votre langue)
- **Classe** : `timestamp`

#### Utilisation
- **Dashboard** : Afficher le prochain rendez-vous
- **Automation** : Déclencher des actions avant l'arrivée

---

### 5. Sensor : Prochain départ

**Nom de l'entité** : `sensor.{enfant}_next_departure`  
**Nom affiché** : `{Enfant} Prochain départ`

#### Description
Date et heure du prochain départ de l'enfant (garde classique ou vacances).

#### Format
- **État** : Objet Timestamp (affichage automatique)
- **Classe** : `timestamp`

#### Utilisation
- **Dashboard** : Afficher le prochain départ
- **Automation** : Déclencher des actions avant le départ

---

### 6. Sensor : Jours restants

**Nom de l'entité** : `sensor.{enfant}_days_remaining`  
**Nom affiché** : `{Enfant} Jours restants`

#### Description
Nombre de jours restants avant le prochain changement de garde.

#### Format
- **État** : Nombre décimal (ex: `3.5`)
- **Unité** : `d` (affiché comme "jours" ou "days")
- **Type** : `duration` (durée)

#### Utilisation
- **Dashboard** : Afficher un compteur de jours
- **Automation** : Déclencher des actions selon le nombre de jours restants

---

### 7. Sensor : Période actuelle

**Nom de l'entité** : `sensor.{enfant}_current_period`  
**Nom affiché** : `{Enfant} Période actuelle`

#### Description
Période actuelle (garde classique, vacances scolaires, ou aucune).

#### États possibles (valeurs brutes de l’entité)
- `"school"` : Période hors vacances (garde classique : weekends/semaines)
- `"vacation"` : Période de vacances scolaires
- `None` ou vide : Aucune période de garde en cours (cas rare)

#### Utilisation
- **Dashboard** : Afficher le type de période actuelle
- **Automation** : Adapter le comportement selon le type de période

---

### 8. Sensor : Prochaines vacances

**Nom de l'entité** : `sensor.{enfant}_next_vacation_name`  
**Nom affiché** : `{Enfant} Prochaines vacances`

#### Description
Nom des prochaines vacances scolaires à venir.

#### États possibles
- Valeurs retournées par l’API des vacances scolaires (ex. `"Vacances de Noël"`, `"Vacances d'Hiver"`, `"Vacances de Printemps"`, `"Vacances de la Toussaint"`, `"Vacances d'Été"`).
- `unknown` ou vide : Aucune prochaine vacance programmée ou zone non configurée.

#### Utilisation
- **Dashboard** : Afficher le nom des prochaines vacances
- **Automation** : Adapter le comportement selon le type de vacances

---

### 9. Sensor : Date des prochaines vacances

**Nom de l'entité** : `sensor.{enfant}_next_vacation_start`  
**Nom affiché** : `{Enfant} Date des prochaines vacances`

#### Description
Date et heure de début des prochaines vacances scolaires.

#### Format
- **État** : Objet Timestamp (affichage automatique)
- **Classe** : `timestamp`

#### Utilisation
- **Dashboard** : Afficher la date de début des prochaines vacances
- **Automation** : Planifier des actions avant le début des vacances

---

### 10. Sensor : Jours jusqu'aux vacances

**Nom de l'entité** : `sensor.{enfant}_days_until_vacation`  
**Nom affiché** : `{Enfant} Jours jusqu'aux vacances`

#### Description
Nombre de jours restants avant le début des prochaines vacances scolaires.

#### Format
- **État** : Nombre décimal (ex: `15.5`)
- **Unité** : `d`
- **Type** : `duration` (durée)

#### Utilisation
- **Dashboard** : Afficher un compteur de jours avant les vacances
- **Automation** : Déclencher des actions avant les vacances


### 11. Capteur : Prochain changement

**Nom de l'entité** : `sensor.{enfant}_next_change`  
**Nom d'affichage** : `{Enfant} Prochain changement`

#### Description
Capteur combiné résumant le prochain événement (arrivée ou départ).

#### Format
- **État** : Texte (ex : "16:15" si aujourd'hui, ou "Vendredi 21/02")
- **Icône** : `mdi:calendar-sync`

---

### 12. Capteur : Lieu de garde

**Nom de l'entité** : `sensor.{enfant}_parent_in_charge`  
**Nom d'affichage** : `{Enfant} Lieu de garde`

#### Description
État explicite indiquant chez qui se trouve l'enfant.

#### États
- **`home`** : Chez moi (Présent)
- **`away`** : Chez l'autre parent (Absent)

#### Icône
Dynamique : `mdi:home-account` si présent, `mdi:account-arrow-right` si absent.

---

## 🎨 Utilisation dans les dashboards

### Exemple 0 : Carte Personne avec device tracker

```yaml
type: person
entity: person.sarah_lea
```

Cette carte affiche automatiquement :
- Le statut de présence (home/not_home)
- La photo de la personne
- L'historique des changements de statut
- Compatible avec les zones personnalisées

---

### Exemple 1 : Carte de présence simple

```yaml
type: entities
title: Custody - {Enfant}
entities:
  - entity: binary_sensor.{enfant}_presence
    name: Présence
    icon: mdi:account-check
  - entity: sensor.{enfant}_current_period
    name: Période actuelle
  - entity: sensor.{enfant}_days_remaining
    name: Jours restants
```

### Exemple 2 : Carte avec prochaines dates

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Prochaines dates
    entities:
      - entity: sensor.{enfant}_next_arrival
        name: Prochaine arrivée
        icon: mdi:calendar-clock
      - entity: sensor.{enfant}_next_departure
        name: Prochain départ
        icon: mdi:calendar-arrow-right
  - type: entities
    title: Vacances scolaires
    entities:
      - entity: sensor.{enfant}_next_vacation_name
        name: Prochaines vacances
        icon: mdi:calendar-star
      - entity: sensor.{enfant}_days_until_vacation
        name: Jours jusqu'aux vacances
        icon: mdi:calendar-clock
```

### Exemple 3 : Carte calendrier

```yaml
type: calendar
entities:
  - entity: calendar.{enfant}_calendar
title: Custody - {Enfant}
```

### Exemple 3 bis : Carte calendrier (vue mensuelle)

```yaml
type: calendar
entities:
  - entity: calendar.{enfant}_calendar
title: Custody - {Enfant}
initial_view: dayGridMonth
```

### Exemple 4 : Carte personnalisée avec badges

```yaml
type: custom:mushroom-entity-card
entity: binary_sensor.{enfant}_presence
name: Présence
icon: mdi:account-check
secondary_info: last-updated
tap_action:
  action: navigate
  navigation_path: /lovelace/planning
```

💡 Pour une vue dédiée **"Calendrier de garde"** (single-child + multi-enfants avec couleurs par enfant), utilisez le guide :
**[README_DASHBOARD_GARDE.fr.md](README_DASHBOARD_GARDE.fr.md)**.

---

## 🤖 Exemples d'automations

### Automation 1 : Notification avant l'arrivée

```yaml
alias: "Notification avant arrivée {Enfant}"
description: "Envoie une notification 1 heure avant l'arrivée de l'enfant"
trigger:
  - platform: template
    value_template: >
      {% set next_arrival = states('sensor.{enfant}_next_arrival') %}
      {% if next_arrival != 'unknown' and next_arrival != '' %}
        {{ (as_timestamp(next_arrival) - as_timestamp(now()) <= 3600) and
           (as_timestamp(next_arrival) - as_timestamp(now()) > 0) }}
      {% else %}
        false
      {% endif %}
condition:
  - condition: state
    entity_id: binary_sensor.{enfant}_presence
    state: 'off'
action:
  - service: notify.mobile_app_votre_telephone
    data:
      title: "Arrivée de {Enfant}"
      message: "{{ states('sensor.{enfant}_next_arrival') }}"
      data:
        actions:
          - action: "URI"
            title: "Voir le planning"
            uri: "/lovelace/planning"
```

### Automation 2 : Chauffage automatique avant arrivée

```yaml
alias: "Chauffage avant arrivée {Enfant}"
description: "Active le chauffage 2 heures avant l'arrivée"
trigger:
  - platform: template
    value_template: >
      {% set next_arrival = states('sensor.{enfant}_next_arrival') %}
      {% if next_arrival != 'unknown' and next_arrival != '' %}
        {{ (as_timestamp(next_arrival) - as_timestamp(now()) <= 7200) and
           (as_timestamp(next_arrival) - as_timestamp(now()) > 0) }}
      {% else %}
        false
      {% endif %}
condition:
  - condition: state
    entity_id: binary_sensor.{enfant}_presence
    state: 'off'
action:
  - service: climate.set_temperature
    target:
      entity_id: climate.salon
    data:
      temperature: 20
```

### Automation 3 : Éclairage automatique pendant la garde

```yaml
alias: "Éclairage pendant garde {Enfant}"
description: "Allume les lumières quand l'enfant est en garde le soir"
trigger:
  - platform: state
    entity_id: binary_sensor.{enfant}_presence
    to: 'on'
condition:
  - condition: time
    after: '18:00:00'
    before: '23:00:00'
action:
  - service: light.turn_on
    target:
      entity_id: light.chambre_enfant
    data:
      brightness: 100
```

### Automation 4 : Notification avant les vacances

```yaml
alias: "Notification avant vacances {Enfant}"
description: "Notifie 7 jours avant le début des vacances"
trigger:
  - platform: template
    value_template: >
      {% set days_until = states('sensor.{enfant}_days_until_vacation') | float(0) %}
      {{ days_until <= 7 and days_until > 6 }}
action:
  - service: notify.mobile_app_votre_telephone
    data:
      title: "Vacances approchent !"
      message: >
        Les {{ states('sensor.{enfant}_next_vacation_name') }} 
        commencent dans {{ states('sensor.{enfant}_days_until_vacation') }} jours
```

### Automation 5 : Mode "Vacances" automatique

```yaml
alias: "Mode vacances {Enfant}"
description: "Active un mode spécial pendant les vacances scolaires"
trigger:
  - platform: state
    entity_id: sensor.{enfant}_current_period
    to: 'vacation'
action:
  - service: input_select.select_option
    target:
      entity_id: input_select.mode_maison
    data:
      option: "Vacances"
  - service: notify.mobile_app_votre_telephone
    data:
      title: "Vacances scolaires"
      message: "Mode vacances activé pour {{ states('sensor.{enfant}_next_vacation_name') }}"
```

### Automation 6 : Compteur de jours restants

```yaml
alias: "Alerte fin de garde {Enfant}"
description: "Notifie quand il reste moins de 1 jour de garde"
trigger:
  - platform: template
    value_template: >
      {% set days_remaining = states('sensor.{enfant}_days_remaining') | float(0) %}
      {{ days_remaining <= 1 and days_remaining > 0 }}
condition:
  - condition: state
    entity_id: binary_sensor.{enfant}_presence
    state: 'on'
action:
  - service: notify.mobile_app_votre_telephone
    data:
      title: "Fin de garde proche"
      message: >
        Il reste {{ states('sensor.{enfant}_days_remaining') }} jour(s) 
        avant le prochain départ
```

---

## 📝 Attributs disponibles

Toutes les entités partagent des attributs communs accessibles via `{{ state_attr('entity_id', 'attribute_name') }}` :

### Attributs de base
- `child_name` : Nom de l'enfant
- `custody_type` : Type de garde classique (ex: `alternate_week`, `alternate_weekend`)
- `current_period` : Période actuelle — valeurs brutes : `school` (hors vacances), `vacation` (vacances scolaires), ou vide

### Attributs de dates
- `next_arrival` : Prochaine arrivée (ISO format)
- `next_departure` : Prochain départ (ISO format)
- `days_remaining` : Jours restants avant changement

### Attributs de vacances
- `vacation_name` : Nom des vacances en cours
- `next_vacation_name` : Nom des prochaines vacances
- `next_vacation_start` : Début des prochaines vacances (ISO format)
- `next_vacation_end` : Fin des prochaines vacances (ISO format)
- `days_until_vacation` : Jours jusqu'aux prochaines vacances
- `school_holidays_raw` : Liste complète des vacances (format JSON)

### Attributs de configuration
- `location` : Lieu d'échange (si configuré)
- `notes` : Notes personnalisées (si configurées)
- `zone` : Zone scolaire ou Subdivision (A, B, C, Cantons, etc.)

---

## 💡 Conseils d'utilisation

### Pour les dashboards
1. **Utilisez des cartes conditionnelles** pour afficher différentes informations selon la période
2. **Combinez plusieurs entités** dans une seule carte pour une vue d'ensemble
3. **Utilisez les icônes** pour rendre les cartes plus visuelles
4. **Créez des vues séparées** pour la garde classique et les vacances scolaires

### Pour les automations
1. **Vérifiez toujours l'état** de `binary_sensor.{enfant}_presence` avant d'agir
2. **Utilisez les templates** pour calculer les délais avant les événements
3. **Testez avec des valeurs de test** avant de mettre en production
4. **Ajoutez des conditions** pour éviter les déclenchements multiples

### Bonnes pratiques
- **Nommez clairement** vos automations avec le nom de l'enfant
- **Documentez** vos automations personnalisées
- **Testez** régulièrement que les entités sont à jour
- **Utilisez les attributs** pour obtenir plus d'informations que l'état seul

---

## 🔧 Dépannage

### Les entités ne se mettent pas à jour
1. Vérifiez que l'intégration est bien configurée
2. Redémarrez Home Assistant
3. Vérifiez les logs pour des erreurs

### Les dates sont incorrectes
1. Vérifiez la configuration de la zone scolaire
2. Vérifiez que `reference_year_custody` (garde classique) et la répartition des vacances sont correctement configurés
3. Vérifiez les horaires d'arrivée/départ

### Les vacances ne s'affichent pas
1. Vérifiez que la zone scolaire est correcte
2. Vérifiez la connexion à l'API des vacances scolaires
3. Consultez les logs pour des erreurs API

---

## 📚 Ressources supplémentaires

- **Documentation garde classique** : [`README_CONFIG_GARDE.fr.md`](README_CONFIG_GARDE.fr.md) ([English](README_CONFIG_GARDE.md))
- **Documentation vacances scolaires** : [`README_CONFIG_VACANCES.fr.md`](README_CONFIG_VACANCES.fr.md) ([English](README_CONFIG_VACANCES.md))
- **Documentation principale** : [`README.fr.md`](README.fr.md) ([English](README.md))

---

## ✅ Récapitulatif des entités

| Type | Entity ID | Nom affiché | Description |
|------|-----------|-------------|-------------|
| Binary Sensor | `binary_sensor.{enfant}_presence` | {Enfant} Présence | Statut de présence |
| Calendar | `calendar.{enfant}_calendar` | {Enfant} Calendrier | Calendrier complet |
| Device Tracker | `device_tracker.{enfant}_tracker` | {Enfant} Tracker / Suivi | Présence (home/not_home) |
| Sensor | `sensor.{enfant}_next_arrival` | {Enfant} Prochaine arrivée | Date/heure arrivée |
| Sensor | `sensor.{enfant}_next_departure` | {Enfant} Prochain départ | Date/heure départ |
| Sensor | `sensor.{enfant}_days_remaining` | {Enfant} Jours restants | Jours avant changement |
| Sensor | `sensor.{enfant}_current_period` | {Enfant} Période actuelle | `school` / `vacation` |
| Sensor | `sensor.{enfant}_next_vacation_name` | {Enfant} Prochaines vacances | Nom des vacances |
| Sensor | `sensor.{enfant}_next_vacation_start` | {Enfant} Début des vacances | Date de début |
| Sensor | `sensor.{enfant}_days_until_vacation` | {Enfant} Jours jusqu'aux vacances | Jours avant vacances |
| Sensor | `sensor.{enfant}_next_change` | {Enfant} Prochain changement | Résumé prochain événement |
| Sensor | `sensor.{enfant}_parent_in_charge` | {Enfant} Lieu de garde | home / away |

---

**Note** : Remplacez `{enfant}` par le slug du prénom de l’enfant (minuscules, espaces → underscores, ex. `lucas`, `sarah_lea`).
