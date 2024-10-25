import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="ZancaAI",
    page_icon="🎵",
    layout="wide",
)

# Título do aplicativo
st.title("Bem-vindo ao ZancaAI")

# Descrição da plataforma
st.write("""
    ZancaAI é uma plataforma inovadora que oferece ferramentas de inteligência artificial para facilitar sua vida como produtor musical.
""")

# Botão "Get Started"
if st.button("Get Started"):
    st.write("Você clicou no botão! Aqui você poderá acessar as funcionalidades da plataforma.")

# Seções adicionais
st.header("Funcionalidades")
st.write("""
    - Análise de áudio
    - Medições de LUFS
    - Sugestões de mixagem
    - E muito mais!
""")

# Rodapé
st.markdown("---")
st.write("Criado por Rodrigo Zancanella. Todos os direitos reservados.")
