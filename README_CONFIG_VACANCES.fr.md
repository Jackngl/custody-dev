# 📖 Guide de Configuration - Vacances Scolaires

[🇫🇷 Version française](README_CONFIG_VACANCES.fr.md) | [🇬🇧 English version](README_CONFIG_VACANCES.md)

Ce guide explique comment configurer les **vacances scolaires** dans l'application Custody.

> ⚠️ **Important** : 
> - Ce guide concerne **uniquement les vacances scolaires**
> - Les **vacances scolaires ont priorité absolue** sur la garde classique (weekends/semaines)
> - Les **jours fériés** ne s'appliquent pas pendant les vacances scolaires
> - Pour la garde classique, voir [`README_CONFIG_GARDE.fr.md`](README_CONFIG_GARDE.fr.md) ([English](README_CONFIG_GARDE.md))

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

### 1. **Garde classique** (voir [`README_CONFIG_GARDE.fr.md`](README_CONFIG_GARDE.fr.md) - [English](README_CONFIG_GARDE.md))
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

## 🏠 Mode Garde Complète (Sans découpage)

Si vous avez **désactivé la gestion de la garde** (via l'option "Activer la gestion de la garde") :

- **Comportement** : L'intégration considère que vous avez la **garde complète** de l'enfant.
- **Vacances** : Toutes les vacances scolaires sont affichées **en entier** (pas de découpage).
- **Configuration** :
  - `reference_year_vacations` (parité) est **ignoré** (vous avez les vacances chaque année).
  - `vacation_split_mode` est **ignoré** (vous avez la totalité des vacances).
- **Statut** : L'enfant est considéré "Présent" pendant toute la durée de toutes les vacances.

> **Note** : Ce mode est idéal si vous êtes le gardien principal et ne partagez pas la garde, mais souhaitez suivre les dates des vacances scolaires.

---


### Pays supportés et APIs

L'application sélectionne automatiquement le fournisseur approprié selon le pays configuré :

| Pays | Source | Type de vacances | Support régional |
|------|--------|------------------|------------------|
| **France** | `data.education.gouv.fr` | Scolaires | Zones A, B, C, Corse, DOM-TOM |
| **Belgique** | `openholidaysapi.org` | Scolaires | Communautés (FR, NL, DE) |
| **Suisse** | `openholidaysapi.org` | Scolaires | Cantons (GE, VD, VS, etc.) |
| **Luxembourg** | `openholidaysapi.org` | Scolaires | National |
| **Québec (CA)** | `canada-holidays.ca` | Fériés | Québec Général (Officiels) |

> [!NOTE]
> Pour le Québec, l'intégration se concentre sur les **jours fériés officiels**, les vacances scolaires étant très variables selon les commissions scolaires locales.

### Fonctionnement (France)

1. **Récupération automatique** : L'application interroge l'API pour votre zone scolaire
2. **Cache** : Les données sont mises en cache pour éviter les appels répétés
3. **Années scolaires** : L'API utilise le format "2024-2025" (septembre à juin)
4. **Filtrage** : Seules les vacances futures ou en cours sont affichées

### Zones scolaires (France)

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

#### 1. **Pays** (`country`)
- **Description** : Pays cible pour les données de vacances
- **Valeurs** : `"FR"` (France), `"BE"` (Belgique), `"CH"` (Suisse), `"LU"` (Luxembourg), `"CA_QC"` (Québec)

#### 2. **Zone Scolaire / Subdivision** (`zone`)
- **Description** : Zone géographique ou subdivision pour les vacances
- **Valeurs** :
  - **France** : `"A"`, `"B"`, `"C"`, `"Corse"`, `"DOM-TOM"`
  - **Suisse** : Cantons (`"CH-GE"`, `"CH-VD"`, etc.)
  - **Belgique** : Communautés (`"FR"`, `"NL"`, `"DE"`)
  - **Québec** : `"QC"` (Général)

#### 2. **Répartition des moitiés** (`vacation_split_mode`)
- **Description** : Détermine quelle moitié des vacances vous avez selon la parité de l'année.
- **Valeurs** :
  - `"odd_first"` : **Années impaires** = 1ère moitié, **Années paires** = 2ème moitié (Défaut)
  - `"odd_second"` : **Années impaires** = 2ème moitié, **Années paires** = 1ère moitié
- **Fonctionnement** :
  - Vous choisissez simplement quelle moitié vous avez les **années impaires** (ex: 2025).
  - Le système attribue automatiquement l'autre moitié pour les années paires.
- **Exemples** :
  - `odd_first` en 2025 (impaire) → **1ère moitié**
  - `odd_first` en 2026 (paire) → **2ème moitié**


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
| **Juillet - 1ère moitié** | `july_first_half` | 1er au 15 juillet<br>S'applique lorsque votre mode vous donne la **1ère Moitié** de l'été. |
| **Juillet - 2ème moitié** | `july_second_half` | 16 au 31 juillet<br>S'applique lorsque votre mode vous donne la **2ème Moitié** de l'été. |
| **Août - 1ère moitié** | `august_first_half` | 1er au 15 août<br>S'applique lorsque votre mode vous donne la **1ère Moitié** de l'été. |
| **Août - 2ème moitié** | `august_second_half` | 16 au 31 août<br>S'applique lorsque votre mode vous donne la **2ème Moitié** de l'été. |

> **Note** : 
> - Les règles de quinzaines sont utilisées via le champ `summer_rule` et s'appliquent uniquement aux vacances d'été.
> - Elles suivent automatiquement votre `vacation_split_mode` (1ère ou 2ème moitié).

---

## 📅 Règles de vacances détaillées

### Système automatique basé sur `vacation_split_mode`

L'application détermine automatiquement quelle moitié des vacances vous avez selon la **parité de l'année** et votre **Mode de Référence** (`vacation_split_mode`).

#### 1. Mode de Référence (`vacation_split_mode`)
Ce réglage définit votre planning de base pour les **Années Impaires** :
- **`odd_first`** (Défaut) : Vous avez la **1ère Moitié** les années impaires (et automatiquement la 2ème Moitié les années paires).
- **`odd_second`** : Vous avez la **2ème Moitié** les années impaires (et automatiquement la 1ère Moitié les années paires).

#### 2. Logique de Parité
- **Années Impaires** (ex: 2025, 2027) :
  - `odd_first` → 1ère Moitié
  - `odd_second` → 2ème Moitié
- **Années Paires** (ex: 2024, 2026) :
  - `odd_first` → 2ème Moitié (Inversé)
  - `odd_second` → 1ère Moitié (Inversé)

#### Exemple
```yaml
zone: "C"
vacation_split_mode: "odd_first"  # Années impaires = 1ère moitié
school_level: "primary"
```
- 2025 (Impaire) : **1ère Moitié**
- 2026 (Paire) : **2ème Moitié**

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

Les dates sont calculées automatiquement selon la règle sélectionnée, la parité de l'année et la répartition des moitiés (`vacation_split_mode`).

---

## 📝 Exemples de configuration

### Exemple 1 : Partage par moitié (toutes vacances)

**Situation** : Partage équitable de toutes les vacances (Noël, Hiver, Printemps, Toussaint, Été) par moitié selon la parité de l'année.

**Configuration Parent A** :
```yaml
zone: "C"
vacation_split_mode: "odd_first"  # Années impaires = 1ère moitié
school_level: "primary"
```

**Configuration Parent B** :
```yaml
zone: "C"
vacation_split_mode: "odd_second" # Années impaires = 2ème moitié
school_level: "primary"
```

**Résultat Parent A** (toutes vacances) :
- **2025 (impaire)** : ✅ 1ère moitié de toutes les vacances
- **2026 (paire)** : ✅ 2ème moitié de toutes les vacances

**Résultat Parent B** (toutes vacances) :
- **2025 (impaire)** : ✅ 2ème moitié de toutes les vacances
- **2026 (paire)** : ✅ 1ère moitié de toutes les vacances

> **Note** : Cette logique s'applique à **toutes les vacances scolaires**. `vacation_split_mode` détermine la moitié pour les années impaires, et l'inverse automatiquement pour les années paires.

---

### Exemple 2 : Partage juillet/août avec règles séparées

**Situation** : Utilisation de `july_rule` et `august_rule` pour partager équitablement juillet et août.

**Configuration Parent A** :
```yaml
zone: "C"
vacation_split_mode: "odd_first"
july_rule: "july_odd"  # Juillet en années impaires
august_rule: "august_even"  # Août en années paires
school_level: "primary"
```

**Configuration Parent B** :
```yaml
zone: "C"
vacation_split_mode: "odd_second"
july_rule: "july_even"  # Juillet en années paires
august_rule: "august_odd"  # Août en années impaires
school_level: "primary"
```

**Résultat Parent A** :
- 2024 (paire) : ✅ Août 2024 complet
- 2025 (impaire) : ✅ Juillet 2025 complet
- 2026 (paire) : ✅ Août 2026 complet

**Résultat Parent B** :
- 2024 (paire) : ✅ Juillet 2024 complet
- 2025 (impaire) : ✅ Août 2025 complet
- 2026 (paire) : ✅ Juillet 2026 complet

---

### Exemple 3 : Partage Quinzaine Juillet

**Situation** : Partage de la 1ère quinzaine de juillet selon la parité de l'année.

**Configuration Parent A** :
```yaml
zone: "C"
vacation_split_mode: "odd_first"   # Impaire = 1ère Moitié
summer_rule: "july_first_half"     # Je veux la 1ère Moitié de Juillet
school_level: "primary"
```

**Configuration Parent B** :
```yaml
zone: "C"
vacation_split_mode: "odd_second"  # Impaire = 2ème Moitié
summer_rule: "july_first_half"     # Je veux la 1ère Moitié de Juillet
school_level: "primary"
```

**Résultat Parent A** (`odd_first`) :
- 2024 (paire) : 2ème Moitié → Règle (1ère) **Ne Correspond Pas**
- 2025 (impaire) : 1ère Moitié → Règle (1ère) **Correspond** → ✅ 1-15 Juillet 2025

**Résultat Parent B** (`odd_second`) :
- 2024 (paire) : 1ère Moitié → Règle (1ère) **Correspond** → ✅ 1-15 Juillet 2024
- 2025 (impaire) : 2ème Moitié → Règle (1ère) **Ne Correspond Pas**

> **Note** : Les deux parents demandent la "1ère Moitié de Juillet". Le système l'attribue au parent qui a *naturellement* la 1ère moitié cette année-là selon son `vacation_split_mode`.

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
3. **Année** : Vérifiez que la parité est correcte pour les règles basées sur la parité

### Les règles ne s'appliquent pas correctement

1. **vacation_split_mode** : Vérifiez si vous avez choisi la 1ère ou 2ème moitié pour les années impaires
2. **july_rule / august_rule / summer_rule** : Vérifiez les règles d’été
3. **Logs** : Consultez les logs pour voir les dates calculées

---

## 📚 Ressources

- **API Éducation Nationale** : https://data.education.gouv.fr/explore/dataset/fr-en-calendrier-scolaire
- **Documentation garde classique** : [`README_CONFIG_GARDE.fr.md`](README_CONFIG_GARDE.fr.md) ([English](README_CONFIG_GARDE.md))
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

