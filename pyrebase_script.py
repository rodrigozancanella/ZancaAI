import os
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore  # Importar Firestore
import requests

# Inicializa o Firebase Admin apenas uma vez
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate('serviceAccountKey.json')  # Verifique o caminho do arquivo
        firebase_admin.initialize_app(cred)
        db = firestore.client()  # Inicializa o Firestore
        initialized_successfully = True
    except ValueError as e:
        st.error(f"Erro ao inicializar o Firebase: {e}")
        initialized_successfully = False
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao inicializar o Firebase: {e}")
        initialized_successfully = False
else:
    initialized_successfully = True

# Mostra a mensagem de sucesso se a inicialização foi bem-sucedida
if initialized_successfully:
    st.success("Firebase inicializado com sucesso!")

# Função para criar um novo usuário
def create_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyChPx0J4Nsy7Jw0aPyTFOgcfqhlOW-9B7U"  # Substitua pela sua API Key
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    response_data = response.json()

    if response.status_code == 200:
        st.success(f'Usuário {email} criado com sucesso!')
        
        # Adiciona o usuário ao Firestore
        user_data = {
            "email": email,
            "dataDeRegistro": firestore.SERVER_TIMESTAMP,
        }
        
        try:
            # Salvar no Firestore
            db.collection('usuarios').add(user_data)  # Adicione o usuário à coleção 'usuarios'
            st.success(f'Dados do usuário salvos com sucesso no Firestore!')
        except Exception as e:
            st.error(f'Erro ao salvar dados no Firestore: {str(e)}')

    else:
        error_message = response_data.get("error", {}).get("message", "Erro desconhecido.")
        st.error(f'Erro ao criar usuário: {error_message}')

# Função para autenticar o usuário
def login(email, password):
    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyChPx0J4Nsy7Jw0aPyTFOgcfqhlOW-9B7U"  # Substitua pela sua API Key
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            user = auth.get_user_by_email(email)  # Para pegar o usuário no Firebase Admin
            st.success(f'Usuário {user.email} autenticado com sucesso!')
        else:
            error_message = response_data.get("error", {}).get("message", "Erro desconhecido.")
            st.error(f'Erro de autenticação: {error_message}')

    except Exception as e:
        st.error(f'Ocorreu um erro ao buscar o usuário: {str(e)}')

# Interface do Streamlit
st.title("ZancaAI - Autenticação")
email = st.text_input("Email")
password = st.text_input("Senha", type='password')

if st.button("Criar Usuário"):
    if email and password:
        create_user(email, password)
    else:
        st.warning("Por favor, preencha todos os campos.")

if st.button("Login"):
    if email and password:
        login(email, password)
    else:
        st.warning("Por favor, preencha todos os campos.")
