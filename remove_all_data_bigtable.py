client = bigtable.Client(project='playground-s-11-fedf5ed1', admin=True)
instance = client.instance('instace-test')
table = instance.table('table_test')

# Definir a família de colunas
column_family_id = 'name'  # Substitua pelo ID real da sua família de colunas

# Calcular a data de corte (dois anos atrás)
cutoff_date = datetime.utcnow() - timedelta(days=730)

# Ler todos os registros da tabela
rows = table.read_rows()
rows.consume_all()  # Consumir todas as linhas para processar

# Iterar sobre cada linha
for row_key, row in rows.rows.items():
    # Obter o valor da coluna 'data'
    cell_value = row.cells[column_family_id]['data'][0].value.decode('utf-8')
    
    # Verificar se a data está mais antiga que dois anos
    row_date = datetime.fromisoformat(cell_value)
    if row_date < cutoff_date:
        # Excluir a linha inteira
        table.mutate_rows([row.delete()])

print("Registros antigos removidos com sucesso.")