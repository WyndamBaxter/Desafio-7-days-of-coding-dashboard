import pandas as pd
df = pd.read_parquet('F:/Programação/Desafio-7-days-of-coding-dashboard/resultados/df_emprestimos_completo.parquet')
print(df.info(memory_usage='deep'))