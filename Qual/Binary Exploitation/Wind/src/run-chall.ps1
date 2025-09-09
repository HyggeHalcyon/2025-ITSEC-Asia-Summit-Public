$exe = 'C:\ctf\chall.exe'
$wd  = Split-Path -LiteralPath $exe

# run as local user 'ctf' (plain text shown here because you asked for no prompt)
$password = ConvertTo-SecureString 'e4e376e447c60ed46473be53a7dd10c9!' -AsPlainText -Force
$cred     = New-Object System.Management.Automation.PSCredential('ctf', $password)

while ($true) {
  try {
    # Launch quietly, discard child stdout/stderr to NUL, suppress PowerShell errors
    $p = Start-Process -FilePath $exe `
                       -WorkingDirectory $wd `
                       -Credential $cred `
                       -WindowStyle Hidden `
                       -PassThru `
                       -ErrorAction SilentlyContinue

    if ($p) {
      Wait-Process -Id $p.Id  # block until it exits
    } else {
      Start-Sleep -Seconds 1  # failed to start; brief backoff without logging
    }
  } catch {
    Start-Sleep -Seconds 1    # swallow errors; keep looping silently
  }
}