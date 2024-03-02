import boto3


def list_security_groups(ec2):
    security_groups = ec2.describe_security_groups()
    return {sg['GroupId']: sg['GroupName'] for sg in
            security_groups['SecurityGroups']}


def list_instances_security_groups(ec2):
    instances = ec2.describe_instances()
    sg_set = set()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            for sg in instance['SecurityGroups']:
                sg_set.add(sg['GroupId'])
    return sg_set


def list_network_interfaces_security_groups(ec2):
    network_interfaces = ec2.describe_network_interfaces()
    sg_set = set()
    for ni in network_interfaces['NetworkInterfaces']:
        for sg in ni['Groups']:
            sg_set.add(sg['GroupId'])
    return sg_set


def find_unused_security_groups(ec2):
    all_sgs = list_security_groups(ec2)
    used_sgs = list_instances_security_groups(ec2).union(
        list_network_interfaces_security_groups(ec2))
    unused_sgs = {sg_id: all_sgs[sg_id] for sg_id in set(all_sgs) - used_sgs}
    return unused_sgs


def main():
    ec2 = boto3.client('ec2')
    unused_sgs = find_unused_security_groups(ec2)
    if unused_sgs:
        print("Unused Security Groups:")
        print("Security Group ID    | Security Group Name")
        print("-------------------- |-------------------------")
        for sg_id, sg_name in unused_sgs.items():
            print(f"{sg_id} | {sg_name}")
    else:
        print("No unused security groups found.")


if __name__ == '__main__':
    main()
