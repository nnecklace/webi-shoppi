# webi-shoppi

Webi-Shopin tarkoitus on olla pieni ja kevyt verkkokauppapalvelu. Käyttjillä on mahdollisuus lisätä, ostaa, poistaa, varata tuotteita.
Käyttjillä on kaksi implisiittisiä rooleja, kuluttaja ja myyjä. Tuotteita voi olla useita. Myyjänä pystyt julkaisemaan tuotteita myytäväksi, asettaa hintaa omille tuotteille. Tuotteilla on yksi myyjä, useita kategorioita sekä useita kuluttajien jättämät kommentit.
Kuluttajana pystyt ostamaan tuotteita, mikäli tililläsi on rahaa tai luottokortilla. Kuluttajana pystyt arvostelemaan tuotteita jättämällä kommentteja. 

[Tietokantakaavio](https://github.com/nnecklace/webi-shoppi/blob/master/diagrams/diagram.md)

[Käyttäjätarinat](https://github.com/nnecklace/webi-shoppi/blob/master/documentation/features.md)

[Heroku](https://webi-shoppi.herokuapp.com/)

## Projektin asentaminen

Varmista, että sinulla on ainakin python 3.7 asennettuna.

Luo virtuaaliympäristö

```python3 -m venv venv```

```source venv/bin/activate```

Lataa projektin riippuvuudet

```pip install --upgrade pip```

```pip install -r requirements.txt```

## Tietokanta

Mikäli sinulla on docker asennettuna niin voit ajaa seuraavat kommenot.

```docker build -t tsoha-db .```

```docker run -it -d -p 5432:5432 tsoha-db```

Jos sinulla ei ole dockeria asennettuna niin voit luoda projektin kansioon `src` `database.db` tiedoston joka SQLite käyttää.

## Projektin ajaminen 

Dockerilla:

```python run.py```

SQLitella:

```ENV=SQLITE python run.py```

## Testaaminen

Herokussa on yksi testikäyttäjä: 
Käyttäjätunnus: `Test1`
Salasana: `password@1`

Voit luoda myös oman testikäyttäjän menemällä polkuun `/register` ja täyttämällä käyttäjätunnuslomakkeen. Salasana täytyy olla minimissään 8 merkkiä pitkä ja sen täytyy sisältää ainakin yhden numeron ja ainakin yksi seuraavista erikoismerkeistä: ` _, /, @, |, -, +`