# 📖 Guide de Configuration - Vacances Scolaires

Ce guide explique comment configurer les **vacances scolaires** dans l'application Planning de garde.

> ⚠️ **Important** : 
> - Ce guide concerne **uniquement les vacances scolaires**
> - Les **vacances scolaires ont priorité absolue** sur la garde classique (weekends/semaines)
> - Les **jours fériés** ne s'appliquent pas pendant les vacances scolaires
> - Pour la garde classique, voir `README_CONFIG_GARDE.md`

---

## 📋 Table des matières

1. [Séparation garde classique / vacances scolaires](#séparation-garde-classique--vacances-scolaires)
2. [API des vacances scolaires](#api-des-vacances-scolaires)
3. [Zones scolaires](#zones-scolaires)
4. [Règles de vacances disponibles](#règles-de-vacances-disponibles)
5. [Configuration de base](#configuration-de-base)
6. [Règles de vacances détaillées](#règles-de-vacances-détaillées)
7. [Règles spéciales pour l'été](#règles-spéciales-pour-lété)
8. [Calcul des dates et horaires](#calcul-des-dates-et-horaires)
9. [Exemples de configuration](#exemples-de-configuration)

---

## 🔀 Séparation garde classique / vacances scolaires

L'application sépare clairement **deux systèmes de garde indépendants** :

### 1. **Garde classique** (voir `README_CONFIG_GARDE.md`)
- **Configuration** : Masque de saisie "Garde classique (weekends/semaines)"
- **Période** : Hors vacances scolaires uniquement
- **Fonctionnalités** :
  - Weekends alternés, semaines alternées, rythmes 2-2-3, etc.
  - Extension automatique avec jours fériés (vendredi/lundi)
  - Basé sur cycles ou parité ISO des semaines

### 2. **Vacances scolaires** (ce guide)
- **Configuration** : Masque de saisie "Vacances scolaires"
- **Période** : Pendant les vacances scolaires uniquement
- **Fonctionnalités** :
  - Récupération automatique des dates depuis l'API Éducation Nationale
  - Règles par moitié, par semaine, par parité d'année
  - Calcul automatique du milieu exact des vacances
  - Priorité absolue sur la garde classique

### ⚠️ Règle de priorité

```
Vacances scolaires > Jours fériés > Garde classique
```

- **Pendant les vacances** : Seules les règles de vacances s'appliquent
- **Hors vacances** : La garde classique s'applique, avec extension fériée si applicable
- **Jours fériés pendant vacances** : Ignorés (les vacances priment déjà)

---

## 🌐 API des vacances scolaires

L'application utilise l'**API officielle du Ministère de l'Éducation Nationale** pour récupérer automatiquement les dates des vacances scolaires.

### Source de données

- **API** : `https://data.education.gouv.fr/api/records/1.0/search/`
- **Dataset** : `fr-en-calendrier-scolaire`
- **Format** : JSON
- **Mise à jour** : Automatique (cache de 15 minutes)

### Fonctionnement

1. **Récupération automatique** : L'application interroge l'API pour votre zone scolaire
2. **Cache** : Les données sont mises en cache pour éviter les appels répétés
3. **Années scolaires** : L'API utilise le format "2024-2025" (septembre à juin)
4. **Filtrage** : Seules les vacances futures ou en cours sont affichées

### Zones supportées

| Zone | Code | Villes principales |
|------|------|-------------------|
| **Zone A** | `A` | Besançon, Bordeaux, Clermont-Ferrand, Dijon, Grenoble, Limoges, Lyon, Poitiers |
| **Zone B** | `B` | Aix-Marseille, Amiens, Lille, Nancy-Metz, Nantes, Nice, Normandie, Orléans-Tours, Reims, Rennes, Strasbourg |
| **Zone C** | `C` | Créteil, Montpellier, Paris, Toulouse, Versailles |
| **Corse** | `Corse` | Corse |
| **DOM-TOM** | `DOM-TOM` | Guadeloupe, Martinique, Guyane, La Réunion, Mayotte |

### Types de vacances récupérés

L'API fournit les périodes suivantes :
- **Vacances de la Toussaint** (octobre)
- **Vacances de Noël** (décembre-janvier)
- **Vacances d'Hiver** (février-mars)
- **Vacances de Printemps** (avril-mai)
- **Vacances d'Été** (juillet-août)
- **Pont de l'Ascension** (mai)

### Corrections manuelles

Certaines dates peuvent être corrigées manuellement dans le code si l'API est incomplète ou incorrecte (ex: Zone C hiver 2025-2026).

---

## ⚙️ Configuration de base

### Champs obligatoires

#### 1. **Zone scolaire** (`zone`)
- **Description** : Zone géographique pour les vacances scolaires
- **Valeurs** : `"A"`, `"B"`, `"C"`, `"Corse"`, `"DOM-TOM"`
- **Exemple** : `"C"` pour la zone C (Paris, Créteil, etc.)

#### 2. **Règle de vacances** (`vacation_rule`)
- **Description** : Règle de partage pendant les vacances scolaires
- **Valeurs** : Voir [Règles de vacances disponibles](#règles-de-vacances-disponibles)
- **Exemple** : `"first_half"` pour la première moitié, `"july"` pour juillet complet

#### 2bis. **Année de référence** (`reference_year`)
- **Description** : Détermine la parité (paire/impaire) pour les règles `july` et `august`
- **Valeurs** : `"even"` (paire), `"odd"` (impaire)
- **Utilisation** :
  - `reference_year: "even"` + `july` → Juillet complet en **années paires** (2024, 2026, ...)
  - `reference_year: "odd"` + `july` → Juillet complet en **années impaires** (2025, 2027, ...)
  - Même logique pour `august`

#### 3. **Niveau scolaire** (`school_level`)
- **Description** : Niveau scolaire de l'enfant (affecte les horaires de sortie)
- **Valeurs** : `"primary"` (primaire), `"middle"` (collège), `"high"` (lycée)
- **Impact** :
  - **Primaire** : Début des vacances = vendredi 16:15 (sortie d'école)
  - **Collège/Lycée** : Début des vacances = samedi matin (selon API)

### Champs optionnels

#### 4. **Règle d'été** (`summer_rule`)
- **Description** : Règle spéciale pour les vacances d'été (juillet-août)
- **Valeurs** : Voir [Règles spéciales pour l'été](#règles-spéciales-pour-lété)
- **Exemple** : `"summer_half_parity"` pour partage par moitié selon parité d'année

---

## 🎯 Règles de vacances disponibles

### Règles générales

| Règle | Code | Description | Utilisation |
|-------|------|-------------|-------------|
| **1ère semaine** | `first_week` | Garde la première semaine complète | Vacances courtes |
| **2ème semaine** | `second_week` | Garde la deuxième semaine complète | Vacances courtes |
| **1ère moitié** | `first_half` | Garde la première moitié (milieu calculé) | Partage équitable |
| **2ème moitié** | `second_half` | Garde la deuxième moitié (milieu calculé) | Partage équitable |
| **Semaines paires** | `even_weeks` | Garde les semaines ISO paires | Partage alterné |
| **Semaines impaires** | `odd_weeks` | Garde les semaines ISO impaires | Partage alterné |
| **Weekends semaines paires** | `even_weekends` | Garde les weekends des semaines paires | Weekends uniquement |
| **Weekends semaines impaires** | `odd_weekends` | Garde les weekends des semaines impaires | Weekends uniquement |
| **Juillet complet** | `july` | Garde tout le mois de juillet (selon `reference_year`) | Été |
| **Août complet** | `august` | Garde tout le mois d'août (selon `reference_year`) | Été |
| **Personnalisé** | `custom` | Règles personnalisées définies manuellement | Cas spécifiques |

> **Note** : Les règles `july` et `august` utilisent le champ `reference_year` pour déterminer la parité :
> - `reference_year: "even"` → Juillet/Août en **années paires** (2024, 2026, ...)
> - `reference_year: "odd"` → Juillet/Août en **années impaires** (2025, 2027, ...)

### Règles spéciales pour l'été (quinzaines)

| Règle | Code | Description |
|-------|------|-------------|
| **Juillet - 1ère moitié** | `july_first_half` | 1er au 15 juillet |
| **Juillet - 2ème moitié** | `july_second_half` | 16 au 31 juillet |
| **Août - 1ère moitié** | `august_first_half` | 1er au 15 août |
| **Août - 2ème moitié** | `august_second_half` | 16 au 31 août |

> **Note** : Ces règles sont utilisées via le champ `summer_rule` et s'appliquent uniquement aux vacances d'été.

---

## 📅 Règles de vacances détaillées

### 1. Première semaine (`first_week`)

**Fonctionnement** :
- Garde la **première semaine complète** des vacances
- Début : Vendredi 16:15 (sortie d'école) ou samedi selon niveau
- Fin : Dimanche 19:00 de la première semaine

**Configuration** :
```yaml
vacation_rule: "first_week"
school_level: "primary"
```

**Exemple** (Vacances de Noël 2025, Zone C) :
- Début officiel : 20/12/2025 (samedi)
- Début effectif : 19/12/2025 16:15 (vendredi sortie école)
- Fin : 28/12/2025 19:00 (dimanche fin 1ère semaine)

---

### 2. Deuxième semaine (`second_week`)

**Fonctionnement** :
- Garde la **deuxième semaine complète** des vacances
- Début : Lundi de la 2ème semaine à l'heure d'arrivée
- Fin : Dimanche 19:00 de la deuxième semaine

**Configuration** :
```yaml
vacation_rule: "second_week"
school_level: "primary"
```

---

### 3. Première moitié (`first_half`)

**Fonctionnement** :
- Garde la **première moitié** des vacances
- **Milieu calculé automatiquement** : Date/heure exacte au milieu de la période effective
- Début : Vendredi 16:15 (sortie d'école)
- Fin : Milieu exact calculé (ex: 27/12/2025 17:37:30)

**Calcul du milieu** :
- Période effective : Vendredi 16:15 → Dimanche 19:00 (fin officielle)
- Milieu = (début + fin) / 2 (avec heures et minutes)

**Configuration** :
```yaml
vacation_rule: "first_half"
school_level: "primary"
```

**Exemple** (Vacances de Noël 2025, Zone C) :
- Début : 19/12/2025 16:15
- Fin officielle : 05/01/2026 00:00 → ajustée à 04/01/2026 19:00
- Milieu calculé : 27/12/2025 17:37:30
- **Fin de garde** : 27/12/2025 17:37:30

---

### 4. Deuxième moitié (`second_half`)

**Fonctionnement** :
- Garde la **deuxième moitié** des vacances
- **Milieu calculé automatiquement** : Date/heure exacte au milieu de la période effective
- Début : Milieu exact calculé (ex: 27/12/2025 17:37:30)
- Fin : Dimanche 19:00 (fin officielle)

**Configuration** :
```yaml
vacation_rule: "second_half"
school_level: "primary"
```

---

### 5. Juillet complet (`july`)

**Fonctionnement** :
- Garde **tout le mois de juillet** selon la parité de l'année
- La parité est déterminée par le champ `reference_year` :
  - `reference_year: "even"` → Juillet en **années paires** (2024, 2026, ...)
  - `reference_year: "odd"` → Juillet en **années impaires** (2025, 2027, ...)

**Configuration** :
```yaml
vacation_rule: "july"
reference_year: "odd"  # "even" = années paires, "odd" = années impaires
school_level: "primary"
```

**Exemple** (`reference_year: "odd"` = années impaires) :
- 2025 (impaire) : ✅ Juillet 2025 complet
- 2026 (paire) : ❌ Pas de garde en juillet
- 2027 (impaire) : ✅ Juillet 2027 complet

---

### 6. Août complet (`august`)

**Fonctionnement** :
- Garde **tout le mois d'août** selon la parité de l'année
- La parité est déterminée par le champ `reference_year` :
  - `reference_year: "even"` → Août en **années paires** (2024, 2026, ...)
  - `reference_year: "odd"` → Août en **années impaires** (2025, 2027, ...)

**Configuration** :
```yaml
vacation_rule: "august"
reference_year: "even"  # "even" = années paires, "odd" = années impaires
school_level: "primary"
```

**Exemple** (`reference_year: "even"` = années paires) :
- 2024 (paire) : ✅ Août 2024 complet
- 2025 (impaire) : ❌ Pas de garde en août
- 2026 (paire) : ✅ Août 2026 complet

---

## ☀️ Règles spéciales pour l'été (quinzaines)

Les règles de quinzaine permettent de partager juillet ou août en deux périodes de 15 jours. Elles sont utilisées via le champ `summer_rule`.

### Juillet - 1ère moitié (`july_first_half`)

**Fonctionnement** :
- Garde la **1ère quinzaine de juillet** (1er au 15 juillet)

**Configuration** :
```yaml
vacation_rule: "first_half"  # ou autre règle générale
summer_rule: "july_first_half"
school_level: "primary"
```

---

### Juillet - 2ème moitié (`july_second_half`)

**Fonctionnement** :
- Garde la **2ème quinzaine de juillet** (16 au 31 juillet)

**Configuration** :
```yaml
vacation_rule: "second_half"  # ou autre règle générale
summer_rule: "july_second_half"
school_level: "primary"
```

---

### Août - 1ère moitié (`august_first_half`)

**Fonctionnement** :
- Garde la **1ère quinzaine d'août** (1er au 15 août)

**Configuration** :
```yaml
vacation_rule: "first_half"  # ou autre règle générale
summer_rule: "august_first_half"
school_level: "primary"
```

---

### Août - 2ème moitié (`august_second_half`)

**Fonctionnement** :
- Garde la **2ème quinzaine d'août** (16 au 31 août)

**Configuration** :
```yaml
vacation_rule: "second_half"  # ou autre règle générale
summer_rule: "august_second_half"
school_level: "primary"
```

---

## 🕐 Calcul des dates et horaires

### Période effective des vacances

L'application ajuste automatiquement les dates de l'API pour correspondre aux horaires de garde :

#### Début effectif
- **Primaire** : Vendredi précédent à 16:15 (sortie d'école)
- **Collège/Lycée** : Samedi matin (selon API)

#### Fin effective
- **Toujours** : Dimanche 19:00 (même si l'API indique "reprise lundi")

### Calcul du milieu exact

Pour les règles `first_half`, `second_half`, `first_week_*_year`, `second_week_*_year` :

1. **Période effective** : Vendredi 16:15 → Dimanche 19:00 (fin officielle)
2. **Milieu** = (début + fin) / 2
3. **Précision** : Jour, heure, minute (ex: 27/12/2025 17:37:30)

**Exemple de calcul** :
```
Début : 19/12/2025 16:15:00
Fin   : 04/01/2026 19:00:00
Durée : 16 jours, 2 heures, 45 minutes
Milieu : 27/12/2025 17:37:30
```

---

## 📝 Exemples de configuration

### Exemple 1 : Partage par moitié

**Situation** : Vous avez la 1ère moitié, l'autre parent a la 2ème moitié.

**Configuration** :
```yaml
zone: "C"
vacation_rule: "first_half"
school_level: "primary"
```

**Résultat** (Vacances de Noël 2025) :
- Début : 19/12/2025 16:15
- Fin : 27/12/2025 17:37:30 (milieu calculé)

---

### Exemple 2 : Juillet complet selon année paire/impaire

**Situation** : Vous avez juillet complet en années impaires (2025, 2027, ...).

**Configuration** :
```yaml
zone: "C"
vacation_rule: "july"
reference_year: "odd"  # "odd" = années impaires
school_level: "primary"
```

**Résultat** :
- 2025 (impaire) : ✅ Juillet 2025 complet
- 2026 (paire) : ❌ Pas de garde en juillet
- 2027 (impaire) : ✅ Juillet 2027 complet

---

### Exemple 3 : Août complet selon année paire/impaire

**Situation** : Vous avez août complet en années paires (2024, 2026, ...).

**Configuration** :
```yaml
zone: "C"
vacation_rule: "august"
reference_year: "even"  # "even" = années paires
school_level: "primary"
```

**Résultat** :
- 2024 (paire) : ✅ Août 2024 complet
- 2025 (impaire) : ❌ Pas de garde en août
- 2026 (paire) : ✅ Août 2026 complet

---

### Exemple 4 : Quinzaine de juillet

**Situation** : Vous avez la 1ère quinzaine de juillet (1-15 juillet).

**Configuration** :
```yaml
zone: "C"
vacation_rule: "first_half"  # Règle générale
summer_rule: "july_first_half"  # 1ère moitié de juillet
school_level: "primary"
```

**Résultat** (Juillet 2025) :
- 1-15 juillet 2025 : ✅ Garde
- 16-31 juillet 2025 : ❌ Pas de garde

---

### Exemple 5 : Première semaine fixe

**Situation** : Vous avez toujours la première semaine, quelle que soit l'année.

**Configuration** :
```yaml
zone: "C"
vacation_rule: "first_week"
school_level: "primary"
```

**Résultat** (Toutes les vacances) :
- Semaine 1 : ✅ Garde
- Semaine 2 : ❌ Pas de garde

---

## 🔧 Dépannage

### L'API ne retourne pas de données

1. **Vérifier la zone** : Assurez-vous que la zone est correcte (A, B, C, Corse, DOM-TOM)
2. **Vérifier l'année scolaire** : L'API utilise le format "2024-2025"
3. **Tester la connexion** : Utilisez le service `test_holiday_api` dans Home Assistant
4. **Vérifier les logs** : Consultez les logs pour voir les erreurs API

### Les dates ne correspondent pas

1. **Niveau scolaire** : Vérifiez que `school_level` est correct (primaire = vendredi 16:15)
2. **Zone** : Vérifiez que la zone correspond à votre académie
3. **Année** : Vérifiez que l'année de référence est correcte pour les règles basées sur la parité

### Le milieu n'est pas calculé correctement

1. **Règle** : Vérifiez que vous utilisez une règle qui calcule le milieu (`first_half`, `first_week_odd_year`, etc.)
2. **Période effective** : Le calcul se base sur Vendredi 16:15 → Dimanche 19:00
3. **Logs** : Consultez les logs pour voir les dates calculées

---

## 📚 Ressources

- **API Éducation Nationale** : https://data.education.gouv.fr/explore/dataset/fr-en-calendrier-scolaire
- **Documentation garde classique** : `README_CONFIG_GARDE.md`
- **Zones scolaires** : https://www.education.gouv.fr/les-zones-de-vacances-12073

---

## ✅ Récapitulatif

### Priorité des règles

```
Vacances scolaires > Jours fériés > Garde classique
```

### Points clés

- ✅ Les vacances sont récupérées automatiquement depuis l'API
- ✅ Les dates sont ajustées pour correspondre aux horaires de garde
- ✅ Le milieu est calculé automatiquement pour les règles de partage
- ✅ Les vacances remplacent complètement la garde classique pendant leur durée
- ✅ Les jours fériés ne s'appliquent pas pendant les vacances

