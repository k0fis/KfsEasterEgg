# 🐰 Velikonoční hra – Game Design (Cartoon Farm Level)

## 🎮 Core Idea

Hráč ovládá zajíce, který skáče po mapě a sbírá velikonoční vajíčka.
Po sesbírání všech vajec se odemyká další level.

Současně:

* hráče nahání pes
* musí se vyhýbat překážkám a plánovat pohyb

---

## 🚜 Farma Level

### 🌿 Prostředí

Farmářská zahrada / dvorek obsahuje:

* stodolu
* balíky sena (kryt i překážky)
* ohrady
* slepice (pohyblivé překážky)
* bahno (zpomaluje pohyb)

---

## 🚜 Traktor (hlavní hazard)

### Chování

* pohybuje se po předem definované trase (např. okruh)
* blokuje cesty
* může srazit hráče → ztráta života / restart

### Variace

* **normální traktor** – pomalý, předvídatelný
* **turbo traktor** – rychlý, chaotický
* **boss traktor** – ničí překážky

---

## 🐕 Pes (nepřítel)

### Chování

* pronásleduje hráče
* ve vyšších levelech:

  * reaguje na pohyb
  * predikuje směr

### Interakce

* pes může být zmaten traktorem
* může měnit směr při kolizi s objekty

---

## 🐔 Další prvky

### Slepice

* náhodný pohyb po mapě
* blokují cestu
* mohou vytvářet chaos

### Interakce

* mohou „spawnovat“ vajíčka (volitelné)

---

## 🥚 Vajíčka (collectibles)

Typy:

* **normální** – základní sběr
* **zlaté** – bonus body
* **speciální**:

  * zpomalení psa
  * štít
  * teleport

---

## ⚠️ Překážky

* keře (blokují pohyb)
* ploty (některé lze přeskočit)
* bahno (zpomalí)
* díry (reset pozice)

---

## 🎮 Gameplay mechaniky

### Pohyb

* zajíc se pohybuje skoky (ne plynule)
* typy skoků:

  * krátký (rychlý, bezpečný)
  * dlouhý (riskantní, překoná překážky)

---

### Strategie

* vyhýbání se psovi
* načasování pohybu vzhledem k traktoru
* plánování trasy sběru vajec

---

## 🎨 Vizuální styl – Roztomilý Cartoon

### Obecně

* pastelové barvy
* měkké, kulaté tvary
* hravý, ne realistický styl

---

### 🐰 Zajíc

* velké oči
* pružné uši
* squash & stretch animace při skoku

---

### 🐕 Pes

* „goofy“ vzhled
* přehnané animace (klouzání, nárazy)

---

### 🚜 Traktor

* velká kola
* lehké poskakování
* zanechává stopu (prach / bahno)

---

### 🥚 Vajíčka

* výrazné barvy
* vzory
* glow efekt u speciálních

---

## 🔊 Zvuky

* skok: „boing“
* pes: „baf“
* traktor: „brm brm“
* sběr vajíčka: „pop“

---

## 📈 Progression

* více psů
* rychlejší traktor
* složitější mapy
* kombinace hazardů

---

## 💡 Extra nápady

* hráč může skočit na balík sena (výhoda výšky)
* traktor může zničit vajíčka
* pes se občas bojí traktoru
* vajíčka se mohou pohybovat

---

## 🎯 MVP (Minimum Viable Product)

* 1 mapa (farma)
* 1 pes
* 1 traktor
* základní typ vajíček
* jednoduchý pohyb (šipky)
* win condition: sesbírat všechna vejce


