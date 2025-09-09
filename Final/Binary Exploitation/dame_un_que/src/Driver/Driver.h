#pragma once

#ifndef _DRIVER_H_
#define _DRIVER_H_

#define DEVICE_NAME         L"\\Device\\Golshi"
#define DOS_DEVICE_NAME     L"\\DosDevices\\Golshi"

NTSTATUS
DriverEntry(
    _In_ PDRIVER_OBJECT DriverObject,
    _In_ PUNICODE_STRING RegistryPath
);

NTSTATUS
IrpCreateHandler(
    _In_ PDEVICE_OBJECT DriverObject,
    _Inout_ PIRP Irp
);

NTSTATUS
IrpCloseHandler(
    _In_ PDEVICE_OBJECT DriverObject,
    _Inout_ PIRP Irp
);

NTSTATUS
IrpIOCTLHandler(
    _In_ PDEVICE_OBJECT DriverObject,
    _Inout_ PIRP Irp
);

NTSTATUS
IrpNotImplementedHandler(
    _In_ PDEVICE_OBJECT DeviceObject,
    _Inout_ PIRP Irp
);

VOID
DriverUnloadHandler(
    _In_ PDRIVER_OBJECT DriverObject
);

#endif // _DRIVER_H_