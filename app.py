import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
from analise_org_de_dados import *

df = carregar_dataset()

st.title("Estatísticas do Mundial de League of Legends 2024")

st.header("Resumo")
st.write(f"Nesse dataset , contemos informações sobre {len(df) -1} jogadores do Mundial de LoL de 2024 ")
st.write(f"O Mundial terminou no dia 2 de novembro com a Equipe T1 como campeã.")

st.header("Dataset")
st.write("O dados desse dataset foram gerados pelo gol.gg e publicados no site Kaggle")
st.dataframe(df)

tab1, tab2, tab3 = st.tabs([
    "Comparação de Jogadores e Times",
    "Visualizações",
    "Performance de Jogadores e Times"
])
    
    
with tab1:
    st.header("Comparação de Jogadores")
    col1, col2 = st.columns(2)
    
    with col1:

        
        player1 = st.selectbox(
            "Selecione o primeiro Jogador",
            options=sorted(df['PlayerName'].unique()),
            key="player1"
        )
    
    with col2:
        player2 = st.selectbox(
            "Selecione o segundo Jogador",
            options=sorted(df['PlayerName'].unique()),
            key="player2"
        )
    
    if st.button("Comparar Jogadores"):
        
        p1_data, p2_data = compara_jogadores(df, player1, player2)
        
        
        col_text1, col_text2 = st.columns(2)
    
        with col_text1:
            st.markdown('<div style="text-align: center"><h3>  %s</h3> </div>'%player1  ,True)
            st.dataframe(p1_data, width = 400)
        with col_text2:
            st.markdown('<div style="text-align: center"><h3>%s</h3> </div>'%player2,True)
            st.dataframe(p2_data, width = 400)

    st.markdown("""<h2 class="func_title">Comparação de Times</h2>""",unsafe_allow_html=True)
    col1_1, col1_2 = st.columns(2)
    
    with col1_1:
        team1 = st.selectbox(
            "Selecione o primeiro Time",
            options=sorted(df['TeamName'].unique()),
            key="team1"
        )
    
    with col1_2:
        team2 = st.selectbox(
            "Selecione o segundo Time",
            options=sorted(df['TeamName'].unique()),
            key="team2"
        )
    
    if st.button("Comparar Times"):

        col1_3, col1_4 = st.columns(2)
        comparacao = compara_times(df)
        with col1_3:
            st.markdown('<div style="text-align: center"><h3> Time : %s</h3> </div>'%team1  ,True)

            st.dataframe(comparacao.loc[team1], width = 400)
        with col1_4:
            st.markdown('<div style="text-align: center"><h3> Time : %s</h3> </div>'%team2  ,True)
            st.dataframe(comparacao.loc[team2],width = 400)
        
    
    
with tab2:
    st.write('Nesta seção, realizamos a verificação e o tratamento do dataset para garantir que ele esteja limpo e realizamos a sua visualização.')
    resumo = resume_dado(df)
    st.header("Resumo do Dataset:")
    

    for key, value in resumo.items():
        if key == "Valores Faltantes":
            
            missing_df = pd.DataFrame({
                "Coluna": value.index,
                "Possui Valores Ausentes?": value.values
            })
            st.write(f"- **{key}**")
            st.table(missing_df)  
        else:
            st.write(f"- **{key}**: {value}")
    st.write(" O conjunto de dados contém informações sobre 81 jogadores profissionais de League of Legends (LoL), sem linhas duplicadas ou valores faltantes. Considerando que cada time no LoL é composto por 5 jogadores, o dataset abrange 16 times, com exceção de um time que inclui um jogador reserva.")
    st.header("Visualizações")
    st.subheader("Análise de Performance por País")
    
    country_perf = performance_paises(df)
    
   
    fig = px.pie(country_perf, 
                names=country_perf.index, 
                values='count', 
                title='Distribuição de Jogadores por País',
                hole=0.3)  

    fig.update_layout(
    width=800,  
    height=600, 
    title_font_size=20,  
    legend_font_size=14 
    )

   
    st.plotly_chart(fig)
    st.write("A partir do gráfico, podemos observar que a maior parte do cenário profissional de League of Legends é composta por jogadores da China e da Coreia do Sul. Esse fenômeno pode ser explicado pelo tamanho do cenário competitivo desses países, que é tão desenvolvido que eles frequentemente importam jogadores de outras regiões. Um exemplo disso é a equipe brasileira Pain Gaming, que, apesar de ser um time do Brasil, conta com apenas 3 jogadores brasileiros, sendo que os outros 2 são coreanos.")


    fig1 = time_winrate_plot(df)
    plt.close(fig1)  

    
    fig2 = kda_posicao_plot(df)
    plt.close(fig2)

    
    fig3 = correlacao_heatmap(df)
    plt.close(fig3)
    
    fig4 = flash_keybind(df)
    plt.close(fig4)

   
    st.subheader("Taxa de Vitória X Time")
    st.pyplot(fig1)
    st.write("A análise da taxa de winrate revela que a T1 foi o time com o maior índice de vitórias no Mundial, o que pode ser atribuído ao fato de que a equipe conquistou o título de campeã. Novamente, o domínio das equipes asiáticas é evidente, já que os cinco times com as maiores taxas de winrate são sul-coreanos ou chineses.")
    st.subheader("KDA X Posição")
    st.pyplot(fig2)
    st.write("Realizamos uma análise utilizando boxplots para examinar a distribuição do KDA (Kills, Deaths, Assists) em diferentes posições. Como observado, os jogadores das posições de top e suporte tendem a apresentar um KDA mais baixo em comparação aos jogadores de ADC e mid. Isso se deve ao fato de que tanto o ADC quanto o mid geralmente são responsáveis pela maior fonte de dano do time, o que resulta em mais abates.")
    st.write(" Além disso, como as posições de top e suporte geralmente são ocupadas por campeões que têm um papel mais voltado para o controle do mapa e o apoio à equipe, esses jogadores acabam se expondo mais ao time inimigo, o que aumenta a probabilidade de mortes e, consequentemente, contribui para um KDA mais baixo.")
    st.subheader("Matriz de Correlação")
    st.pyplot(fig3)
    st.write('Neste gráfico, apresentamos a matriz de correlação entre todas as variáveis quantitativas do Dataset. Os valores variam de -1 a 1 e indicam o grau de relação entre as colunas. Um exemplo prático é a relação entre o KDA e a média de mortes: quanto maior a média de mortes, menor tende a ser o KDA, o que configura uma relação inversamente proporcional. Isso é comprovado pela correlação de -0,83 entre "KDA" e "Avg deaths". Outra relação interessante que encontramos foi entre Visão por Minuto (VSPM) e CS por Minuto (CSperMin). Como é comum que os suportes coloquem mais visão no mapa e não ganhem ouro por farmar, a correlação entre CSperMin e VSPM foi de -0,93.')

    st.subheader("Taxa de Vitória X Tecla do Flash")
    st.pyplot(fig4)
    st.write('Neste gráfico, analisamos a taxa de winrate em função da tecla atribuída ao feitiço de Flash. Existe uma grande discussão na comunidade sobre qual é a melhor tecla para o Flash: "D" ou "F". Ao observar os dados dos melhores jogadores do mundo, notamos que, em média, a taxa de vitórias é maior para jogadores que utilizam o Flash na tecla "F". Curiosamente, ao analisar o time campeão, a T1, todos os jogadores utilizam o Flash exclusivamente na tecla "F".')
    
    
   
    
with tab3:
    st.header("Performance por Rota")
    

    
    role = st.selectbox('Selecione a Role:', ['Top', 'Jungle', 'Mid', 'Adc', 'Support'])
    role_df = df[df['Position'] == role]

    
    media_kda_role = role_df['KDA'].mean()
    max_kda_role = role_df['KDA'].max()
    maior_kda_player = df[df['KDA'] == max_kda_role]['PlayerName'].tolist()[0]
    min_kda_role = role_df['KDA'].min()
    menor_kda_player = df[df['KDA'] == min_kda_role]['PlayerName'].tolist()[0]

    
    st.write(f"A média de Abates/Mortes/Assistências (KDA) é de: {media_kda_role:,.2f}\n")
    st.write(f"O jogador {maior_kda_player} possui o maior KDA: {max_kda_role}")
    st.write(f"O jogador {menor_kda_player} possui o menor KDA: {min_kda_role}")

   
    scatter = alt.Chart(role_df).mark_circle(size=100).encode(
        x='PlayerName',
        y='KDA',
        
        tooltip=['PlayerName', 'KDA']
    ).properties(
        width=700,
        height=400
    )

    
    line = alt.Chart(pd.DataFrame({'media': [media_kda_role]})).mark_rule(color='red', strokeDash=[5, 5]).encode(
        y='media:Q'
    )

   
    chart = scatter + line
    st.altair_chart(chart, use_container_width=True)

    st.caption("Os jogadores com KDA acima da média estão acima da linha vermelha. Os jogadores com KDA abaixo da média estão abaixo da linha vermelha.")






    st.header("Performance da Equipe")

    
    team = st.selectbox("Selecione uma equipe", df['TeamName'].unique())
    team_df = df[df['TeamName'] == team]

    

    
    st.write("Para esta análise, iremos utilizar como métrica a Diferença de Gold em 15 minutos em relação ao time inimigo.")

    
    scatter = alt.Chart(team_df).mark_circle(size=150).encode(
        x='PlayerName',
        y='GD@15',
        tooltip=['PlayerName', 'GD@15']
    ).properties(
        width=700,
        height=400
    )

    
    line = alt.Chart(pd.DataFrame({'base': [0]})).mark_rule(color='red', strokeDash=[5, 5]).encode(
        y='base:Q'
    )
    chart = scatter + line
    st.altair_chart(chart, use_container_width=True)

    st.caption("Os jogadores com GD@15 positivo estão acima da linha vermelha. Os jogadores com GD@15 negativo estão abaixo da linha vermelha.")

   

