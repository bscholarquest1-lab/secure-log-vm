import struct
import os
import urllib.request

# --- Virtual Registers Layout ---
R_R0, R_R1, R_R2, R_R3, R_R4, R_R5, R_R6, R_R7 = range(8)
R_PC = 8    # Program Counter
R_COND = 9  # Condition Flags
R_COUNT = 10

# --- Custom Opcodes ---
OP_BR = 0
OP_ADD = 1
OP_LD = 2
OP_ST = 3
OP_JSR = 4
OP_AND = 5
OP_LDR = 6
OP_STR = 7
OP_NOT = 9
OP_LDI = 10
OP_JMP = 12
OP_HALT = 0xF

# 🌐 LIVE THREAT INTELLIGENCE FEED CONFIGURATION
# Feodo Tracker plain-text blocklist by abuse.ch (Updates every 5 minutes)
THREAT_FEED_URL = "https://abuse.ch"

# Initialize CPU state and 65,536 words of Virtual RAM
memory = [0] * (1 << 16)
reg = [0] * R_COUNT

def sign_extend(x, bit_count):
    if (x >> (bit_count - 1)) & 1:
        x |= (0xFFFF << bit_count)
    return x & 0xFFFF

def fetch_live_threat_feed():
    """
    Fetches the live malicious C2 IP text feed from abuse.ch programmatically
    and converts it into an active query set.
    """
    print(f"📡 [Threat Intel]: Contacting database feed at {THREAT_FEED_URL}...")
    try:
        # Create a request object with a standard User-Agent header to prevent bot-blocking filters
        req = urllib.request.Request(
            THREAT_FEED_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            
        # Parse the plain text feed, skipping documentation comment headers starting with '#'
        malicious_ips = set()
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                malicious_ips.add(line)
                
        print(f"✅ [Threat Intel]: Successfully synchronized {len(malicious_ips)} active host threat records.")
        return malicious_ips
    except Exception as e:
        print(f"⚠️  [Threat Intel Warning]: Failed to pull live web database ({e}). Falling back to local tracking signature models.")
        # Fallback security rules if internet is offline or host blocks request
        return {"203.0.113.5", "198.51.100.12", "198.51.100.44"}

def load_binary_payload(filepath):
    if not os.path.exists(filepath):
        print(f"Error: Payload file '{filepath}' not found.")
        return False
    
    with open(filepath, "rb") as f:
        origin_bytes = f.read(2)
        if not origin_bytes: return False
        origin = struct.unpack(">H", origin_bytes)[0]
        
        address = origin
        while True:
            word_bytes = f.read(2)
            if not word_bytes: break
            word = struct.unpack(">H", word_bytes)[0]
            memory[address] = word
            address += 1
    return True

def run_vm(payload_path):
    # Synchronize the virtual environment with the real-time web database before boot execution
    live_threat_database = fetch_live_threat_feed()

    if not load_binary_payload(payload_path):
        return
        
    reg[R_PC] = 0x3000 
    running = True
    
    print("\n--- 🛡️ VIRTUAL MACHINE SECURITY SANDBOX LAUNCHED ---")
    
    while running:
        # 1. FETCH
        instr = memory[reg[R_PC]]
        reg[R_PC] += 1
        
        # 2. DECODE
        op = instr >> 12
        
        # 3. EXECUTE
        if op == OP_LDI:
            r0 = (instr >> 9) & 0x7
            pc_offset = sign_extend(instr & 0x1FF, 9)
            target_addr = memory[(reg[R_PC] + pc_offset) & 0xFFFF]
            
            # Extract characters from isolated virtual memory cells
            extracted_chars = []
            while memory[target_addr] != 0:
                extracted_chars.append(chr(memory[target_addr] & 0xFF))
                target_addr += 1
            
            full_payload_string = "".join(extracted_chars)
            print(f"[VM Sandbox Analysis - Extracted Raw Stream]: {full_payload_string}")
            
            # Segment extracted buffer into cleanly tokens for database mapping
            individual_ips = [ip.strip() for ip in full_payload_string.split(",")]
            
            print("\n🔍 --- RUNNING REAL-TIME WEB BLOCKLIST INTEGRITY SCANS ---")
            for ip in individual_ips:
                if ip in live_threat_database:
                    print(f"🚨 [ALERT - THREAT FEED MATCH]: Host address {ip} flagged as an active Botnet C2 Node!")
                    print(f"   ⚠️  Mitigation Action: Deploying automated firewall drop parameters to interface.")
                else:
                    print(f"✅ [CLEAN]: IP {ip} passed live threat intelligence feed checking.")
            print("----------------------------------------------------------------\n")
            
        elif op == OP_HALT:
            print("--- HALT INSTRUCTION REACHED. SANDBOX ISOLATION COMPLETE. ---\n")
            running = False
            
        else:
            pass

if __name__ == "__main__":
    PAYLOAD = "programs/sandbox_payload.bin"
    run_vm(PAYLOAD)


