import random
from datetime import datetime, timedelta
from google.cloud import bigtable

# Configurações de conexão
client = bigtable.Client(project='seu-projeto-id', admin=True)
instance = client.instance('sua-instancia-id')
table = instance.table('sua-tabela-id')

# Definir a família de colunas
column_family_id = 'cf1'  # Substitua pelo ID real da sua família de colunas

# Função para gerar uma data aleatória entre 1, 2 e 3 anos atrás
def random_past_date():
    years_ago = random.choice([1, 2, 3])
    random_days = random.randint(0, 365 * years_ago)
    return datetime.utcnow() - timedelta(days=random_days)

# Inserir 100 registros aleatórios
for i in range(100):
    row_key = f"registro-{i}"
    name = f"Name_{random.randint(1000, 9999)}"
    age = random.randint(20, 50)
    data = random_past_date().isoformat()  # Converte para ISO 8601

    # Criar a linha no Bigtable
    row = table.direct_row(row_key)
    row.set_cell(column_family_id, 'name', name)
    row.set_cell(column_family_id, 'age', str(age))  # Convertendo para string
    row.set_cell(column_family_id, 'data', data)
    row.commit()

print("100 registros aleatórios adicionados com sucesso.")

from google.cloud import bigtable
from datetime import datetime, timedelta