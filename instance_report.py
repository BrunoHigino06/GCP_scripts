import google.auth
from googleapiclient.discovery import build
import json

# List of projects (you can add or modify your project IDs here)
projects = ['your-project-id-1', 'your-project-id-2']  # Replace with your project IDs

# List of zones in North America and Europe
zones = [
    'us-central1-a', 'us-west1-b', 'us-east1-c', 'us-east4-a',  # North America
    'europe-west1-b', 'europe-west2-c', 'europe-west3-d', 'europe-west4-a', 'europe-west6-a'  # Europe
]

# Function to list instances
def list_instances(project, zone):
    compute_service = build('compute', 'v1', credentials=credentials)
    
    # Fetching instances in the zone
    result = compute_service.instances().list(project=project, zone=zone).execute()
    
    instances = result.get('items', [])
    return instances

# Function to check the status of instances
def check_instance_status(instance_name, zone):
    compute_service = build('compute', 'v1', credentials=credentials)
    project_id = project
    
    # Check the status of the instance
    instance = compute_service.instances().get(project=project_id, zone=zone, instance=instance_name).execute()
    return instance['status'] == 'RUNNING'

# Function to generate the report
def generate_report(instances):
    report = []
    for instance in instances:
        instance_name = instance['name']
        zone = instance['zone'].split('/')[-1]  # Extract the zone from the 'zone' field
        
        # Check if the instance is running
        if check_instance_status(instance_name, zone):
            public_ip = None
            # Fetch the public IP address
            for network_interface in instance.get('networkInterfaces', []):
                if 'accessConfigs' in network_interface:
                    for access_config in network_interface['accessConfigs']:
                        if access_config.get('type') == 'ONE_TO_ONE_NAT':
                            public_ip = access_config.get('natIP')
                            break
            
            # Link to access the instance in the console
            instance_link = f'https://console.cloud.google.com/compute/instancesDetail/zones/{zone}/instances/{instance_name}?project={project}'
            
            report.append({
                'name': instance_name,
                'state': 'RUNNING',
                'zone': zone,
                'public_ip': public_ip if public_ip else 'No Public IP',
                'link': instance_link
            })
    
    return report

# Main function
def main():
    # Iterate over the projects and zones
    for project in projects:
        for zone in zones:
            print(f"Fetching instances in project {project} in zone {zone}...")
            instances = list_instances(project, zone)
            report = generate_report(instances)
            
            # Saving the report to a JSON file
            with open(f'instances_report_{project}_{zone}.json', 'w') as f:
                json.dump(report, f, indent=4)
            
            print(f"Report generated successfully for {project} in zone {zone}! Check the file 'instances_report_{project}_{zone}.json'.")

# Authentication setup and Compute client
credentials, project = google.auth.default()
 
# Run the script
if __name__ == '__main__':
    main()
