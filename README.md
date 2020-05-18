# webi-shoppi

Webi-Shopin tarkoitus on olla pieni ja kevyt verkkokauppapalvelu. Käyttjillä on mahdollisuus lisätä, ostaa, poistaa, varata tuotteita.
Käyttjillä on kaksi implisiittisiä rooleja, kuluttaja ja myyjä. Tuotteita voi olla useita. Myyjänä pystyt laittamaan tuotteita myytäväksi, asettaa hintaa tuotteelle. Tuotteella on yksi myyjä, useita kategorioita sekä useita kuluttajien jättämät kommentit.
Kuluttajana pystyt ostamaan tuotteita, mikäli tililläsi on rahaa. Kuluttajana pystyt arvostelemaan tuotteita jättämällä kommentin tuotteelle. 

[Tietokantakaavio](https://github.com/nnecklace/webi-shoppi/blob/master/diagrams/diagram.md)

[Käyttäjätarinat](https://github.com/nnecklace/webi-shoppi/blob/master/documentation/features.md)

[Heroku](https://webi-shoppi.herokuapp.com/)

## Projektin asentaminen

Varmista, että sinulla on vähintään python 3.7 asennettuna.

Luo virtuaaliympäristö

```python3 -m venv venv```

```source venv/bin/activate```

Lataa projektin riippuvuudet

```pip install --upgrade pip```

```pip install -r requirements.txt```

## Tietokanta

Mikäli sinulla on docker asennettuna niin voit suorittaa seuraavat kommenot.

```docker build -t <joku-nimi> .```

```docker run -it -d -p 5432:5432 <joku-nimi>```

Jos sinulla ei ole dockeria asennettuna niin voit luoda projektin juureen `database.db` tiedoston ja käyttää SQLite.

## Projektin suorittaminen

Dockerilla:

```python run.py```

SQLitella:

```ENV=SQLITE python run.py```