## City Climate WebApp

If you have ever wondered which cities have similar climates you might be tempted to look up a world map of the different climate zones, however these climates are fairly broadly defined so cities with quite different climates can end up in the same zone. Also, due to the hard boundary between climate zones, border cities (like Frankfurt or Philadelphia) can have cities in a different climate zone that are more similar to them than others in their own zone. 

This the Python based app compares detailed climate data from throusands of cities and calculate how similar they are.

### Python/Flask application with Nginx proxy

Project structure:
```
.
├── compose.yaml
├── flask
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── server.py
│   ├── templates
│         ├── index.html
└── nginx
    ├── nginx.conf
    ├── static
```

## Deploy with docker compose

##Deploying on Amazon Lightsail
Add the following as launch script:
```
curl -o lightsail-compose.sh https://raw.githubusercontent.com/guszejnovdavid/City_Climate_WebApp/main/lightsail_compose.sh

chmod +x ./lightsail-compose.sh

./lightsail-compose.sh
```