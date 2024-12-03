
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def carregar_dataset():
    
    return pd.read_csv('player_statistics_cleaned_final.csv' , sep = ';')

def resume_dado(df):
    
    resumo_dataframe = {
        "Descrição": df.describe(),
        "Dataset Shape": df.shape,
        "Linhas Duplicadas": True in df.duplicated(),
        "Valores Faltantes": df.isna().any(),
    }

    return resumo_dataframe


def performance_paises(df):
    
    performance_pais = df.groupby('Country')['Win rate'].agg(['mean', 'count']).sort_values('count', ascending=False)
    return performance_pais



def compara_times(df):
    df['Flash_F'] = (df['FlashKeybind'] == 'F').astype(int)  
    df['Flash_D'] = (df['FlashKeybind'] == 'D').astype(int)  

   
    metrica_time = df.groupby('TeamName').agg({
        'Win rate': 'mean',
        'KDA': 'mean',
        'Avg kills': 'mean',
        'DamagePercent': 'mean',
        'Flash_F': 'sum', 
        'Flash_D': 'sum'   
    }).sort_values('Win rate', ascending=False)

    metrica_time = metrica_time.round(2)  
    return metrica_time.copy()

def time_winrate_plot(df):
    
    time_winrate = df.groupby('TeamName')['Win rate'].mean().sort_values(ascending=False)
    
    fig,ax =plt.subplots(figsize=(12, 6))
    ax.bar(time_winrate.index, time_winrate, color='#0088A3', label='Contagem', alpha=0.7)

    ax.set_facecolor('none')  
    fig.patch.set_facecolor('none')  
    
   
    ax.title.set_color('white')  
    ax.xaxis.label.set_color('white')  
    ax.yaxis.label.set_color('white')  

    
    for tick in ax.get_xticklabels():
        tick.set_color('white')  
    for tick in ax.get_yticklabels():
        tick.set_color('white')  

    plt.title('Win Rate Médio por Time')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

def kda_posicao_plot(df):
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.set_facecolor('none')  
    fig.patch.set_facecolor('none')  
    
    
    ax.title.set_color('white')  
    ax.xaxis.label.set_color('white')  
    ax.yaxis.label.set_color('white')  

    
    for tick in ax.get_xticklabels():
        tick.set_color('white') 
    for tick in ax.get_yticklabels():
        tick.set_color('white')  

    sns.boxplot(x='Position', y='KDA', data=df,color ='#0088A3', ax=ax)

    
    plt.title('Distribuição de KDA por Posição', fontsize=16, color='white')
    
    
    ax.grid(False)
    
    return fig

def flash_keybind(df):
    
    flash_perf = df.groupby('FlashKeybind')['Win rate'].agg(['mean', 'count']).sort_values('count', ascending=False)

    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(flash_perf.index, flash_perf['mean'], color='#0088A3', label='Contagem', alpha=0.7)

    ax.title.set_color('white')  
    ax.xaxis.label.set_color('white')  
    ax.yaxis.label.set_color('white')

    for tick in ax.get_xticklabels():
        tick.set_color('white')  
    for tick in ax.get_yticklabels():
        tick.set_color('white')  
   

    
    fig.suptitle('Desempenho de FlashKeybind - Média de Win Rate e Contagem', fontsize=14, color='white')
    
    
    
    ax.set_facecolor('none')  
   
    fig.patch.set_facecolor('none') 
    
    
    plt.grid(False)
    return fig
    

def correlacao_heatmap(df):
    
    df_quantitativo = df.drop(columns=["TeamName", "PlayerName", "Position", "Country", "FlashKeybind"])
    df_quantitativo.replace("-", 0, inplace=True)
    
    fig ,ax= plt.subplots(figsize=(16,10))

    ax.set_facecolor('none')  
    fig.patch.set_facecolor('none')  
    
    
    ax.title.set_color('white')  
    ax.xaxis.label.set_color('white')  
    ax.yaxis.label.set_color('white')  

    
    for tick in ax.get_xticklabels():
        tick.set_color('white')  
    for tick in ax.get_yticklabels():
        tick.set_color('white')  
    sns.heatmap(df_quantitativo.corr(), annot=True, vmax=1, vmin=-1, cmap="mako")
    return fig

def compara_jogadores(df , player1, player2):
    
   
    comparacao_colunas = ['TeamName', 'Win rate', 'KDA', 'DamagePercent', 'VSPM', 'Country']
    
  
    p1_dado = df[df['PlayerName'] == player1][comparacao_colunas].iloc[0].round(2)
    p2_dado = df[df['PlayerName'] == player2][comparacao_colunas].iloc[0].round(2)
    
    
    
    return p1_dado , p2_dado