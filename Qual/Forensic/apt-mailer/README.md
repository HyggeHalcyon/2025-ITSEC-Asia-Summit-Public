# Forensic - APT Mailer

1. Given a PCAP file which contains several traffic log.
2. Analyze the SMTP log which is a phishing email then retrieve the VBS file.
3. Analyze the obfuscated VBS file, obfuscated with (https://github.com/BaptisteVeyssiere/vba-macro-obfuscator)

This is the base obfuscation code which will perform XOR and LEFT shift for every character. 
```
Private Function zYWTgOUvCUasUF(fyVzjyrSVfUN As Variant, wmcgYwnuVvaWgrd As Variant)
Dim guZtvRhfxgcxFR As String
guZtvRhfxgcxFR = ""
For vochkYPjMXMeW = LBound(fyVzjyrSVfUN) To UBound(fyVzjyrSVfUN)
guZtvRhfxgcxFR = guZtvRhfxgcxFR & Chr(wmcgYwnuVvaWgrd(vochkYPjMXMeW) Xor fyVzjyrSVfUN(vochkYPjMXMeW)) * (2 ^ (2 - 0))
Next
zYWTgOUvCUasUF = guZtvRhfxgcxFR
```

decoded function:
```
class EncryptionFormatter(StringFormatter):
    DECRYPT_VBA = """
Private Function decrypt(ciphertext As Variant, key As Variant)
    Dim plaintext As String
    plaintext = ""
    
    For i = LBound(ciphertext) To UBound(ciphertext)
        plaintext = plaintext & Chr(key(i) Xor ciphertext(i)) * (2 ^ 2)
    Next
    decrypt = plaintext
End Function
"""
```

After XOR-ing the characters, there is another simple encryption algorithm (Caesar Cipher)

```
Function bETonJcHVNTUdH(text, shift)
Dim vochkYPjMXMeW, result, charCode
result = 
For vochkYPjMXMeW = (1 XOR 0) To Len(text)
charCode = Asc(Mid(text, vochkYPjMXMeW, 1))
charCode = charCode + shift
result = result & Chr(charCode)
Next
bETonJcHVNTUdH = result
End Function
```

deobfuscated function:
```
Function enc(text, shift)
    Dim i, result, charCode
    result = ""

    For i = 1 To Len(text)
        charCode = Asc(Mid(text, i, 1))
        charCode = charCode + shift
        result = result & Chr(charCode)
    Next
    enc = result
End Function
```

Also there is a function that will write something into the registry.

```
Function pPBAddHxuvSqSyj(regPath, regName, regValue, regType)
On Error Resume Next
Dim gmLGTlQYtwLoT
Set gmLGTlQYtwLoT = WScript.CreateObject(zYWTgOUvCUasUF(Array((141 - 37),(1443 - 547),((686 - 175) XOR (1091 - 396)),(233 + 211),720,(261 - 125),(172 + 232),(6 + 10),((180 - 53) + (1310 - 653)),100,((850 - 340) + (106 - 16)),968,796),Array(77,179,(345 - 168),(57 - 28),221,82,((23 - 9) XOR 31),42,(87 XOR 192),(45 + 68),((224 - 37) XOR (96 - 24)),(160 - 2),(153 XOR (30 + 20)))))
Dim chfqRkgAaNapL
chfqRkgAaNapL = regPath & regName
gmLGTlQYtwLoT.RegWrite chfqRkgAaNapL, regValue, regType
End Function
```

deobfuscated function:
```
Function WriteRegistry(regPath, regName, regValue, regType)
    On Error Resume Next
    Dim objShell
    Set objShell = WScript.CreateObject("WScript.Shell")
    Dim fullPath

    fullPath = regPath & regName
    objShell.RegWrite fullPath, regValue, regType
End Function
```


4. Reverse the encryption mechanism to retrieve the full source code.

simple python script
```
def decode_obfuscated(enc, key):
    result = ""
    for x in range(len(enc)):
        for i in range(len(enc[x])):
            decoded_char = chr(enc[x][i]>>2 ^ key[x][i]) 
            result += decoded_char
    return result

flag = ""

enc = [
    [(228 + 112),(459 + 405),(570 ^ (256 - 78)),140,880,324,(197 + (568 - 205)),296,(231 + (329 - 36)),(638 ^ (39 + 231)),(547 + 261),(809 + 51),((960 - 21) ^ 83),(260 - 128),((1349 - 505) + (112 - 56))],
    [176,180,(61 ^ (137 + (659 - 23))),(467 ^ 683),300,((168 - 51) ^ 9),((274 + 140) ^ (33 + 81)),(529 + 391),(((11 - 1) + 170) ^ 908),(380 - 148),((2 + (3 - 1)) ^ 692),48,(645 - 33),(635 - 179),(318 + 494)],
    [(62 ^ 94),384,((342 - 135) ^ (164 + (185 - 6))),((1340 - 562) ^ 234),(627 - 71),(118 + 874),((49 + 183) ^ 556),(320 - 88),(20 + (1029 - 117)),((60 + 52) ^ 992),(451 ^ 683),(929 - 45),(878 - 258),216,976], , ....snipped ...
]


key = [
    [(60 - 22),170,((72 - 10) + 154),(147 - 72),169,(26 ^ (72 - 11)),((210 - 60) ^ (165 - 52)),34,(201 ^ (28 + (14 - 5))),((35 - 14) + 158),(11 + 240),((39 + (194 - 82)) ^ (59 - 19)),133,73,(279 - 85)],
    [(6 + 22),(167 - 43),((184 - 18) ^ 26),((108 - 54) + 87),104,47,42,(63 + 85),191,118,143,(100 - 40),(26 + 169),81,128],
    [116,((2 + (0 - 0)) ^ (2 + 3)),((1 - 0) + 0),144,(116 ^ 142),(395 - 176),129,(186 - 72),(99 + (62 - 9)),130,(((33 - 12) + 67) ^ 161),128,((129 + (88 - 27)) ^ (189 - 62)),103,134], ....snipped ...
]

print(decode_obfuscated(enc,key))
```

5. Perform caesar cipher 3 characters to the left.
`srzhuvkhoo1h{h#0QrS#0QrqL#0Z#Klgghq#0Hqf#]ZQre|EWYoMXXoYRQ4YtWp8QZH7z\58v]oYHWqomhn]9]HURgYo9Wp]VeIM\VYQJRT@@` -> `powershell.exe~-NoP~-NonI~-W~Hidden~-Enc~ZWNobyBTVlJUUlVON1VqTm5NWE4wY25sZlVETnljekZ6ZEROdVl6TmZSbFJYSVNGOQ==`

6. It seems the attacker executed the payload with base64 encoded powershell command to Windows registry, decode the base64 payload.

Flag: ITSEC{R3g1stry_P3rs1st3nc3_FTW!!}