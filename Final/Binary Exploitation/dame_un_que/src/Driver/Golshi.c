#include <wdm.h>
#include "Golshi.h"

extern int _fltused;
int _fltused = 1;

PTRAINER Trainers[STABLE_CAPACITY] = { 0 };

NTSTATUS
HireTrainer(
	ULONG TrainerIdx
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PTRAINER Trainer = NULL;
	PCHAR TrainerName = NULL;

	PAGED_CODE();

	__try
	{
		DbgPrint("[*] Hiring new trainer\n");

		if (TrainerIdx >= STABLE_CAPACITY || Trainers[TrainerIdx] != NULL)
		{
			DbgPrint("[-] Invalid Index: %lu\n", TrainerIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Trainer = (PTRAINER)ExAllocatePool2(
			POOL_FLAG_PAGED | POOL_FLAG_USE_QUOTA,
			CALCULATE_TRAINER_OBJECT_SIZE(0x2),
			TRAINER_TAG
		);

		if (!Trainer)
		{
			DbgPrint("[-] Failed to allocate memory for Trainer\n");
			Status = STATUS_MEMORY_NOT_ALLOCATED;
			return Status;
		}

		Trainer->Size = 0x1;
		TrainerName = TRAINER_GET_NAME_PTR(Trainer);

		Trainers[TrainerIdx] = Trainer;
	}
	__except (EXCEPTION_EXECUTE_HANDLER)
	{
		Status = GetExceptionCode();
		DbgPrint("[-] Exception in HireTrainer: %#x\n", Status);
	}

	return Status;
}

NTSTATUS
ForceResignTrainer(
	ULONG TrainerIdx
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PTRAINER Trainer = NULL;

	PAGED_CODE();

	__try
	{
		DbgPrint("[*] Resigning trainer\n");

		if (TrainerIdx >= STABLE_CAPACITY || Trainers[TrainerIdx] == NULL)
		{
			DbgPrint("[-] Invalid Index: %lu\n", TrainerIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Trainer = Trainers[TrainerIdx];

		// free all the horses
		for (ULONG i = 0; i < Trainer->Size; i++) {
			if (Trainer->Horses[i] != NULL)
			{
				ExFreePoolWithTag(
					Trainer->Horses[i],
					HORSE_TAG
				);
				Trainer->Horses[i] = NULL;
			}
		}

		ExFreePoolWithTag(
			Trainers[TrainerIdx],
			TRAINER_TAG
		);

		Status = STATUS_SUCCESS;
	}
	__except (EXCEPTION_EXECUTE_HANDLER)
	{
		Status = GetExceptionCode();
		DbgPrint("[-] Exception in ForceResignTrainer: %#x\n", Status);
	}

	return Status;
}

NTSTATUS
BreedHorse(
	ULONG TrainerIdx
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	LONG FreeIdx = -1;
	PHORSE Foal = NULL;
	PTRAINER Trainer = NULL;
	PTRAINER NewTrainer = NULL;

	PAGED_CODE();

	__try
	{
		DbgPrint("[*] Breeding Horse\n");

		if (TrainerIdx >= STABLE_CAPACITY)
		{
			DbgPrint("[-] Invalid Trainer Index: %lu\n", TrainerIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Trainer = Trainers[TrainerIdx];

		// look for available index
		for (ULONG i = 0; i < Trainer->Size; i++)
		{
			if (Trainer->Horses[i] == NULL && FreeIdx == -1)
			{
				FreeIdx = i;
				DbgPrint("[*] Found free index at %lu\n", FreeIdx);
			}
		}

		// if no free index are found, expand the capacity of the trainer
		if (FreeIdx == -1)
		{
			DbgPrint("[*] No free index found, expanding trainer memory\n");

			NewTrainer = (PTRAINER)ExAllocatePool2(
				POOL_FLAG_PAGED | POOL_FLAG_USE_QUOTA,
				CALCULATE_TRAINER_OBJECT_SIZE(Trainer->Size + 2),
				TRAINER_TAG
			);

			if (!NewTrainer)
			{
				DbgPrint("[-] Failed to expand memory for Trainer\n");
				Status = STATUS_MEMORY_NOT_ALLOCATED;
				return Status;
			}

			NewTrainer->Size = Trainer->Size + 2;

			for (ULONG i = 0; i < Trainer->Size; i++)
			{
				NewTrainer->Horses[i] = Trainer->Horses[i];
			}

			RtlCopyMemory(
				TRAINER_GET_NAME_PTR(NewTrainer),
				TRAINER_GET_NAME_PTR(Trainer),
				MAX_NAME_LENGTH
			);

			FreeIdx = Trainer->Size;

			Trainer = NewTrainer;
			Trainers[TrainerIdx] = NewTrainer;
		}

		Foal = (PHORSE)ExAllocatePool2(
			POOL_FLAG_PAGED | POOL_FLAG_USE_QUOTA,
			sizeof(HORSE),
			HORSE_TAG
		);

		Trainer->Horses[FreeIdx] = Foal;

		Status = STATUS_SUCCESS;
	}
	__except (EXCEPTION_EXECUTE_HANDLER)
	{
		Status = GetExceptionCode();
		DbgPrint("[-] Exception in HorseAllocater: %x\n", Status);
	}

	return Status;
}

NTSTATUS
MournHorse(
	ULONG TrainerIdx,
	ULONG HorseIdx
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PTRAINER Trainer = NULL;
	PHORSE Horse = NULL;

	PAGED_CODE();

	__try
	{
		DbgPrint("[*] Mourning Horse\n");

		if (TrainerIdx >= STABLE_CAPACITY)
		{
			DbgPrint("[-] Invalid Trainer Index: %lu\n", TrainerIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Trainer = Trainers[TrainerIdx];

		if (HorseIdx >= Trainer->Size || Trainer->Horses[HorseIdx] == NULL)
		{
			DbgPrint("[-] Invalid Horse Index: %lu\n", HorseIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Horse = Trainer->Horses[HorseIdx];

		ExFreePoolWithTag(
			Horse,
			HORSE_TAG
		);

		Trainer->Horses[HorseIdx] = NULL;

		Status = STATUS_SUCCESS;
	}
	__except (EXCEPTION_EXECUTE_HANDLER)
	{
		Status = GetExceptionCode();
		DbgPrint("[-] Exception in HorseMourner: %x\n", Status);
	}

	return Status;
}

NTSTATUS
NameTrainer(
	ULONG TrainerIdx,
	PCHAR Name
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PTRAINER Trainer = NULL;

	PAGED_CODE();

	__try
	{
		DbgPrint("[*] Naming Trainer\n");

		if (TrainerIdx >= STABLE_CAPACITY || Trainers[TrainerIdx] == NULL)
		{
			DbgPrint("[-] Invalid Trainer Index: %lu\n", TrainerIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Trainer = Trainers[TrainerIdx];

		ProbeForRead(Name, MAX_NAME_LENGTH, 0x8);

		RtlCopyMemory(
			TRAINER_GET_NAME_PTR(Trainer),
			Name,
			MAX_NAME_LENGTH
		);

		Status = STATUS_SUCCESS;
	}
	__except (EXCEPTION_EXECUTE_HANDLER)
	{
		Status = GetExceptionCode();
		DbgPrint("[-] Exception in NameStallion: %x\n", Status);
	}

	return Status;
}

NTSTATUS
NameStallion(
	ULONG TrainerIdx,
	ULONG HorseIdx,
	PCHAR Name
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PTRAINER Trainer = NULL;
	PHORSE Horse = NULL;

	__try
	{
		DbgPrint("[*] Naming Stallion\n");

		if (TrainerIdx >= STABLE_CAPACITY || Trainers[TrainerIdx] == NULL)
		{
			DbgPrint("[-] Invalid Trainer Index: %lu\n", TrainerIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Trainer = Trainers[TrainerIdx];

		if (HorseIdx >= Trainer->Size || Trainer->Horses[HorseIdx] == NULL)
		{
			DbgPrint("[-] Invalid Horse Index: %lu\n", HorseIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Horse = Trainer->Horses[HorseIdx];

		ProbeForRead(Name, MAX_NAME_LENGTH, 0x8);

		RtlCopyMemory(
			Horse->Name,
			Name,
			MAX_NAME_LENGTH
		);

		Status = STATUS_SUCCESS;
	}
	__except (EXCEPTION_EXECUTE_HANDLER)
	{
		Status = GetExceptionCode();
		DbgPrint("[-] Exception in NameStallion: %x\n", Status);
	}

	return Status;
}

NTSTATUS
FeedHorse(
	ULONG TrainerIdx,
	ULONG HorseIdx,
	ULONG FoodInKG
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PTRAINER Trainer = NULL;
	PHORSE Horse = NULL;

	__try
	{
		DbgPrint("[*] Feeding Horse\n");

		if (TrainerIdx >= STABLE_CAPACITY || Trainers[TrainerIdx] == NULL)
		{
			DbgPrint("[-] Invalid Trainer Index: %lu\n", TrainerIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Trainer = Trainers[TrainerIdx];

		if (HorseIdx >= Trainers[TrainerIdx]->Size || Trainers[TrainerIdx]->Horses[HorseIdx] == NULL)
		{
			DbgPrint("[-] Invalid Horse Index: %lu\n", HorseIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Horse = Trainers[TrainerIdx]->Horses[HorseIdx];

		Horse->Weight += FoodInKG / 2;
		Horse->Height += FoodInKG / 5;

		Status = STATUS_SUCCESS;
	}
	__except (EXCEPTION_EXECUTE_HANDLER)
	{
		Status = GetExceptionCode();
		DbgPrint("[-] Exception in FeedHorse: %x\n", Status);
	}

	return Status;
}

NTSTATUS
TrainHorse(
	ULONG TrainerIdx,
	ULONG HorseIdx,
	ULONG TimeSpent
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PTRAINER Trainer = NULL;
	PHORSE Horse = NULL;

	PAGED_CODE();

	__try
	{
		DbgPrint("[*] Training Horse\n");

		if (TrainerIdx >= STABLE_CAPACITY)
		{
			DbgPrint("[-] Invalid Trainer Index: %lu\n", TrainerIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Trainer = Trainers[TrainerIdx];

		if (HorseIdx >= Trainer->Size || Trainer->Horses[HorseIdx] == NULL)
		{
			DbgPrint("[-] Invalid Horse Index: %lu\n", HorseIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Horse = Trainer->Horses[HorseIdx];
		Horse->Speed = TimeSpent * 7;
		Horse->Weight = (ULONG)(Horse->Weight * 0.95);
		Horse->Age += 1;

		Status = STATUS_SUCCESS;
	}
	__except (EXCEPTION_EXECUTE_HANDLER)
	{
		Status = GetExceptionCode();
		DbgPrint("[-] Exception in HorseMourner: %x\n", Status);
	}

	return Status;
}

NTSTATUS
ONamaeWaNanDesukaTrainerSan(
	ULONG TrainerIdx,
	PCHAR OutputBuffer,
	ULONG Length
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PTRAINER Trainer = NULL;

	PAGED_CODE();

	__try
	{
		if (TrainerIdx >= STABLE_CAPACITY)
		{
			DbgPrint("[-] Invalid Trainer Index: %lu\n", TrainerIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Trainer = Trainers[TrainerIdx];

		if (Length >= MAX_HORSE_AT_ONETIME)
		{
			DbgPrint("[-] Invalid Length: %lu, %lu\n", Length, Trainer->Size);
			Status = STATUS_UNSUCCESSFUL;
			return Status;
		}

		ProbeForWrite(OutputBuffer, MAX_NAME_LENGTH, 0x8);

		RtlCopyMemory(
			OutputBuffer,
			Trainer->Horses[Length],
			MAX_NAME_LENGTH
		);

		Status = STATUS_SUCCESS;
	}
	__except (EXCEPTION_EXECUTE_HANDLER)
	{
		Status = GetExceptionCode();
		DbgPrint("[-] Exception in ONamaeWaNanDesukaTrainerSan: %x\n", Status);
	}

	return Status;
}

NTSTATUS
ONamaeWaNanDesukaHorseChan(
	ULONG TrainerIdx,
	ULONG HorseIdx,
	PCHAR OutputBuffer
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PTRAINER Trainer = NULL;
	PHORSE Horse = NULL;

	PAGED_CODE();

	__try
	{
		if (TrainerIdx >= STABLE_CAPACITY)
		{
			DbgPrint("[-] Invalid Trainer Index: %lu\n", TrainerIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Trainer = Trainers[TrainerIdx];

		if (HorseIdx >= Trainer->Size || Trainer->Horses[HorseIdx] == NULL)
		{
			DbgPrint("[-] Invalid Horse Index: %lu\n", HorseIdx);
			Status = STATUS_INVALID_PARAMETER;
			return Status;
		}

		Horse = Trainer->Horses[HorseIdx];

		ProbeForWrite(OutputBuffer, MAX_NAME_LENGTH, 0x8);

		RtlCopyMemory(
			OutputBuffer,
			Horse->Name,
			MAX_NAME_LENGTH
		);

		Status = STATUS_SUCCESS;
	}
	__except (EXCEPTION_EXECUTE_HANDLER)
	{
		Status = GetExceptionCode();
		DbgPrint("[-] Exception in ONamaeWaNanDesukaHorseChan: %x\n", Status);
	}

	return Status;
}

NTSTATUS
AllocateTrainerHandler(
	_In_ PIRP Irp,
	_In_ PIO_STACK_LOCATION IrpSp
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PREQUEST Request = NULL;

	UNREFERENCED_PARAMETER(Irp);
	PAGED_CODE();

	Request = (PREQUEST)IrpSp->Parameters.DeviceIoControl.Type3InputBuffer;
	if (Request)
	{
		Status = HireTrainer(Request->TrainerIdx);
	}

	return Status;
}

NTSTATUS
FreeTrainerHandler(
	_In_ PIRP Irp,
	_In_ PIO_STACK_LOCATION IrpSp
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PREQUEST Request = NULL;

	UNREFERENCED_PARAMETER(Irp);
	PAGED_CODE();

	Request = (PREQUEST)IrpSp->Parameters.DeviceIoControl.Type3InputBuffer;
	if (Request)
	{
		Status = ForceResignTrainer(Request->TrainerIdx);
	}

	return Status;
}

NTSTATUS
AllocateHorseHandler(
	_In_ PIRP Irp,
	_In_ PIO_STACK_LOCATION IrpSp
)
{
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PREQUEST Request = NULL;

	UNREFERENCED_PARAMETER(Irp);
	PAGED_CODE();

	Request = (PREQUEST)IrpSp->Parameters.DeviceIoControl.Type3InputBuffer;

	if (Request)
	{
		Status = BreedHorse(Request->TrainerIdx);
	}

	return Status;
}

NTSTATUS
FreeHorseHandler(
	_In_ PIRP Irp,
	_In_ PIO_STACK_LOCATION IrpSp
)
{
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PREQUEST Request = NULL;

	UNREFERENCED_PARAMETER(Irp);
	PAGED_CODE();

	Request = (PREQUEST)IrpSp->Parameters.DeviceIoControl.Type3InputBuffer;

	if (Request)
	{
		Status = MournHorse(Request->TrainerIdx, Request->HorseIdx);
	}

	return Status;
}

NTSTATUS
SetTrainerHandler(
	_In_ PIRP Irp,
	_In_ PIO_STACK_LOCATION IrpSp
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PREQUEST Request = NULL;

	UNREFERENCED_PARAMETER(Irp);
	PAGED_CODE();

	Request = (PREQUEST)IrpSp->Parameters.DeviceIoControl.Type3InputBuffer;

	if (Request)
	{
		Status = NameTrainer(Request->TrainerIdx, Request->Name);
	}

	return Status;
}

NTSTATUS
SetHorseHandler(
	_In_ PIRP Irp,
	_In_ PIO_STACK_LOCATION IrpSp
)
{
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PREQUEST Request = NULL;

	UNREFERENCED_PARAMETER(Irp);
	PAGED_CODE();

	Request = (PREQUEST)IrpSp->Parameters.DeviceIoControl.Type3InputBuffer;

	if (Request)
	{
		Status = NameStallion(Request->TrainerIdx, Request->HorseIdx, Request->Name);
	}

	return Status;
}

NTSTATUS
FeedHorseHandler(
	_In_ PIRP Irp,
	_In_ PIO_STACK_LOCATION IrpSp
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PREQUEST Request = NULL;

	UNREFERENCED_PARAMETER(Irp);
	PAGED_CODE();

	Request = (PREQUEST)IrpSp->Parameters.DeviceIoControl.Type3InputBuffer;

	if (Request)
	{
		Status = FeedHorse(Request->TrainerIdx, Request->HorseIdx, Request->FoodInKg);
	}

	return Status;
}

NTSTATUS
TrainHorseHandler(
	_In_ PIRP Irp,
	_In_ PIO_STACK_LOCATION IrpSp
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PREQUEST Request = NULL;

	UNREFERENCED_PARAMETER(Irp);
	PAGED_CODE();

	Request = (PREQUEST)IrpSp->Parameters.DeviceIoControl.Type3InputBuffer;

	if (Request)
	{
		Status = TrainHorse(Request->TrainerIdx, Request->HorseIdx, Request->TimeSpent);
	}

	return Status;
}

NTSTATUS
GetTrainerNameHandler(
	_In_ PIRP Irp,
	_In_ PIO_STACK_LOCATION IrpSp
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PREQUEST Request = NULL;

	UNREFERENCED_PARAMETER(Irp);
	PAGED_CODE();

	Request = (PREQUEST)IrpSp->Parameters.DeviceIoControl.Type3InputBuffer;

	if (Request)
	{
		Status = ONamaeWaNanDesukaTrainerSan(Request->TrainerIdx, Request->OutputBuffer, Request->Length);
	}

	return Status;
}

NTSTATUS
GetHorseNameHandler(
	_In_ PIRP Irp,
	_In_ PIO_STACK_LOCATION IrpSp
) {
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	PREQUEST Request = NULL;

	UNREFERENCED_PARAMETER(Irp);
	PAGED_CODE();

	Request = (PREQUEST)IrpSp->Parameters.DeviceIoControl.Type3InputBuffer;

	if (Request)
	{
		Status = ONamaeWaNanDesukaHorseChan(Request->TrainerIdx, Request->HorseIdx, Request->OutputBuffer);
	}

	return Status;
}

VOID CleanAllocations()
{
	for (ULONG i = 0; i < STABLE_CAPACITY; i++)
	{
		if (Trainers[i] != NULL)
		{
			ForceResignTrainer(i);
			Trainers[i] = NULL;
		}
	}
}