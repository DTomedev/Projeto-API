import streamlit as st
import requests
import folium
from streamlit_folium import st_folium


api_key = "544c0965f29c4c7610304e7ed9b08e2f"

st.image("H:\Gabriel\Davi Tomé\BACK-END\Projeto api-clima\imagem_clima.jpg")
st.title(" Clima em Tempo Real - OpenWeather")
st.write("**DIgite o nome da cidade para obter informações climáticas.**")

# Entrada das Cidades
cidades_populares = ["São Paulo", "Curitiba", "Rio de Janeiro", "Belo Horizonte"]
digite_cidade = st.text_input("**Cidade (ex: São Paulo, Curitiba):**")
selecione_cidade = st.selectbox("**Ou escolha uma cidade polular:**", cidades_populares, index=None)
escolha_cidade = digite_cidade if digite_cidade else selecione_cidade


if escolha_cidade:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={escolha_cidade}&appid={api_key}&lang=pt_br&units=metric"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()

            st.subheader(f"Clima em {escolha_cidade.title()}")
            icone = dados['weather'][0].get('icon')
            if icone:
                st.image(f"http://openweathermap.org/img/wn/{icone}@2x.png", width=80)

           # Mostra as informações climáticas em caixinhas de métricas
            col1, col2 = st.columns(2)
            col1.metric("Temperatura:", f"{dados['main']['temp']}°C")
            col2.metric("Descrição:", f"{dados['weather'][0]['description'].title()}")

            col3, col4, col5 = st.columns(3)
            col3.metric("Sensação Térmica:", f"{dados['main']['feels_like']}°C")
            col4.metric("Umidade:", f"{dados['main']['humidity']}%")
            col5.metric("Velocidade do Vento:", f"{dados['wind']['speed']} m/s")

            # Localização
            lat, lon = dados['coord']['lat'], dados['coord']['lon']

            # mapa interativo
            mapa = folium.Map(location=[lat,lon], zoom_start=10)
            folium.Marker(
                [lat, lon],
                    tooltip=f"{escolha_cidade.title()} - {dados['main']['temp']}°C",
            popup=f"Clima: {dados['weather'][0]['description'].title()}"
                ).add_to(mapa)
            
            #renderizar o mapa
            st_folium(mapa, width=700, height=500)
        else:
            st.error("Cidade não encontrada. Por favor, verifique o nome e tente novamente.")
