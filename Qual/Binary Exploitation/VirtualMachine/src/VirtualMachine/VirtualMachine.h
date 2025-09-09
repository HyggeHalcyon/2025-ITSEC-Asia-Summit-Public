#pragma once
#include "common.h"

#define MAX_STATICS 0x10
#define MAX_DYNAMICS 8
#define MAX_CODE_SIZE 0x200
#define MAGICBYTES "WHEN_YH_SEJAGO_ZAFIRR_LINZ_MSFIR"

enum
{
    R_R0 = 0,   /* 000 */
    R_R1,       /* 001 */
    R_R2,       /* 010 */
    R_R3,       /* 011 */
    R_R4,       /* 100 */
    R_R5,       /* 101 */
    R_R6,       /* 110 */
    R_R7,       /* 111 */
    R_PC,
    R_COND,
    R_COUNT
};

enum
{
    OP_ADD = 0, /* add 0000 */
    OP_DEC,     /* dec 0001 */
    OP_LD,      /* load 0010 */
    OP_ST,      /* store 0011 */
    OP_PUTS,    /* trap 0100 */
    OP_JMP,     /* jmp 0101 */
    OP_SET,     /* set 0110 */
    OP_CMPE,    /* cmp equal 0111 */
    OP_CMPNE,   /* cmp not equal 1000 */
    OP_CMPL,    /* cmp less than 1001 */
    OP_CMPG,    /* cmp greater than 1010 */
    OP_ALLOC,   /* allocate 1011 */
    OP_RET,     /* return 1100 */
	OP_GETC,    /* get character 1101 */
};

typedef struct DynamicMem {
    ULONGLONG Size;
    CHAR Data;
} DynamicMem;

typedef struct DynamicPool {
    DynamicMem* allocations[MAX_DYNAMICS];
} DynamicPool;

typedef struct Memory {
    DynamicPool* dynamics;
    PCHAR statics;
} Memory;

class VirtualMachine {
private:
    ULONGLONG reg[R_COUNT] = {};
    Memory* memory = NULL;
    PULONG code = NULL;

    VOID Add();
    VOID Dec();
    VOID Load();
    VOID Store();
    VOID Puts();
    VOID Getc();
    VOID Jump();
    VOID Set();
    VOID Cmp_Equal();
    VOID Cmp_Not_Equal();
    VOID Cmp_Less();
    VOID Cmp_Greater();
    VOID Allocate();
public:
    VirtualMachine(PCHAR, size_t);
    VOID Execute();
    VOID CleanUp();
    PVOID operator new(size_t);
    VOID operator delete(void*);
};
