import boto3
import sys
from vmware.vapi.vmc.client import create_vmc_client
from com.vmware.vapi.std.errors_client import NotFound

# AWS credentials
AWS_ACCESS_KEY = 'your_aws_access_key'
AWS_SECRET_KEY = 'your_aws_secret_key'
AWS_REGION = 'your_aws_region'

# VMC credentials
REFRESH_TOKEN = 'your_vmc_refresh_token'
ORG_ID = 'your_org_id'
SDDC_ID = 'your_sddc_id'

def enumerate_aws_public_ips():
    ec2 = boto3.client('ec2', region_name=AWS_REGION,
                       aws_access_key_id=AWS_ACCESS_KEY,
                       aws_secret_access_key=AWS_SECRET_KEY)
    addresses = ec2.describe_addresses()
    for address in addresses['Addresses']:
        print(f"AWS Public IP: {address['PublicIp']}")

def enumerate_vmc_public_ips():
    try:
        vmc_client = create_vmc_client(REFRESH_TOKEN)
        sddc = vmc_client.orgs.Sddcs.get(ORG_ID, SDDC_ID)
        for public_ip in sddc.resource_config.public_ips:
            print(f"VMC Public IP: {public_ip}")
    except NotFound:
        print("Error: Invalid VMC credentials or SDDC not found")

def main():
    enumerate_aws_public_ips()
    enumerate_vmc_public_ips()

if __name__ == '__main__':
    main()
