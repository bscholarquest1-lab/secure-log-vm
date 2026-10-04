#ifndef HARDWARE_H
#define HARDWARE_H

#include <stdint.h>

/* --- Virtual Registers --- */
enum {
    R_R0 = 0,
    R_R1,
    R_R2,
    R_R3,
    R_R4,
    R_R5,
    R_R6,
    R_R7,
    R_PC,   // Program Counter: tracks the next instruction address
    R_COND, // Condition Flag: tracks positive, zero, or negative outcomes
    R_COUNT
};

/* --- Condition Flag Signatures --- */
enum {
    FL_POS = 1 << 0, // Positive result sign
    FL_ZRO = 1 << 1, // Zero result sign
    FL_NEG = 1 << 2  // Negative result sign
};

/* --- Virtual Machine Opcodes (Our Custom ISA) --- */
enum {
    OP_BR = 0, // 0000: Branch (Conditional Jump)
    OP_ADD,    // 0001: Add two registers
    OP_LD,     // 0010: Load data directly from memory
    OP_ST,     // 0011: Store register data to memory
    OP_JSR,    // 0100: Jump to subroutine
    OP_AND,    // 0101: Bitwise AND math
    OP_LDR,    // 0110: Load Base + Offset
    OP_STR,    // 0111: Store Base + Offset
    OP_NOT,    // 1001: Bitwise NOT logic inversion
    OP_LDI,    // 1010: Load Indirect (Load string array pointers)
    OP_JMP,    // 1100: Absolute jump to address
    OP_HALT = 0xF // 1111: Terminate sandbox loop
};

#endif
