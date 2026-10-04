#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "hardware.h"

#define MEMORY_MAX (1 << 16) // 65,536 Addressable Words (Virtual RAM)

uint16_t memory[MEMORY_MAX]; // Our Simulated RAM Array
uint16_t reg[R_COUNT];       // Our Simulated CPU Registers Array

/* --- Helper Function: Sign Extension --- */
uint16_t sign_extend(uint16_t x, int bit_count) {
    if ((x >> (bit_count - 1)) & 1) {
        x |= (0xFFFF << bit_count);
    }
    return x;
}

/* --- Helper Function: Update CPU Flags --- */
void update_flags(uint16_t r) {
    if (reg[r] == 0) {
        reg[R_COND] = FL_ZRO;
    } else if (reg[r] >> 15) { // Check if the highest bit is 1 (negative)
        reg[R_COND] = FL_NEG;
    } else {
        reg[R_COND] = FL_POS;
    }
}

/* --- Function: Load Binary Program File into Virtual Memory --- */
void read_image_file(const char* image_path) {
    FILE* file = fopen(image_path, "rb");
    if (!file) {
        printf("Error: Failed to open compiled program image at: %s\n", image_path);
        exit(1);
    }

    // The first 16 bits of our binary tell us the starting address (Origin)
    uint16_t origin;
    if (fread(&origin, sizeof(origin), 1, file) != 1) return;
    
    // Swap endianness from standard network byte order to host layout
    origin = (origin << 8) | (origin >> 8); 

    uint16_t max_read = MEMORY_MAX - origin;
    uint16_t* p = memory + origin;
    size_t read = fread(p, sizeof(uint16_t), max_read, file);

    // Swap endianness for all the instruction words loaded
    while (read-- > 0) {
        *p = (*p << 8) | (*p >> 8);
        p++;
    }
    fclose(file);
}

/* --- Main VM Clock Cycle Execution Loop --- */
int main(int argc, const char* argv[]) {
    if (argc < 2) {
        printf("Usage: my_vm [compiled_program.bin]\n");
        return 1;
    }

    // Load the input program binary file into virtual memory
    read_image_file(argv[1]);

    // Set Program Counter to typical execution start address (0x3000)
    reg[R_PC] = 0x3000;
    int running = 1;

    printf("--- SECURITY SANDBOX VM STARTED ---\n");

    while (running) {
        /* 1. FETCH */
        uint16_t instr = memory[reg[R_PC]++];
        
        /* 2. DECODE */
        uint16_t op = instr >> 12; // Extract the 4-bit Opcode

        /* 3. EXECUTE */
        switch (op) {
            case OP_ADD: {
                uint16_t r0 = (instr >> 9) & 0x7;       // Destination Register
                uint16_t r1 = (instr >> 6) & 0x7;       // Source Register 1
                uint16_t imm_flag = (instr >> 5) & 0x1; // Immediate mode flag

                if (imm_flag) {
                    uint16_t imm5 = sign_extend(instr & 0x1F, 5);
                    reg[r0] = reg[r1] + imm5;
                } else {
                    uint16_t r2 = instr & 0x7;           // Source Register 2
                    reg[r0] = reg[r1] + reg[r2];
                }
                update_flags(r0);
                break;
            }

            case OP_AND: {
                uint16_t r0 = (instr >> 9) & 0x7;
                uint16_t r1 = (instr >> 6) & 0x7;
                uint16_t imm_flag = (instr >> 5) & 0x1;

                if (imm_flag) {
                    uint16_t imm5 = sign_extend(instr & 0x1F, 5);
                    reg[r0] = reg[r1] & imm5;
                } else {
                    uint16_t r2 = instr & 0x7;
                    reg[r0] = reg[r1] & reg[r2];
                }
                update_flags(r0);
                break;
            }

            case OP_NOT: {
                uint16_t r0 = (instr >> 9) & 0x7;
                uint16_t r1 = (instr >> 6) & 0x7;
                reg[r0] = ~reg[r1]; // Invert bits
                update_flags(r0);
                break;
            }

            case OP_BR: {
                uint16_t pc_offset = sign_extend(instr & 0x1FF, 9);
                uint16_t cond_flag = (instr >> 9) & 0x7;
                
                // Jump if the condition bits match our CPU status flag
                if (cond_flag & reg[R_COND]) {
                    reg[R_PC] += pc_offset;
                }
                break;
            }

            case OP_JMP: {
                uint16_t r1 = (instr >> 6) & 0x7;
                reg[R_PC] = reg[r1]; // Absolute jump to address inside register
                break;
            }

            case OP_LDI: {
                uint16_t r0 = (instr >> 9) & 0x7;
                uint16_t pc_offset = sign_extend(instr & 0x1FF, 9);
                // Indirect load: read pointer location, then get real data string element
                reg[r0] = memory[memory[reg[R_PC] + pc_offset]];
                update_flags(r0);
                break;
            }

            case OP_HALT:
                printf("\n--- HALT ENCOUNTERED. VM SHUTTING DOWN SAFELY. ---\n");
                running = 0;
                break;

            default:
                printf("Error: Unrecognized opcode encountered. Aborting execution.\n");
                running = 0;
                break;
        }
    }
    return 0;
}
