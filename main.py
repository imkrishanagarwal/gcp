from google.auth import compute_engine
from googleapiclient import discovery

def delete_all_vms(request):
    try:
        # Authenticate with Google Cloud Platform
        auth_client = compute_engine.Credentials()

        # Initialize Compute Engine API
        compute = discovery.build('compute', 'v1', credentials=auth_client)

        # Retrieve a list of all regions
        regions = compute.regions().list(project='training121-417909').execute()

        # Iterate over each region
        for region in regions['items']:
            region_name = region['name']

            # Retrieve a list of VM instances in the current region
            zone = region['zones'][0].split('/')[-1]  # Extracting zone name from URL
            vms = compute.instances().list(project='training121-417909', zone=zone).execute()

            # Iterate over each VM instance and delete it
            if 'items' in vms:
                for vm in vms['items']:
                    vm_name = vm['name']

                    # Delete the VM instance
                    compute.instances().delete(project='training121-417909', zone=zone, instance=vm_name).execute()

                    print(f"Deleted VM instance {vm_name} in region {region_name}")

        return 'All VM instances deleted successfully', 200
    except Exception as e:
        print('Error deleting VM instances:', e)
        return 'Error deleting VM instances', 500