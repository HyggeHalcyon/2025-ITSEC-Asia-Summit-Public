#include "VirtualMachine.h"
#include "common.h"

VirtualMachine::VirtualMachine(PCHAR CodeBuffer, size_t CodeSize)
{
	if (strncmp(CodeBuffer, MAGICBYTES, sizeof(MAGICBYTES) - 1) != 0)
	{
		Panic("Invalid Magic Bytes");
	}

	this->memory = (Memory*)HeapAlloc(hHeap, HEAP_ZERO_MEMORY, sizeof(Memory));
	this->memory->statics = (PCHAR)HeapAlloc(hHeap, HEAP_ZERO_MEMORY, MAX_STATICS);
	this->memory->dynamics = (DynamicPool*)HeapAlloc(hHeap, HEAP_ZERO_MEMORY, MAX_DYNAMICS * sizeof(size_t));
	this->code = (PULONG)HeapAlloc(hHeap, HEAP_ZERO_MEMORY, CodeSize);

	this->reg[R_PC] = (ULONGLONG)this->code;

	CopyMemory(this->code, (CodeBuffer + sizeof(MAGICBYTES) - 1), (CodeSize - sizeof(MAGICBYTES) + 1));
#if defined(_DEBUG)
	//printf("code: %s\n", this->code);
#endif

}

PVOID VirtualMachine::operator new(size_t size)
{
	PVOID ptr = HeapAlloc(hHeap, HEAP_ZERO_MEMORY, size);
	if (ptr == NULL)
	{
		Panic("Memory allocation failed");
	}
	return ptr;
}

VOID VirtualMachine::operator delete(void* ptr)
{
	if (ptr != NULL)
	{
		HeapFree(hHeap, NULL, ptr);
	}
}

VOID VirtualMachine::Execute()
{
	while (TRUE)
	{
		WORD instr = *((WORD*)this->reg[R_PC]);
#if defined(_DEBUG)
		printf("instr: %#x\n", instr);
#endif
		switch (instr & 0b1111)
		{
		case OP_ADD:
#if defined(_DEBUG)
			printf("[+] Executing ADD\n");
#endif
			this->Add();
			break;
		case OP_DEC:
#if defined(_DEBUG)
			printf("[+] Executing DEC\n");
#endif
			this->Dec();
			break;
		case OP_LD:
#if defined(_DEBUG)
			printf("[+] Executing LOAD\n");
#endif
			this->Load();
			break;
		case OP_ST:
#if defined(_DEBUG)
			printf("[+] Executing STORE\n");
#endif
			this->Store();
			break;
		case OP_PUTS:
#if defined(_DEBUG)
			printf("[+] Executing PUTS\n");
#endif
			this->Puts();
			break;
		case OP_JMP:
			this->Jump();
			continue;
			break;
		case OP_SET:
#if defined(_DEBUG)
			printf("[+] Executing SET\n");
#endif
			this->Set();
			break;
		case OP_CMPE:
			this->Cmp_Equal();
			break;
		case OP_CMPNE:
			this->Cmp_Not_Equal();
			break;
		case OP_CMPL:
			this->Cmp_Less();
			break;
		case OP_CMPG:
			this->Cmp_Greater();
			break;
		case OP_ALLOC:
#if defined(_DEBUG)
			printf("[+] Executing ALLOCATE\n");
#endif
			this->Allocate();
			break;
		case OP_GETC:
#if defined(_DEBUG)
			printf("[+] Executing GETC\n");
#endif
			this->Getc();
			break;
		case OP_RET:
#if defined(_DEBUG)
			printf("[+] Executing RETURN\n");
#endif
			return;
			break;
		default:
			BYTE opcode = (instr >> 4) & 0xF;
			printf("[-] opcode=%d%d%d%d\n",
				(opcode >> 3) & 1,
				(opcode >> 2) & 1,
				(opcode >> 1) & 1,
				opcode & 1);
			Panic("Unknown Instruction");
			break;
		}

		this->reg[R_PC] += 0x2;

		if ((*(WORD*)this->reg[R_PC] & 0b1111) == NULL)
		{
			return;
		}
	}
}

/*
	4 bit opcode
	3 bit destination register 
	3 bit source register 
	1 bit immediate flag
	5 bit immediate literal
	| 4 | 3 | 3 | 1 | 5 |
*/
VOID VirtualMachine::Add()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	WORD r_dest = (instr >> 4) & 0b111;
	WORD r_src = (instr >> 7) & 0b111;
	BYTE imm_flag = (instr >> 10) & 0b1;
	ULONG literal = (instr >> 11);

	if (imm_flag)
	{
		this->reg[r_dest] += literal;
	}
	else 
	{
		this->reg[r_dest] += this->reg[r_src];
	}
}

/*
	4 bit opcode
	3 bit destination register
	3 bit source register
	1 bit immediate flag
	5 bit immediate literal
	| 4 | 3 | 3 | 1 | 5 |
*/
VOID VirtualMachine::Dec()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	WORD r_dest = (instr >> 4) & 0b111;
	WORD r_src = (instr >> 7) & 0b111;
	BYTE imm_flag = (instr >> 10) & 0b1;
	ULONG literal = (instr >> 11);

	if (imm_flag)
	{
		this->reg[r_dest] -= literal;
	}
	else
	{
		this->reg[r_dest] -= this->reg[r_src];
	}
}

/*
	4 bit opcode
	3 bit destination register
	5 bit offset literal
	1 bit flag
	3 bit index
	| 4 | 3 | 5 | 1 | 3 | 
*/
// CHECK FOR OOB (CHECKED)
VOID VirtualMachine::Load()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	WORD r_dest = (instr >> 4) & 0b111;
	ULONG offset = (instr >> 7) & 0b11111;
	BYTE flag = (instr >> 12) & 0b1;
	WORD index = (instr >> 13) & 0b111;

	if (flag)
	{
		if (this->memory->dynamics->allocations[index] == NULL)
		{
			Panic("NULL POINTER");
		}

		if (index > MAX_DYNAMICS)
		{
			Panic("OUT OF BOUNDS");
		}

		// VULN: no offset check hehe :^)

		this->reg[r_dest] = *(PULONGLONG)(((PCHAR)&this->memory->dynamics->allocations[index]->Data) + offset);
	}
	else
	{
		if (offset > MAX_STATICS)
		{
			Panic("OUT OF BOUNDS");
		}
		this->reg[r_dest] = *(this->memory->statics + offset);
	}
}

/*
	4 bit opcode
	3 bit source register
	5 bit offset literal
	1 bit flag
	3 bit index
	| 4 | 3 | 5 | 1 | 3 |
*/
// CHECK FOR OOB (CHECKED)
VOID VirtualMachine::Store()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	WORD r_dest = (instr >> 4) & 0b111;
	ULONG offset = (instr >> 7) & 0b11111;
	BYTE flag = (instr >> 12) & 0b1;
	WORD index = (instr >> 13) & 0b111;

	if (flag)
	{
		if (this->memory->dynamics->allocations[index] == NULL)
		{
			Panic("NULL POINTER");
		}

		if (index > MAX_DYNAMICS)
		{
			Panic("OUT OF BOUNDS");
		}

		if (offset > this->memory->dynamics->allocations[index]->Size)
		{
			Panic("OUT OF BOUNDS");
		}

		*(PULONGLONG)(((PCHAR)&this->memory->dynamics->allocations[index]->Data) + offset) = this->reg[r_dest];
	}
	else
	{
		// VULN: no offset check hehe :^)
		*(PULONGLONG)(this->memory->statics + offset) = this->reg[r_dest];
	}
}

/*
	4 bit opcode 
	5 bit offset literal
	1 bit flag
	3 bit index
	3 bit unused
	| 4 | 5 | 1 | 3 | 3 |
*/
// CHECK FOR OOB (CHECKED)
VOID VirtualMachine::Puts()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	ULONG offset = (instr >> 4) & 0b11111;
	BYTE flag = (instr >> 9) & 0b1;
	WORD index = (instr >> 12) & 0b111;

	if (flag)
	{
		if (this->memory->dynamics->allocations[index] == NULL)
		{
			Panic("NULL POINTER");
		}

		if (index > MAX_DYNAMICS)
		{
			Panic("OUT OF BOUNDS");
		}

		if (offset > this->memory->dynamics->allocations[index]->Size)
		{
			Panic("OUT OF BOUNDS");
		}

		puts(((PCHAR)&this->memory->dynamics->allocations[index]->Data) + offset);
	}
	else
	{
		if (offset > MAX_STATICS)
		{
			Panic("OUT OF BOUNDS");
		}
		puts(this->memory->statics + offset);
	}
}

/*
	4 bit opcode
	1 bit immediate flag
	6 bit offset/index literal
	5 bit unused
	| 4 | 1 | 6 | 5 |
*/ 
// CHECK FOR OOB (CHECKED)
VOID VirtualMachine::Getc()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	BYTE imm_flag = (instr >> 4) & 0b1;
	ULONG offset = (instr >> 5) & 0b111111;

	printf(">> ");
	if (imm_flag)
	{
		if (this->memory->dynamics->allocations[offset] == NULL)
		{
			Panic("NULL POINTER");
		}
		ULONGLONG Size = this->memory->dynamics->allocations[offset]->Size;
		ReadLine((PCHAR)&this->memory->dynamics->allocations[offset]->Data, Size);
	} 
	else
	{
		if (offset > MAX_STATICS)
		{
			Panic("OUT OF BOUNDS");
		}

		CHAR c = getchar();
		this->memory->statics[offset] = (BYTE) c;
	}
}


/*
	4 bit opcode
	6 bit offset literal
	6 bit unused
	| 3 | 6 | 7 |
*/
VOID VirtualMachine::Jump()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	ULONG offset = (instr >> 4) & 0b11111;

	this->reg[R_PC] += offset;
}

/*
	4 bit opcode
	3 bit destination register
	5 bit offset literal
	4 bit unused
	| 4 | 3 | 5 | 4 |
*/
VOID VirtualMachine::Set()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	WORD r_dest = (instr >> 4) & 0b111;
	ULONG literal = (instr >> 7) & 0b111111;

	this->reg[r_dest] = literal;
}

/*
	3 bit opcode
	3 bit register 1
	3 bit register 2
	1 bit immediate flag
	6 bit immediate literal
	| 4 | 3 | 3 | 1 | 5 |
*/
VOID VirtualMachine::Cmp_Equal()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	WORD r1 = (instr >> 4) & 0b111;
	WORD r2 = (instr >> 7) & 0b111;
	BYTE imm_flag = (instr >> 10) & 0b1;
	ULONG literal = (instr >> 11);

	this->reg[R_COND] = 0x0;
	if (imm_flag)
	{
		if (r1 == literal)
		{
			this->reg[R_COND] = 0x1;
		}
	}
	else
	{
		if (r1 == r2)
		{
			this->reg[R_COND] = 0x1;
		}
	}
}

/*
	4 bit opcode
	3 bit register 1
	3 bit register 2
	1 bit immediate flag
	5 bit immediate literal
	| 4 | 3 | 3 | 1 | 5 |
*/
VOID VirtualMachine::Cmp_Not_Equal()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	WORD r1 = (instr >> 4) & 0b111;
	WORD r2 = (instr >> 7) & 0b111;
	BYTE imm_flag = (instr >> 10) & 0b1;
	ULONG literal = (instr >> 11);

	this->reg[R_COND] = 0x0;
	if (imm_flag)
	{
		if (r1 != literal)
		{
			this->reg[R_COND] = 0x1;
		}
	}
	else
	{
		if (r1 != r2)
		{
			this->reg[R_COND] = 0x1;
		}
	}
}

/*
	4 bit opcode
	3 bit register 1
	3 bit register 2
	1 bit immediate flag
	5 bit immediate literal
	| 4 | 3 | 3 | 1 | 5 |
*/
VOID VirtualMachine::Cmp_Less()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	WORD r1 = (instr >> 4) & 0b111;
	WORD r2 = (instr >> 7) & 0b111;
	BYTE imm_flag = (instr >> 10) & 0b1;
	ULONG literal = (instr >> 11);

	this->reg[R_COND] = 0x0;
	if (imm_flag)
	{
		if (r1 < literal)
		{
			this->reg[R_COND] = 0x1;
		}
	}
	else
	{
		if (r1 < r2)
		{
			this->reg[R_COND] = 0x1;
		}
	}
}

/*
	4 bit opcode
	3 bit register 1
	3 bit register 2
	1 bit immediate flag
	5 bit immediate literal
	| 4 | 3 | 3 | 1 | 5 |
*/
VOID VirtualMachine::Cmp_Greater()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	WORD r1 = (instr >> 4) & 0b111;
	WORD r2 = (instr >> 7) & 0b111;
	BYTE imm_flag = (instr >> 10) & 0b1;
	ULONG literal = (instr >> 11);

	this->reg[R_COND] = 0x0;
	if (imm_flag)
	{
		if (r1 > literal)
		{
			this->reg[R_COND] = 0x1;
		}
	}
	else
	{
		if (r1 > r2)
		{
			this->reg[R_COND] = 0x1;
		}
	}
}

/*
	4 bit opcode
	6 bit size
	6 bit index
	| 4 | 6 | 6 | 
*/
VOID VirtualMachine::Allocate()
{
	WORD instr = *((WORD*)this->reg[R_PC]);
	ULONG size = (instr >> 4) & 0b111111;
	ULONG index = (instr >> 10) & 0b111111;

	if (this->memory->dynamics->allocations[index] != NULL)
	{
		hFree(this->memory->dynamics->allocations[index]);
	}

	this->memory->dynamics->allocations[index] = (DynamicMem*)hAlloc(size + sizeof(ULONGLONG));
	this->memory->dynamics->allocations[index]->Size = size;
}

VOID VirtualMachine::CleanUp()
{
	for(WORD i = 0; i < MAX_DYNAMICS; i++)
	{
		if (this->memory->dynamics->allocations[i] != NULL)
		{
			hFree(this->memory->dynamics->allocations[i]);
		}
	}

	hFree(this->memory->dynamics);
	hFree(this->memory->statics);
	hFree(this->code);
}