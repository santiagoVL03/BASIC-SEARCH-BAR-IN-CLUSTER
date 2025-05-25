import os
import sys
import Utils.functions as utils
import paramiko
import asyncio
async def create_ssh_session(host, user, password):
    """
    Create an SSH session to a remote host.
    
    Parameters:
    - host: The hostname or IP address of the remote host.
    - user: The username for SSH authentication.
    - password: The password for SSH authentication.
    
    Returns:
    - ssh_client: An SSH client object connected to the remote host.
    """
    
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh_client.connect(hostname=host, username=user, password=password)
        print(f"Connected to {host} as {user}")
        return ssh_client
    except Exception as e:
        print(f"Failed to connect to {host}: {e}")
        sys.exit(1)
    finally:
        print(f"SSH session to {host} closed.")
        ssh_client.close()
    
async def execute_object_detection_to_hdfs(config_nodes):
    """
    Execute the object detection script on the remote host and upload results to HDFS.
    
    This function creates SSH sessions to the master and worker nodes, executes the object detection script,
    and uploads the results to HDFS.
    """
    
    # Define the SSH credentials
    user = "hduser"
    password = "kali"
    master = config_nodes.split(":")[0]
    worker1 = config_nodes.split(":")[1]
    worker2 = config_nodes.split(":")[2]
    worker3 = config_nodes.split(":")[3]
    
    # Create SSH sessions
    master_ssh = await create_ssh_session(master, user, password)
    worker1_ssh = await create_ssh_session(worker1, user, password)
    worker2_ssh = await create_ssh_session(worker2, user, password)
    worker3_ssh = await create_ssh_session(worker3, user, password)
    
    # Execute the object detection script on each node
    command = "python3 -m Src.join_object_detection"
    master_ssh.exec_command(command)
    worker1_ssh.exec_command(command)
    worker2_ssh.exec_command(command)
    worker3_ssh.exec_command(command)
    print("Object detection script executed on all nodes and submitted results to hdfs.")
    
if __name__ == "__main__":
    # Example usage
    
    with open("node_name.txt") as config_file:
        config = config_file.read().strip()
    
    asyncio.run(execute_object_detection_to_hdfs(config))
    