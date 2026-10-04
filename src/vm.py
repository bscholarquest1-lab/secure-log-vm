import struct
import os

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

# 🛑 SIMULATED THREAT INTELLIGENCE FEED (Known Malicious IP Blocklist)
KNOWN_MALICIOUS_IPS = {
    "203.0.113.5": "Threat Group Alpha - Active SSH Brute-Forcing Campaign",
    "198.51.100.12": "State-Sponsored Actor - Critical Database Injection Target",
    "185.220.101.4": "Known Tor Exit Node - Automated Vulnerability Scanner"
}

# Initialize CPU state and 65,536 words of Virtual RAM
memory = [0] * (1 << 16)
reg = [0] * R_COUNT

def sign_extend(x, bit_count):
    if (x >> (bit_count - 1)) & 1:
        x |= (0xFFFF << bit_count)
    return x & 0xFFFF

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
            
            # Extract characters from the isolated memory array
            extracted_chars = []
            while memory[target_addr] != 0:
                extracted_chars.append(chr(memory[target_addr] & 0xFF))
                target_addr += 1
            
            full_payload_string = "".join(extracted_chars)
            print(f"[VM Sandbox Analysis - Extracted Raw Stream]: {full_payload_string}")
            
            # 🔍 BROADCAST MATCH CHECK: Split and cross-reference against Threat Intel database
            individual_ips = [ip.strip() for ip in full_payload_string.split(",")]
            
            print("\n🔍 --- RUNNING AUTOMATED THREAT BLOCKLIST INTEGRITY SCANS ---")
            for ip in individual_ips:
                if ip in KNOWN_MALICIOUS_IPS:
                    print(f"🚨 [ALERT - MATCH FOUND]: IP {ip} matched threat signature base!")
                    print(f"   ⚠️  Intelligence Context: {KNOWN_MALICIOUS_IPS[ip]}")
                else:
                    print(f"✅ [CLEAN]: IP {ip} passed blocklist database signature scan.")
            print("-------------------------------------------------------------\n")
            
        elif op == OP_HALT:
            print("--- HALT INSTRUCTION REACHED. SANDBOX ISOLATION COMPLETE. ---\n")
            running = False
            
        else:
            pass

if __name__ == "__main__":
    PAYLOAD = "programs/sandbox_payload.bin"
    run_vm(PAYLOAD)
