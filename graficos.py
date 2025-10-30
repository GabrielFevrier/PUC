import pandas as pd
import matplotlib.pyplot as plt  # <-- ADICIONE ESTA LINHA
import seaborn as sns

def graficos_linhas_continente(df, continent: str, observado: str, coluna_ano: str = 'year'):
    """"
    Args:
        df (pd.DataFrame): O DataFrame original.
        continent (str): O nome do continente a ser selecionado.
        observado (str): O nome da coluna que será agregada (eixo Y).
        coluna_ano (str): O nome da coluna de tempo (eixo X). Padrão é 'ano'.
    """
    df_filtrado = df[df['continent'] == continent].copy()
    if df_filtrado.empty:
        print(f"Não foram encontrados dados para o continente: {continent}")
        return
    plt.figure(figsize=(12, 8))
    # x=coluna_ano (Eixo X)
    # y=observado (Eixo Y - será a média dos valores para cada ano)
    sns.lineplot(
        x=coluna_ano,
        y=observado,
        data=df_filtrado,
        marker='o',          # Adiciona marcadores para os pontos
        errorbar='sd',       # Linha sólida = Média. Sombra = Desvio Padrão ('sd').
                             # Use 'ci' para Intervalo de Confiança (padrão)
        linewidth=2,
        color='darkorange'
    )
    title_text = f'Evolução da Média de {observado.replace("_", " ").title()} em {continent}'
    title_text += f'\n(Sombra = Desvio Padrão)'
    plt.title(title_text, fontsize=16, fontweight='bold')
    # Rótulos
    plt.xlabel(coluna_ano.capitalize(), fontsize=14)
    plt.ylabel(f'Média de {observado.replace("_", " ").title()}', fontsize=14)
    # Configuração dos Ticks (para garantir que apenas os anos existentes apareçam)
    plt.xticks(df_filtrado[coluna_ano].unique(), rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def graficos_linhas_pais(df, pais: str, observado: str, coluna_ano: str = 'year'):
    """
    Função para plotar um gráfico de linha da evolução de uma variável ao longo do tempo
    para um país específico usando sns.lineplot.
    
    Args:
        df (pd.DataFrame): O DataFrame original.
        pais (str): O nome do país a ser selecionado (assume coluna 'country' no df).
        observado (str): O nome da coluna que será plotada (eixo Y).
        coluna_ano (str): O nome da coluna de tempo (eixo X). Padrão é 'year'.
    """
    # 1. Filtragem (Assume que a coluna de país é 'country')
    df_filtrado = df[df['country'] == pais].copy()   
    if df_filtrado.empty:
        print(f"Não foram encontrados dados para o país: {pais}")
        return  
    # Garantir que os dados estejam ordenados por ano
    df_filtrado = df_filtrado.sort_values(by=coluna_ano)
    # 2. Plotagem com Seaborn
    plt.figure(figsize=(12, 8))
    sns.lineplot(
        x=coluna_ano,
        y=observado,
        data=df_filtrado,
        marker='o',
        linewidth=2,
        color='darkgreen'
    )

    # 3. Configurações do Gráfico
    title_text = f'Evolução de {observado.replace("_", " ").title()} no(a) {pais}'
    plt.title(title_text, fontsize=16, fontweight='bold')  
    # Rótulos
    plt.xlabel(coluna_ano.capitalize(), fontsize=14)
    plt.ylabel(observado.replace("_", " ").title(), fontsize=14) 
    # Configuração dos Ticks
    plt.xticks(df_filtrado[coluna_ano].unique(), rotation=45)  
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def comparando_cont(df, variavel_observada: str, coluna_ano: str = 'year', titulo_extra: str = ""):
    """
    Plota a evolução da média de uma variável ao longo do tempo para todos os continentes.

    Args:
        df (pd.DataFrame): O DataFrame original.
        variavel_observada (str): Nome da coluna para o eixo Y (ex: 'lifeExp', 'gdpPercap').
        coluna_ano (str): Nome da coluna do tempo (eixo X). Padrão é 'year'.
        titulo_extra (str): Texto opcional para adicionar ao título.
    """
    # sns.lineplot agrega automaticamente a média para cada ano por continente
    plt.figure(figsize=(14, 8))
    
    sns.lineplot(
        x=coluna_ano,
        y=variavel_observada,
        hue='continent',
        data=df,
        errorbar='sd',  # Linha é a Média, Sombra é o Desvio Padrão
        linewidth=3
    )
    
    # Formatação do Título e Rótulos
    var_title = variavel_observada.replace("Percap", " Per Capita").title()
    plt.title(f'Evolução da Média de {var_title} por Continente {titulo_extra}', fontsize=18, fontweight='bold')
    plt.xlabel(coluna_ano.capitalize(), fontsize=14)
    plt.ylabel(f'Média de {var_title}', fontsize=14)
    
    # Ajustar o eixo X para mostrar apenas os anos presentes (ticks)
    plt.xticks(df[coluna_ano].unique(), rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title='Continente', title_fontsize='12', loc='best')
    plt.tight_layout()
    plt.show()


def distribuicao_por_continente(df, ano: int, variavel_observada: str, tipo_grafico: str = 'box'):
    """
    Plota a distribuição de uma variável entre os continentes para um ano específico.

    Args:
        df (pd.DataFrame): O DataFrame original.
        ano (int): O ano que será filtrado.
        variavel_observada (str): Nome da coluna a ser analisada (ex: 'lifeExp', 'gdpPercap').
        tipo_grafico (str): 'box' para Box Plot ou 'violin' para Violin Plot.
    """
    
    # 1. Filtrar o DataFrame pelo ano
    df_filtrado = df[df['year'] == ano].copy()
    
    if df_filtrado.empty:
        print(f"Não foram encontrados dados para o ano: {ano}")
        return

    plt.figure(figsize=(12, 7))

    # 2. Selecionar o tipo de gráfico
    if tipo_grafico == 'box':
        sns.boxplot(
            x='continent',
            y=variavel_observada,
            data=df_filtrado,
            palette='Set2'
        )
    elif tipo_grafico == 'violin':
        sns.violinplot(
            x='continent',
            y=variavel_observada,
            data=df_filtrado,
            palette='Set2',
            inner='quartile' # Mostra os quartis dentro do violin plot
        )
    else:
        print("Tipo de gráfico inválido. Use 'box' ou 'violin'.")
        return
    
    # 3. Formatação
    var_title = variavel_observada.replace("Percap", " Per Capita").title()
    plt.title(f'Distribuição de {var_title} por Continente em {ano} ({tipo_grafico.title()} Plot)', fontsize=18, fontweight='bold')
    plt.xlabel('Continente', fontsize=14)
    plt.ylabel(var_title, fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def plotar_comparacao_dois_continentes(
    df,
    continentes: list,
    variavel_observada: str,
    coluna_continente: str = 'continent',
    coluna_ano: str = 'year'
):
    """
    Plota a evolução da média de uma variável ao longo do tempo, comparando dois continentes.

    Args:
        df (pd.DataFrame): O DataFrame original.
        continentes (list): Uma lista contendo os nomes dos dois continentes a serem comparados.
        variavel_observada (str): Nome da coluna para o eixo Y (ex: 'lifeExp', 'gdpPercap').
        coluna_continente (str): Nome da coluna do continente. Padrão é 'continent'.
        coluna_ano (str): Nome da coluna do tempo (eixo X). Padrão é 'year'.
    """
    
    if len(continentes) != 2:
        print("Erro: A lista 'continentes' deve conter exatamente dois nomes.")
        return

    # 1. Filtrar o DataFrame para incluir apenas os dois continentes
    df_filtrado = df[df[coluna_continente].isin(continentes)].copy()
    
    if df_filtrado.empty:
        print(f"Não foram encontrados dados para os continentes: {', '.join(continentes)}")
        return

    # 2. Plotagem com Seaborn
    plt.figure(figsize=(14, 8))
    
    # sns.lineplot agrega automaticamente a média para cada ano por continente
    sns.lineplot(
        x=coluna_ano,
        y=variavel_observada,
        hue=coluna_continente, # Cor por continente
        data=df_filtrado,
        errorbar='sd',         # Linha é a Média, Sombra é o Desvio Padrão
        marker='o',            # Adiciona marcadores nos pontos de dados
        linewidth=3
    )
    
    # 3. Formatação do Gráfico
    
    # Ajustar nome da variável para o título
    var_title = variavel_observada.replace("Percap", " Per Capita").title()
    
    title_continents = f'{continentes[0]} vs. {continentes[1]}'
    plt.title(f'Comparação da Média de {var_title} ao Longo do Tempo\n({title_continents})', 
              fontsize=18, fontweight='bold')
    
    plt.xlabel(coluna_ano.capitalize(), fontsize=14)
    plt.ylabel(f'Média de {var_title}', fontsize=14)
    
    # Ajustar o eixo X para mostrar apenas os anos presentes (ticks)
    plt.xticks(df[coluna_ano].unique(), rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title='Continente', title_fontsize='12', loc='best')
    plt.tight_layout()
    plt.show()

def graficos_mundos (df, X, Y):
    """
    Plota um gráfico de linha da evolução de uma variável (Y) ao longo do tempo (X).
    Adiciona uma linha horizontal para representar a média de Y ao longo do tempo.
    
    Args:
        df (pd.DataFrame): DataFrame que contém a série temporal (preferencialmente já agregada).
        X (str): Coluna do eixo horizontal (tempo).
        Y (str): Coluna do eixo vertical (valor).
    """
    
    # 1. Calcular a média da coluna Y
    media_y = df[Y].mean()
    
    plt.figure(figsize=(12,8)) 
    
    # Plot da evolução da série temporal
    sns.lineplot(
        data=df, 
        x=X, 
        y=Y, 
        marker='o', 
        linewidth=2, 
        color='darkgreen', 
        label=Y.replace('_', ' ').title()
    ) 
    
    # 2. Adicionar a linha horizontal da média
    plt.axhline(
        y=media_y, 
        color='red', 
        linestyle='--', 
        linewidth=2,
        label=f'Média Geral ({Y.replace("_", " ").title()}): {media_y:.2f}' 
    )

    # Configurações do gráfico
    plt.xlabel(X.capitalize(), fontsize=14)
    plt.ylabel(Y.replace("_", " ").title(), fontsize=14)
    plt.xticks(df[X].unique(), rotation=45)  
    plt.title(f"Evolução Global de {Y.replace('_', ' ').title()} com Média Horizontal", fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()

def plotar_comparacao_multiplos_paises(
    df,
    paises: list,
    variavel_observada: str,
    coluna_pais: str = 'country',
    coluna_ano: str = 'year'
):
    """
    Plota a evolução de uma variável ao longo do tempo, comparando múltiplos países.

    Args:
        df (pd.DataFrame): O DataFrame original.
        paises (list): Uma lista contendo os nomes dos países a serem comparados.
        variavel_observada (str): Nome da coluna para o eixo Y (ex: 'lifeExp', 'gdpPercap').
        coluna_pais (str): Nome da coluna do país. Padrão é 'country'.
        coluna_ano (str): Nome da coluna do tempo (eixo X). Padrão é 'year'.
    """
    
    if len(paises) < 2:
        print("Erro: A lista 'paises' deve conter no mínimo dois nomes para comparação.")
        return

    # 1. Filtrar o DataFrame para incluir apenas os países selecionados
    df_filtrado = df[df[coluna_pais].isin(paises)].copy()
    
    if df_filtrado.empty:
        print(f"Não foram encontrados dados para os países: {', '.join(paises)}")
        
        # Dica útil: verificar se o nome dos países está correto (case-sensitive)
        paises_nao_encontrados = [p for p in paises if p not in df[coluna_pais].unique()]
        if paises_nao_encontrados:
             print(f"Verifique se o nome dos seguintes países está correto (case-sensitive): {', '.join(paises_nao_encontrados)}")
        return

    # 2. Plotagem com Seaborn
    plt.figure(figsize=(14, 8))
    
    # sns.lineplot plota cada país individualmente
    sns.lineplot(
        x=coluna_ano,
        y=variavel_observada,
        hue=coluna_pais,         # Cor diferente para cada país
        data=df_filtrado,
        # Como estamos plotando dados de países individuais, não precisamos de errorbar/agregação
        errorbar=None, 
        marker='o',              # Adiciona marcadores nos pontos de dados
        linewidth=3
    )
    
    # 3. Formatação do Gráfico
    
    # Ajustar nome da variável para o título
    var_title = variavel_observada.replace("Percap", " Per Capita").title()
    
    plt.title(f'Comparação da Evolução de {var_title} ao Longo do Tempo', 
              fontsize=18, fontweight='bold')
    
    plt.xlabel(coluna_ano.capitalize(), fontsize=14)
    plt.ylabel(var_title, fontsize=14)
    
    # Ajustar o eixo X para mostrar apenas os anos presentes (ticks)
    plt.xticks(df[coluna_ano].unique(), rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title='País', title_fontsize='12', loc='best')
    plt.tight_layout()
    plt.show()

def plotar_pais_vs_media_continente(
    df,
    pais: str,
    observado: str,
    coluna_pais: str = 'country',
    coluna_continente: str = 'continent',
    coluna_ano: str = 'year'
):
    """
    Cria um gráfico de linhas comparando a evolução de uma variável para um país
    com a média de seu continente ao longo do tempo.

    Args:
        df (pd.DataFrame): O DataFrame original.
        pais (str): O nome do país a ser analisado.
        observado (str): O nome da coluna para o eixo Y (ex: 'lifeExp', 'gdpPercap').
        coluna_pais (str): Nome da coluna do país. Padrão é 'country'.
        coluna_continente (str): Nome da coluna do continente. Padrão é 'continent'.
        coluna_ano (str): Nome da coluna do tempo (eixo X). Padrão é 'year'.
    """

    # --- 1. Obter o nome do Continente e fazer verificações ---
    if pais not in df[coluna_pais].unique():
        print(f"Erro: País '{pais}' não encontrado no DataFrame.")
        return

    # Obter o continente do país na primeira ocorrência
    continente = df[df[coluna_pais] == pais][coluna_continente].iloc[0]
    
    # --- 2. Preparar os Dados para o Continente (Média) ---
    nome_coluna_media = f'media_{observado}'
    
    # Calcular a média por continente e ano
    df_agregado = df.groupby([coluna_continente, coluna_ano])[observado].mean().reset_index(name=nome_coluna_media)
    
    # Filtrar apenas o continente do país
    df_continente = df_agregado[df_agregado[coluna_continente] == continente].copy()
    
    # --- 3. Preparar os Dados para o País (Valor Individual) ---
    df_pais = df[df[coluna_pais] == pais].copy()
    
    # --- 4. Plotagem com Matplotlib e Seaborn ---
    plt.figure(figsize=(14, 8))
    
    # Plotar a linha do País (Valor real)
    sns.lineplot(
        x=coluna_ano,
        y=observado,
        data=df_pais,
        label=f'País: {pais}',
        marker='o',
        linewidth=3,
        color='blue',
        errorbar=None 
    )
    
    # Plotar a linha da Média do Continente
    sns.lineplot(
        x=coluna_ano,
        y=nome_coluna_media,
        data=df_continente,
        label=f'Média do Continente: {continente}',
        linestyle='--', # Linha tracejada para diferenciar
        linewidth=3,
        color='red',
        errorbar=None
    )
    
    # --- 5. Formatação do Gráfico ---
    var_title = observado.replace("Percap", " Per Capita").title()
    
    plt.title(f'Evolução de {var_title}: {pais} vs. Média da {continente}', 
              fontsize=18, fontweight='bold')
    
    plt.xlabel(coluna_ano.capitalize(), fontsize=14)
    plt.ylabel(var_title, fontsize=14)
    
    # Ajustar o eixo X para mostrar apenas os anos presentes (ticks)
    plt.xticks(df[coluna_ano].unique(), rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title='Legenda', title_fontsize='12', loc='best')
    plt.tight_layout()
    plt.show()
