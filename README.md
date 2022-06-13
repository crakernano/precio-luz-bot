# Precio de la luz
[![Deploy](https://github.com/crakernano/precio-luz-bot/actions/workflows/deploy.yml/badge.svg)](https://github.com/crakernano/precio-luz-bot/actions/workflows/deploy.yml)
---
Pequeño bot para obtener el precio de la luz en España. Permite conocer las horas más caras, más baratas, la media del día... etc

## Como activarlo

### Opción con docker

1. Renombrar el fichero .env-example como .env y colocar en su interior el Token obtenido del bot BotFather en Telegram
2. Levantar el bot usando el comando docker-compose up

 
## Comandos
```
/resumen
```

Muestra un resumen de las tarifas del día, indicando la hora más cara, la más barata y la media. 

```
/maximo
```

Indica a que hora será más cara la luz durante el día de hoy y cual será su precio

```
/minimo
```

Indica a que hora será más barata la luz durante el día de hoy y cual será su precio

```
/media
```

Indica el precio medio del Kw/h durante el día de hoy

```
/mejores
```

Indica los intervalos más economicos del día, ideal para planificar el uso de los elementos que más consumen.

```
/hoy  
```

Muestr el calor de cada hora, así como una gráfica de la evolución del precio del kw/h a lo largo del día



## Ejemplo

![Ejemplo](https://www.crakernano.com/img/portfolio/bots/bot-luz.png)