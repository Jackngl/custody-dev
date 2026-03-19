# 📊 Dashboard Guide - Custody Schedule

[🇫🇷 Version française](README_DASHBOARD_GARDE.fr.md) | [🇬🇧 English version](README_DASHBOARD_GARDE.md)

This guide provides a dedicated Lovelace **Custody Schedule** view with:
- a mockup-like global layout,
- a **multi-child** layout with distinct colors per child.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Example 1 - Mockup-like global view](#example-1---mockup-like-global-view)
3. [Example 2 - Multi-child with dedicated colors](#example-2---multi-child-with-dedicated-colors)
4. [Readability checklist](#readability-checklist)

---

## ✅ Prerequisites

- Custody integration configured.
- Available entities for each child (`calendar.*`, `sensor.*`, `binary_sensor.*`).
- Custom cards installed if used (`mushroom`).

---

## Example 1 - Mockup-like global view

```yaml
title: Custody Schedule
path: custody-schedule
icon: mdi:calendar-month
type: sections
max_columns: 2
sections:
  - title: Global view
    cards:
      - type: custom:mushroom-title-card
        title: CUSTODY SCHEDULE
        subtitle: Custody Schedule
      - type: custom:mushroom-chips-card
        chips:
          - type: template
            content: Mom
            icon: mdi:account
            icon_color: blue
          - type: template
            content: Dad
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
            name: Next arrival
            icon: mdi:calendar-clock
          - entity: sensor.lucas_next_departure
            name: Next departure
            icon: mdi:calendar-arrow-right
          - entity: sensor.lucas_days_remaining
            name: Days remaining
            icon: mdi:timer-outline
```

---

## Example 2 - Multi-child with dedicated colors

Principle: fixed color per child + dedicated section per child.

Sample palette:
- Lucas: `blue`
- Emma: `green`
- Noah: `deep-purple`

```yaml
title: Custody Schedule
path: custody-schedule
icon: mdi:calendar-month
type: sections
max_columns: 2
sections:
  - title: Children legend
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
        secondary: "Visual cue: blue"
        icon: mdi:account-child
        icon_color: blue
      - type: entities
        entities:
          - entity: binary_sensor.lucas_presence
            name: Presence
          - entity: sensor.lucas_current_period
            name: Current period
          - entity: sensor.lucas_days_remaining
            name: Days remaining
      - type: calendar
        title: Lucas planning
        entities:
          - entity: calendar.lucas_calendar

  - title: Emma
    cards:
      - type: custom:mushroom-template-card
        primary: Emma
        secondary: "Visual cue: green"
        icon: mdi:account-child
        icon_color: green
      - type: entities
        entities:
          - entity: binary_sensor.emma_presence
            name: Presence
          - entity: sensor.emma_current_period
            name: Current period
          - entity: sensor.emma_days_remaining
            name: Days remaining
      - type: calendar
        title: Emma planning
        entities:
          - entity: calendar.emma_calendar

  - title: Noah
    cards:
      - type: custom:mushroom-template-card
        primary: Noah
        secondary: "Visual cue: purple"
        icon: mdi:account-child
        icon_color: deep-purple
      - type: entities
        entities:
          - entity: binary_sensor.noah_presence
            name: Presence
          - entity: sensor.noah_current_period
            name: Current period
          - entity: sensor.noah_days_remaining
            name: Days remaining
      - type: calendar
        title: Noah planning
        entities:
          - entity: calendar.noah_calendar
```

---

## Readability checklist

- Keep a fixed color per child across all cards.
- Repeat the child name in both section title and calendar title.
- Avoid visually similar colors on the same screen.
- Check contrast in both light and dark themes.

