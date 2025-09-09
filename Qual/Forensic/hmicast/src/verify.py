import socket
import threading

def handle_client(client_socket):
    try:
        client_socket.send("Verify your answer here.\n\n".encode('utf-8'))

        questions = [
            "1. Is the phone rooted? format: yes/no || Answer: ",
            "\n\n2. What is the malicious package name? format: com.abc.xyl || Answer: ",
            "\n\n3. What is the download link of the malicious package? format: https://evil.com/maliciousfile || Answer: ",
            "\n\n4. What is the Android API that attacker use to capture victim's screen? format: android.xxx.yyy.zzz|| Answer: ",
            "\n\n5. What is the secretkey for image encryption process? || Answer: ",
            "\n\n6. Where the encrypted image sent to? format: Application Name (i.e. Pastebin) || Answer: ",
            "\n\n7. What is the bot API token || Answer: ",
            "\n\n8. What is the bot username? || Answer: ",
            "\n\n9. What is the group name and invite link? format: (name,link) || Answer: ",
            "\n\n10. What is the login credential that was captured and sent at this window of time [Tuesday, July 29, 2025 5:26 AM - Tuesday, July 29, 2025 5:30 AM]? format: username:password || Answer: "
        ]
        answers = [
            "yes",
            "com.itsec.android.hmi",
            "https://mega.nz/file/uddABYRD#c__klT8jtAiAhKLWNfuOuywoZiRfZfSXqxxryrVslj8",
            "android.media.projection.MediaProjectionManager",
            "dPGgF7tQlBaGqqmj",
            "Telegram",
            "8369776437:AAFYoPjexy1-_wdpuCHAjIS4ZW9eJ6B-T0Q",
            "guntershelpsBot",
            "mycrib,https://t.me/+RVvaMCn_f7FmZmFl",
            "operator1337:HM1_standin9_Str0nk"
        ]

        for i in range(len(questions)):
            client_socket.send(questions[i].encode('utf-8'))
            data = client_socket.recv(1024).strip().decode("utf-8")
            print(f"Received answer: {data}")

            if data != answers[i]:
                client_socket.sendall(b"Incorrect answer. Connection closing.")
                print("Incorrect answer. Closing connection with client.")
                return
        
        client_socket.sendall(b"You have caught the culprit. Here is your flag: ITSEC{gunt3rs_is_th3_culpr1t_88ebf35eac}")
        print("All answers correct. Success message sent.")
    
    except Exception as e:
        print("An error occurred while handling the client:", e)
    
    finally:
        client_socket.close()
        print("Client connection closed.")

def create_server(host, port):
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server_socket.settimeout(20)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server is listening on {host}:{port}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            client_socket.settimeout(60)
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

    except Exception as e:
        print("An error occurred with the server:", e)
    
    finally:
        # Close the server socket
        if server_socket:
            server_socket.close()

create_server('0.0.0.0', 14437)  
