import streamlit as st
import random
from typing import List, Dict

# ────────────────────────────────────────────────
# Seiten-Konfiguration
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="Asiatische Resteküche",
    page_icon="🍜",
    layout="wide"
)

# ────────────────────────────────────────────────
# Beispiel-Rezepte-Datenbank (kann später stark erweitert werden)
# ────────────────────────────────────────────────
REZEPTE: List[Dict] = [
    {
        "name_de": "Gebratener Reis mit Ei und Gemüse",
        "name_original": "Yangzhou Fried Rice / 扬州炒饭",
        "herkunft": "China",
        "schwierigkeit": "leicht",
        "zeit": "15–20 min",
        "vegetarisch": True,
        "vegan": False,
        "glutenfrei": False,
        "scharf": False,
        "zutaten": ["Jasminreis", "Ei", "Frühlingszwiebeln", "Erbsen", "Karotten", "Sojasauce", "Sesamöl", "Knoblauch"],
        "fehlende_max": 3
    },
    {
        "name_de": "Pad Thai mit Tofu",
        "name_original": "ผัดไทย",
        "herkunft": "Thailand",
        "schwierigkeit": "mittel",
        "zeit": "25 min",
        "vegetarisch": True,
        "vegan": True,
        "glutenfrei": False,
        "scharf": True,
        "zutaten": ["Reisnudeln", "Tofu", "Eier", "Bohnensprossen", "Frühlingszwiebeln", "Erdnüsse", "Tamarindenpaste", "Fischsauce", "Chili", "Limette"],
        "fehlende_max": 5
    },
    {
        "name_de": "Koreanischer Bibimbap (einfach)",
        "name_original": "비빔밥",
        "herkunft": "Korea",
        "schwierigkeit": "mittel",
        "zeit": "30 min",
        "vegetarisch": True,
        "vegan": True,
        "glutenfrei": False,
        "scharf": True,
        "zutaten": ["Jasminreis", "Spinat", "Karotten", "Zucchini", "Pilze", "Ei", "Gochujang", "Sesamöl", "Sojasauce", "Knoblauch"],
        "fehlende_max": 4
    },
    {
        "name_de": "Teriyaki-Hähnchen mit Reis",
        "name_original": "照り焼きチキン",
        "herkunft": "Japan",
        "schwierigkeit": "leicht",
        "zeit": "25 min",
        "vegetarisch": False,
        "vegan": False,
        "glutenfrei": False,
        "scharf": False,
        "zutaten": ["Hähnchen", "Sojasauce", "Mirin", "Sake", "Zucker", "Ingwer", "Knoblauch", "Jasminreis"],
        "fehlende_max": 4
    },
    {
        "name_de": "Einfache Miso-Suppe mit Tofu",
        "name_original": "味噌汁",
        "herkunft": "Japan",
        "schwierigkeit": "leicht",
        "zeit": "10–15 min",
        "vegetarisch": True,
        "vegan": True,
        "glutenfrei": False,
        "scharf": False,
        "zutaten": ["Miso-Paste", "Tofu", "Seetang (Wakame)", "Frühlingszwiebeln", "Dashi oder Gemüsebrühe"],
        "fehlende_max": 3
    },
    {
        "name_de": "Gemüse-Curry mit Kokosmilch",
        "name_original": "แกงเขียวหวานเจ",
        "herkunft": "Thailand",
        "schwierigkeit": "mittel",
        "zeit": "30 min",
        "vegetarisch": True,
        "vegan": True,
        "glutenfrei": True,
        "scharf": True,
        "zutaten": ["Kokosmilch", "Grüne Curry-Paste", "Tofu oder Gemüse", "Bambussprossen", "Aubergine", "Basilikum", "Fischsauce", "Zucker"],
        "fehlende_max": 5
    },
    # Hier können noch 10–20 weitere Rezepte hin
]

# ────────────────────────────────────────────────
# Alle möglichen Zutaten (aus den Rezepten extrahiert + ergänzt)
# ────────────────────────────────────────────────
ZUTATEN_GRUPPEN = {
    "Reis, Nudeln & Getreide": ["Jasminreis", "Reisnudeln", "Glasnudeln"],
    "Würzpasten & Saucen": ["Sojasauce", "Fischsauce", "Austernsauce", "Miso-Paste", "Gochujang", "Grüne Curry-Paste", "Tamarindenpaste"],
    "Gewürze & Basics": ["Knoblauch", "Ingwer", "Frühlingszwiebeln", "Sesamöl", "Sesamsamen", "Zucker", "Limette"],
    "Frisches Gemüse & Kräuter": ["Karotten", "Zucchini", "Paprika", "Spinat", "Bohnensprossen", "Pilze", "Aubergine", "Basilikum", "Koriander"],
    "Proteine": ["Ei", "Tofu", "Hähnchen", "Schweinefleisch", "Rindfleisch"],
    "Sonstiges": ["Kokosmilch", "Erdnüsse", "Dashi oder Gemüsebrühe", "Mirin", "Sake"]
}

ALLE_ZUTATEN = sorted(set(z for gruppe in ZUTATEN_GRUPPEN.values() for z in gruppe))

# ────────────────────────────────────────────────
# App
# ────────────────────────────────────────────────
st.title("🍜 Asiatische Resteküche")
st.markdown("Wähle, **was du schon zu Hause hast** – wir finden Gerichte mit möglichst wenigen Einkäufen.")

# ────────────────────────────────────────────────
# Filter & Personen
# ────────────────────────────────────────────────
with st.sidebar:
    st.header("Filter & Einstellungen")

    vegetarisch = st.checkbox("Vegetarisch", value=False)
    vegan = st.checkbox("Vegan", value=False)
    kein_schwein = st.checkbox("Kein Schwein", value=False)
    scharf_option = st.selectbox("Scharf / Mild", ["Egal", "Scharf", "Mild / nicht scharf"])
    glutenfrei = st.checkbox("Glutenfrei", value=False)

    personen = st.radio("Portionen", [1, 2, 4], horizontal=True, index=1)

# ────────────────────────────────────────────────
# Zutaten-Auswahl
# ────────────────────────────────────────────────
st.subheader("Was hast du zu Hause? (Mehrfachauswahl)")

vorhandene_zutaten = set()

for kategorie, zutaten in ZUTATEN_GRUPPEN.items():
    with st.expander(kategorie, expanded=(kategorie == "Reis, Nudeln & Getreide")):
        cols = st.columns(3)
        for i, zutat in enumerate(zutaten):
            if cols[i % 3].checkbox(zutat, key=f"zutat_{zutat}"):
                vorhandene_zutaten.add(zutat)

# ────────────────────────────────────────────────
# Passende Rezepte finden
# ────────────────────────────────────────────────
if vorhandene_zutaten:
    st.subheader("Passende Rezepte – sortiert nach wenigen Einkäufen")

    gefilterte_rezepte = []

    for rezept in REZEPTE:
        # Filter prüfen
        if vegan and not rezept["vegan"]:
            continue
        if vegetarisch and not rezept["vegetarisch"]:
            continue
        if kein_schwein and "Schweinefleisch" in rezept["zutaten"]:
            continue
        if glutenfrei and "Sojasauce" in rezept["zutaten"] and "glutenfrei" not in rezept.get("hinweise", []):
            continue  # hier könnte man später bessere Logik einbauen
        if scharf_option == "Scharf" and not rezept["scharf"]:
            continue
        if scharf_option == "Mild / nicht scharf" and rezept["scharf"]:
            continue

        # Fehlende Zutaten zählen
        fehlende = [z for z in rezept["zutaten"] if z not in vorhandene_zutaten]
        anz_fehlende = len(fehlende)

        gefilterte_rezepte.append({
            "rezept": rezept,
            "fehlende": fehlende,
            "anz_fehlende": anz_fehlende
        })

    # Sortieren: zuerst wenigste fehlende, dann nach Zeit/Schwierigkeit
    gefilterte_rezepte.sort(key=lambda x: (x["anz_fehlende"], x["rezept"]["zeit"]))

    # Top 4–5 zeigen
    for item in gefilterte_rezepte[:5]:
        r = item["rezept"]
        fehlende = item["fehlende"]

        with st.container(border=True):
            st.markdown(f"**{r['name_de']}**  ({r['name_original']})")
            cols = st.columns([2, 1, 1])
            cols[0].markdown(f"**Herkunft:** {r['herkunft']}")
            cols[1].markdown(f"**Schwierigkeit:** {r['schwierigkeit']}")
            cols[2].markdown(f"**Zeit:** {r['zeit']} • {personen} Portionen")

            st.markdown(f"**Neue Zutaten:** {', '.join(fehlende) if fehlende else 'Keine!'}")

            st.markdown("**Zutaten** (für {} Personen):".format(personen))
            for z in r["zutaten"]:
                menge = "nach Bedarf"  # hier später realistische Mengen einfügen
                haken = "✓" if z in vorhandene_zutaten else ""
                st.write(f"- {z} {haken}")

            st.markdown("**Kurzanleitung** (vereinfacht):")
            st.markdown("1. Reis/Nudeln kochen\n2. Gemüse & Protein anbraten\n3. Würzen & Soßen hinzufügen\n4. Alles vermengen & heiß servieren\n(vollständige Anleitung später erweiterbar)")

            st.caption("Tipp: Mit etwas Sesamöl oder Frühlingszwiebeln wird's noch besser!")

else:
    st.info("Wähle mindestens ein paar Zutaten aus, damit wir passende Rezepte finden können 😊")

st.markdown("---")
st.caption("Noch mehr Rezepte, genauere Mengen, Einkaufslisten & echte Schritt-für-Schritt-Anleitungen können später leicht ergänzt werden.")
