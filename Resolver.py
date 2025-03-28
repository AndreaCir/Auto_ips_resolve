import socket
import csv
import logging
from concurrent.futures import ThreadPoolExecutor

#logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#Resolve IP addresses
def resolve_ip(ip):
    try:
        hostname, aliases, _ = socket.gethostbyaddr(ip)
        return ip, hostname, ", ".join(aliases)
    except socket.herror as e:
        logging.error(f"Resolution failed for IP {ip}: {e}")
        return ip, "Resolution Failed", "N/A"

# Read IPs from CSV
def read_ips_from_csv(input_file):
    ip_list = []
    with open(input_file, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Assicurati che la riga non sia vuota
                ip_list.append(row[0])
    return ip_list

#output
def write_results_to_csv(output_file, results):
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IP Address", "Hostname", "Aliases"])
        writer.writerows(results)

def main(input_file, output_file):
    ip_list = read_ips_from_csv(input_file)
    results = []

    # Use ThreadPoolExecutor for concurrent resolution
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(resolve_ip, ip_list))

    write_results_to_csv(output_file, results)
    logging.info(f"Results saved to {output_file}")

if __name__ == "__main__":
    input_file = "ip_list.csv"
    output_file = "ip_resolution.csv"
    main(input_file, output_file)
