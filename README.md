# webi-shoppi

Webi-Shopin tarkoitus on olla pieni ja kevyt verkkokauppapalvelu. Käyttjillä on mahdollisuus lisätä, ostaa, poistaa, varata tuotteita.
Käyttjillä on kaksi implisiittisiä rooleja, kuluttaja ja myyjä. Tuotteita voi olla useita. Myyjänä pystyt julkaisemaan tuotteita myytäväksi, asettaa hintaa omille tuotteille. Tuotteilla on yksi myyjä, useita kategorioita sekä useita kuluttajien jättämät kommentit.
Kuluttajana pystyt ostamaan tuotteita, mikäli tililläsi on rahaa tai luottokortilla. Kuluttajana pystyt arvostelemaan tuotteita jättämällä kommentteja. 

[Tietokantakaavio](https://github.com/nnecklace/webi-shoppi/blob/master/diagrams/diagram.md)

[Käyttäjätarinat](https://github.com/nnecklace/webi-shoppi/blob/master/documentation/features.md)

[Heroku](https://webi-shoppi.herokuapp.com/)

[CREATE TABLE -lauseet](https://github.com/nnecklace/webi-shoppi/blob/master/documentation/create_table.md)

[Käyttöohjeet](https://github.com/nnecklace/webi-shoppi/blob/master/documentation/manual.md)

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

Kun tietokanta on luoto, voit lisätä verkokaupalle tuotekategoriat

```insert into categories (name) values ('Koti'), ('Elektroniikka'), ('Elintarvike'), ('Kirja'), ('Auto'), ('Peli'), ('Urheilu'), ('Hyvinvointi'), ('Hygieni'), ('Viihde');```

## Projektin ajaminen 

Dockerilla:

```python run.py```

SQLitella:

```ENV=SQLITE python run.py```

Huom! Ohjelma voi toimia tosi epäluotettavasti SQLitella! Suosittelen dockeria tai lokaali postgres tietokanta.
Esim. Käyttäjätilin poistaminen voi aiheuttaa pahoja bugeja, joista yksi on semmoinen jossa seuraava käyttäjä perii äsken positetun käyttäjän tuotteet ja kommentit.

## Testaaminen

Herokussa on yksi testikäyttäjä: 
Käyttäjätunnus: `Test1`
Salasana: `password@1`

Voit luoda myös oman testikäyttäjän menemällä polkuun `/register` ja täyttämällä käyttäjätunnuslomakkeen. Salasana täytyy olla minimissään 8 merkkiä pitkä ja sen täytyy sisältää ainakin yhden numeron ja ainakin yksi seuraavista erikoismerkeistä: ` _, /, @, |, -, +`

## Heroku

Varmista, että sinulla on heroku-cli työkalu asennettuna.

Mikäli projektin juuressa ei ole `Procfile` -tiedostoa, niin voit luoda tiedoston seuraavalla komennolla.

```touch Procfile && echo "web: gunicorn --preload --workers 1 run:app" > Procfile```

Seuraavaksi voit luoda projektille heroku-projektin, projektia luodaan seuraavalla komennolla.

```heroku create <nimi> --buildpack heroku/python```

Asenna projektille tietokannan. Heroku tarjoaa ilmaisen postgres tietokannan. Voit asentaa tietokannan projektille seuraavalla komennolla.

```heroku addons:create heroku-postgresql:hobby-dev```

Projektissa käytetään `uuid v4` kirjastoa. Kirjaston tarkoitus on generoida ainutlaatuisia id arvoja käyttäjille. Kirjastoa täytyy asentaa erikseen.

Ota ensin yhteys tietokantaan.

```heroku pg:psql --app <nimi>```

Kun olet ottanut yhteyttä tietokantaan voit ajaa seuraavaa komentoa.

```CREATE EXTENSION IF NOT EXISTS "uuid-ossp";```

Nyt `uuid v4` kirjasto on asennettu.

Voit nyt siirtää sovelluksen herokuun komennolla.

```git push heroku master```

Kun sovellus on siirretty herokuun tietokantaan pitäisi vielä lisätä oletus kategorioita.

```heroku pg:psql --app <nimi>```
```insert into categories (name) values ('Koti'), ('Elektroniikka'), ('Elintarvike'), ('Kirja'), ('Auto'), ('Peli'), ('Urheilu'), ('Hyvinvointi'), ('Hygieni'), ('Viihde');```

Nyt voit kokeila sovellusta seilamessa. Seuraava komento avaa sovelluksen selaimessa.

```heroku open```


## Bugeja

Sovelluksessa on muutamia bugeja. Suurin osa bugeista johtuvat SQLitestä. SQLite ei tue `passive_deletes` eikä `DELETE ON CASCADE`. Tämä tarkoittaa sitä, että tuotteen poistaminen ei poista tuotteen kommentit. Samoin, jos käyttäjä poistaa tilinsä niin käyttäjän tuoteilmoitukset jäävät tietokantaan.
