from datetime import datetime, timedelta
from google.cloud import bigtable

# Configuração do Bigtable
client = bigtable.Client(project='playground-s-11-fedf5ed1', admin=True)
instance = client.instance('instace-test')
table = instance.table('table_test')

# Definir a família de colunas
column_family_id = 'name'
column_qualifier = 'data'  # Nome da coluna com a data

# Definir a data de corte (dois anos atrás)
cutoff_date = datetime.now().replace(tzinfo=None) - timedelta(days=730)

# Lê todas as linhas da tabela
rows = table.read_rows()
rows.consume_all()

# Iterar sobre cada linha e verificar se deve ser removida
for row_key, row in rows.rows.items():
    print(f"Processando linha com chave: {row_key}")
    
    # Verificar a estrutura de colunas e encontrar a coluna 'data'
    data_found = False
    for family, columns in row.cells.items():
        for qualifier, cells in columns.items():
            for cell in cells:
                cell_value = cell.value.decode('utf-8') if isinstance(cell.value, bytes) else cell.value
                if qualifier == column_qualifier.encode('utf-8'):  # Usar encode para correspondência exata
                    data_found = True
                    row_date = datetime.fromisoformat(cell_value)
                    print(f"  Verificando data: {row_date} para a linha {row_key}")
                    # Comparar a data da linha com a data de corte
                    if row_date < cutoff_date:
                        print(f"Marcando linha para remoção: {row_key}, data: {row_date}")
                        direct_row = table.direct_row(row_key)
                        if direct_row:  # Verificar se direct_row não é None
                            try:
                                direct_row.delete()
                                table.mutate_rows([direct_row])
                                print(f"Linha {row_key} removida com sucesso.")
                            except Exception as e:
                                print(f"Erro ao remover a linha {row_key}: {e}")
    
    if not data_found:
        print(f"Linha com chave: {row_key} não possui coluna de data ou está com nome incorreto.")

print("Processo de verificação e remoção concluído.")
