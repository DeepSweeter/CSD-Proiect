import subprocess

PORT = 110568


def scan_ports(ip_range):
    ip_list = []

    try:
        command = f'nmap -p {PORT} {ip_range}'
        output = subprocess.check_output(command, shell=True, universal_newlines=True)

        # Parse output to find open ports
        for line in output.split('\n'):
            if f'{PORT}/tcp' in line and 'open' in line:
                ip_address = line.split()[1]
                ip_list.append(ip_address)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    return ip_list

def testing():
    ip_range = "192.168.1.0/24"

    ip_list = scan_ports(ip_range)
    if ip_list:
        print("IP addresses with port", PORT, "open:")
        for ip in ip_list:
            print(ip)
    else:
        print("No IP addresses found with port", PORT, "open.")
