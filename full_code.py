import os
from paramiko import SSHClient, AutoAddPolicy, RSAKey


def copy_from_ec2_to_s3():
    """
    copy mlruns directory from ec2 to s3 bucket
    """

    # Connect to EC2 instance
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    private_key = RSAKey(filename=os.environ['ec2_private_key_path'])
    stdout = []

    try:
        # connect
        ssh.connect(os.environ['ec2_instance_ip'], username=os.environ['ec2_username'], pkey=private_key)
        # run linux command - copy mlruns directory from ec2 to s3
        copy_command = "aws s3 sync {} s3://{}/{}".format(os.environ['ec2_path'],
                                                          os.environ['s3_name'],
                                                          os.environ['s3_path'])
        # get output
        _, stdout, _ = ssh.exec_command(copy_command)
        stdout = stdout.read().decode().split("\n")

    finally:
        ssh.close()

    return stdout


def lambda_handler(event, context):
    copy_output = copy_from_ec2_to_s3()
    return {"copy_output": copy_output}
