#pragma once
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <io.h>
#include <fcntl.h>
#include <stdlib.h>
#include <windows.h>

extern HANDLE hHeap;
extern HANDLE hStdin;

inline PVOID hAlloc(size_t Size)
{
	return HeapAlloc(hHeap, HEAP_ZERO_MEMORY, Size);
}

inline VOID hFree(PVOID Ptr)
{
	HeapFree(hHeap, NULL, Ptr);
}

inline VOID Panic(CONST CHAR* Msg)
{
	printf("[-] Panic: %s\n", Msg);
	_exit(1);
}

inline VOID ReadLine(PCHAR Buffer, size_t Size)
{
    ULONG BytesRead = 0;
	if (!ReadFile(hStdin, Buffer, Size, &BytesRead, NULL))
	{
		Panic("Error reading input");
	}
}

inline LONG ReadLong()
{
	CHAR Buf[0x10];
	ReadLine(Buf, 0x10 - 1);
	return atol(Buf);
}