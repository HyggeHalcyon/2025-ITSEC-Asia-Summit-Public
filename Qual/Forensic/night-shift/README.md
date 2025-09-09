# Forensic - Night Shift

1. Filter the log by the "is_malicious" parameter that has true value, it will sort out most of the log.
2. Analyze those logs by "payload" parameter. One of the log has payload value that will run RCE via SSTI and encoded flag.
3. Decode the flag using base64.
4. Flag: ITSEC{l0g_1s_1mp0rt4nt_7753a4b5}