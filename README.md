Backup and Validation of network device configurations. <br/>
Using Netmiko, it connects to network devices via SSH, retrieves the running configurations, and saves them with timestamped filenames. The tool also validates device configurations by running predefined commands like show ip route and show vlan brief. <br/>

**Key Features:**
Automated backup of network device configurations.
Timestamped backup filenames.
Validation with predefined commands.
Error handling for connection and authentication issues.
Supports multiple devices via YAML inventory.
