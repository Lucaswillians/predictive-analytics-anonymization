import pandas as pd
import hashlib

file_path = "./dataset/operacoes-exportacao-operacoes-de-exportacao-pos-embarque-bens.csv"
df = pd.read_csv(file_path, delimiter=';', encoding='iso-8859-1', engine='python')

original_cols = list(df.columns)
df_anon = df.copy()

# Hashing Function
def hash_value(value):
    return hashlib.sha256(str(value).encode('utf-8')).hexdigest()

# Mascaramento Function
def mask_operation(op_num):
    op_str = str(op_num)
    if len(op_str) > 4:
        # Mantém 2 primeiros + X's + 2 últimos
        masked_part = 'X' * (len(op_str) - 4)
        return op_str[:2] + masked_part + op_str[-2:]
    return 'X' * len(op_str)

# 1. Pseudonimização (exportador)
unique_exporters = df_anon['exportador'].unique()
exporter_id_map = {name: f"Exportador_{i+1}" for i, name in enumerate(unique_exporters)}
df_anon['exportador_anon'] = df_anon['exportador'].map(exporter_id_map)

# 2. Hashing (cnpj_do_exportador)
df_anon['cnpj_anon'] = df_anon['cnpj_do_exportador'].apply(hash_value)

# 3. Mascaramento (numero_da_operacao)
df_anon['numero_da_operacao_anon'] = df_anon['numero_da_operacao'].apply(mask_operation)

# Definir a nova ordem das colunas
final_cols = []
for col in original_cols:
    if col == 'exportador':
        final_cols.append('exportador_anon')
    elif col == 'cnpj_do_exportador':
        final_cols.append('cnpj_anon')
    elif col == 'numero_da_operacao':
        final_cols.append('numero_da_operacao_anon')
    else:
        final_cols.append(col)

# Reordenar o DataFrame
df_anon = df_anon[final_cols]

# Salvar em UTF-8 (com BOM)
output_file = './dataset/operacoes_exportacao_anonimizado.csv'
df_anon.to_csv(output_file, index=False, sep=';', encoding='utf-8-sig')