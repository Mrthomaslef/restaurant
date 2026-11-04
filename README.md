<p align="center">
  <img src="assets/icon.svg" width="96" height="96" alt="Resto en Amoureux" />
</p>

<h1 align="center">🍷 Resto en Amoureux • Marie, Thomas &amp; Relais d'Émile</h1>

<p align="center">
  Application web mobile (PWA) connectée à <strong>Agenda Famille</strong> et <strong>Cochin RI</strong> pour mettre en évidence automatiquement les jours et soirées où <strong>Thomas Lefèvre</strong> et <strong>Marie Parizot</strong> ne travaillent pas et où <strong>Émile</strong> est gardé par ses grands-parents, avec lancement de <strong>réservation automatique de restaurant</strong> en 1 clic.
</p>

---

## ✨ Fonctionnalités Principales

1. **🌟 Détection Automatique des « Jours d'Or » (`Marie + Thomas libres + Émile chez les Grands-Parents`)**
   - Croise en temps réel :
     - Le planning de **Thomas** à l'Hôpital Cochin (Radio B, gardes de nuit/samedi, jeudis libres jusqu'au 07/01/2027 puis libéral Paris 5e, déplacements Valence, réunions Bone Club, semaine de congés validée du 28/12 au 03/01).
     - Le planning de **Marie** à l'Hôpital Trousseau (gardes 24h, demi-gardes 23h, gardes urgences 9h–21h, astreintes des 5–6 décembre, annulation de la demi-garde du 23/12).
     - Les relais des **Grands-Parents** pour **Émile** (Maman & Papa de Thomas à Fontenay-sous-Bois, Maman de Marie & Vincent Parizot) ainsi que les horaires de **Mabrouka Gdaiem**.
2. **🤖 Bouton de Réservation Automatique de Restaurant**
   - Pré-remplit automatiquement vos coordonnées (`Thomas Lefèvre & Marie Parizot`, `2 couverts`, `thomaslefevre18@live.fr`, `06 07 68 84 99`), copie le récapitulatif dans le presse-papiers, ouvre le portail de réservation (`Zenchef`, `TheFork`, `SevenRooms`) sur le créneau choisi, inscrit la soirée dans l'**Agenda Famille** (local + Cloud) et génère l'invitation **Apple Calendar (`.ics`)** ou le **SMS pour Marie**.
3. **👵👴 Hub Grands-Parents & Relais en 1 Clic**
   - Permet d'envoyer un SMS pré-rempli aux grands-parents (`Maman de Thomas`, `Papa de Thomas`, `Vincent Parizot`) sur les créneaux où Marie et Thomas sont libres tous les deux, ou d'enregistrer une garde d'Émile en 1 clic.
4. **🔄 Standard Pull-to-Refresh (`mobile-pull-to-refresh`)**
   - Glisser vers le bas en haut de l'écran actualise en direct les événements depuis `/Users/thomaslefevre/Documents/agenda-famille/family_data.json` et le Cloud Google Apps Script.

---

## 🚀 Lancement

- **En direct (Fichier statique / PWA)** : ouvrir [`index.html`](index.html)
- **Avec le serveur local de synchronisation** :
  ```bash
  python3 server.py
  # Puis ouvrir http://localhost:8790
  ```
