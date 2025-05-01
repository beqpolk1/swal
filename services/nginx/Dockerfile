FROM nginx:1.26.2
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

ENV FTP_USER=swal_image \
    FTP_PASS=swallowth3p4ssword
    
RUN apt-get update \
    && apt-get install -y vsftpd \
    && apt-get clean

RUN rm /etc/vsftpd.conf
COPY vsftpd.conf /etc/vsftpd.conf
COPY 50-start-vsftpd.sh /docker-entrypoint.d

RUN useradd -m $FTP_USER \
    && echo "$FTP_USER:$FTP_PASS" | chpasswd \
    && echo "$FTP_USER" | tee -a /etc/vsftpd.user_list

EXPOSE 20 21 21100-21110