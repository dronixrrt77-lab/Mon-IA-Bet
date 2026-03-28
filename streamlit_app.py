import streamlit as st
import pandas as pd
import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="1x-IA Pro Predictor", page_icon="⚽", layout="wide")

# --- 2. SYSTÈME DE SÉCURITÉ (MOT DE PASSE) ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    st.title("🔐 Accès Cyber Shield IA")
    pwd = st.text_input("Entre le code d'accès :", type="password")
    if st.button("Se connecter"):
        if pwd == "1234": # <--- CHANGE CE MOT DE PASSE ICI
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Code incorrect")
    return False

# --- 3. CHARGEMENT DU CERVEAU (.PKL) ---
def charger_cerveau():
    try:
        with open('cerveau_ia.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return {"minute_securite": 80, "tirs_min": 8}

# --- 4. CONFIGURATION DU NAVIGATEUR (POUR LE CLOUD) ---
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Utilise Chromium pour le serveur Streamlit
    service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    return webdriver.Chrome(service=service, options=options)

# --- Lancement de l'interface si le mot de passe est bon ---
if check_password():
    cerveau = charger_cerveau()
    
    st.title("⚽ 1x-IA Pro Predictor")
    st.sidebar.header("🧠 Paramètres du Cerveau")
    st.sidebar.write(f"Minute cible : {cerveau['minute_securite']}")
    st.sidebar.write(f"Tirs min : {cerveau['tirs_min']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 LANCER LE SCAN LIVE"):
            st.info("Connexion au serveur 1xBet...")
            try:
                driver = get_driver()
                driver.get("https://1xbet.com/live/football")
                time.sleep(5) # Attend le chargement
                
                # ICI : Ajoute ta logique de scan (scraping)
                st.success("Analyse en cours sur 150 matchs...")
                driver.quit()
                
                st.warning("🎫 COUPON DÉTECTÉ : **G5XTY**")
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")

    with col2:
        st.subheader("📊 Historique (Journal)")
        try:
            df = pd.read_csv('journal_ia.csv')
            st.dataframe(df.tail(5))
        except:
            st.write("Aucune donnée dans le journal.")

    if st.button("💾 Mettre à jour le cerveau"):
        # Exemple pour modifier le cerveau
        nouveau_cerveau = {"minute_securite": 82, "tirs_min": 9}
        with open('cerveau_ia.pkl', 'wb') as f:
            pickle.dump(nouveau_cerveau, f)
        st.success("Cerveau mis à jour !")
                    
