# 🏛️ System Architecture & Data Flow Layout

This design spec details how data is parsed, assembled, packaged, and isolated across the security pipeline.

## 🔄 End-to-End Data Lifecycle

```text
[ server_access.log ]
          │
          ▼
┌────────────────────────────────────────────────────────┐
│ 1. Log Ingestion & Threat Detection (log_parser.py)    │
│    - Regex checks lines for "Invalid password"         │
│    - Extracts malicious host IP telemetry variables    │
└────────────────────────────────────────────────────────┘
          │
          ▼  (Passes string: "203.0.113.5, 198.51.100.12...")
┌────────────────────────────────────────────────────────┐
│ 2. Bytecode Packaging & Telemetry Structuring         │
│    - Packs custom 16-bit operation codes (e.g. OP_LDI) │
│    - Encodes string characters into ASCII word maps     │
└────────────────────────────────────────────────────────┘
          │
          ▼  (Writes network byte-ordered byte stream)
[ programs/sandbox_payload.bin ]
          │
          ▼  (Loads binary into index 0x3000)
┌────────────────────────────────────────────────────────┐
│ 3. Isolated Virtual Hardware Simulation (vm.py)       │
│    - Allocation of 65,536 Addressable Memory Words     │
│    - General-Purpose Register Management Loop (R0-R7)   │
└────────────────────────────────────────────────────────┘
          │
          ▼  (Executes Fetch-Decode-Execute Loops)
┌────────────────────────────────────────────────────────┐
│ 4. Threat Intelligence Engine Integration            │
│    - Custom pointer references extract text streams    │
│    - Cross-references tokens with threat database      │
└────────────────────────────────────────────────────────┘
          │
          ▼
 [ Real-Time Security Warning Terminal Alert Displays ]
```

## 💾 Virtual Memory Space Allocation Contract

```text
0x0000 ┌────────────────────────────────────────┐
       │ Reserved System Vectors                │
0x3000 ├────────────────────────────────────────┤
       │ VM Instruction Bytecode Block          │ (Executes sequentially)
0x3005 ├────────────────────────────────────────┤
       │ Extracted Threat Payload Text Buffer   │ (Dynamic ASCII string array)
       │ ...                                    │
0xFFFF └────────────────────────────────────────┘
```
