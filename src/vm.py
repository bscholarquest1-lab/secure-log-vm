import struct
import os

# --- Virtual Registers Layout ---
R_R0, R_R1, R_R2, R_R3, R_R4, R_R5, R_R6, R_R7 = range(8)
R_PC = 8    # Program Counter
R_COND = 9  # Condition Flags
R_COUNT = 10

# --- Condition Flag Signatures ---
FL_POS = 1 << 0
FL_ZRO = 1 << 1
FL_NEG = 1 << 2

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

# Initialize CPU state and 65,536 words of Virtual RAM
memory = [0] * (1 << 16)
reg = [0] * R_COUNT

def sign_extend(x, bit_count):
    if (x >> (bit_count - 1)) & 1:
        x |= (0xFFFF << bit_count)
    return x & 0xFFFF

def update_flags(r):
    if reg[r] == 0:
        reg[R_COND] = FL_ZRO
    elif reg[r] & 0x8000: # Check sign bit
        reg[R_COND] = FL_NEG
    else:
        reg[R_COND] = FL_POS

def load_binary_payload(filepath):
    if not os.path.exists(filepath):
        print(f"Error: Payload file '{filepath}' not found.")
        return False
    
    with open(filepath, "rb") as f:
        # Read the 16-bit origin loading address (0x3000)
        origin_bytes = f.read(2)
        if not origin_bytes: return False
        origin = struct.unpack(">H", origin_bytes)[0]
        
        # Load the remaining data words into memory array cells
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
        
    reg[R_PC] = 0x3000 # Set execution entry target
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
            # Indirect pointer read logic to extract text logs safely
            target_addr = memory[(reg[R_PC] + pc_offset) & 0xFFFF]
            
            # Print the extracted threat payload characters using Memory-Mapped tracking!
            print("[VM Sandbox Analysis - Extracting Threat Signature]: ", end="")
            while memory[target_addr] != 0:
                print(chr(memory[target_addr] & 0xFF), end="")
                target_addr += 1
            print() # Newline
            
        elif op == OP_HALT:
            print("--- HALT INSTRUCTION REACHED. SANDBOX ISOLATION COMPLETE. ---\n")
            running = False
            
        else:
            # Fallback handler for unmapped basic instructions
            pass

if __name__ == "__main__":
    PAYLOAD = "programs/sandbox_payload.bin"
    run_vm(PAYLOAD)
