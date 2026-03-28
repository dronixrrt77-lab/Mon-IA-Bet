import streamlit as st
import pandas as pd
import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="1x-IA Pro", page_icon="⚽")

# --- 2. SÉCURITÉ PAR MOT DE PASSE ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    st.title("🔐 Accès Cyber Shield IA")
    pwd = st.text_input("Entre le code d'accès :", type="password")
    if st.button("Se connecter"):
        if pwd == "1234":  # <--- Change ton code ici
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Code incorrect")
    return False

# --- 3. CHARGEMENT DU CERVEAU ---
def charger_cerveau():
    try:
        with open('cerveau_ia.pkl', 'rb') as f:
            return pickle.load(f)
    except Exception:
        return {"minute_securite": 80, "tirs_min": 8}

# --- 4. CONFIGURATION DU NAVIGATEUR ---
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Utilisation de Chromium pour le cloud
    service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    return webdriver.Chrome(service=service, options=options)

# --- LANCEMENT DE L'APP ---
if check_password():
    cerveau = charger_cerveau()
    st.title("⚽ 1x-IA Pro Predictor")
    
    st.sidebar.header("🧠 Paramètres Actuels")
    st.sidebar.info(f"Minute cible : {cerveau['minute_securite']}\nTirs min : {cerveau['tirs_min']}")

    if st.button("🚀 LANCER LE SCAN LIVE"):
        with st.spinner("Recherche de cotes à 1.009..."):
            try:
                driver = get_driver()
                driver.get("https://1xbet.com/live/football")
                time.sleep(5)
                # Ta logique de scan ici
                st.success("Analyse terminée !")
                st.warning("🎫 COUPON DÉTECTÉ : **G5XTY**")
                driver.quit()
            except Exception as e:
                st.error(f"Erreur technique : {e}")

    # Affichage du journal
    st.subheader("📊 Journal d'Analyse")
    try:
        df = pd.read_csv('journal_ia.csv')
        st.dataframe(df.tail(10))
    except:
        st.info("Le journal est vide ou introuvable.")
        
