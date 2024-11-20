import google.auth
from googleapiclient.discovery import build
import json

# Configuração da autenticação e cliente Compute Engine
credentials, project = google.auth.default()

# Verificando se o projeto foi obtido corretamente
if not project:
    print("Erro: Nenhum projeto foi identificado. Verifique as credenciais e autenticação.")
    project = "seu-projeto-id"  # Substitua pelo seu ID de projeto
    print(f"Usando o projeto manualmente: {project}")

compute_service = build('compute', 'v1', credentials=credentials)

# Função para listar as instâncias de máquina virtual
def list_instances():
    zone = 'us-central1-a'  # Defina a zona desejada ou use 'global' para todas as zonas
    instances = []
    
    # Listando as instâncias da zona especificada
    result = compute_service.instances().list(project=project, zone=zone).execute()
    
    # Adicionando as instâncias encontradas à lista
    if 'items' in result:
        instances.extend(result['items'])
    
    return instances

# Função para verificar o estado de execução das instâncias
def check_instance_status(instance):
    return instance['status'] == 'RUNNING'

# Função para gerar o relatório com IP público
def generate_report(instances):
    report = []
    for instance in instances:
        instance_name = instance['name']
        zone = instance['zone'].split('/')[-1]  # Extraímos a zona do campo 'zone'
        
        # Verifica se a instância está em execução
        if check_instance_status(instance):
            public_ip = None
            # Buscando o endereço IP público
            for network_interface in instance.get('networkInterfaces', []):
                if 'accessConfigs' in network_interface:
                    for access_config in network_interface['accessConfigs']:
                        if access_config.get('type') == 'ONE_TO_ONE_NAT':
                            public_ip = access_config.get('natIP')
                            break
            
            # Link para acessar a instância no console
            instance_link = f'https://console.cloud.google.com/compute/instancesDetail/zones/{zone}/instances/{instance_name}?project={project}'
            
            report.append({
                'name': instance_name,
                'state': 'RUNNING',
                'zone': zone,
                'public_ip': public_ip if public_ip else 'No Public IP',
                'link': instance_link
            })
    
    return report

# Função principal
def main():
    instances = list_instances()
    report = generate_report(instances)
    
    # Salvando o relatório em um arquivo JSON
    with open('instances_report.json', 'w') as f:
        json.dump(report, f, indent=4)
    
    print("Relatório gerado com sucesso! Verifique o arquivo 'instances_report.json'.")

# Rodando o script
if __name__ == '__main__':
    main()
