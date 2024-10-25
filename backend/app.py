import streamlit as st

st.set_page_config(
    page_title="ZancaAI",
    page_icon="🎵",
    layout="wide",
)

st.title("Bem-vindo ao ZancaAI")
st.write("ZancaAI é uma plataforma inovadora que oferece ferramentas de inteligência artificial para facilitar sua vida como produtor musical.")

if st.button("Get Started"):
    st.write("Você clicou no botão! Aqui você poderá acessar as funcionalidades da plataforma.")

st.header("Funcionalidades")
st.write("- Análise de áudio\n- Medições de LUFS\n- Sugestões de mixagem\n- E muito mais!")

st.markdown("---")
st.write("Criado por Rodrigo Zancanella. Todos os direitos reservados.Deus, obrigado!a")
