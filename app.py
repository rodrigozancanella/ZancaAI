import os
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore
import requests

# Inicializa o Firebase Admin apenas uma vez
def initialize_firebase():
    if not firebase_admin._apps:  # Verifica se o Firebase já foi inicializado
        try:
            cred = credentials.Certificate('serviceAccountKey.json')  # Verifique o caminho do arquivo
            firebase_admin.initialize_app(cred)
            return firestore.client()  # Retorna o cliente do Firestore
        except ValueError as e:
            st.error(f"Erro ao inicializar o Firebase: {e}")
            return None
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado ao inicializar o Firebase: {e}")
            return None
    else:
        return firestore.client()  # Retorna o cliente do Firestore se já foi inicializado

# Inicializa o Firestore
db = initialize_firebase()

# Verifica se o Firestore foi inicializado corretamente
if db is not None:
    st.success("Firebase inicializado com sucesso!")
else:
    st.error("Falha ao inicializar o Firebase. O aplicativo não pode continuar.")

# Função para criar um novo usuário
def create_user(email, password):
    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyChPx0J4Nsy7Jw0aPyTFOgcfqhlOW-9B7U"  # Substitua pela sua API Key
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            user_data = {
                "email": email,
                "senha": password,
                # Adicione outros campos que deseja armazenar
            }
            db.collection('usuarios').add(user_data)  # Adicione o usuário à coleção 'usuarios'
            st.success(f'Usuário {email} criado com sucesso!')
        else:
            error_message = response_data.get("error", {}).get("message", "Erro desconhecido.")
            st.error(f'Erro ao criar usuário: {error_message}')
    except Exception as e:
        st.error(f'Erro ao salvar dados no Firestore: {str(e)}')

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
            if error_message == "INVALID_EMAIL":
                st.error("Erro de autenticação: O email fornecido é inválido.")
            elif error_message == "USER_DISABLED":
                st.error("Erro de autenticação: O usuário foi desativado.")
            elif error_message == "INVALID_PASSWORD":
                st.error("Erro de autenticação: A senha fornecida é inválida.")
            elif error_message == "EMAIL_NOT_FOUND":
                st.error("Erro de autenticação: O email não foi encontrado.")
            else:
                st.error(f'Erro de autenticação: {error_message}')
    except Exception as e:
        st.error(f'Ocorreu um erro ao buscar o usuário: {str(e)}')

# Interface do Streamlit
st.title("ZancaAI - Autenticação")
email = st.text_input("Email")
password = st.text_input("Senha", type='password')

# Botão para criar um novo usuário
if st.button("Criar Usuário"):
    if email and password:
        create_user(email, password)
    else:
        st.warning("Por favor, preencha todos os campos.")

# Botão para fazer login
if st.button("Login"):
    if email and password:
        login(email, password)
    else:
        st.warning("Por favor, preencha todos os campos.")
