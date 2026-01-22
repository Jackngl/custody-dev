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

#### 2. **Année de référence pour les vacances** (`reference_year_vacations`)
- **Description** : Indique pour quelles **années (paires ou impaires)** vous avez des vacances scolaires
- **Valeurs** : `"even"` (paire), `"odd"` (impaire)
- **Configuration** : Dans le masque de saisie "Vacances scolaires" (séparé du `reference_year_custody` de la garde classique)
- **Fonctionnement** : La **parité de l'année en cours** détermine si vous avez des vacances cette année
  - `reference_year_vacations: "odd"` → vous avez des vacances **les années impaires**
  - `reference_year_vacations: "even"` → vous avez des vacances **les années paires**
- **Exemples** :
  - Année 2025 (impaire) + `reference_year_vacations: "odd"` → Vous avez les vacances
  - Année 2026 (paire) + `reference_year_vacations: "even"` → Vous avez les vacances
- **Note** : 
  - Cette logique s'applique à **toutes les vacances** (Noël, Hiver, Printemps, Toussaint)
  - Pour l'été, utilisez `july_rule` et `august_rule` pour choisir indépendamment juillet ou août selon les années
  - Le `reference_year_vacations` des vacances est **indépendant** du `reference_year_custody` de la garde classique

#### 3. **Répartition des moitiés** (`vacation_split_mode`)
- **Description** : Définit **quelle moitié** des vacances vous avez selon la parité de l'année
- **Valeurs** :
  - `"odd_first"` : **années impaires = 1ère moitié**, années paires = 2ème moitié (par défaut)
  - `"odd_second"` : **années impaires = 2ème moitié**, années paires = 1ère moitié
- **Exemples** :
  - Année 2025 (impaire) + `odd_first` → 1ère moitié
  - Année 2026 (paire) + `odd_first` → 2ème moitié
  - Année 2025 (impaire) + `odd_second` → 2ème moitié (inverse)
  - Année 2026 (paire) + `odd_second` → 1ère moitié (inverse)

#### 4. **Niveau scolaire** (`school_level`)
- **Description** : Niveau scolaire de l'enfant (affecte les horaires de sortie)
- **Valeurs** : `"primary"` (primaire), `"middle"` (collège), `"high"` (lycée)
- **Impact** :
  - **Primaire** : Début des vacances = vendredi 16:15 (sortie d'école)
  - **Collège/Lycée** : Début des vacances = samedi matin (selon API)

### Champs optionnels

#### 5. **Règle d'été** (`summer_rule`)
- **Description** : Règle spéciale pour les vacances d'été (juillet-août)
- **Valeurs** : Voir [Règles spéciales pour l'été](#règles-spéciales-pour-lété)
- **Exemple** : `"summer_half_parity"` pour partage par moitié selon parité d'année

---

## 🎯 Règles de vacances disponibles

### Système simplifié basé sur `reference_year_vacations` + `vacation_split_mode`

L'application utilise un **système automatique** basé sur :
- `reference_year_vacations` → **quelles années** (paires/impaires) vous avez des vacances
- `vacation_split_mode` → **quelle moitié** des vacances s'applique cette année

- **`reference_year_vacations: "odd"` (impaire)** → vous avez les vacances **les années impaires**

- **`reference_year_vacations: "even"` (paire)** → vous avez les vacances **les années paires**

### Exemples

**Configuration Parent A** : `reference_year_vacations: "odd"`, `vacation_split_mode: "odd_first"`
- **2025 (impaire)** : ✅ Parent A a la **1ère moitié**
- **2026 (paire)** : ❌ Pas de garde (année paire, parent B)

**Configuration Parent B** : `reference_year_vacations: "even"`, `vacation_split_mode: "odd_first"`
- **2024 (paire)** : ✅ Parent B a la **2ème moitié**
- **2025 (impaire)** : ❌ Pas de garde (année impaire, parent A)

> **Note** : Les deux parents ont des configurations complémentaires. Le `vacation_split_mode` permet l'inverse (années impaires = 2ème moitié).

### Règles spéciales pour l'été

#### Règles pour juillet et août (mois complets)

| Règle | Code | Description |
|-------|------|-------------|
| **Juillet (années paires)** | `july_even` | Juillet complet en années paires uniquement |
| **Juillet (années impaires)** | `july_odd` | Juillet complet en années impaires uniquement |
| **Août (années paires)** | `august_even` | Août complet en années paires uniquement |
| **Août (années impaires)** | `august_odd` | Août complet en années impaires uniquement |

> **Note** : 
> - Ces règles sont configurées via les champs `july_rule` et `august_rule` dans le masque "Vacances scolaires"
> - Chaque parent peut choisir indépendamment juillet ou août, et pour quelles années (paires ou impaires)
> - Cela permet une flexibilité totale : un parent peut avoir juillet en années impaires et août en années paires, ou l'inverse

#### Règles pour les quinzaines (moitiés de mois)

| Règle | Code | Description |
|-------|------|-------------|
| **Juillet - 1ère moitié** | `july_first_half` | 1er au 15 juillet<br>- `reference_year_vacations: "even"` : années impaires seulement<br>- `reference_year_vacations: "odd"` : années paires seulement |
| **Juillet - 2ème moitié** | `july_second_half` | 16 au 31 juillet<br>- `reference_year_vacations: "even"` : années paires seulement<br>- `reference_year_vacations: "odd"` : années impaires seulement |
| **Août - 1ère moitié** | `august_first_half` | 1er au 15 août<br>- `reference_year_vacations: "even"` : années impaires seulement<br>- `reference_year_vacations: "odd"` : années paires seulement |
| **Août - 2ème moitié** | `august_second_half` | 16 au 31 août<br>- `reference_year_vacations: "even"` : années paires seulement<br>- `reference_year_vacations: "odd"` : années impaires seulement |

> **Note** : 
> - Les règles de quinzaines sont utilisées via le champ `summer_rule` et s'appliquent uniquement aux vacances d'été
> - Elles utilisent `reference_year_vacations` pour déterminer automatiquement si elles s'appliquent selon la parité de l'année

---

## 📅 Règles de vacances détaillées

### Système automatique basé sur `reference_year_vacations` + `vacation_split_mode`

L'application détermine automatiquement :
- **quelles années** vous avez des vacances (via `reference_year_vacations`)
- **quelle moitié** vous avez cette année (via `vacation_split_mode`)

#### 1. Années concernées (`reference_year_vacations`)
- `reference_year_vacations: "odd"` → vous avez des vacances **les années impaires**
- `reference_year_vacations: "even"` → vous avez des vacances **les années paires**

#### 2. Répartition des moitiés (`vacation_split_mode`)
- `odd_first` : années impaires = **1ère moitié**, années paires = **2ème moitié**
- `odd_second` : années impaires = **2ème moitié**, années paires = **1ère moitié**

#### Exemple (mode par défaut)
```yaml
zone: "C"
reference_year_vacations: "odd"
vacation_split_mode: "odd_first"
school_level: "primary"
```

#### Exemple (inverse)
```yaml
zone: "C"
reference_year_vacations: "odd"
vacation_split_mode: "odd_second"
school_level: "primary"
```

> **Note** : Le calcul du **milieu exact** reste identique (milieu = (début + fin) / 2).

### Calcul du milieu exact

Pour les règles de partage par moitié, le milieu est calculé automatiquement :

- **Période effective** : Vendredi 16:15 → Dimanche 19:00 (fin officielle)
- **Milieu** = (début + fin) / 2 (avec heures et minutes précises)
- **Exemple** : 19/12/2025 16:15 → 05/01/2026 19:00 → Milieu = 27/12/2025 17:37:30

---

## ☀️ Règles spéciales pour l'été

Les règles d'été permettent de configurer spécifiquement les vacances d'été (juillet-août). Elles sont configurées dans le masque de saisie "Vacances scolaires".

### ✅ Choisir entre **mois complets** et **quinzaines**

Pour l'été, vous avez **deux approches distinctes** :

1) **Mois complets** (recommandé si vous partagez juillet/août)
- Utilisez **`july_rule`** et/ou **`august_rule`**
- Chaque règle donne **un mois complet** (juillet ou août) selon la parité
- Vous pouvez **activer l’un, l’autre, ou les deux**

2) **Quinzaines** (partage 1–15 / 16–31)
- Utilisez **`summer_rule`** (ex: `july_first_half`, `august_second_half`)
- La moitié est déterminée par **`vacation_split_mode`**

> ⚠️ **Priorité** : si `july_rule` ou `august_rule` est défini, la règle `summer_rule` n’est **pas** utilisée pour l’été.

### Juillet (années paires) (`july_even`)

**Fonctionnement** :
- Garde le mois de juillet complet en années paires uniquement
- Années impaires : pas de garde en juillet (l'autre parent peut avoir juillet ou août)

**Configuration** :
```yaml
zone: "C"
reference_year_vacations: "even"  # ou "odd", pour les autres vacances
july_rule: "july_even"  # Juillet en années paires
school_level: "primary"
```

**Résultat** :
- 2024 (paire) : ✅ Juillet 2024 complet
- 2025 (impaire) : ❌ Pas de garde en juillet
- 2026 (paire) : ✅ Juillet 2026 complet

---

### Juillet (années impaires) (`july_odd`)

**Fonctionnement** :
- Garde le mois de juillet complet en années impaires uniquement
- Années paires : pas de garde en juillet

**Configuration** :
```yaml
zone: "C"
reference_year_vacations: "even"  # ou "odd", pour les autres vacances
july_rule: "july_odd"  # Juillet en années impaires
school_level: "primary"
```

**Résultat** :
- 2024 (paire) : ❌ Pas de garde en juillet
- 2025 (impaire) : ✅ Juillet 2025 complet
- 2026 (paire) : ❌ Pas de garde en juillet

---

### Août (années paires) (`august_even`)

**Fonctionnement** :
- Garde le mois d'août complet en années paires uniquement
- Années impaires : pas de garde en août

**Configuration** :
```yaml
zone: "C"
reference_year_vacations: "even"  # ou "odd", pour les autres vacances
august_rule: "august_even"  # Août en années paires
school_level: "primary"
```

**Résultat** :
- 2024 (paire) : ✅ Août 2024 complet
- 2025 (impaire) : ❌ Pas de garde en août
- 2026 (paire) : ✅ Août 2026 complet

---

### Août (années impaires) (`august_odd`)

**Fonctionnement** :
- Garde le mois d'août complet en années impaires uniquement
- Années paires : pas de garde en août

**Configuration** :
```yaml
zone: "C"
reference_year_vacations: "even"  # ou "odd", pour les autres vacances
august_rule: "august_odd"  # Août en années impaires
school_level: "primary"
```

**Résultat** :
- 2024 (paire) : ❌ Pas de garde en août
- 2025 (impaire) : ✅ Août 2025 complet
- 2026 (paire) : ❌ Pas de garde en août

---

### Juillet - 1ère moitié (`july_first_half`)

**Fonctionnement** :
- Garde la **1ère quinzaine de juillet** (1er au 15 juillet)
- Utilise `reference_year_vacations` pour déterminer si la règle s'applique selon la parité de l'année
- **`reference_year_vacations: "even"`** : s'applique uniquement les années impaires
- **`reference_year_vacations: "odd"`** : s'applique uniquement les années paires

**Configuration** :
```yaml
zone: "C"
reference_year_vacations: "even"  # ou "odd", détermine quand la règle s'applique
summer_rule: "july_first_half"
school_level: "primary"
```

**Résultat avec `reference_year_vacations: "even"`** :
- 2024 (paire) : ❌ Ne s'applique pas
- 2025 (impaire) : ✅ 1-15 juillet 2025
- 2026 (paire) : ❌ Ne s'applique pas

**Résultat avec `reference_year_vacations: "odd"`** :
- 2024 (paire) : ✅ 1-15 juillet 2024
- 2025 (impaire) : ❌ Ne s'applique pas
- 2026 (paire) : ✅ 1-15 juillet 2026

---

### Juillet - 2ème moitié (`july_second_half`)

**Fonctionnement** :
- Garde la **2ème quinzaine de juillet** (16 au 31 juillet)
- Utilise `reference_year_vacations` pour déterminer si la règle s'applique selon la parité de l'année
- **`reference_year_vacations: "even"`** : s'applique uniquement les années paires
- **`reference_year_vacations: "odd"`** : s'applique uniquement les années impaires

**Configuration** :
```yaml
zone: "C"
reference_year_vacations: "even"  # ou "odd", détermine quand la règle s'applique
summer_rule: "july_second_half"
school_level: "primary"
```

**Résultat avec `reference_year_vacations: "even"`** :
- 2024 (paire) : ✅ 16-31 juillet 2024
- 2025 (impaire) : ❌ Ne s'applique pas
- 2026 (paire) : ✅ 16-31 juillet 2026

**Résultat avec `reference_year_vacations: "odd"`** :
- 2024 (paire) : ❌ Ne s'applique pas
- 2025 (impaire) : ✅ 16-31 juillet 2025
- 2026 (paire) : ❌ Ne s'applique pas

---

### Août - 1ère moitié (`august_first_half`)

**Fonctionnement** :
- Garde la **1ère quinzaine d'août** (1er au 15 août)
- Utilise `reference_year_vacations` pour déterminer si la règle s'applique selon la parité de l'année
- **`reference_year_vacations: "even"`** : s'applique uniquement les années impaires
- **`reference_year_vacations: "odd"`** : s'applique uniquement les années paires

**Configuration** :
```yaml
zone: "C"
reference_year_vacations: "even"  # ou "odd", détermine quand la règle s'applique
summer_rule: "august_first_half"
school_level: "primary"
```

**Résultat avec `reference_year_vacations: "even"`** :
- 2024 (paire) : ❌ Ne s'applique pas
- 2025 (impaire) : ✅ 1-15 août 2025
- 2026 (paire) : ❌ Ne s'applique pas

**Résultat avec `reference_year_vacations: "odd"`** :
- 2024 (paire) : ✅ 1-15 août 2024
- 2025 (impaire) : ❌ Ne s'applique pas
- 2026 (paire) : ✅ 1-15 août 2026

---

### Août - 2ème moitié (`august_second_half`)

**Fonctionnement** :
- Garde la **2ème quinzaine d'août** (16 au 31 août)
- Utilise `reference_year_vacations` pour déterminer si la règle s'applique selon la parité de l'année
- **`reference_year_vacations: "even"`** : s'applique uniquement les années paires
- **`reference_year_vacations: "odd"`** : s'applique uniquement les années impaires

**Configuration** :
```yaml
zone: "C"
reference_year_vacations: "even"  # ou "odd", détermine quand la règle s'applique
summer_rule: "august_second_half"
school_level: "primary"
```

**Résultat avec `reference_year_vacations: "even"`** :
- 2024 (paire) : ✅ 16-31 août 2024
- 2025 (impaire) : ❌ Ne s'applique pas
- 2026 (paire) : ✅ 16-31 août 2026

**Résultat avec `reference_year_vacations: "odd"`** :
- 2024 (paire) : ❌ Ne s'applique pas
- 2025 (impaire) : ✅ 16-31 août 2025
- 2026 (paire) : ❌ Ne s'applique pas

---

## 🕐 Calcul des dates et horaires

### Période effective des vacances

L'application ajuste automatiquement les dates de l'API pour correspondre aux horaires de garde :

#### Début effectif
- **Primaire** : Vendredi précédent à 16:15 (sortie d'école)
- **Collège/Lycée** : Samedi matin (selon API)

#### Fin effective
- **Toujours** : Dimanche 19:00 (même si l'API indique "reprise lundi")

### Calcul des dates

Les dates sont calculées automatiquement selon la règle sélectionnée, la parité de l'année (`reference_year_vacations`) et la répartition des moitiés (`vacation_split_mode`).

---

## 📝 Exemples de configuration

### Exemple 1 : Partage par moitié (toutes vacances)

**Situation** : Partage équitable de toutes les vacances (Noël, Hiver, Printemps, Toussaint, Été) par moitié selon la parité de l'année.

**Configuration Parent A** :
```yaml
zone: "C"
reference_year_vacations: "odd"  # 1ère partie (1ère moitié) en années impaires
vacation_split_mode: "odd_first"
school_level: "primary"
```

**Configuration Parent B** :
```yaml
zone: "C"
reference_year_vacations: "even"  # 2ème partie (2ème moitié) en années paires
vacation_split_mode: "odd_first"
school_level: "primary"
```

**Résultat Parent A** (toutes vacances) :
- **2025 (impaire)** : ✅ 1ère moitié de toutes les vacances
  - Noël 2025 : 19/12/2025 16:15 → 27/12/2025 17:37:30
  - Hiver 2025 : 1ère moitié
  - Printemps 2025 : 1ère moitié
  - Toussaint 2025 : 1ère moitié
- **2026 (paire)** : ❌ Pas de garde (car c'est la 2ème partie, le parent B a la garde)

**Résultat Parent B** (toutes vacances) :
- **2025 (impaire)** : ❌ Pas de garde (car c'est la 1ère partie, le parent A a la garde)
- **2026 (paire)** : ✅ 2ème moitié de toutes les vacances
  - Noël 2026 : 27/12/2026 17:37:30 → 03/01/2027 19:00
  - Hiver 2026 : 2ème moitié
  - Printemps 2026 : 2ème moitié
  - Toussaint 2026 : 2ème moitié

> **Note** : Cette logique s'applique à **toutes les vacances scolaires** (Noël, Hiver, Printemps, Toussaint, Été). Le champ `reference_year_vacations` détermine **les années concernées**, et `vacation_split_mode` détermine **la moitié**.

**Variante inverse** (années impaires = 2ème moitié) :
```yaml
zone: "C"
reference_year_vacations: "odd"
vacation_split_mode: "odd_second"
school_level: "primary"
```

---

### Exemple 2 : Partage juillet/août avec règles séparées

**Situation** : Utilisation de `july_rule` et `august_rule` pour partager équitablement juillet et août.

**Configuration Parent A** :
```yaml
zone: "C"
reference_year_vacations: "even"  # Pour les autres vacances (Noël, Hiver, Printemps, Toussaint)
july_rule: "july_odd"  # Juillet en années impaires
august_rule: "august_even"  # Août en années paires
school_level: "primary"
```

**Configuration Parent B** :
```yaml
zone: "C"
reference_year_vacations: "odd"  # Pour les autres vacances (Noël, Hiver, Printemps, Toussaint)
july_rule: "july_even"  # Juillet en années paires
august_rule: "august_odd"  # Août en années impaires
school_level: "primary"
```

**Résultat Parent A** :
- 2024 (paire) : ✅ Août 2024 complet
- 2025 (impaire) : ✅ Juillet 2025 complet
- 2026 (paire) : ✅ Août 2026 complet
- 2027 (impaire) : ✅ Juillet 2027 complet

**Résultat Parent B** :
- 2024 (paire) : ✅ Juillet 2024 complet (complémentaire du parent A)
- 2025 (impaire) : ✅ Août 2025 complet (complémentaire du parent A)
- 2026 (paire) : ✅ Juillet 2026 complet (complémentaire du parent A)
- 2027 (impaire) : ✅ Août 2027 complet (complémentaire du parent A)

> **Note** : Chaque parent configure indépendamment `july_rule` et `august_rule`. Cela permet une flexibilité totale : un parent peut avoir juillet en années impaires et août en années paires, ou toute autre combinaison. Les deux parents obtiennent des mois différents chaque année, garantissant une alternance équitable.

---

### Exemple 3 : Quinzaine de juillet avec `reference_year_vacations`

**Situation** : Partage de la 1ère quinzaine de juillet selon la parité de l'année.

**Configuration Parent A** :
```yaml
zone: "C"
reference_year_vacations: "even"  # Détermine quand la règle s'applique
summer_rule: "july_first_half"  # 1ère moitié de juillet
school_level: "primary"
```

**Configuration Parent B** :
```yaml
zone: "C"
reference_year_vacations: "odd"  # Détermine quand la règle s'applique
summer_rule: "july_first_half"  # 1ère moitié de juillet
school_level: "primary"
```

**Résultat Parent A** (`reference_year_vacations: "even"`) :
- 2024 (paire) : ❌ Ne s'applique pas
- 2025 (impaire) : ✅ 1-15 juillet 2025
- 2026 (paire) : ❌ Ne s'applique pas

**Résultat Parent B** (`reference_year_vacations: "odd"`) :
- 2024 (paire) : ✅ 1-15 juillet 2024 (complémentaire du parent A)
- 2025 (impaire) : ❌ Ne s'applique pas (le parent A a la garde)
- 2026 (paire) : ✅ 1-15 juillet 2026 (complémentaire du parent A)

> **Note** : Les deux parents utilisent la même règle `july_first_half`, mais avec des `reference_year_vacations` différents. En 2025 (année impaire), seul le parent A a la garde. En 2024 et 2026 (années paires), seul le parent B a la garde.

---

### Exemple 4 : Quinzaine d'août avec `reference_year_vacations`

**Situation** : Partage de la 2ème quinzaine d'août selon la parité de l'année.

**Configuration Parent A** :
```yaml
zone: "C"
reference_year_vacations: "even"  # Détermine quand la règle s'applique
summer_rule: "august_second_half"  # 2ème moitié d'août
school_level: "primary"
```

**Configuration Parent B** :
```yaml
zone: "C"
reference_year_vacations: "odd"  # Détermine quand la règle s'applique
summer_rule: "august_second_half"  # 2ème moitié d'août
school_level: "primary"
```

**Résultat Parent A** (`reference_year_vacations: "even"`) :
- 2024 (paire) : ✅ 16-31 août 2024
- 2025 (impaire) : ❌ Ne s'applique pas
- 2026 (paire) : ✅ 16-31 août 2026

**Résultat Parent B** (`reference_year_vacations: "odd"`) :
- 2024 (paire) : ❌ Ne s'applique pas (le parent A a la garde)
- 2025 (impaire) : ✅ 16-31 août 2025 (complémentaire du parent A)
- 2026 (paire) : ❌ Ne s'applique pas (le parent A a la garde)

> **Note** : Les deux parents utilisent la même règle `august_second_half`, mais avec des `reference_year_vacations` différents. En 2024 et 2026 (années paires), seul le parent A a la garde. En 2025 (année impaire), seul le parent B a la garde.

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

### Les règles ne s'appliquent pas correctement

1. **reference_year_vacations** : Vérifiez que vous avez sélectionné les années concernées (paire / impaire)
2. **vacation_split_mode** : Vérifiez si vous avez choisi la 1ère ou 2ème moitié pour les années impaires
3. **july_rule / august_rule / summer_rule** : Vérifiez les règles d’été
4. **Logs** : Consultez les logs pour voir les dates calculées

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

