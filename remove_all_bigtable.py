from google.cloud import bigtable
from datetime import datetime

client = bigtable.Client(project='ewx-innax-staging', admin=True)
instance = client.instance('ewx-eu-bigtable')
table = instance.table('enrx_org_011')


# Ler todos os registros da tabela
rows = table.read_rows()
rows.consume_all()  # Consumir todas as linhas para processar

# Iterar sobre cada linha e excluir
mutations = []
for row_key, _ in rows.rows.items():
    row = table.row(row_key)  # Criar um objeto Row para o row_key
    row.delete()              # Adicionar a operação de exclusão
    mutations.append(row)

# Executar a exclusão em lote
table.mutate_rows(mutations)

print("Todos os registros removidos com sucesso.")
