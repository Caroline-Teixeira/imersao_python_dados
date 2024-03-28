import pandas as pd
import plotly.express as px

# O caminho do arquivo
caminho_arquivo = "Imersão Python - Tabela de ações2.xlsx"

# Para ler o arquivo Excel
df_principal = pd.read_excel(caminho_arquivo, sheet_name="Principal")
df_total_acoes = pd.read_excel(caminho_arquivo, sheet_name="Total_de_acoes")
df_ticker = pd.read_excel(caminho_arquivo, sheet_name="Ticker")
df_chat_gpt = pd.read_excel(caminho_arquivo, sheet_name="chat gpt")

# print(df_principal.head())  # Exibição das primeiras linhas do DataFrame
# print(df_principal)  # Exibição do DataFrame
# print(df_total_acoes)
# print(df_ticker)
# print(df_chat_gpt)


df_principal = df_principal.loc[:, ['Ativo', 'Data', 'Último (R$)',
                                    'Var. Dia (%)']].copy()  # Seleciona as colunas desejadas e cria uma cópia
df_principal = df_principal.rename(
    columns={'Último (R$)': 'valor_final', 'Var. Dia (%)': 'var_dia_pct'}).copy()  # Renomeia as colunas

df_principal['Var_pct'] = df_principal['var_dia_pct'] / 100

# Variação Dia % = x / 100 e Valor Inicial (R$) = valor_final / (Var % + 1)
df_principal['valor_inicial'] = df_principal['valor_final'] / (df_principal['Var_pct'] + 1)

# Função MERGE (para agrupar colunas)
df_principal = df_principal.merge(df_total_acoes, left_on='Ativo', right_on='Código', how='left')
df_principal = df_principal.drop(columns=['Código'])  # para eliminar colunas repetidas
# Cálculos
# Variacao_rs
df_principal['Variacao_rs'] = (df_principal['valor_final'] - df_principal['valor_inicial']) * df_principal['Qtde. Teórica']
pd.options.display.float_format = '{:.2f}'.format  # formatação
df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(int)  # Conversão de float para int
df_principal = df_principal.rename(columns={'Qtde. Teórica': 'Qtd_teorica'}).copy()  # renomear colunas
# resultados
df_principal['Resultado'] = df_principal['Variacao_rs'].apply(lambda x: 'Subiu' if x > 0 else ('Desceu' if x < 0 else 'Estável'))
# Nomes das empresas
df_principal = df_principal.merge(df_ticker, left_on='Ativo', right_on='Ticker', how='left')
df_principal = df_principal.drop(columns=['Ticker'])
df_principal = df_principal.merge(df_chat_gpt, left_on='Nome', right_on='Nome da empresa', how='left')
df_principal = df_principal.drop(columns=['Nome da empresa'])
df_principal = df_principal.rename(columns={'Idade em anos': 'Idade'}).copy()  # renomear colunas
df_principal = df_principal.rename(columns={'Ano de Início das Operações': 'ano'}).copy()  # renomear colunas

# Cálculos de faixas de idades
df_principal['Cat_idade'] = df_principal['Idade'].apply(lambda x: 'Mais de 100' if x > 100 else ('Menos de 50' if x < 50 else 'Entre 50 e 100'))

# Exibe o DataFrame resultante
# print(df_principal)

# ANÁLISES
# Calculando o maior valor
maior = df_principal['Variacao_rs'].max()

# Calculando o menor valor
menor = df_principal['Variacao_rs'].min()

# Calculando a média
media = df_principal['Variacao_rs'].mean()

# Calculando a média de quem subiu
media_subiu = df_principal[df_principal['Resultado'] == 'Subiu']['Variacao_rs'].mean()

# Calculando a média de quem desceu
media_desceu = df_principal[df_principal['Resultado'] == 'Desceu']['Variacao_rs'].mean()

# Imprimindo os resultados
# print(f"Maior\tR$ {maior:,.2f}")
# print(f"Menor\tR$ {menor:,.2f}")
# print(f"Média\tR$ {media:,.2f}")
# print(f"Média de quem subiu\tR$ {media_subiu:,.2f}")
# print(f"Média de quem desceu\tR$ {media_desceu:,.2f}")

# Análise de segmentos
df_principal_subiu = df_principal[df_principal['Resultado'] == 'Subiu']
# print(df_principal_subiu)

df_analise_segmento = df_principal_subiu.groupby('Segmento')['Variacao_rs'].sum().reset_index()
# print(df_analise_segmento)

# Análise de saldos
df_analise_saldo = df_principal.groupby('Resultado')['Variacao_rs'].sum().reset_index()
# print(df_analise_saldo)

# Cria o gráfico de barras usando o Plotly Express
fig = px.bar(df_analise_saldo, x='Resultado', y='Variacao_rs', text='Variacao_rs', title='Variação Reais por Resultado')
# fig.show()  # Exibe o gráfico

# DESAFIO ALURA
# Desafio 1 - mudar a formatação
fig.update_traces(texttemplate='R$ %{text:,.2f}', textposition='outside')
# fig.show()

# Desafio 2 - gráfico de pizza
fig2 = px.pie(df_analise_segmento, names='Segmento', values='Variacao_rs', title='Variação Reais por Segmento')
# fig2.show()

# Desafio 3 - GroupBy da categoria de idades e gráfico de barras
# Agrupando os dados pela categoria de idades e calculando a soma das variações de reais
df_analise_cat_idade = df_principal.groupby('Cat_idade')['Variacao_rs'].sum().reset_index()
print(df_analise_cat_idade)

# Criando o gráfico de barras
fig3 = px.bar(df_analise_cat_idade, x='Cat_idade', y='Variacao_rs', text='Variacao_rs', title='Variação Reais por Categoria de Idade')
fig3.update_traces(texttemplate='R$ %{text:,.2f}', textposition='outside')
fig3.show()



