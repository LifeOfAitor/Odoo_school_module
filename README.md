# Eskola - Skolaren Kudeaketa Modulua

Skolaren kudeaketa osoa egiteko modulua. Ikasleak, irakasleak, ikaslearen ekipoa eta mantenimendua kudeatu ahal izango duzu.

## Nola Martxan Jarri
```bash
    Docker compose up -d
```
- Docker compose up egin
### Baldintzak
- Docker desktop instalatuta
- `stock` eta `purchase` moduluak aktiboak izan behar dute

### Instalazio pausuak

1. **Modulua kopialtu**
   ```
   custom_addons/eskola/ karpeta Odoo-ren custom_addons direktorioan kopialatu
   ```

2. **Modulua aktivatu**
   - Odoo administradorea gisa sartu
   - Aplikazioak > Moduluak > Moduluak ikuspegia
   - "Eskola" bilatu
   - Instalatu botoia sakatu

3. **Biltegi kokalekua konfiguratu**
   - Biltegi-a eta biltegi-aren kokalekuak konfiguratu:
     - Nagusia: `WH/Biltegi Nagusia` (100 ordenagailuak dituzten)
     - Gelak: `WH/Gela 1`, `WH/Gela 2`, etab.

4. **Produktua sortu**
   - Ordenagailu eta pantaila produktuak sortu stock aplikazioan

## Erabiltzaile Motak

Moduluak 2 erabiltzaile talde ditu:

### 1. Irakasleak (Irakasle taldea)
- Ikasleak, gelak eta ikaslearen datuen kudeaketa
- Ikasleen kalifikazioak eta faltak kudeatu
- Ekipoen intzidentzia ikusi

**Baimena:**
- Ikasleen irakurri eta idatzi
- Gelak ikusi
- Ekipoen intzidentzia sortu eta ikusi

### 2. Mantenimendua (Mantenimendu taldea)
- Ekipoen intzidentzia kudeatu
- Ekipoen mantenimendu zuloetan ibilbideak osatu

**Baimena:**
- Ekipoen intzidentzia irakurri eta idatzi
- Ekipoa inzidentzia egoera eguneratu

## Moduluaren Funtzionamendua

### 1. Ikasleak (Ikasle-ren Kudeaketa)

**Eremua:**
- Izena eta abizena
- **Jaiotze data** - Adina automatikoki kalkulatzen da
- Argazkia
- Generoa
- Gela eta zikloa

**Funtzionalitatea:**
- Adina automatikoki kalkulatzen da jaiotze dataren arabera
- Ikasle bakoitza gela bati lotua dago
- Ikasleari ekipoa eslei daiteke (ordenagailua, pantaila, etab.)

### 2. Gelak (Aula-ren Kudeaketa)

**Eremua:**
- Gelaren izena
- Ikasle kopurua (automatikoki kalkulatua)
- Kokalekua (biltegian)
- Zikloa

**Funtzionalitatea:**
- Gelaren ikasle kopurua automatikoki eguneratzen da
- Gela bakoitzak bere biltegi-kokalekua du
- Ekipoa gelari eslei daiteke

### 3. Ekipoa (Ordenagailu eta Pantailen Kudeaketa)

**Eremua:**
- Izena eta deskripzioa
- Mota (PC edo Pantaila)
- Produktua
- Gela (aukerakoa)
- Ikaslea (aukerakoa, baina gela bereko ikasleen bakarrik)

**Automatiko Funtzionalitatea:**

#### a) Biltegi Mugimendua
Ekipoa gelari esleitzerakoan:
- **Sortu**: Biltegi Nagusitik (WH/Biltegi Nagusia) gelaren kokalekura transferentzia
- **Mugitu**: Ekipoa gelaren kokalekua deitzen
- **Itzuli**: Ekipoa biltegira itzuli (ezabatzerakoan)

**Adibidea:**
1. Gela 1-ean 2 PC sortu
2. Biltegitik → Gela 1-era automatikoki transferitzen dira
3. Gela 2-era mugitzen badituzu → Gela 1etik → Gela 2-era transferitzen dira
4. Ezabatzen badituzu → Gela 2tik → Biltegira itzultzen dira

#### b) Ikasleen Filtroa
- Ekipoan ikaslea aukeratzean, biltze zerrendak **soilik gela bereko ikasleen** erakusten ditu
- Gela aldatzean, ikasleen zerrendak ere eguneratzen da

### 4. Zikloak (Ikasketa Zikloak)

**Eremua:**
- Zikloaren izena
- Ikasketa gaiak

### 5. Ikasgaiak (Ikasgaia-ren Kudeaketa)

**Eremua:**
- Ikasgaiaren izena
- Zikloa

### 6. Notak (Ikasleen Kalifikazioak)

**Eremua:**
- Nota (0-10 bitartean)
- Ikaslea
- Ikasgaia
- Zikloa (automatikoki beteta)

**Baldintzak:**
- Ikasle bakoitzak ikasgai bakoitzean nota bakarra izan daiteke

### 7. Faltak (Ikasleen Prezentziak)

**Eremua:**
- Data
- Motoa (Justifikatua / Justifikatu gabea)
- Oharra (aukerakoa)
- Ikaslea

**Baldintzak:**
- Ikasle bakoitzak data bakoitzean falta bakarra izan daiteke

### 8. Intzidentziak (Ekipoaren Mantenimendua)

**Eremua:**
- Deskripzioa
- Egoera (Zain / Eginda)
- Ekipoa

**Funtzionalitatea:**
- Ekipoan mantenimendurako arazoak intzidentzia gisa jasotzen dira
- Egoera "Zain" → "Eginda" eguneratzen da

### 9. Irakasleak

**Eremua:**
- Izena eta abizena
- Erabiltzailea (Odoo user)
- Argazkia

**Automatiko Funtzionalitatea:**
- Irakasleak sortzean, erabiltzailea automatikoki "Irakasle" taldera gehitzen da

### 10. Mantenimendua

**Eremua:**
- Izena eta abizena
- Erabiltzailea (Odoo user)
- Argazkia

**Automatiko Funtzionalitatea:**
- Mantenimendua sortzean, erabiltzailea automatikoki "Mantenimendu" taldera gehitzen da

## Workflow Adibidea

### Eszenarioa: Gela berri bat sortu eta ordenagailuak eslei

1. **Gela sortu**
   - `Gela 1` sortu
   - `WH/Gela 1` kokalekua eslei

2. **Produktua sortu** (stock aplikazioan)
   - `Ordenagailu Dell` produktua sortu
   - 100 unitatean biltegian

3. **Ekipoa sortu**
   - `Ordenagailu-1` sortu
   - Mota: PC
   - Produktua: Ordenagailu Dell
   - Gela: Gela 1

4. **Automatiko prozesu:**
   - Transferentzia sortzea: Biltegi Nagusitik → Gela 1
   - Transferentzia automatikoki validatu
   - Biltegian orain: 99 unitaetan
   - Gela 1ean orain: 1 unitatean

5. **Ikasleari eslei**
   - `Orderagailu-1`-ean `Ikasleak > Josu Perez` aukeratu
   - Gela 1-eko ikasleen bakarrik biltzen dira
