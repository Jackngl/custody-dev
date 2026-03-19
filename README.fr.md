<div align="center">

# 👨‍👩‍👧‍👦 Custody Schedule

**Intégration Home Assistant pour la gestion intelligente des gardes alternées**

[![Version](https://img.shields.io/badge/version-1.8.37-blue.svg)](https://github.com/Jackngl/custody/releases)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.12-green.svg)](https://www.home-assistant.io/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)

<img src="https://github.com/Jackngl/custody-dev/raw/main/brand/logo.png" alt="Custody Schedule Logo" width="200"/>

[🇫🇷 Version française](README.fr.md) | [🇬🇧 English version](README.md)

</div>

---

## 📖 À propos

**Custody Schedule** est une intégration complète pour Home Assistant qui simplifie la gestion des gardes alternées. Elle automatise le calcul des périodes de garde, synchronise avec votre calendrier, et permet d'automatiser votre maison intelligente selon la présence des enfants.

### ✨ Pourquoi Custody Schedule ?

- 🎯 **Configuration intuitive** : Interface guidée étape par étape
- 🤖 **Automatisation complète** : Calcul intelligent des périodes et gestion des vacances scolaires
- 📅 **Synchronisation calendrier** : Intégration native avec Google Calendar
- 🏠 **Automatisation domotique** : Contrôle du chauffage, lumières, notifications selon la présence
- 🌍 **Support international** : Zones scolaires françaises, belges, suisses, luxembourgeoises et québécoises
- 🗣️ **Assistants vocaux** : Compatible avec Alexa et Home Assistant Assist

---

## 🚀 Démarrage rapide

### Installation via HACS (recommandé)

1. **Installer HACS** si nécessaire : [Documentation HACS](https://hacs.xyz/docs/setup/download)

2. **Ajouter le dépôt** :
   
   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Jackngl&repository=custody&category=integration)
   
   *Ou ajoutez manuellement* : `https://github.com/Jackngl/custody` dans **HACS** > **Dépôts personnalisés**

3. **Installer et redémarrer** :
   - Cliquez sur **Télécharger** dans HACS
   - Redémarrez Home Assistant

4. **Configurer** :
   - **Paramètres** → **Appareils & services** → **Ajouter une intégration**
   - Recherchez "Custody" et suivez l'assistant de configuration

### Installation manuelle

```bash
cd /config
git clone https://github.com/Jackngl/custody.git
cp -r custody/custom_components/custody_schedule /config/custom_components/
```

Redémarrez Home Assistant puis ajoutez l'intégration via l'interface.

---

## ✨ Fonctionnalités principales

### 🎛️ Configuration simplifiée

- Parcours guidé avec labels clairs (enfant ➜ garde ➜ vacances ➜ options)
- Interface utilisateur intuitive et complète
- Support multi-enfants avec configurations indépendantes

### 🧮 Calcul intelligent

- **Rythmes de garde** :
  - Semaine alternée (1/1)
  - Week-end alterné
  - Rythme personnalisé (sélection jour par jour sur 14 jours)
  - Rythmes 2-2-3 ou 2-2-5-5
  - **Jour de retour** flexible (ex: Dimanche soir ou Lundi matin à l'école)
  - Exceptions et règles personnalisées (dates fixes)

- **Gestion des vacances** :
  - Alternance automatique des vacances chaque année
  - Gestion des priorités (vacances et fêtes parentales découpent proprement les week-ends)
  - **Extensions de garde intelligentes** : Report automatique de la fin de garde si le jour de retour est un jour férié (ex: retour école lundi férié reporté au mardi)
  - Règles flexibles : 1ère/2ème semaine, moitiés, semaines paires/impaires, juillet/août
  - Gestion automatique des Fêtes des Mères et des Pères

- **Support International** :
  - 🇫🇷 **France** : API officielle (`data.education.gouv.fr`) pour les vacances scolaires (Zones A, B, C, etc.)
  - 🇧🇪 **Belgique**, 🇨🇭 **Suisse**, 🇱🇺 **Luxembourg** : API OpenHolidays pour les vacances scolaires (Communautés/Cantons/National)
  - 🇨🇦 **Canada (Québec)** : API Canada-Holidays pour les jours fériés (Fériés officiels)
- **URL d'API personnalisable** pour sources alternatives
- **Service de test** intégré pour diagnostiquer les problèmes

### 🔗 Intégrations

- **Synchronisation Google Calendar** : Création et suppression automatique des événements
- **Calendrier intégré** : Visualisation complète des périodes de garde
- **Événements Home Assistant** : Déclencheurs pour automatisations
- **Services dédiés** : Exceptions, forcer présence/absence, recalcul

### 🎙️ Assistants vocaux

- **Amazon Alexa** : Blueprints pour annonces automatiques
- **Home Assistant Assist** : Questions naturelles sur la présence
- **Support bilingue** : Français et Anglais

---

## ⚙️ Configuration

La configuration se fait entièrement via l'interface utilisateur Home Assistant.

### Étapes de configuration

1. **Informations de l'enfant** : Nom, icône, photo
2. **Rythme de garde** : Sélection du rythme (semaine alternée, weekend, etc.) et année de référence
3. **Horaires et Jour de retour** : Heures d'arrivée/départ, jour de reprise de l'école et lieu
4. **Pays et Vacances** :
   - Choix du pays (France, Belgique, Suisse, Luxembourg, Canada)
   - Zone ou Subdivision (A/B/C pour FR, Cantons pour CH, Communautés pour BE)
   - Règles de partage des vacances (moitiés, parité)
5. **Options avancées** :
   - Notes personnalisées
   - Notifications
   - Synchronisation calendrier (Google Calendar)
   - Exceptions (UI avancée)
   - URL d'API personnalisée (optionnel)

### Synchronisation Google Calendar

Activez la synchronisation pour créer automatiquement les événements de garde sur votre calendrier Home Assistant.

**Configuration** :
1. **Paramètres** → **Appareils & services** → **Custody** → **Options**
2. Sélectionnez **Options avancées**
3. Activez **Synchronisation Google Calendar**
4. Choisissez le **Calendrier cible**
5. Définissez la **fenêtre de synchro** (3, 6, 12 ou 24 mois)
6. Définissez l'**intervalle de synchro** (défaut : 1 heure)

### Exceptions

Gérez les exceptions (jours supplémentaires, gardes en semaine, etc.) via l'interface :

1. **Paramètres** → **Appareils & services** → **Custody** → **Options**
2. Sélectionnez **Exceptions**
3. Ajoutez, modifiez ou supprimez une exception (début + fin + titre)

#### Exceptions récurrentes

Dans le même écran, gérez des exceptions récurrentes (hebdomadaires) :
- Jour de la semaine + heure début/fin
- Optionnel : date de début / date de fin

Les exceptions (ponctuelles et récurrentes) apparaissent dans le calendrier de l'intégration.

### Configuration de l'URL d'API

Pour utiliser une API alternative pour les vacances scolaires :

1. **Paramètres** → **Appareils & services** → **Custody** → **Options**
2. Sélectionnez **Options avancées**
3. Entrez votre URL personnalisée dans **URL API vacances scolaires**
   - L'URL doit contenir les placeholders `{year}` et `{zone}`
   - Exemple : `https://api.example.com/holidays?year={year}&zone={zone}`

---

## 🛠️ Diagnostic et Nettoyage (Purge)

Si vous constatez des doublons ou des événements qui ne se suppriment pas correctement dans votre Google Calendar, utilisez le service de purge robuste.

Depuis la version 1.3.0, la purge utilise une méthode d'accès direct aux entités Home Assistant pour récupérer les identifiants réels (UID).

### Purge manuelle

1. Allez dans **Outils de développement** → **Actions** (ou Services)
2. Sélectionnez `Custody: Purger les événements Google` (service `custody_schedule.purge_calendar_events`)
3. Passez en **mode YAML** et utilisez :

```yaml
action: custody_schedule.purge_calendar_events
data:
  entry_id: "VOTRE_ENTRY_ID"
  days: 365
  debug: true
```

> [!TIP]
> Pour trouver votre `entry_id`, utilisez ce modèle dans l'outil Modèles de HA :
> `{{ config_entry_id('binary_sensor.NOM_ENFANT_presence') }}`

---

## 🎨 Tableaux de bord (Lovelace)

### Carte Mushroom (Recommandé 🌟)

Cette carte change de couleur et d'icône selon la présence de l'enfant.

```yaml
type: custom:mushroom-template-card
primary: |-
  {% if is_state('binary_sensor.lucas_presence', 'on') %}
    Lucas est à la maison
  {% else %}
    Lucas est chez l'autre parent
  {% endif %}
secondary: |-
  {% if is_state('binary_sensor.lucas_presence', 'on') %}
    Départ : {{ states('sensor.lucas_next_departure') }}
  {% else %}
    Retour : {{ states('sensor.lucas_next_arrival') }}
  {% endif %}
icon: |-
  {% if is_state('binary_sensor.lucas_presence', 'on') %}
    mdi:home-heart
  {% else %}
    mdi:home-export-outline
  {% endif %}
icon_color: |-
  {% if is_state('binary_sensor.lucas_presence', 'on') %}
    blue
  {% else %}
    grey
  {% endif %}
tap_action:
  action: navigate
  navigation_path: /config/devices/dashboard
```

### Badge de statut minimaliste

Idéal pour une vue condensée en haut de dashboard.

```yaml
type: custom:mushroom-chips-card
chips:
  - type: template
    content: "Lucas: {{ states('sensor.lucas_days_remaining') }}j"
    icon: mdi:account-clock
    icon_color: "{{ 'green' if is_state('binary_sensor.lucas_presence', 'on') else 'orange' }}"
    tap_action:
      action: more-info
      entity: binary_sensor.lucas_presence
```

---

## 🔧 Services disponibles

### `custody_schedule.set_manual_dates`

Ajoute des périodes ponctuelles de présence (vacances, échanges spécifiques).

**Paramètres** :
- `entry_id` (requis) : ID de l'intégration
- `dates` (requis) : Liste de périodes avec `start`, `end`, et optionnellement `label`

**Exemple** :
```yaml
action: custody_schedule.set_manual_dates
data:
  entry_id: "1234567890abcdef1234567890abcdef"
  dates:
    - start: "2024-07-15T08:00:00+02:00"
      end: "2024-07-22T19:00:00+02:00"
      label: "Vacances chez papa"
```

### `custody_schedule.override_presence`

Force l'état présent/absent pour une durée donnée.

**Paramètres** :
- `entry_id` (requis) : ID de l'intégration
- `state` (requis) : `on` (présent) ou `off` (absent)
- `duration` (optionnel) : Durée en minutes

**Exemple** :
```yaml
action: custody_schedule.override_presence
data:
  entry_id: "1234567890abcdef1234567890abcdef"
  state: "on"
  duration: 120  # 2 heures
```

### `custody_schedule.refresh_schedule`

Déclenche immédiatement un recalcul du planning.

**Paramètres** :
- `entry_id` (requis) : ID de l'intégration

**Exemple** :
```yaml
action: custody_schedule.refresh_schedule
data:
  entry_id: "1234567890abcdef1234567890abcdef"
```

### `custody_schedule.test_holiday_api`

Teste la connexion à l'API des vacances scolaires et affiche les résultats dans les logs.

**Paramètres** :
- `entry_id` (optionnel) : ID de l'intégration (utilise la config de cette intégration)
- `zone` (optionnel, défaut: "A") : Zone scolaire à tester
- `year` (optionnel) : Année scolaire au format "2024-2025"

**Exemple** :
```yaml
action: custody_schedule.test_holiday_api
data:
  entry_id: "1234567890abcdef1234567890abcdef"
  zone: "C"
  year: "2024-2025"
```

### `custody_schedule.export_exceptions`

Exporte les exceptions (ponctuelles + récurrentes) vers un fichier JSON dans `/config/www`.

**Paramètres** :
- `entry_id` (requis) : ID de l'intégration
- `filename` (optionnel) : Nom du fichier (ex: `custody_exceptions.json`)

**Exemple** :
```yaml
action: custody_schedule.export_exceptions
data:
  entry_id: "1234567890abcdef1234567890abcdef"
  filename: "custody_exceptions.json"
```

### `custody_schedule.import_exceptions`

Importe des exceptions depuis un fichier JSON ou un payload direct.

**Paramètres** :
- `entry_id` (requis) : ID de l'intégration
- `filename` (optionnel) : Nom du fichier dans `/config/www`
- `exceptions` (optionnel) : Liste d'exceptions ponctuelles
- `recurring` (optionnel) : Liste d'exceptions récurrentes

**Exemple** :
```yaml
action: custody_schedule.import_exceptions
data:
  entry_id: "1234567890abcdef1234567890abcdef"
  filename: "custody_exceptions.json"
```

### `custody_schedule.purge_calendar_events`

Supprime manuellement les événements du calendrier. Cette méthode identifie les événements créés par Custody même lorsqu'ils sont orphelins ou dupliqués.

**Paramètres** :
- `entry_id` (requis) : ID de l'intégration
- `days` (optionnel) : Fenêtre de scan en jours (défaut: 365)
- `include_unmarked` (optionnel) : Tente de supprimer même les événements sans marqueur explicite
- `purge_all` (optionnel) : Supprime absolument TOUS les événements trouvés (attention)
- `match_text` (optionnel) : Supprime les événements contenant ce texte dans le résumé
- `debug` (optionnel) : Affiche les détails techniques dans les logs (recommandé)

**Exemple** :
```yaml
action: custody_schedule.purge_calendar_events
data:
  entry_id: "01KF1ZW5K8JNX55258QBCF1STF"
  debug: true
```

---

## 📡 Événements Home Assistant

L'intégration émet automatiquement des événements pour déclencher des automatisations :

### `custody_arrival`

Déclenché quand l'enfant arrive (transition de `off` à `on`).

**Données** :
- `entry_id` : ID de l'intégration
- `child` : Nom de l'enfant
- `next_departure` : Prochain départ (ISO format)
- `next_arrival` : Prochaine arrivée (ISO format)

### `custody_departure`

Déclenché quand l'enfant part (transition de `on` à `off`).

**Données** :
- `entry_id` : ID de l'intégration
- `child` : Nom de l'enfant
- `next_departure` : Prochain départ (ISO format)
- `next_arrival` : Prochaine arrivée (ISO format)

### `custody_vacation_start`

Déclenché au début des vacances scolaires.

**Données** :
- `entry_id` : ID de l'intégration
- `holiday` : Nom de la période de vacances

### `custody_vacation_end`

Déclenché à la fin des vacances scolaires.

**Données** :
- `entry_id` : ID de l'intégration
- `holiday` : Nom de la période de vacances qui se termine

---

## 📊 Entités générées

Pour chaque enfant configuré, les entités suivantes sont créées automatiquement :

| Entité | Type | Description |
|--------|------|-------------|
| `binary_sensor.<nom>_presence` | Binary Sensor | État présent/absent (`on`/`off`) |
| `device_tracker.<nom>_tracker` | Device Tracker | Suivi de présence (`home`/`not_home`) |
| `sensor.<nom>_next_arrival` | Sensor | Prochaine arrivée (datetime) |
| `sensor.<nom>_next_departure` | Sensor | Prochain départ (datetime) |
| `sensor.<nom>_days_remaining` | Sensor | Jours restants avant prochain changement |
| `sensor.<nom>_current_period` | Sensor | Période actuelle (`school`/`vacation`) |
| `sensor.<nom>_next_vacation_name` | Sensor | Prochaines vacances scolaires |
| `sensor.<nom>_next_vacation_start` | Sensor | Date des prochaines vacances |
| `sensor.<nom>_days_until_vacation` | Sensor | Jours jusqu'aux vacances |
| `calendar.<nom>_calendar` | Calendar | Calendrier avec toutes les périodes |

> **Note** : `<nom>` correspond au nom de l'enfant normalisé en minuscules avec les espaces remplacés par des underscores. Les `entity_id` sont toujours en anglais (ASCII uniquement), même si le nom d'affichage contient des accents.
>
> **Exemples** :
> - "Lucas" → `binary_sensor.lucas_presence`, `calendar.lucas_calendar`
> - "Sarah-Léa" → `binary_sensor.sarah_lea_presence`, `calendar.sarah_lea_calendar`
> - "François" → `binary_sensor.francois_presence`, `calendar.francois_calendar`

Les noms affichés dans l'interface Home Assistant sont localisés selon la langue configurée (français/anglais) et préservent les caractères originaux du nom.

**Attributs disponibles** :
- `vacation_name` : Nom de la période de vacances en cours
- `zone` : Zone scolaire configurée
- `location` : Lieu configuré
- `notes` : Notes configurées

---

## 🤖 Automatisations et exemples

### 1. Ajuster le chauffage selon la présence

```yaml
automation:
  - alias: "Chauffage chambre enfant"
    description: "Ajuste le chauffage selon la présence de l'enfant"
    trigger:
      - platform: state
        entity_id: binary_sensor.lucas_presence
    action:
      - service: climate.set_preset_mode
        target:
          entity_id: climate.chambre_lucas
        data:
          preset_mode: "{{ 'comfort' if trigger.to_state.state == 'on' else 'eco' }}"
      - service: climate.set_temperature
        target:
          entity_id: climate.chambre_lucas
        data:
          temperature: "{{ 20 if trigger.to_state.state == 'on' else 16 }}"
```

### 2. Notification avant l'arrivée

```yaml
automation:
  - alias: "Notification arrivée enfant"
    description: "Notifie 1 jour avant l'arrivée"
    trigger:
      - platform: numeric_state
        entity_id: sensor.lucas_days_remaining
        below: 1
        above: 0
    condition:
      - condition: state
        entity_id: binary_sensor.lucas_presence
        state: "off"
    action:
      - service: notify.mobile_app_telephone
        data:
          message: "Lucas arrive demain ! N'oublie pas de préparer sa chambre."
          title: "Arrivée prévue"
```

### 3. Allumer les lumières à l'arrivée

```yaml
automation:
  - alias: "Lumières à l'arrivée"
    description: "Allume les lumières quand l'enfant arrive"
    trigger:
      - platform: event
        event_type: custody_arrival
        event_data:
          entry_id: "1234567890abcdef1234567890abcdef"
    action:
      - service: light.turn_on
        target:
          entity_id: light.chambre_lucas
        data:
          brightness: 200
          color_temp: 370
```

### 4. Éteindre les appareils au départ

```yaml
automation:
  - alias: "Économie d'énergie au départ"
    description: "Éteint les appareils quand l'enfant part"
    trigger:
      - platform: event
        event_type: custody_departure
        event_data:
          entry_id: "1234567890abcdef1234567890abcdef"
    action:
      - service: light.turn_off
        target:
          entity_id: 
            - light.chambre_lucas
            - light.bureau_lucas
      - service: climate.set_preset_mode
        target:
          entity_id: climate.chambre_lucas
        data:
          preset_mode: "away"
```

### 5. Notification début de vacances

```yaml
automation:
  - alias: "Notification début vacances"
    description: "Notifie au début des vacances scolaires"
    trigger:
      - platform: event
        event_type: custody_vacation_start
        event_data:
          entry_id: "1234567890abcdef1234567890abcdef"
    action:
      - service: notify.mobile_app_telephone
        data:
          message: "Les vacances de {{ trigger.event.data.holiday }} commencent !"
          title: "Vacances scolaires"
```

### 6. Dashboard conditionnel

```yaml
type: entities
title: Custody
entities:
  - entity: binary_sensor.lucas_presence
    name: Présence
  - entity: sensor.lucas_next_arrival
    name: Prochaine arrivée
  - entity: sensor.lucas_next_departure
    name: Prochain départ
  - entity: sensor.lucas_days_remaining
    name: Jours restants
  - entity: sensor.lucas_current_period
    name: Période
  - type: custom:auto-entities
    card:
      type: entities
      title: "Détails"
    filter:
      include:
        - entity_id: sensor.lucas_*
          attributes:
            - vacation_name
            - zone
            - location
```

### 7. Script pour forcer présence temporaire

```yaml
script:
  presence_temporaire:
    alias: "Forcer présence temporaire"
    sequence:
      - service: custody_schedule.override_presence
        data:
          entry_id: "1234567890abcdef1234567890abcdef"
          state: "on"
          duration: 180  # 3 heures
      - service: notify.mobile_app_telephone
        data:
          message: "Présence forcée pour 3 heures"
```

### 8. Automatisation basée sur les jours restants

```yaml
automation:
  - alias: "Préparer chambre 2 jours avant"
    description: "Active le chauffage 2 jours avant l'arrivée"
    trigger:
      - platform: numeric_state
        entity_id: sensor.lucas_days_remaining
        below: 2.5
        above: 1.5
    condition:
      - condition: state
        entity_id: binary_sensor.lucas_presence
        state: "off"
    action:
      - service: climate.set_preset_mode
        target:
          entity_id: climate.chambre_lucas
        data:
          preset_mode: "comfort"
```

---

## 🎙️ Assistants Vocaux

### Amazon Alexa

Utilisez un **Blueprint** pour qu'Alexa annonce automatiquement les changements de garde sur vos enceintes (Echo, Dot, etc.).

**Configuration** :
1. Téléchargez `alexa_custody_announcement.yaml` depuis le dossier `blueprints`
2. Placez-le dans `/config/blueprints/automation/`
3. **Paramètres** → **Automatisations et scènes** → **Blueprints**
4. Créez une automatisation à partir du modèle "Annonce Alexa - Changement de Garde"

### Home Assistant Assist

Grâce à la classe d'appareil `presence` sur les capteurs binaires, posez des questions naturelles :
- *"Est-ce que Lucas est présent ?"*
- *"Quel est le statut de présence de Lucas ?"*

> [!TIP]
> Pour une meilleure expérience avec Alexa, exposez l'entité `binary_sensor.<nom>_presence` via Nabu Casa ou votre intégration manuelle Alexa.

---

## 🌐 API des vacances scolaires

L'intégration utilise l'API officielle du ministère de l'Éducation nationale (`data.education.gouv.fr`) pour récupérer automatiquement les dates des vacances scolaires.

### Fonctionnalités

- ✅ Récupération automatique des vacances par zone (A, B, C, Corse, DOM-TOM)
- ✅ Gestion des années scolaires (format "2024-2025")
- ✅ Cache intelligent pour réduire les appels API
- ✅ Support multi-entrées avec URLs d'API différentes
- ✅ Service de test pour diagnostiquer les problèmes

### Zones supportées

- **Zone A** : Besançon, Bordeaux, Clermont-Ferrand, Dijon, Grenoble, Limoges, Lyon, Poitiers
- **Zone B** : Aix-Marseille, Amiens, Lille, Nancy-Metz, Nantes, Nice, Normandie, Orléans-Tours, Reims, Rennes, Strasbourg
- **Zone C** : Créteil, Montpellier, Paris, Toulouse, Versailles
- **Corse** : Corse
- **DOM-TOM** : Guadeloupe (par défaut), Martinique, Guyane, La Réunion, Mayotte

### Personnalisation de l'API

Vous pouvez configurer une URL d'API personnalisée dans les options avancées. L'URL doit contenir les placeholders `{year}` et `{zone}`.

**Format attendu** :
```
https://api.example.com/holidays?year={year}&zone={zone}
```

### Tester l'API

Utilisez le service `custody_schedule.test_holiday_api` pour tester la connexion :

```yaml
service: custody_schedule.test_holiday_api
data:
  zone: "A"
  year: "2024-2025"
```

Les résultats sont disponibles dans les logs Home Assistant (**Paramètres** → **Système** → **Logs**).

---

## 🗺️ Roadmap

### v1.0 ✅
- [x] Configuration UI complète
- [x] Calcul automatique des périodes
- [x] API vacances scolaires
- [x] Services et événements
- [x] Support multi-enfants
- [x] URL API personnalisable
- [x] Service de test API

### v1.1 ✅
- [x] Calendrier avancé avec vue mensuelle
- [x] Synchronisation Google Calendar
- [x] Notifications natives Home Assistant
- [x] Gestion d'exceptions avancée
- [x] Export PDF du planning

### v1.5 ✅
- [x] Dashboards Lovelace "Ready-to-use" (Exemples premium)
- [x] Support des jours fériés régionaux (Alsace-Moselle)
- [x] Localisation française intégrale
- [x] Nettoyage automatique des logs de démarrage

### v1.7 ✅
- [x] **Support Vocal** : Support optimisé pour **Amazon Alexa**
- [x] **Blueprints** : Ajout du premier modèle d'annonce Alexa
- [x] **Raffinements Assist** : Phrases personnalisées ("Qui a Lucas ?")

### v1.8 (Publié ✅)
- [x] **Support Bilingue** : Traductions intégrales Français / Anglais (Entities, Config Flow, Assist)
- [x] **Internationalisation** : Support des calendriers scolaires et jours fériés pour Belgique, Suisse, Luxembourg et Québec
- [x] **Détection de langue** : Adaptation automatique selon la configuration HA pour Assist
- [x] **Stabilité & Maintenance** : Améliorations CI/CD, corrections de bugs (Intents, Imports) et mise à jour du logo

### v1.9 (En cours 🚧)
- [ ] **Mode "Échange Rapide"** : Bouton de confirmation d'échange avec notification au co-parent et log historique
- [ ] **Dashboard "One-tap Override"** : Gérer les imprévus (retards, dodo supplémentaire) en un clic

### v2.0 (Vision Future 🌟)
- [ ] **Mode Co-parent** : Synchronisation entre deux instances Home Assistant
- [ ] **Gestion financière** : Suivi des frais partagés et pensions
- [ ] **Journal d'échange** : Notes et photos partagées lors des transitions

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Fork** le projet
2. **Créer** une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

### Développement

Pour développer localement :

```bash
# Cloner le dépôt
git clone https://github.com/Jackngl/custody.git
cd custody

# Installer dans Home Assistant
cp -r custom_components/custody_schedule /config/custom_components/
```

### Workflow CI/CD

Le projet utilise plusieurs workflows automatisés pour assurer la qualité et la maintenance :

#### Tests et validation automatiques

À chaque push ou pull request, les workflows suivants sont exécutés :

- **Lint & Code Quality** : Vérification du formatage (Black), tri des imports (Isort), linting (Flake8), validation YAML
- **Security Scan** : Analyse de sécurité avec Bandit
- **Unit Tests** : Tests unitaires avec Pytest et génération de rapports de couverture
- **Hassfest Validation** : Validation de la conformité avec les standards Home Assistant
- **HACS Validation** : Vérification de la compatibilité HACS
- **Core Compatibility Check** : Vérification de la compatibilité avec Home Assistant Core

#### Workflow de versioning

Le projet utilise un workflow automatisé pour la création des tags et des releases :

- **Auto-incrémentation** : Toute fusion (merge) sur `main` incrémente automatiquement la version (patch)
- **Création de tags** : Un tag Git est créé automatiquement pour chaque nouvelle version
- **GitHub Releases** : Une release GitHub est générée automatiquement avec les notes de version
- **Mise à jour du badge** : Le badge de version dans le README est mis à jour automatiquement

**Important** : Si vous effectuez un changement de version manuel ou une correction documentaire qui ne nécessite pas de nouvelle release, ajoutez **`[skip version]`** dans votre message de commit pour désactiver l'auto-incrémentation.

#### Promotion vers le dépôt officiel

Lorsqu'une release est publiée, un workflow automatique promeut les changements vers le dépôt officiel (`Jackngl/custody`) avec validation de fast-forward pour garantir la sécurité.

### Tests

Les tests peuvent être effectués via le service de test de l'API :

```yaml
service: custody_schedule.test_holiday_api
data:
  zone: "A"
```

Pour exécuter les tests localement :

```bash
# Installer les dépendances de test
pip install -r requirements_test.txt

# Exécuter les tests
pytest tests --cov=custom_components/custody_schedule --cov-report=term-missing
```

---

## 📝 Licence

MIT © Custody Schedule

---

## 🙏 Remerciements

Merci à :
- La communauté Home Assistant pour son support
- Le ministère de l'Éducation nationale pour l'API des vacances scolaires
- Tous les parents en garde alternée qui utilisent cette intégration

---

## 📚 Documentation supplémentaire

Pour des guides de configuration détaillés, consultez :

### Français
- **[Guide de Configuration - Garde Classique](README_CONFIG_GARDE.fr.md)** - Configurer les weekends et semaines alternées
- **[Guide de Configuration - Vacances Scolaires](README_CONFIG_VACANCES.fr.md)** - Configurer les règles de vacances scolaires
- **[Guide des Entités](README_ENTITES.fr.md)** - Référence complète de toutes les entités et leur utilisation
- **[Guide Dashboard - Calendrier de garde](README_DASHBOARD_GARDE.fr.md)** - Dashboard dédié prêt à l'emploi (mono et multi-enfants)

### English
- **[Regular Custody Configuration Guide](README_CONFIG_GARDE.md)** - Configure weekends and alternate weeks
- **[School Holidays Configuration Guide](README_CONFIG_VACANCES.md)** - Configure school holiday rules
- **[Entities Guide](README_ENTITES.md)** - Complete reference of all entities and their usage
- **[Dashboard Guide - Custody Schedule](README_DASHBOARD_GARDE.md)** - Ready-to-use dedicated dashboard (single and multi-child)

---

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/Jackngl/custody/issues)
- **Documentation** : Ce README
- **Logs** : Vérifiez les logs Home Assistant pour diagnostiquer les problèmes

---

<div align="center">

**Fait avec ❤️ pour les familles en garde alternée**

</div>
