#!/bin/sh
service vsftpd start
echo "Started vsftpd service"
chmod 555 /www/user/media
echo "Adjusted permissions for media dir for FTP compatibility"