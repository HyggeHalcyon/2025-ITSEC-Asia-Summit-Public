#include "common.h"
#include "VirtualMachine.h"

HANDLE hHeap = NULL;
HANDLE hStdin = NULL;

VOID init()
{
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
	_setmode(_fileno(stdout), O_BINARY);
	_setmode(_fileno(stdin), O_BINARY);
	hHeap = HeapCreate(HEAP_GROWABLE, 0, 0);
	hStdin = GetStdHandle(STD_INPUT_HANDLE);
}

INT main()
{
	VirtualMachine* VM;
	CHAR tempCodeBuffer[MAX_CODE_SIZE+1];
	ULONG Size;

	init();
	while (TRUE)
	{
		printf("Size >> ");
		Size = ReadLong();

		if (Size > MAX_CODE_SIZE)
		{
			printf("eh malas la\n");
			continue;
		}

		printf("Code >> ");
		ReadLine(tempCodeBuffer, Size);

		VM = new VirtualMachine(tempCodeBuffer, Size);
#if defined(_DEBUG)
		printf("vm: %#llx\n", VM);
		//printf("temp: %p\n", tempCodeBuffer);
		//printf("temp: %s\n", tempCodeBuffer);
#endif
		puts("Executing...");
;		VM->Execute();
		puts("Execution finished.");
		puts("Cleaning up...");
		VM->CleanUp();
		delete VM;
		puts("Done.");
		
		// just to make it easier to calculate stack offset
		printf("total code ran: %lu\n", (ULONG)(&tempCodeBuffer - sizeof(MAGICBYTES)) & 0xfff );

		fflush(stdout);
		fflush(stdin);
	}
}

