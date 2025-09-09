This is a Windows Driver Challenge, your objective is to escalate privilege to Administrator or NT/Authority System.

Sorry it had to be windows again, but I read too much STARLABS writeups recently and I just can't help myself.

You can use the provided OVF for your exploit environment (this one mimics exactly what the author will be using for verification) or build/setup your own environment, here's how you can do it:
- Download the Windows 11 ISO: https://www.microsoft.com/en-us/software-download/windows11
- Create the virtual machine in your choice of hypervisor (VMWare/VirtualBox/etc)
- Follow the windows installation steps
- While installing, download OSRLoader and optionally Sysinternals Suite
- Once the windows installation is completed, feel free to disable antivirus and autoupdates, then copy the OSRLoader and Sysinternals Suite into the machine.
- Then install VirtualKD-Redux, follow the tutorial to install it in both of your debugger and debuggee machine.
- Take a sanity check! shutdown the machine and boot it up again with vmmon.exe of VirtualKD running, if you're able to intercept and debug the machine, then its all good! 
- Once all done, take a snapshot while its still running, this will be the revert point for your future exploit development.

There's no remote connection, once you have managed to exploit it locally, feel free to open a ticket and send your exploit (preferrably with the source code as well) and the author will validate it manually.

The challenge will be ran againts:
- Windows 24H2
- Low Integrity Level
- Antivirus disabled

Feel free to discuss with the author if you need anything (other than the flag of the exploit poc)

### References
- https://starlabs.sg/blog/2023/11-exploitation-of-a-kernel-pool-overflow-from-a-restrictive-chunk-size-cve-2021-31969
- https://github.com/MrAle98/CVE-2025-21333-POC/tree/master
- https://www.nccgroup.com/research-blog/cve-2021-31956-exploiting-the-windows-kernel-ntfs-with-wnf-part-1
- https://www.nccgroup.com/research-blog/cve-2021-31956-exploiting-the-windows-kernel-ntfs-with-wnf-part-2
- https://starlabs.sg/blog/2024/all-i-want-for-christmas-is-a-cve-2024-30085-exploit/#obtaining-a-kernel-pointer-leak
- https://github.com/vp777/Windows-Non-Paged-Pool-Overflow-Exploitation
- https://vuln.dev/windows-kernel-exploitation-hevd-x64-use-after-free
- https://rootkits.xyz/blog/2017/11/kernel-pool-overflow
- https://connormcgarr.github.io/swimming-in-the-kernel-pool-part-1
- https://connormcgarr.github.io/swimming-in-the-kernel-pool-part-2
- https://blog.quarkslab.com/playing-with-the-windows-notification-facility-wnf.html
- https://3sjay.github.io/2024/09/08/Windows-Kernel-Pool-Exploitation-CVE-2021-31956-Part1.html
- https://3sjay.github.io/2024/09/20/Windows-Kernel-Pool-Exploitation-CVE-2021-31956-Part2.html
- https://nu1lptr0.github.io/2024/10/10/windows-kernel-challenge-process-flipper.html
- https://wetw0rk.github.io/posts/0x03-approaching-the-modern-windows-kernel-heap/