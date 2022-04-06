upstream Ferumbel{
    server django:8000
}
server {
    listen 80;
    listen [::]:80

    location / {
        proxy_pass http://django;
        proxy_set_header X-Forwarded $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

     location /media/ {
       alias /home/maksim/Ferumbel/Rerumel/Ferumbel/media/;
     }

     location /static/ {
       alias /home/maksim/Ferumbel/Rerumel/Ferumbel/static/;
     }
}