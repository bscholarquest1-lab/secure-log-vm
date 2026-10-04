#  Isolated Security Log Analysis Virtual Machine Sandbox

An advanced, end-to-end cybersecurity analytics platform featuring a custom-built **16-bit application Virtual Machine (VM)** integrated with an automated **Security Log Parser**. This repository simulates a secure hardware enclave/co-processor architecture, isolating and checking indicators of compromise (IoCs) entirely within a sandboxed runtime environment.

##  System Architecture & Workflow
1. **Ingestion & Parsing (`log_parser.py`):** Scans raw server logs (`server_access.log`) for critical events like failed password attacks or unauthorized database access attempts.
2. **Bytecode Compilation:** The parser extracts offending threat metrics and acts as an assembler, converting human-readable string signatures into an architectural 16-bit binary payload (`programs/sandbox_payload.bin`).
3. **Sandboxed Execution Simulator (`vm.py`):** A custom simulated CPU with virtual registers (`R0-R7`, `PC`, `COND`), memory arrays, and a Fetch-Decode-Execute clock loop boots up, mounts the binary payload, and securely extracts the threat data string using indirect memory pointer indexing without exposing the host OS stack.

##  Technical Specs
* **Word Size:** 16-bit architecture simulation
* **Virtual Address Space:** 65,536 word-addressable cells (Simulated RAM Layout)
* **Registers:** 8 General Purpose Registers, 1 Program Counter (`PC`), 1 Status Flag tracking register (`COND`)
* **Custom ISA Opcodes:** Support for basic structural instruction signals including `LDI` (Load Immediate), `LD` (Load Indirect string streams), and `HALT`.

##  Execution & Verification
To execute the log parsing pipeline and verify sandboxed virtual isolation, run the core tools sequentially:

```bash
# Step 1: Process logs and inject threat data into the architecture matrix
python log_parser.py

# Step 2: Boot up the virtual CPU sandbox to isolate and display threat payloads
python vm.py
```

###  Sandbox Execution Output Logs
```text
---  VIRTUAL MACHINE SECURITY SANDBOX LAUNCHED ---
[VM Sandbox Analysis - Extracting Threat Signature]: 203.0.113.5, 198.51.100.44, 198.51.100.12
--- HALT INSTRUCTION REACHED. SANDBOX ISOLATION COMPLETE. ---
```

##  Core Engineering Challenges Solved
* **Memory Pointers & Mapping:** Handled string conversions to architectural ASCII numeric arrays wrapped with structural hardware metadata instructions.
* **Instruction Set Architecture (ISA) Validation:** Developed a functional Fetch-Decode-Execute cycle loop capable of navigating virtual memory cell indices smoothly without structural overflows.

