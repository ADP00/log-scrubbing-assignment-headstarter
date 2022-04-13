# log-scrubbing-assignment-headstarter
Python code to scan through csv files and send an email alert when pii is found.

## Instructions
The only file that must be added is emails.json in the main directory.
It must be in the format:
```json
{
  "sender":"sender email",
  "receiver":"receiver email",
  "password":"sender's password"
}
```
The sender email must be a yahoo account, otherwise the code must be changed. If a yahoo account is used, a password must be generated for use with a third party application. This can be done in settings, account security, other ways to sign in.
