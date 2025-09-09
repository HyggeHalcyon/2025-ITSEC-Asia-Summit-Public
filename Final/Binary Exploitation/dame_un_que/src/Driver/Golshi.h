#pragma once
#include <wdm.h>

#ifndef _GOLSHI_H_
#define _GOLSHI_H_

#define IOCTL(Function) CTL_CODE(FILE_DEVICE_UNKNOWN, Function, METHOD_NEITHER, FILE_ANY_ACCESS)

#define IOCTL_HIRE_TRAINER          IOCTL(0)
#define IOCTL_FORCE_RESIGN_TRAINER  IOCTL(1)
#define IOCTL_NEW_FOAL              IOCTL(2)
#define IOCTL_RETIRE_STALLION       IOCTL(3)
#define IOCTL_SET_TRAINER           IOCTL(4)
#define IOCTL_SET_STALLION          IOCTL(5)
#define IOCTL_FEED_STALLION         IOCTL(6)
#define IOCTL_TRAIN_STALLION        IOCTL(7)
#define IOCTL_GET_TRAINER_NAME      IOCTL(8)
#define IOCTL_GET_STALLION_NAME     IOCTL(9)

#define MAX_NAME_LENGTH		    0x28
#define MAX_HORSE_AT_ONETIME    0x20
#define MAX_SPEED               0x71
#define HORSE_TAG		        'sroh'
#define TRAINER_TAG             'iart'
#define STABLE_CAPACITY		    0x8

#define CALCULATE_TRAINER_OBJECT_SIZE(cnt) \
    (sizeof(ULONG) + sizeof(PHORSE) * (cnt) + (MAX_NAME_LENGTH))

#define TRAINER_GET_NAME_PTR(ptr) ((CHAR*)(&(ptr)->Horses[(ptr)->Size]))

typedef struct _REQUEST {
    ULONG TrainerIdx;
    ULONG TimeSpent;
    ULONG FoodInKg;
    ULONG Length;
    ULONG HorseIdx;
    PCHAR Name;
    PCHAR OutputBuffer;
} REQUEST, * PREQUEST;

typedef struct _HORSE {
    CHAR Name[MAX_NAME_LENGTH];
    ULONG Age;
    ULONG Speed;
    ULONG Weight;
    ULONG Height;
} HORSE, * PHORSE;

typedef struct _TRAINER {
    ULONG Size;
    PHORSE Horses[1];
    //CHAR Name[MAX_NAME_LENGTH];
} TRAINER, * PTRAINER;

NTSTATUS HireTrainer(
    ULONG TrainerIdx
);

NTSTATUS ForceResignTrainer(
    ULONG TrainerIdx
);

NTSTATUS BreedHorse(
    ULONG TrainerIdx
);

NTSTATUS MournHorse(
    ULONG TrainerIdx,
    ULONG HorseIdx
);

NTSTATUS NameTrainer(
    ULONG TrainerIdx,
    PCHAR Name
);

NTSTATUS NameStallion(
    ULONG TrainerIdx,
    ULONG HorseIdx,
    PCHAR Name
);

NTSTATUS FeedHorse(
    ULONG TrainerIdx,
    ULONG HorseIdx,
    ULONG FoodInKG
);

NTSTATUS TrainHorse(
    ULONG TrainerIdx,
    ULONG HorseIdx,
    ULONG TimeSpent
);

NTSTATUS ONamaeWaNanDesukaTrainerSan(
    ULONG TrainerIdx,
    PCHAR OutputBuffer,
    ULONG Length
);

NTSTATUS ONamaeWaNanDesukaHorseChan(
    ULONG TrainerIdx,
    ULONG HorseIdx,
    PCHAR OutputBuffer
);

NTSTATUS AllocateTrainerHandler(
    _In_ PIRP Irp,
    _In_ PIO_STACK_LOCATION IrpSp
);

NTSTATUS FreeTrainerHandler(
    _In_ PIRP Irp,
    _In_ PIO_STACK_LOCATION IrpSp
);

NTSTATUS AllocateHorseHandler(
    _In_ PIRP Irp,
    _In_ PIO_STACK_LOCATION IrpSp
);

NTSTATUS FreeHorseHandler(
    _In_ PIRP Irp,
    _In_ PIO_STACK_LOCATION IrpSp
);

NTSTATUS SetTrainerHandler(
    _In_ PIRP Irp,
    _In_ PIO_STACK_LOCATION IrpSp
);

NTSTATUS SetHorseHandler(
    _In_ PIRP Irp,
    _In_ PIO_STACK_LOCATION IrpSp
);

NTSTATUS FeedHorseHandler(
    _In_ PIRP Irp,
    _In_ PIO_STACK_LOCATION IrpSp
);

NTSTATUS TrainHorseHandler(
    _In_ PIRP Irp,
    _In_ PIO_STACK_LOCATION IrpSp
);

NTSTATUS GetTrainerNameHandler(
    _In_ PIRP Irp,
    _In_ PIO_STACK_LOCATION IrpSp
);

NTSTATUS GetHorseNameHandler(
    _In_ PIRP Irp,
    _In_ PIO_STACK_LOCATION IrpSp
);

VOID CleanAllocations();

#endif // _GOLSHI_H_