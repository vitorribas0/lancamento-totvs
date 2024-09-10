import streamlit as st
import speech_recognition as sr

# Função para realizar a transcrição
def transcribe_audio(file):
    recognizer = sr.Recognizer()

    # Abre o arquivo de áudio
    with sr.AudioFile(file) as source:
        audio_data = recognizer.record(source)
    
    # Tenta reconhecer o áudio usando o Google Speech Recognition
    try:
        text = recognizer.recognize_google(audio_data, language='pt-BR')
        return text
    except sr.UnknownValueError:
        return "Não foi possível entender o áudio"
    except sr.RequestError as e:
        return f"Erro ao conectar ao serviço de reconhecimento: {e}"

# Título da aplicação
st.title("Upload e Transcrição de Áudio")

# Upload de arquivos
uploaded_file = st.file_uploader("Escolha um arquivo de áudio", type=["mp3", "m4a", "wav"])

if uploaded_file is not None:
    # Exibe informações do arquivo
    st.write(f"Nome do arquivo: {uploaded_file.name}")
    
    # Realiza a transcrição
    with st.spinner('Transcrevendo o áudio...'):
        transcription = transcribe_audio(uploaded_file)
    
    # Exibe a transcrição
    st.write("**Transcrição:**")
    st.write(transcription)
else:
    st.write("Nenhum arquivo foi carregado.")