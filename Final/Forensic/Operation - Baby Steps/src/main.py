def main():
    questions = [
        {
            "question": "1. What is the name of the malicious UDF library file uploaded by the Threat Actor, which is used for executing system commands?",
            "format": "file_name.ext"
        },
        { 
            "question": "2. What is the evidence from the registry or system configuration that RDP was enabled by the user for persistence?",
            "format": "XXXX\XXXXXX\XXXXXXXXXXXXX\XXXXXXX\XXXXXXXX XXXXXX\XXXXXXXXXXXXXXXXXX=X"
        },
        { 
            "question": "3. What is the name of the Windows privilege that was exploited for privilege escalation to SYSTEM?",
            "format": "-"
        },
        { 
            "question": "4. What is the original timestamp of a webshell file’s CreationTime that was modified by an attacker, rather than the timestomped value, given that the recorded creation time is after the timestomping process? (UTC+07:00)",
            "format": "XXXX-XX-XX XX:XX:XX"
        },
        { 
            "question": "5. What anti-forensic technique was used to hide the original timestamp of the file activity?",
            "format": "-"
        },
        { 
            "question": "6. What is the destination address of the command & control (C2) server embedded in the backdoor sl.exe and used for outbound communication?",
            "format": "IP:PORT"
        },
        { 
            "question": "7. What is the email identity found and associated with the threat actor during the exfiltration process?",
            "format": "threatactor@example.com"
        },
        { 
            "question": "8. Upon examining the C2 malware binary, it appears that the binary failed to establish a connection. What was the Discord bot username the malware attempted to contact during execution, and what is its bot API key?",
            "format": "username:BOT_API_KEY"
        },
        { 
            "question": "9. What is the name of the command callback function used to establish persistence?",
            "format": "-"
        },
        { 
            "question": "10. What is the text channel ID used by the threat actor to communicate with the bot and receive output?",
            "format": "ID"
        },
        { 
            "question": "11. What was the first CWE exploited by the Threat Actor in the binary named Higan, and what is 2 CWEs exploited related to Heap Memory in the binary named Procland?",
            "format": "CWE-XXX,CWE-XXX,CWE-XXX"
        },
        { 
            "question": "12. What is the full initial instruction from gadgets used by Threat Actor to allow puts@got passed as the first argument used in exploit scripts for Higan binary?",
            "format": "Full Gadgets Chain"
        },
        { 
            "question": "13. What is the 32-bit local variable value does the attacker overwrite to bypass security checks for Higan binary?",
            "format": "0xaaa"
        },
        { 
            "question": "14. It is known that the threat actor clobbered the tcache entry structure in the procland binary. What is the tampered pointer?",
            "format": "xxxxxx_xxx"
        },
        {
            "question": "15. It is known that the threat actor performed post-exploitation activities on a compromised Linux Docker container. The attacker deleted a legitimate system binary and replaced it with a forged malicious binary of the same name and path. What is the MITRE ATT&CK technique ID for this activity?",
            "format": "TXXXX.XXX"
        }
    ]

    answers = [
        "libmysql_execstr.dll",
        r"HKLM\SYSTEM\ControlSet001\Control\Terminal Server\fDenyTSConnections=0",
        "SeImpersonatePrivilege",
        "2025-08-01 15:57:33",
        "Timestomping",
        "103.167.137.91:4455",
        "rizal.testing1@gmail.com",
        "Sigvarr:MTM2MzQ0MDcxNDUxNTc0MjgwMQ.GVE2rR.-K9fcEdUThjTSNJS-Zn3WwgoDhjL5NaLHRS6Rk",
        "SIGVAR",
        "548372455996129282",
        "CWE-125,CWE-416,CWE-415",
        "xchg r12, rdi; pop rbp; nop; pop rdx; xor rax, rax; ret;",
        "0xde4db33f",
        "tcache_key",
        "T1036.003"
    ]

    def validate_answer(user_answer, correct_answer, question_index):
        # Question 5 - timestomping (case insensitive)
        if question_index == 4:  # 0-indexed, so question 5 is index 4
            return user_answer.lower().strip() == correct_answer.lower().strip()
        
        # Question 11 - CWE validation (first must be correct, second and third can be in any order)
        elif question_index == 10:  # 0-indexed, so question 11 is index 10
            try:
                user_cwes = [cwe.strip() for cwe in user_answer.split(',')]
                correct_cwes = [cwe.strip() for cwe in correct_answer.split(',')]
                
                # Must have exactly 3 CWEs
                if len(user_cwes) != 3 or len(correct_cwes) != 3:
                    return False
                
                # First CWE must match exactly
                if user_cwes[0] != correct_cwes[0]:
                    return False
                
                # Second and third CWEs can be in any order
                user_remaining = sorted(user_cwes[1:])
                correct_remaining = sorted(correct_cwes[1:])
                
                return user_remaining == correct_remaining
            except:
                return False
    
        else:
            return user_answer.strip() == correct_answer.strip()

    print("Please answers the questions provided below:")

    correct_answers = 0

    for index, q in enumerate(questions, start=1):
        print(f"\nNo {index}:")
        print("Questions: " + q["question"])
        print("Format: " + q["format"])
        user_answer = input("Ans: ").strip()
        print(f"Your answer: '{user_answer}'")
        
        if validate_answer(user_answer, answers[index - 1], index - 1):
            correct_answers += 1
            print("Correct!")
        else:
            print("Incorrect")
            return
    
    if correct_answers == len(questions):
        print("\nCongrats! Flag: ITSEC{F010358092E6E224BDFE35BAF0E23C0D7E20976B80C813D85DEAE4FEB19795F8}")

if __name__ == "__main__":
    main()
