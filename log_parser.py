import os
import datetime
import struct

def export_to_vm_sandbox(suspicious_string, output_filename="programs/sandbox_payload.bin"):
    """
    Takes an alert string/IP, wraps it with custom VM instructions, 
    and writes out a binary image file that the C Virtual Machine can execute.
    """
    vm_instructions = [
        0xA202, # LDI R1, Offset 2 -> Looks up memory location for data start (0x3005)
        0x2201, # LD  R0, R1       -> Loads the first character into Register 0
        0xF000, # HALT             -> Stops the engine loop safely
        0x3005  # Custom Hardcoded Pointer: Address where the log text string starts
    ]
    
    log_data_words = [ord(char) for char in suspicious_string]
    log_data_words.append(0) # Null terminator
    
    full_image_payload = vm_instructions + log_data_words
    
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    with open(output_filename, "wb") as f:
        f.write(struct.pack(">H", 0x3000)) # Starting origin address
        for word in full_image_payload:
            f.write(struct.pack(">H", word))
            
    print(f"[🛡️ VM Bridge]: Injected payload data into '{output_filename}' ({len(log_data_words)} bytes).")

def parse_log_file(input_file, output_report):
    if not os.path.exists(input_file):
        print(f"[ERROR] Target log file '{input_file}' not found.")
        return

    print(f"[*] Processing security metrics from {input_file}...")
    
    failed_attempts = 0
    suspicious_ips = set()
    alert_lines = []

    with open(input_file, 'r') as file:
        for line in file:
            if "Invalid password attempt" in line or "unauthorized access" in line:
                failed_attempts += 1
                ip_address = line.strip().split()[-1]
                suspicious_ips.add(ip_address)
                alert_lines.append(f"[ALERT] {line.strip()}")

    if suspicious_ips:
        threat_payload = ", ".join(list(suspicious_ips))
        export_to_vm_sandbox(threat_payload)

    with open(output_report, 'w') as report:
        report.write(f"==================================================\n")
        report.write(f"AUTOMATED INCIDENT RESPONSE REPORT - {datetime.date.today()}\n")
        report.write(f"==================================================\n\n")
        report.write(f"[+] Total Malicious Events Flagged: {failed_attempts}\n")
        report.write(f"[+] Unique Offending IP Addresses Isolated: {list(suspicious_ips)}\n\n")
        report.write(f"--- DETAILED INCIDENT LOG ---\n")
        for alert in alert_lines:
            report.write(f"{alert}\n")
            
    print(f"[SUCCESS] Analysis complete. Security report generated: '{output_report}'")

if __name__ == "__main__":
    LOG_FILE = "server_access.log"
    REPORT_FILE = "security_report.txt"
    parse_log_file(LOG_FILE, REPORT_FILE)



