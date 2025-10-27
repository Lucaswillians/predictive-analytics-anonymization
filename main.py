import os
import pandas as pd
import hashlib
import matplotlib.pyplot as plt
 
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
 
# =========================
# SEÇÃO DE PLOTS (matplotlib)
# =========================
 
# pasta de saída para as figuras
plots_dir = "./dataset/plots"
os.makedirs(plots_dir, exist_ok=True)
 
def save_show(fig_name: str):
    """Helper: salva figura em PNG e faz tight_layout/close."""
    plt.tight_layout()
    full_path = os.path.join(plots_dir, fig_name)
    plt.savefig(full_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Figura salva em: {full_path}")
 
def first_existing(col_candidates):
    """Retorna a primeira coluna existente na lista de candidatos, senão None."""
    for c in col_candidates:
        if c in df_anon.columns:
            return c
    return None
 
# 1) Top 10 exportadores (pseudonimizados) por quantidade de operações
if 'exportador_anon' in df_anon.columns:
    counts = df_anon['exportador_anon'].value_counts().head(10)
    if not counts.empty:
        plt.figure()
        counts.sort_values(ascending=True).plot(kind='barh')
        plt.title('Top 10 Exportadores (por quantidade de operações)')
        plt.xlabel('Quantidade de operações')
        plt.ylabel('Exportador (anônimo)')
        save_show("top10_exportadores_qtd.png")
 
# 2) Histograma de valor (se existir alguma coluna de valor)
valor_col = first_existing([
    'valor', 'valor_total', 'valor_financiado', 'valor_da_operacao',
    'valor_da_exportacao', 'vlr_operacao', 'valor_usd'
])
 
if valor_col is not None:
    serie_valor = pd.to_numeric(df_anon[valor_col], errors='coerce').dropna()
    if not serie_valor.empty:
        plt.figure()
        plt.hist(serie_valor, bins=30)
        plt.title(f'Histograma de {valor_col}')
        plt.xlabel(valor_col)
        plt.ylabel('Frequência')
        save_show(f"hist_{valor_col}.png")
 
        # Boxplot para dar noção de outliers
        plt.figure()
        plt.boxplot(serie_valor, vert=True, showfliers=True)
        plt.title(f'Boxplot de {valor_col}')
        plt.ylabel(valor_col)
        save_show(f"boxplot_{valor_col}.png")
 
# 3) Evolução temporal de operações (se existir alguma coluna de data)
data_col = first_existing([
    'data_da_operacao', 'data_operacao', 'data', 'data_de_contratacao',
    'data_do_desembolso', 'dt_operacao'
])
 
if data_col is not None:
    datas = pd.to_datetime(df_anon[data_col], dayfirst=True, errors='coerce')
    ts = datas.dropna()
    if not ts.empty:
        # Séries por mês (contagem de operações)
        df_tmp = pd.DataFrame({'data': ts})
        df_tmp['ym'] = df_tmp['data'].dt.to_period('M').dt.to_timestamp()
        serie_mensal = df_tmp.groupby('ym').size()
 
        if not serie_mensal.empty:
            plt.figure()
            plt.plot(serie_mensal.index, serie_mensal.values)
            plt.title('Quantidade de operações por mês')
            plt.xlabel('Mês')
            plt.ylabel('Quantidade')
            save_show("operacoes_por_mes.png")
 
# 4) Top 10 por UF (ou Estado) de origem, se existir
uf_col = first_existing(['UF', 'uf', 'estado', 'sg_uf', 'UF_exportador'])
if uf_col is not None:
    top_uf = df_anon[uf_col].dropna().astype(str).value_counts().head(10)
    if not top_uf.empty:
        plt.figure()
        top_uf.sort_values(ascending=True).plot(kind='barh')
        plt.title(f'Top 10 {uf_col} por quantidade de operações')
        plt.xlabel('Quantidade de operações')
        plt.ylabel(uf_col)
        save_show(f"top10_{uf_col}_qtd.png")
 
# 5) Top 10 países de destino (se existir)
pais_col = first_existing([
    'pais_destino', 'pais', 'pais_do_importador', 'pais_do_destino',
    'pais_de_destino'
])
if pais_col is not None:
    top_pais = df_anon[pais_col].dropna().astype(str).value_counts().head(10)
    if not top_pais.empty:
        plt.figure()
        top_pais.sort_values(ascending=True).plot(kind='barh')
        plt.title(f'Top 10 países de destino ({pais_col})')
        plt.xlabel('Quantidade de operações')
        plt.ylabel('País')
        save_show(f"top10_{pais_col}_qtd.png")
 
print("Concluído. Arquivo anonimizado salvo em:", output_file)
print("Seção de plots finalizada. PNGs em:", plots_dir)