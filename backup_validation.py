import yaml
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from datetime import datetime
import os


def load_inventory(file="inventory.yaml"):
    with open(file, "r") as inventory_file:
        return yaml.safe_load(inventory_file)

def backups_config(device):
    try:
        net_connect = ConnectHandler(
            ip=device["ip"],
            device_type=["device_type"],
            username=device["username"],
            password=device["password"], 
            port=device.get("port", 22)
        )
        print(f"Connected to {device['ip']}")
        
        config = net_connect.send_command("show running-config")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{device['ip']}_{timestamp}.txt"

        os.makedirs("backups", exist_ok=True)
        with open(f"backups/{filename}", "w") as backup_file:
            backup_file.write(config)

        print(f"backup for {device['ip']} saved as backups/{filename}")

        net_connect.disconnect()

    except NetmikoTimeoutException:
        print(f"Connection timed out to {device['ip']}")
    except NetmikoAuthenticationException:
        print(f"Authentication failed for {device['ip']}")
    except Exception as e:
        print(f"An error occured: {e}")

def validate_config(device, commands):
    try:
        net_connect = ConnectHandler(
            ip=device["ip"],
            device_type=device["device_type"],
            username=device["username"],
            password=device["password"],
            port=device.get("port", 22)
        )
        for command in commands:
            print(f"Validating command: {command}")
            output = net_connect.send_command(command)
            print(output)

        net_connect.disconnect()

    except NetmikoTimeoutException:
        print(f"Connection timed out to {device['ip']}")
    except NetmikoAuthenticationException:
        print(f"Authentication failed for {device['ip']}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    inventory = load_inventory()

    validation_commands = [
        "show ip route",
        "show vlan brief",
        "show running-config"
    ]

    for device in inventory["devices"]:
        print(f"\nProcessing device: {device['ip']}")

        backups_config(device)

        validate_config(device, validation_commands)