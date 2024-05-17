server {     
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name jonatanlantonio.com;
    add_header Strict-Transport-Security "max-age=15552000; includeSubDomains" always;
    client_max_body_size 10M;

    location /ranking-app/api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_next_upstream error  timeout invalid_header http_500 http_502 http_503;         
        proxy_set_header Host $host;        
        proxy_set_header X-Real-IP $remote_addr;    
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;       
        proxy_read_timeout 5m;
        rewrite ^/ranking-app/api/(.*)$ /$1 break;
    }

    location /ranking-app/api {
        proxy_pass http://127.0.0.1:8000/;
        proxy_next_upstream error  timeout invalid_header http_500 http_502 http_503;         
        proxy_set_header Host $host;        
        proxy_set_header X-Real-IP $remote_addr;    
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;       
        proxy_read_timeout 5m;
        rewrite ^/ranking-app/api(.*)$ /$1 break;
    }

    listen [::]:443 ssl ipv6only=on;
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/jonatanlantonio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/jonatanlantonio.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}