## City Climate WebApp

If you have ever wondered which cities have similar climates you might be tempted to look up a world map of the different climate zones, however these climates are fairly broadly defined so cities with quite different climates can end up in the same zone. Also, due to the hard boundary between climate zones, border cities (like Frankfurt or Philadelphia) can have cities in a different climate zone that are more similar to them than others in their own zone. 

This the Python based app compares detailed climate data from throusands of cities and calculate how similar they are. For more details check out the [web app](http://www.david-guszejnov.com/climate_app) and [blog post](https://medium.com/@guszejnov.david/data-science-based-climate-zones-24fd5085d24).

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

## Deploying on Amazon Lightsail
Add the following as launch script:
```
sudo curl -o lightsail-compose.sh https://raw.githubusercontent.com/guszejnovdavid/City_Climate_WebApp/main/lightsail_compose.sh

sudo chmod +x ./lightsail-compose.sh

sudo ./lightsail-compose.sh
```
If you are running low on memory, you can enable swapping (disabled on AWS Lightsail by default):
```
sudo fallocate -l 512MB /swapfile

sudo chmod 600 /swapfile

sudo mkswap /swapfile

sudo swapon /swapfile
```

