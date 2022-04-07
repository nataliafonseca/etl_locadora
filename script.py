# Importações
import sqlalchemy
import pandas as pd
import numpy as np

# bugs da oracle
import cx_Oracle
import os

pathname = os.path.join(os.getcwd(), 'assets', 'instantclient_21_3')

try:
    cx_Oracle.init_oracle_client(lib_dir=pathname)
except:
    pass

# Criação da engine do sql alchemy para a tabela
db_connection = sqlalchemy.create_engine(
    'oracle+cx_oracle://system:123456@localhost:1521/?encoding=UTF-8&nencoding=UTF-8'
)

# 1 - EXTRACT
# Extração da tabela locacoes para dataframe do pandas
locacoes_df = pd.read_sql(
    'SELECT * FROM locadora_origin.locacoes', db_connection)

# Extração da tabela socios para dataframe do pandas
socios_df = pd.read_sql('SELECT * FROM locadora_origin.socios', db_connection)

# Extração da tabela tipos_socios para dataframe do pandas
tipos_socios_df = pd.read_sql(
    'SELECT * FROM locadora_origin.tipos_socios', db_connection)

# Extração da tabela itens_locacoes para dataframe do pandas
itens_locacoes_df = pd.read_sql(
    'SELECT * FROM locadora_origin.itens_locacoes', db_connection)

# Extração da tabela copias para dataframe do pandas
copias_df = pd.read_sql(
    'SELECT * FROM locadora_origin.copias', db_connection
)

# Extração da tabela titulos para dataframe do pandas
titulos_df = pd.read_sql(
    'SELECT * FROM locadora_origin.titulos', db_connection
)

# Extração da tabela artistas para dataframe do pandas
artistas_df = pd.read_sql(
    'SELECT * FROM locadora_origin.artistas', db_connection)

# Extração da tabela gravadoras para dataframe do pandas
gravadoras_df = pd.read_sql(
    'SELECT * FROM locadora_origin.gravadoras', db_connection
)

# 2 - TRANSFORM

# DM_SOCIO
# Merge de socios e tipos_socios
dm_socio_df = pd.merge(
    left=socios_df, right=tipos_socios_df, how='left', on='cod_tps'
)
# Remoção das colunas desnecessárias
dm_socio_df.drop(columns=['dat_cad', 'cod_tps',
                 'sta_soc', 'lim_tit', 'val_base'], inplace=True)
# Renomeando colunas
dm_socio_df.rename(
    columns={
        'cod_soc': 'id_soc',
        'dsc_tps': 'tipo_socio',
    },
    inplace=True,
)

# DM_TITULO
# Remoção das colunas desnecessárias
dm_titulo_df = titulos_df.drop(
    columns=['qtd_cop', 'dat_lanc', 'cod_art', 'cod_grav'], inplace=False)
# Renomeando colunas
dm_titulo_df.rename(
    columns={
        'cod_tit': 'id_titulo',
        'tpo_tit': 'tpo_titulo',
        'cla_tit': 'cla_titulo',
        'dsc_tit': 'dsc_titulo',
    },
    inplace=True,
)

# DM_ARTISTA
# Remoção das colunas desnecessárias
dm_artista_df = artistas_df.drop(
    columns=['cod_grav', 'qtd_tit', 'med_anual'], inplace=False)
# Renomeando colunas
dm_artista_df.rename(
    columns={
        'cod_art': 'id_art',
    },
    inplace=True,
)

# DM_GRAVADORA
# Renomeando colunas
dm_gravadora_df = gravadoras_df.rename(
    columns={'cod_grav': 'id_grav'}, inplace=False)

# DM_TEMPO
# Criando o dataframe
dm_tempo_df = pd.DataFrame()

# Adicionando dados
dm_tempo_df['id_tempo'] = (locacoes_df['dat_loc'].astype(
    str).str.replace('-', '')).astype(int)
dm_tempo_df['dt_tempo'] = pd.to_datetime(locacoes_df['dat_loc'])

dm_tempo_df['nu_ano'] = pd.DatetimeIndex(dm_tempo_df['dt_tempo']).year
dm_tempo_df['nu_mes'] = pd.DatetimeIndex(dm_tempo_df['dt_tempo']).month
dm_tempo_df['nu_dia'] = pd.DatetimeIndex(dm_tempo_df['dt_tempo']).day

dm_tempo_df['nu_anomes'] = (dm_tempo_df['nu_ano'].astype(
    str) + dm_tempo_df['nu_mes'].astype(str).str.zfill(2)).astype(int)

dm_tempo_df['nm_mes'] = pd.DatetimeIndex(dm_tempo_df['dt_tempo']).month
dm_tempo_df['nm_mes'] = dm_tempo_df['nm_mes'].replace(1, 'janeiro')
dm_tempo_df['nm_mes'] = dm_tempo_df['nm_mes'].replace(2, 'fevereiro')
dm_tempo_df['nm_mes'] = dm_tempo_df['nm_mes'].replace(3, 'março')
dm_tempo_df['nm_mes'] = dm_tempo_df['nm_mes'].replace(4, 'abril')
dm_tempo_df['nm_mes'] = dm_tempo_df['nm_mes'].replace(5, 'maio')
dm_tempo_df['nm_mes'] = dm_tempo_df['nm_mes'].replace(6, 'junho')
dm_tempo_df['nm_mes'] = dm_tempo_df['nm_mes'].replace(7, 'julho')
dm_tempo_df['nm_mes'] = dm_tempo_df['nm_mes'].replace(8, 'agosto')
dm_tempo_df['nm_mes'] = dm_tempo_df['nm_mes'].replace(9, 'setembro')
dm_tempo_df['nm_mes'] = dm_tempo_df['nm_mes'].replace(10, 'outubro')
dm_tempo_df['nm_mes'] = dm_tempo_df['nm_mes'].replace(11, 'novembro')
dm_tempo_df['nm_mes'] = dm_tempo_df['nm_mes'].replace(12, 'dezembro')

dm_tempo_df['sg_mes'] = dm_tempo_df['nm_mes'].astype(str).str[0:3]

dm_tempo_df['nm_mesano'] = dm_tempo_df['sg_mes'].astype(
    str) + '/' + dm_tempo_df['nu_ano'].astype(str)

dm_tempo_df['turno'] = 'N/A'
dm_tempo_df['nu_hora'] = 0

# Removendo duplicatas
dm_tempo_df.drop_duplicates(inplace=True)

# FT_LOCACOES
ft_locacoes_df = pd.merge(
    left=itens_locacoes_df, right=titulos_df, how='left', on='cod_tit'
)
ft_locacoes_df = pd.merge(
    left=ft_locacoes_df, right=artistas_df, how='left', on='cod_art'
)

ft_locacoes_df['id_tempo'] = ft_locacoes_df['dat_loc'].astype(
    str).str.replace('-', '')

ft_locacoes_df.rename(
    columns={
        'cod_soc': 'id_soc',
        'cod_tit': 'id_titulo',
        'cod_art': 'id_art',
        'cod_grav_x': 'id_grav'
    },
    inplace=True,
)
ft_locacoes_df.drop(columns=['num_cop', 'sta_mul', 'cla_tit', 'tpo_tit', 'qtd_cop', 'dat_lanc',
                    'dsc_tit', 'tpo_art', 'nac_bras', 'cod_grav_y', 'qtd_tit', 'med_anual', 'nom_art'], inplace=True)

ft_locacoes_df['temp_colum'] = (pd.to_datetime(
    ft_locacoes_df['dat_dev']) - pd.to_datetime(ft_locacoes_df['dat_loc'])) // np.timedelta64(1, 'D') - 1


def get_temp_dev(tempo):
    lista = []
    for tempo in tempo:
        if tempo == 0:
            lista.append(1)
        elif tempo == -1:
            lista.append(0)
        else:
            lista.append(tempo)
    return lista


ft_locacoes_df['tempo_devolucao'] = get_temp_dev(
    ft_locacoes_df['temp_colum'].fillna(-1))
ft_locacoes_df.drop(columns=['temp_colum'], inplace=True)

ft_locacoes_df['temp_colum'] = (pd.to_datetime(ft_locacoes_df['dat_dev']) -
                                pd.to_datetime(ft_locacoes_df['dat_prev'])) // np.timedelta64(1, 'D') - 1


def get_multa_atraso(tempo, val_loc):
    lista = []
    for i in range(0, len(tempo)):
        if tempo[i] == 1:
            lista.append(val_loc[i])
        elif tempo[i] > 1:
            lista.append(val_loc[i] + 0.3*val_loc[i]*(tempo[i]-1))
        else:
            lista.append(0)
    return lista


ft_locacoes_df['multa_atraso'] = get_multa_atraso(
    ft_locacoes_df['temp_colum'].fillna(-1), ft_locacoes_df['val_loc'])
ft_locacoes_df.drop(columns=['temp_colum'], inplace=True)

ft_locacoes_df['valor_arrecadado'] = ft_locacoes_df['val_loc'] + \
    ft_locacoes_df['multa_atraso']
ft_locacoes_df.drop(columns=['dat_loc', 'dat_prev',
                    'val_loc', 'dat_dev'], inplace=True)

# 3 - LOAD
# Função para calculo do chunksize


def get_chunksize(table_columns):
    cs = 2097 // len(table_columns)
    cs = (1000 if cs > 1000 else cs)
    return cs

    # Exportação do dataframe dm_artista_df do pandas para a tabela dm_artista
dm_artista_df.to_sql(
    name='dm_artista',
    schema='locadora_destiny',
    con=db_connection,
    index=False,
    if_exists='replace',
    chunksize=get_chunksize(dm_artista_df.columns),
)

# Exportação do dataframe dm_gravadora_df do pandas para a tabela dm_gravadora
dm_gravadora_df.to_sql(
    name='dm_gravadora',
    schema='locadora_destiny',
    con=db_connection,
    index=False,
    if_exists='replace',
    chunksize=get_chunksize(dm_gravadora_df.columns),
)

# Exportação do dataframe dm_socio_df do pandas para a tabela dm_socio
dm_socio_df.to_sql(
    name='dm_socio',
    schema='locadora_destiny',
    con=db_connection,
    index=False,
    if_exists='replace',
    chunksize=get_chunksize(dm_socio_df.columns),
)

# Exportação do dataframe dm_titulo_df do pandas para a tabela dm_titulo
dm_titulo_df.to_sql(
    name='dm_titulo',
    schema='locadora_destiny',
    con=db_connection,
    index=False,
    if_exists='replace',
    chunksize=get_chunksize(dm_titulo_df.columns),
)

# Exportação do dataframe dm_tempo_df do pandas para a tabela dm_tempo
dm_tempo_df.to_sql(
    name='dm_tempo',
    schema='locadora_destiny',
    con=db_connection,
    index=False,
    if_exists='replace',
    chunksize=get_chunksize(dm_tempo_df.columns),
)

# Exportação do dataframe ft_locacoes_df do pandas para a tabela ft_locacoes
ft_locacoes_df.to_sql(
    name='ft_locacoes',
    schema='locadora_destiny',
    con=db_connection,
    index=False,
    if_exists='replace',
    chunksize=get_chunksize(ft_locacoes_df.columns),
)
