# Käyttöohjeet

Seuraavassa dokumentissa käydään läpi sovelluksen ominaisuuksia, miten ominaisuudet toimivat, mitä ominaisuuksilla tehdään ja mahdollisia rajoitteita.

## Rekisteröityminen

Polku: `/register`

Sivulta löytyy rekisteröitymislomake. Lomaketta täyttämällä voit rekisteröityä palvelulle ja luoda tuoteilmoituksia ja voit kirjoittaa kommentteja. 

Lomakkeen kaikki kentät ovat pakollisia. Käyttäjätunnukset ovat uniikkeja (_ei toistuvia käyttäjätunnuksi_), minimipituus on 4 merkkiä, ja maksimipituus 150 merkkiä. Sähköposti täytyy olla validi sähköpostiosoite. Salasana täytyy olla vähintään 8 merkkiä pitkä ja sen täytyy sisältää ainakin yksi numero ja yksi seuraavista erikoismerkeistä: `_, /, @, |, -, +`. Salasanan maksimipituus on 56 merkkiä, tämä johtuu siitä, että sovelluksessa käytetään brcypt blowfish salaus algoritmia joka tuottaa pitkän hajautetun merkkijonon. Bcryptin yläraja on 72 merkkiä, tämä tarkoittaa sitä, että jos salasana on pidempi kuin 72 merkkiä, niin brcypt käyttää vain salasanan ensimmäiset 72 merkkiä. Eri lähteiden perusteella, yläraja voi myös olla 56, tämän takia päätin laittaa  ylärajaksi 56.

Rekisteröitymisen jälkeen sovellus ilmoittaa joko onnistuneesta tai epäonnistuneesta rekisteröitymisestä. Onnistuneen rekisteröitymisen jälkeen voit kirjautua sisään.

## Kirjautuminen

Polku: mikä tahansa

Kirjautumislomake löytyy jokaiselta (mikäli et ole kirjautunut sisään). Lomake löytyy oikeasta yläkulmasta. `Kirjaudu`- nappia painamalla voit paljastaa kirjautumislomakkeen. Lomake on vaatii validin käyttäjätunnus- & salasana kombinaation. Sovellus ilmoittaa mikäli kirjautuminen epäonnistui. Mikäli kirjautuminen onnistuu, niin sovellus uudelleenohjaa käyttäjää omalle käyttäjäprofiili-sivulle.

## Tuoteilmoitus

Polku: `/users/<username>/products/form`

Tuoteilmoituksen julkaiseminen vaatii sisäänkirjautumisen.

Tuoteilmoitus lomakeessa on kolmekenttää, joista jokainen on pakollinen, ja kategoriavalikoima, kategoriat ovat valinnaisia.
Tuotteen nimen maksimipituus on 150 merkkiä pitkä. Hinnan ja kappalemäärän maksimimäärät ovat 1073741824 (2^30). Tämä yläraja voisi olla suurempi. SQLiten suurin kokonaisluku on 64-bittinen numero (2^63).

Julkaisun jälkeen käyttäjää ohjataan tuotelistaus -sivulle.

## Tuoteiden selailu

Polku: `/products`

Tuotelista -sivu näyttää kaikki tuoteilmoitukset julkaisupäivämäärä järjestyksessä ja mikäli ilmoituksessa olevalla tuotteella on enemmän kuin 0 kappaletta jäljellä.

## Tuoteiden hakeminen

Polku: `/search`

Sivulta löytyy hakulomake. Hakulomake on toivottavasti mahdollisimman itsestäänselvä. Voit hakea tuotteita, nimen, hinnan, julkaisupäivämäärän, myyjän, kategorian perusteella. Voit myös yhdistää kriteerit, eli voit hakea vaikka kaikki tuoteilmoitukset jotka kuuluvat _auto_ -kategoriaan ja joiden hinta on korkeintaan 1000€ ja joissa on käytetty sanaa _audi_.

Tekstikentät ovat kaikki _case insensitive_ eli ei ole väliä miten kirjoitat myyjän nimi yms.

## Tuotteen ostaminen

Polku: `/products/<id>`

Sivulta näet tarkempia tietoja tuoteilmoituksesta. Sivulla on kanssa _osta_ -nappia, jota painamalla voit ostaa tuotetta. Mikäli ilmoituksesi on omasi, sinulla ei ole tarpeeksi saldoa, tai jos kappaleita ei ole ole enää, niin et voi ostaa tuotetta tässä tapauksessa. Sivulla voit myös listata kaikki kommentit joita muut kuluttajat ovat jättäneet.

## Ilmoituksen päivittäminen

Polku: `/users/<username>/products/<id>`

Tuoteilmoituksen päivittäminen vaatii sisäänkirjautumisen.

Sivulta löytyy vastaavanlainen lomake kuin tuoteilmoitus sivulla. Samat säännöt pätee tässäkin lomakkeessa. Lomakkeessa voi muokata tuotteen nimeä, hintaa, kappalemäärää ja lisätä/poistaa kategoriat.

## Ilmoituksen poistaminen

Polku: `/users/<username>/products/<id>`

Tuoteilmoituksen poistaminen vaatii sisäänkirjautumisen.

Äsken mainitulla sivulla on myös _poista ilmoitus_ -nappi. Tätä nappia painamalla voit poistaa tuoteilmoituksen. Tuoteilmoituksen poistaminen poistaa kanssa kaikki tuoteilmoituksen kommentit.

## Tilin tietojen päivittäminen

Polku: `/users/<username>`

Tilin päivittäminen vaatii sisäänkirjautumisen.

Kun kirjaudut sisään sinut uudelleenohjataan omalle profiilisivulle. Profiilisivulta löytyy lomake, jolla voi päivittää omia tietojasi. Lomakkeessa pätee samat säännöt kuin rekisteröitymislomakkeessa.

## Saldon lisääminen

Polku: `/users/<username>/balance`

Saldon lisääminen vaatii sisäänkirjautumisen.

Sivulta löytyy yksinkertainen lomake, jossa on ainoastaan yksi kenttä. Kenttää voit kirjoittaa kuinka paljon saldoa haluat lisätä. Saldon maksimimäärä on sama kuin kaikki muut maksimimäärät mitkä tässä dokumentissa on mainittu. (2^30)

Negatiivisiä lukuja ei sallita.

## Salasanan vaihto

Polku: `/users/<username>`

Salasanan vaihtaminen vaatii sisäänkirjautumisen.

Profiili sivulta löytyy _vaihda salasana_ -nappi. Nappia painamalla avautuu _salasanan vaihto modaali-ikkuna_. Ikkunnassa on pieni lomake. Lomakkeessa on kolme kenttää, joista jokainen on pakollinen. Salasanan säännöt ovat samat kuin rekisteröitymislomakkeessa. 

Salasanan vaihto onnistuu vain, jos kirjoitat oikean vanhan salasanan, ja uuden validi salasanan.

## Tilin poistaminen

Polku: `/users/<username>`

Tilin poistaminen vaatii sisäänkirjautumisen.

Profiilisivulta löytyy _poista tilisi_ -nappi. Nappia painamalla poistat tilisi, nappia painamalla sovellus haluaa varmistaa että olet varma, että oikeasti haluat poistaa tilisi. Kun tilisi poistetaan, samalla poistetaan kaikki sinun lisäämät kommentit, ja kaikki sinun lisäämät tuoteilmoitukset.

SQLitessä tilin poistaminen ei poista muuta kuin käyttäjän tiedot, kommentit ja tuoteilmoitukset jäävät tietokantaan.

## Kommenttien lisääminen

Polku: `/products/<id>`

Kommentin lisääminen vaatii sisäänkirjautumisen.

Sivulta pääset katsomaan kaikki kommentit joita kuluttajat ovat jättäneet. Voit itse antaa kommentin kirjoittamalla kommentin kommentti-kenttää ja painamalla lähetä. Mikäli kommentin lisääminen onnistuu, näkyy se tuotteen kommenttilistassa.
