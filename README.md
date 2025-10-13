# 🧠 Atividade – Anonimização e Pseudoanonimização de Dados Pessoais  
**Aluno(a): [seu nome aqui]**  
**Dataset:** Operações de Exportação Pós-Embarque – BNDES  
**Link:** [CSV BNDES](https://dadosabertos.bndes.gov.br/dataset/f27e48cd-653b-4bfa-bc4f-08b637793873/resource/0cfe4594-44bf-48a8-a79a-686fc2d0db95/download/operacoes-exportacao-operacoes-de-exportacao-pos-embarque-bens.csv)

---

## 1️⃣ Contexto do problema

O dataset contém informações sobre **operações de exportação de bens** financiadas pelo BNDES. Algumas colunas podem identificar diretamente empresas exportadoras:

- `cnpj_do_exportador`  
- `numero_da_operacao`  
- `exportador`  

Para análises estatísticas ou preditivas, **é necessário proteger essas informações**, respeitando boas práticas similares às exigidas pela LGPD, mesmo que não envolvam pessoas físicas diretamente.

---

## 2️⃣ Técnicas de anonimização aplicáveis

| Coluna | Técnica sugerida | Descrição |
|--------|-----------------|-----------|
| `cnpj_do_exportador` | **Hashing** | Transformar o CNPJ em um código irreversível para que a empresa não seja identificável |
| `numero_da_operacao` | **Mascaramento** | Ocultar parte do número ou substituir por identificador genérico, preservando a relação interna |
| `exportador` | **Pseudoanonimização** | Substituir o nome real por um código ou pseudônimo (ex: "Empresa_001") |

**Exemplo de aplicação:**

- `cnpj_do_exportador = "12.345.678/0001-90"` → `hash_sha256("12.345.678/0001-90")`  
- `numero_da_operacao = "OP-2023-00123"` → `OP-XXXX-00123`  
- `exportador = "Empresa ABC LTDA"` → `Empresa_001`

---

## 3️⃣ Benefícios da anonimização

- Preserva a **privacidade das empresas** exportadoras.  
- Permite a **realização de análises estatísticas e preditivas** (como valores financiados, setores de exportação e produtos mais exportados) sem expor informações confidenciais.  
- Mantém conformidade com **boas práticas de proteção de dados**, similar à LGPD.

---

## 4️⃣ Conclusão

O dataset do BNDES pode ser usado de forma ética e segura em análises estatísticas ou machine learning ao aplicar **anonimização e pseudoanonimização** nas colunas identificáveis (`cnpj_do_exportador`, `numero_da_operacao`, `exportador`).  
Essas técnicas garantem **privacidade e conformidade** enquanto preservam a utilidade analítica dos dados.
