# note app revenge

- Set custom_theme to true, by ignoring options.js script.
- You need to use tag `<script>` to ignore the that script.
- Due to CSP and CSP violation handler, tag `<script>` only will redirect the page. Instead, `<script type="text/plain">` will solve the problem.
- To set the value of custom_theme to true, we can use DOM clobbering technique.
- Now, we got CSS Injection that can be abused to leak path of the flag.

# Ref