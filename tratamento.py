import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def import_data(path,separador = ',', encoding = 'utf-8'):
    #Importa arquivos csv
    #Parâmetros: path = caminho do arquivo, separador = separador do arquivo, encoding = codificação do arquivo
    #retorna um dataframe
    try:
        df = pd.read_csv(path, sep=separador, encoding=encoding)
        print("Arquivo importado com sucesso!")
        return df
    except UnicodeDecodeError as ue:
        print(f"Erro de codificação: {ue}. Tente outro encoding.")
    except FileNotFoundError as fnf:
        print(f"Arquivo não encontrado: {fnf}. Verifique o caminho.")
    except Exception as e:
        print(f"Erro ao importar o arquivo: {e}")

def renomeando_gp (df, nomes:dict):
    df.rename(columns={'pop' : 'population', 'lifeExp' : 'Life expectation', 'gdpPercap' : 'Gold per capta'}, inplace= True)
    df['country'] = df['country'].replace(nomes)
    return df


def verificar_NaN (dataframe: pd.DataFrame):
    #Verifica a quantidade de valores NaN em cada coluna do dataframe
    #Retorna colunas com NaN, a quantidade de NaN em cada coluna e o percentual de NaN em cada coluna
    quantidade_NaN = dataframe.isna().sum()
    df_NaN = quantidade_NaN.reset_index()
    df_NaN = df_NaN.rename(columns={'index':'coluna', 0:'qnt_NaN'})
    df_NaN = df_NaN[df_NaN['qnt_NaN'] > 0]
    df_NaN['percentual_NaN'] = ((df_NaN['qnt_NaN'] / len(dataframe)) * 100).round(2)
    df_NaN['percentual_NaN'] = df_NaN['percentual_NaN'].apply(lambda x: f'{x:.2f}%') 
    df_NaN = df_NaN.sort_values(by='qnt_NaN', ascending=False).reset_index(drop=True)
    return df_NaN


def verificar_duplicados (dataframe): #Corrigir
    #Verifica a quantidade de valores duplicados em cada coluna do dataframe
    #Retorna colunas com duplicados, a quantidade de duplicados em cada coluna e o percentual de duplicados em cada coluna
    quantidade_duplicados = pd.DataFrame.duplicated().sum()
    if quantidade_duplicados == 0:
        print("Não há valores duplicados no dataframe.")
    else:
        df_dup = quantidade_duplicados.reset_index()
        df_dup = df_dup.rename(columns={'index':'coluna', 0:'qnt_dup'})
        df_dup = df_dup[df_dup['qnt_dup'] > 0]
        df_dup['percentual_dup'] = ((df_dup['qnt_dup'] / len(dataframe)) * 100).round(2)
        df_dup['percentual_dup'] = df_dup['percentual_dup'].apply(lambda x: f'{x:.2f}%') 
        df_dup = df_dup.sort_values(by='qnt_dup', ascending=False).reset_index(drop=True)
        return df_dup

def gerar_metadados(dataframe):
    # Gera um dataframe com metadados do dataframe original
    # Parâmetros: dataframe = dataframe original
    # Retorna um dataframe com os metadados

    metadados = pd.DataFrame({
        'nome_variavel': dataframe.columns,
        'tipo': dataframe.dtypes.values,
        'qt_nulos': dataframe.isnull().sum().values,
        'percent_nulos': round((dataframe.isnull().sum() / len(dataframe)) * 100, 2).values,
        'cardinalidade': dataframe.nunique().values,
    })

    # Não reordena as colunas
    metadados = metadados.reset_index(drop=True)

    return metadados

def verifica_dados_duplicados(dataframe):
    qtd = dataframe.duplicated().sum()
    print(f'Foram encontrados {qtd} de registros duplicados\n')
    print('Prévia dos dados')
    filtro = dataframe.duplicated()
    return dataframe[filtro]

# Função verifica se o pais esta presente em ambas as bases
def integrar_dataframes_por_pais(df1, df2, coluna_pais_df1='country', coluna_pais_df2='country'):
    """
    Harmoniza nomes de países, compara, imprime os ausentes/extras e retorna
    ambos os DataFrames (df1 e df2) filtrados para conter APENAS os países que
    estão na interseção de ambos.

    Args:
        df1 (pd.DataFrame): O DataFrame base.
        df2 (pd.DataFrame): O DataFrame a ser integrado.
        coluna_pais_df1 (str): Nome da coluna de país no df1. Padrão é 'country'.
        coluna_pais_df2 (str): Nome da coluna de país no df2. Padrão é 'country'.

    Returns:
        (pd.DataFrame, pd.DataFrame): Uma tupla com (df1_filtrado, df2_filtrado).
    """
    
    # --- 1. Mapeamento de Correção de Nomes (Harmonização Manual) ---
    mapa = {
    'Congo Dem. Rep' : 'Congo Democratic Republic',
    'Democratic Republic of Congo' : 'Congo Democratic Republic',
    'Korea' : 'North Korea',
    'Congo Rep' : 'Congo Republic',
    'Hong Kong China' : 'Hong Kong',
    ' Korea Dem. Rep.' : 'North Korea',
    'Korea Rep.' : 'South Korea',
    'Yemen Rep.' : 'Yemen Republic',
    'Yemen' : 'Yemen Republic' 
    }
    
    # Criar cópias para evitar SettingWithCopyWarning e manter os originais intocados
    df1_temp = df1.copy()
    df2_temp = df2.copy()
    
    # Aplicar correções (antes da conversão para minúsculas para o .replace funcionar)
    df1_temp[coluna_pais_df1] = df1_temp[coluna_pais_df1].replace(mapa)
    df2_temp[coluna_pais_df2] = df2_temp[coluna_pais_df2].replace(mapa)
    
    # --- 2. Padronização de Case (Minúsculas) e Limpeza de Espaços ---
    # É fundamental para que a comparação seja robusta.
    df1_temp[coluna_pais_df1] = df1_temp[coluna_pais_df1].str.lower().str.strip()
    df2_temp[coluna_pais_df2] = df2_temp[coluna_pais_df2].str.lower().str.strip()
    
    # --- 3. Criação de Conjuntos (Sets) ---
    paises_df1 = set(df1_temp[coluna_pais_df1].unique())
    paises_df2 = set(df2_temp[coluna_pais_df2].unique())
    
    # --- 4. Cálculo da Interseção e Diferença ---
    interc = paises_df1 & paises_df2
    ausentes_df2 = paises_df1 - paises_df2  # Países em df1, mas não em df2
    extras_df2 = paises_df2 - paises_df1    # Países em df2, mas não em df1
    
    # --- 5. Impressão dos Países Ausentes/Extras ---
    print("-" * 50)
    print("ANÁLISE DE DATASETS PARA INTEGRAÇÃO")
    print("-" * 50)
    print(f"Número de Países na Interseção: {len(interc)}")
    
    if ausentes_df2:
        print(f"\nPaíses presentes no DF1, mas AUSENTES no DF2 ({len(ausentes_df2)}):")
        print(sorted(list(ausentes_df2)))
    else:
        print("\n✅ Todos os países do DF1 estão presentes no DF2.")

    if extras_df2:
        print(f"\nPaíses presentes no DF2, mas AUSENTES no DF1 ({len(extras_df2)}):")
        print(sorted(list(extras_df2)))
    else:
        print("\n✅ Todos os países do DF2 estão presentes no DF1.")
    
    print("-" * 50)

    # --- 6. Filtragem de AMBOS os DataFrames (Usando a Interseção) ---
    
    # O filtro é aplicado nas colunas originais, mas é convertido para lower/strip 
    # no momento da filtragem para comparar com o conjunto 'interc' (que está em minúsculas).
    
    # Filtra df1 original
    df1_filtrado = df1[df1[coluna_pais_df1].str.lower().str.strip().isin(interc)].copy()
    
    # Filtra df2 original
    df2_filtrado = df2[df2[coluna_pais_df2].str.lower().str.strip().isin(interc)].copy()
    
    print(f"Conclusão: DF1 e DF2 foram filtrados para a Interseção.")

    return df1_filtrado, df2_filtrado


