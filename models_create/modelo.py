import numpy as np
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt

from pycaret.classification import *

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 40)
pd.set_option('display.max_colwidth', 1000)


df = pd.read_csv('data\Risco_Fogo.csv', sep=';', encoding='utf-8')
df = df.drop_duplicates()
df['data_hora_gmt'] = pd.to_datetime(df['data_hora_gmt'], format='%d/%m/%Y %H:%M')
df['data'] = df['data_hora_gmt'].dt.date
df['horario'] = df['data_hora_gmt'].dt.strftime('%H:%M')
df['horario'] = pd.to_datetime(df['horario'], format='%H:%M').dt.hour
df = df.drop('data_hora_gmt', axis=1)

# Definindo os limites dos bins e os rótulos
bins = [0, 0.3, 0.6, 0.8, 1.0]
labels = ['Baixo', 'Médio', 'Alto', 'Muito Alto']

#Binning
df['risco_fogo_binned'] = pd.cut(df['risco_fogo'],
                                 bins=bins,
                                 labels=labels,
                                 include_lowest=True,
                                 right=True)
#Dropando a Feture Risco_Fogo
df = df.drop('risco_fogo', axis=1)
df['dia_de_semana'] = pd.to_datetime(df['data']).dt.day_name()
dia_semana_portugues = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

df['dia_de_semana'] = df['dia_de_semana'].map(dia_semana_portugues)
df = df.drop('data', axis=1)

# sample 5% of data to be used as unseen data
df_train_test = df.sample(frac=0.95, random_state=123)
df_valid = df.drop(df_train_test.index)
df_train_test.reset_index(inplace=True, drop=True)
df_valid.reset_index(inplace=True, drop=True)

s = setup(data = df_train_test,
          target = 'risco_fogo_binned',
          fix_imbalance = True,
          remove_outliers = True,
          categorical_features = ['municipio', 'estado', 'bioma', 'dia_de_semana'],
          session_id = 123)

models = compare_models()
mdl_rf = create_model('rf')
tuned_rf = tune_model(mdl_rf)
save_model(tuned_rf, 'models\pickle_tuned_rf_pycaret3')
save_model(mdl_rf, 'models\pickle_mdl_rf_pycaret3')