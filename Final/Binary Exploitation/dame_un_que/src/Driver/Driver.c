#include <wdm.h>
#include "Driver.h"
#include "Golshi.h"

#ifdef ALLOC_PRAGMA
#pragma alloc_text(INIT, DriverEntry)
#pragma alloc_text(PAGE, DriverUnloadHandler)
#pragma alloc_text(PAGE, IrpCloseHandler)
#pragma alloc_text(PAGE, IrpCreateHandler)
#pragma alloc_text(PAGE, IrpIOCTLHandler)
#pragma alloc_text(PAGE, IrpNotImplementedHandler)
#endif

BOOLEAN InUse = FALSE;
FAST_MUTEX Lock;
PDEVICE_OBJECT g_DriverObject = NULL;

NTSTATUS
DriverEntry(
    _In_ PDRIVER_OBJECT DriverObject,
    _In_ PUNICODE_STRING RegistryPath
) {
    PDEVICE_OBJECT DeviceObject = NULL;
    NTSTATUS Status = STATUS_UNSUCCESSFUL;
    UNICODE_STRING DeviceName, DosDeviceName = { 0 };

    UNREFERENCED_PARAMETER(RegistryPath);
    PAGED_CODE();

    RtlInitUnicodeString(&DeviceName, DEVICE_NAME);
    RtlInitUnicodeString(&DosDeviceName, DOS_DEVICE_NAME);
    ExInitializeFastMutex(&Lock);

    Status = IoCreateDevice(DriverObject, 0, &DeviceName, FILE_DEVICE_UNKNOWN, FILE_DEVICE_SECURE_OPEN, FALSE, &DeviceObject);
    if (!NT_SUCCESS(Status)) {
        if (DeviceObject) {
            IoDeleteDevice(DeviceObject);
        }
        DbgPrint("[-] Error Creating Device\n");
        return Status;
    }

    for (INT32 i = 0; i <= IRP_MJ_MAXIMUM_FUNCTION; i++) {
        DriverObject->MajorFunction[i] = IrpNotImplementedHandler;
    }

    DriverObject->MajorFunction[IRP_MJ_CREATE] = IrpCreateHandler;
    DriverObject->MajorFunction[IRP_MJ_CLOSE] = IrpCloseHandler;
    DriverObject->MajorFunction[IRP_MJ_DEVICE_CONTROL] = IrpIOCTLHandler;

    DriverObject->DriverUnload = DriverUnloadHandler;

    DeviceObject->Flags |= DO_DIRECT_IO;
    DeviceObject->Flags &= ~DO_DEVICE_INITIALIZING;

    Status = IoCreateSymbolicLink(&DosDeviceName, &DeviceName);

    g_DriverObject = DeviceObject;

    DbgPrint("[+] Device Created and Loaded\n");

    return Status;
}

VOID
DriverUnloadHandler(
    _In_ PDRIVER_OBJECT DriverObject
) {
    UNICODE_STRING DosDeviceName = { 0 };

    PAGED_CODE();

    ExAcquireFastMutex(&Lock);

    RtlInitUnicodeString(&DosDeviceName, DOS_DEVICE_NAME);

    IoDeleteSymbolicLink(&DosDeviceName);

    IoDeleteDevice(DriverObject->DeviceObject);

    CleanAllocations();

    DbgPrint("[+] Device Deleted\n");

    ExReleaseFastMutex(&Lock);
}

NTSTATUS
IrpNotImplementedHandler(
    _In_ PDEVICE_OBJECT DeviceObject,
    _Inout_ PIRP Irp
) {
    ExAcquireFastMutex(&Lock);

    Irp->IoStatus.Information = 0;
    Irp->IoStatus.Status = STATUS_NOT_SUPPORTED;

    UNREFERENCED_PARAMETER(DeviceObject);
    PAGED_CODE();

    IoCompleteRequest(Irp, IO_NO_INCREMENT);

    ExReleaseFastMutex(&Lock);
    return STATUS_NOT_SUPPORTED;
}

NTSTATUS
IrpCreateHandler(
    _In_ PDEVICE_OBJECT DriverObject,
    _Inout_ PIRP Irp
) {
    NTSTATUS Status = STATUS_SUCCESS;

    UNREFERENCED_PARAMETER(DriverObject);

    ExAcquireFastMutex(&Lock);

    if (InUse) {
        Status = STATUS_DEVICE_BUSY;
        DbgPrint("[-] Failed to open device: in use by another process\n");
    }
    else {
        InUse = TRUE;
        DbgPrint("[+] Device opened\n");
    }

    Irp->IoStatus.Information = 0;
    Irp->IoStatus.Status = Status;
    IoCompleteRequest(Irp, IO_NO_INCREMENT);

    ExReleaseFastMutex(&Lock);
    return Status;
}

NTSTATUS
IrpCloseHandler(
    _In_ PDEVICE_OBJECT DriverObject,
    _Inout_ PIRP Irp
) {
    NTSTATUS Status = STATUS_SUCCESS;

    UNREFERENCED_PARAMETER(DriverObject);

    ExAcquireFastMutex(&Lock);

    InUse = FALSE;
    DbgPrint("[+] Device closed\n");

    Irp->IoStatus.Information = 0;
    Irp->IoStatus.Status = Status;
    IoCompleteRequest(Irp, IO_NO_INCREMENT);

    ExReleaseFastMutex(&Lock);
    return Status;
}

NTSTATUS
IrpIOCTLHandler(
    _In_ PDEVICE_OBJECT DriverObject,
    _Inout_ PIRP Irp
) {
    PIO_STACK_LOCATION IrpSp = NULL;
    ULONG IoControlCode = 0;
    NTSTATUS Status = STATUS_NOT_SUPPORTED;

    UNREFERENCED_PARAMETER(DriverObject);
    PAGED_CODE();

    ExAcquireFastMutex(&Lock);

    IrpSp = IoGetCurrentIrpStackLocation(Irp);

    if (IrpSp) {
        IoControlCode = IrpSp->Parameters.DeviceIoControl.IoControlCode;

        switch (IoControlCode) {
        case IOCTL_HIRE_TRAINER:
            Status = AllocateTrainerHandler(Irp, IrpSp);
            break;
        case IOCTL_FORCE_RESIGN_TRAINER:
            Status = FreeTrainerHandler(Irp, IrpSp);
            break;
        case IOCTL_NEW_FOAL:
            Status = AllocateHorseHandler(Irp, IrpSp);
            break;
        case IOCTL_RETIRE_STALLION:
            Status = FreeHorseHandler(Irp, IrpSp);
            break;
        case IOCTL_SET_TRAINER:
            Status = SetTrainerHandler(Irp, IrpSp);
            break;
        case IOCTL_SET_STALLION:
            Status = SetHorseHandler(Irp, IrpSp);
            break;
        case IOCTL_FEED_STALLION:
            Status = FeedHorseHandler(Irp, IrpSp);
            break;
        case IOCTL_TRAIN_STALLION:
            Status = TrainHorseHandler(Irp, IrpSp);
            break;
        case IOCTL_GET_TRAINER_NAME:
            Status = GetTrainerNameHandler(Irp, IrpSp);
            break;
        case IOCTL_GET_STALLION_NAME:
            Status = GetHorseNameHandler(Irp, IrpSp);
            break;
        default:
            Status = STATUS_INVALID_DEVICE_REQUEST;
            DbgPrint("[-] Unknown IOCTL Code: %#x\n", IoControlCode);
            break;
        }
    }

    Irp->IoStatus.Information = 0;
    Irp->IoStatus.Status = Status;
    IoCompleteRequest(Irp, IO_NO_INCREMENT);

    ExReleaseFastMutex(&Lock);
    return Status;
}