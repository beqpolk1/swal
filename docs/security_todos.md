* nginx <-> web TLS
* web <-> mongo TLS
* mongo default credentials -> secure storage
* don't allow nginx to serve sensitive static content (e.g. .env)
* XSS sanitization on entry inputs
* Filter for specific formats & size limits on artwork file uploads
* Revisit FTP config for vulnerabilities
* Use SSL (or SFTP??) for FTP transfers web -> nginx