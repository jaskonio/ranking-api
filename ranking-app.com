server {     
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name jonatanlantonio.com;

    listen [::]:443 ssl ipv6only=on;
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/jonatanlantonio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/jonatanlantonio.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location /ranking-app/api {
        proxy_pass http://127.0.0.1:8000;
        proxy_next_upstream error  timeout invalid_header http_500 http_502 http_503;         
        proxy_set_header Host $host;        
        proxy_set_header X-Real-IP $remote_addr;    
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;       
        proxy_read_timeout 5m;
        rewrite ^/ranking-app/api(.*)$ $1 break;
    }


    location / {
        return 404;
    }

    # Excepciones para recursos específicos (por ejemplo, archivos CSS, JS, imágenes)
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg)$ {
        root /var/www/html;
        try_files $uri $uri/ =404;
    }

    location ~* /\.(ht|git|svn|hg) {
        return 404;
    }

    # Bloquear acceso a archivos ocultos
    location ~ /\.(?!well-known).* {
        return 404;
    }
}