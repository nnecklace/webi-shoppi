# Käyttäjätarinat ja Puuttuvat/Tulevat Ominaisuudet

Alla on kuvattu alustavat käyttäjätarinat. Käyttäjätarinoita lisätään enemmän projektin edetessä.

## Definition of Done
Tarina on tehty kun se on viety masteriin ja toimii Herokussa.

## Roolit

- Kuluttaja -- Käyttäjä joka ei ole välttämättä rekisteröitynyt palveluun
- Käyttäjä -- Käyttäjä joka on rekisteröitynyt palveluun
- Myyjä -- Käyttäjä joka on rekisteröitynyt ja jolla on tuotteita myynnissä

## Kyselyt

_Kyselyissä on käytetty sqlalchemyn placeholder-arvoja_.

### Kirjautuminen Ja Rekisteröiminen
- Käyttäjänä pystyn kirjautumaan sisään, jotta voin myydää tuotteita [DONE]
- Käyttäjänä pystyn rekisteröitymään, jotta voin myydä tuotteita [DONE]
- Käyttäjänä pystyn rekisteröitymään, jotta voin ostaa tuotteita [DONE]

```sql
INSERT INTO users (created_at, modified_at, first_name, last_name, email, username, password, balance) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(first_name)s, %(last_name)s, %(email)s, %(username)s, %(password)s, %(balance)s) RETURNING users.id
```

```sql
SELECT users.created_at AS users_created_at, users.modified_at AS users_modified_at, users.id AS users_id, users.first_name AS users_first_name, users.last_name AS users_last_name, users.email AS users_email, users.username AS users_username, users.password AS users_password, users.balance AS users_balance  
FROM users 
WHERE users.username = %(username_1)s
```

Kyselyn jälkeen tarkistetaan vielä, että käyttäjällä on oikea salasana:

```python
if check_pwd(user.password, password):
    return user
```

### Tuotteiden selailu
- Kuluttajana voin etsiä tuotteita hakusanoilla, jotta voin löytää nopeasti tuotteita [DONE]
- Kuluttajana voin etsiä tuotteita tuotekategorian (tai kategorioiden) perusteella, jotta pystyn "suodattaa" pois tuotteita, joita en halua tuotevalikoimaan [DONE]
- Kuluttajana voin etsiä tuotteita ilman kategoriaa [DONE]
- Kuluttajana voin etsiä tuotteita tietyn aikavälin perusteella [DONE]
- Kuluttajana voin etsiä kaupan halvin tuote [DONE]
- Kuluttajana voin etsiä useiden kategorioiden halvin tuote [DONE]
- Kuluttajana voin etsiä tuotteita, joiden hinta on enintään _x_ [DONE]
- Kuluttajana voin etsiä tuotteita myyjän nimen perusteella [DONE]
- Kuluttajana voin etsiä halvin tuote, jolla ei ole kategoriaa [DONE]

```sql
SELECT products.id, products.name, products.created_at, products.price, products.quantity, users.username 
FROM products 
LEFT JOIN categories_products 
ON categories_products.product_id = products.id 
LEFT JOIN categories 
ON categories.id = categories_products.category_id 
INNER JOIN users 
ON users.id = products.user_id 
WHERE products.quantity > 0 AND products.name LIKE %(name)s 
GROUP BY products.id, users.username 
ORDER BY products.created_at DESC
```

```sql
SELECT products.id, products.name, products.created_at, products.price, products.quantity, users.username 
FROM products 
LEFT JOIN categories_products 
ON categories_products.product_id = products.id 
LEFT JOIN categories 
ON categories.id = categories_products.category_id 
INNER JOIN users 
ON users.id = products.user_id 
WHERE products.quantity > 0 AND 
AND categories.id IN (SELECT categories.id FROM categories WHERE categories.id = %(cat_0)s OR categories.id = %(cat_1)s) 
GROUP BY products.id, users.username 
ORDER BY products.created_at DESC
```

```sql
SELECT products.id, products.name, products.created_at, products.price, products.quantity, users.username 
FROM products 
LEFT JOIN categories_products 
ON categories_products.product_id = products.id 
LEFT JOIN categories 
ON categories.id = categories_products.category_id 
INNER JOIN users 
ON users.id = products.user_id 
WHERE products.quantity > 0 AND 
GROUP BY products.id, users.username 
HAVING COUNT(categories_products.product_id) = 0 
ORDER BY products.created_at DESC
```

```sql
SELECT products.id, products.name, products.created_at, products.price, products.quantity, users.username 
FROM products 
LEFT JOIN categories_products 
ON categories_products.product_id = products.id 
LEFT JOIN categories 
ON categories.id = categories_products.category_id 
INNER JOIN users
ON users.id = products.user_id
WHERE products.quantity > 0 
AND products.created_at >= %(published_start)s AND products.created_at <= %(published_end)s
GROUP BY products.id, users.username
ORDER BY products.created_at DESC
```

```sql
SELECT products.id, products.name, products.created_at, products.price, products.quantity, users.username 
FROM products 
LEFT JOIN categories_products 
ON categories_products.product_id = products.id 
LEFT JOIN categories 
ON categories.id = categories_products.category_id 
INNER JOIN users 
ON users.id = products.user_id 
WHERE products.price = (SELECT MIN(products.price) FROM products) 
GROUP BY products.id, users.username 
ORDER BY products.created_at DESC
```

```sql
SELECT products.id, products.name, products.created_at, products.price, products.quantity, users.username 
FROM products 
INNER JOIN users 
ON users.id = products.user_id 
WHERE products.price = (
    SELECT MIN(products.price) FROM products
    LEFT JOIN categories_products 
    ON categories_products.product_id = products.id
    LEFT JOIN categories 
    ON categories.id = categories_products.category_id
    WHERE products.quantity > 0 
    AND categories.id IN (
        SELECT categories.id 
        FROM categories 
        WHERE categories.id = %(cat_0)s 
        OR categories.id = %(cat_1)s 
        OR categories.id = %(cat_2)s
    )
)
ORDER BY products.created_at DESC
```
Price alikyselyssä olevat joinit ovat turhia

```sql
SELECT products.id, products.name, products.created_at, products.price, products.quantity, users.username 
FROM products 
LEFT JOIN categories_products 
ON categories_products.product_id = products.id 
LEFT JOIN categories 
ON categories.id = categories_products.category_id 
INNER JOIN users 
ON users.id = products.user_id 
WHERE products.quantity > 0 AND 
AND products.price <= %(price)s 
GROUP BY products.id, users.username 
ORDER BY products.created_at DESC
```

```sql
SELECT products.id, products.name, products.created_at, products.price, products.quantity, users.username 
FROM products 
LEFT JOIN categories_products 
ON categories_products.product_id = products.id 
LEFT JOIN categories 
ON categories.id = categories_products.category_id 
INNER JOIN users 
ON users.id = products.user_id 
WHERE products.quantity > 0 
AND users.username LIKE %(seller)s 
GROUP BY products.id, users.username 
ORDER BY products.created_at DESC
```

```sql
SELECT products.id, products.name, products.created_at, products.price, products.quantity, users.username 
FROM products 
INNER JOIN users 
ON users.id = products.user_id 
WHERE products.price = (
    SELECT MIN(products.price) FROM products
    LEFT JOIN categories_products 
    ON categories_products.product_id = products.id
    LEFT JOIN categories 
    ON categories.id = categories_products.category_id
    WHERE products.quantity > 0 
    GROUP BY products.id, users.username 
    HAVING COUNT(categories_products.product_id) = 0 
)
ORDER BY products.created_at DESC
```

### Tuotteiden ostaminen
- Kuluttajana voin ostaa tuotteita (ei omia), mikäli minulla on tarpeeksi paljon saldoa (rahaa) [DONE]
- Käyttäjänä voin lisätä saldoa, jotta voin ostaa tuotteita [DONE]

```sql
UPDATE users SET modified_at=CURRENT_TIMESTAMP, balance=%(balance)s WHERE users.id = %(users_id)s
UPDATE products SET modified_at=CURRENT_TIMESTAMP, quantity=%(quantity)s WHERE products.id = %(products_id)s
```

```sql
UPDATE users SET modified_at=CURRENT_TIMESTAMP, balance=%(balance)s WHERE users.id = %(users_id)s
```

### Kommentit
- Käyttäjänä voin lisätä tuotteelle kommentin, jotta muut ihmiset näkevät mitä mieltä olin tuotteesta [DONE]
- Käyttäjänä voin listata kaikki yksittäisen tuotteen kommentit [DONE]

```sql
INSERT INTO comments (created_at, modified_at, content, product_id, user_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(content)s, %(product_id)s, %(user_id)s) RETURNING comments.id
```

_Kyselyssä käytetään eager loading_
```sql
SELECT products.id AS products_id, products.created_at AS products_created_at, products.modified_at AS products_modified_at, products.name AS products_name, products.price AS products_price, products.quantity AS products_quantity, products.user_id AS products_user_id, users_1.created_at AS users_1_created_at, users_1.modified_at AS users_1_modified_at, users_1.id AS users_1_id, users_1.first_name AS users_1_first_name, users_1.last_name AS users_1_last_name, users_1.email AS users_1_email, users_1.username AS users_1_username, users_1.password AS users_1_password, users_1.balance AS users_1_balance, categories_1.id AS categories_1_id, categories_1.created_at AS categories_1_created_at, categories_1.modified_at AS categories_1_modified_at, categories_1.name AS categories_1_name, users_2.created_at AS users_2_created_at, users_2.modified_at AS users_2_modified_at, users_2.id AS users_2_id, users_2.first_name AS users_2_first_name, users_2.last_name AS users_2_last_name, users_2.email AS users_2_email, users_2.username AS users_2_username, users_2.password AS users_2_password, users_2.balance AS users_2_balance, comments_1.id AS comments_1_id, comments_1.created_at AS comments_1_created_at, comments_1.modified_at AS comments_1_modified_at, comments_1.content AS comments_1_content, comments_1.product_id AS comments_1_product_id, comments_1.user_id AS comments_1_user_id 
FROM products 
LEFT OUTER JOIN users AS users_1 
ON users_1.id = products.user_id 
LEFT OUTER JOIN (categories_products AS categories_products_1 JOIN categories AS categories_1 ON categories_1.id = categories_products_1.category_id) 
ON products.id = categories_products_1.product_id 
LEFT OUTER JOIN comments AS comments_1 
ON products.id = comments_1.product_id 
LEFT OUTER JOIN users AS users_2 
ON users_2.id = comments_1.user_id 
WHERE products.id = %(param_1)s
```

### Tuotteiden myyminen
- Myyjänä pystyn laittamaan tuotteita myyntiin, jotta voin saada rahaa [DONE]
- Myyjänä pystyn antamaan yksittäiselle tuotteelle kategorian, jotta kuluttaja löytää kyseisen tuotteen oikeasta kategoriavalikoimasta [DONE]
- Myyjänä pystyn antamaan tuotteelle hinnan, jotta voin määritellä kuinka paljon kyseinen tuote maksaa [DONE]
- Myyjänä pystyn asettamaan tuotteiden määrä, jotta voin myydä tuotteesta useita kappaleita [DONE]
- Myyjänä pysytn poistamaan tuoteilmoitukseni, jotta kukaan ei enää pysty ostamaan kyseistä tuotetta [DONE]

```sql
INSERT INTO products (created_at, modified_at, name, price, quantity, user_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(name)s, %(price)s, %(quantity)s, %(user_id)s) RETURNING products.id
```

```sql
INSERT INTO products (created_at, modified_at, name, price, quantity, user_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(name)s, %(price)s, %(quantity)s, %(user_id)s) RETURNING products.id
```

```sql
INSERT INTO products (created_at, modified_at, name, price, quantity, user_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(name)s, %(price)s, %(quantity)s, %(user_id)s) RETURNING products.id
```

```sql
INSERT INTO products (created_at, modified_at, name, price, quantity, user_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(name)s, %(price)s, %(quantity)s, %(user_id)s) RETURNING products.id
INSERT INTO categories_products (category_id, product_id) VALUES (%(category_id)s, %(product_id)s)
```

```sql
DELETE FROM categories_products WHERE categories_products.category_id = %(category_id)s AND categories_products.product_id = %(product_id)s
DELETE FROM products WHERE products.id = %(id)s
```

### Ilmoituksien päivittäminen
- Myyjänä pystyn muokkaamaan ilmoituksessa olevan tuotteen nimeä [DONE] 
- Myyjänä pystyn muokkaamaan ilmoituksessa olevan tuotteen hintaa [DONE]
- Myyjänä pystyn muokkaamaan ilmoituksessa olevan tuotteen kpl määrää [DONE]
- Myyjänä pystyn lisäämään ilmoituksessa olevan tuotteeseen kategorian [DONE]

```sql
UPDATE products SET modified_at=CURRENT_TIMESTAMP, name=%(name)s WHERE products.id = %(products_id)s
```

```sql
UPDATE products SET modified_at=CURRENT_TIMESTAMP, price=%(price)s WHERE products.id = %(products_id)s
```

```sql
UPDATE products SET modified_at=CURRENT_TIMESTAMP, quantity=%(quantity)s WHERE products.id = %(products_id)s
```

```sql
UPDATE products SET modified_at=CURRENT_TIMESTAMP, quantity=%(quantity)s WHERE products.id = %(products_id)s
```

```sql
DELETE FROM categories_products WHERE categories_products.product_id = %(product_id_1)s AND categories_products.category_id NOT IN (%(category_id_1)s, %(category_id_2)s, %(category_id_3)s, %(category_id_4)s

INSERT INTO categories_products (category_id, product_id) VALUES (%(category_id)s, %(product_id)s)
```

### Tilin hallinta
- Käyttäjänä pystyn vaihtamaan salasanani [DONE]
- Käyttäjänä pystyn päivittämään tietojani, jotta tiedot pysyvät ajan tasalla [DONE]
- Käyttäjänä pystyn poistamaan tilini, jotta voin päästä eroon tilistäni [DONE]

```sql
UPDATE users SET modified_at=CURRENT_TIMESTAMP, password=%(password)s WHERE users.id = %(users_id)s
```

```sql
UPDATE users SET modified_at=CURRENT_TIMESTAMP, username=%(username)s, email=%(email)s, first_name=%(first_name)s, WHERE users.id = %(users_id)s
```

```sql
DELETE FROM users WHERE users.id = %(id)s
```


## Puuttuvat/Tulevat ominaisuudet

### Ostoskori

Alunperin olin ajatellut toteuttaa ostoskori ominaisuuden, jotta kuluttajat pystyisi lisäämään ja ostamaan useita tuotteita samaan aikaan. Tarkoitus oli, että käyttäjä voisi hallita oman ostoskorinsa, muokata tuotteiden kappalemäärää yms. Ja lopuksi käyttäjä olisi pystynyt varmistaa tilauksen ja antaa tarkempia tilaustietoja, kuten esim. lähiosoite yms.

### Luottokortin/Tilinsiirto validointi

Olin myös miettinyt, että saldoa lisätessä, käyttäjä olisi voinut valita millä tavalla saldoa lisätään. Luottokorttimaksulla, tilinsiirrolla tms. Ajattelin, että olisin voinut lisätä _stripe_ integraation sovellukseen, jotta luottokorttimaksujen ja tilinsiirrtojen toteuttaminen olisi ollut suhteellisen yksinkertaista. Samalla olisin voinut lisätä _osta ilman tiliä_ -ominaisuuden. Tällöin kuluttajan olisi voinut ostaa minkä tahansa tuotteen ilman rekisteröitymistä.

### Tuotekuva ja -kuvaus

Tuotteilta puuttuu tällä hetkellä kuvia ja kuvaus. Kuvat ja kuvaus auttaisi kuluttaja ymmärtämään mitä hän on ostamassa. Ajatuksena on, että kuvat säilytetään AWS-S3:ssa ja tietokannassa kuvauksen tietotyyppi olisi _text_. Itse  tietokannassa  ei olisi mitään tietoo tuotteenkuvista.

### Parempi etusivu

Tällä hetkellä etusivu on tosi kevyt. Etusivulla voisi vaikka näyttää tällä hetkellä suosituimmat tuotteet tms.

### Sisäänkirjautuminen sähköpostilla

Alunperin oli tarkoitus, että käyttäjä olisi voinut kirjautua sisään myös sähköpostiosoitteella. Tämä ominaisuus jäi kuitenkin toteuttamatta.

### Sivutus (engl pagination)

Tällä hetkellä jos tuotteita on useita, esim 10000, niin kaikki tuotteet näytetään yhdellä sivulla. Ts. sivusta tulee tosi pitkä ja epämukava käyttää. Parempi ratkaisu on lisätä sivunumerointi (eng. pagination). Näin voidaan rajoittaa tuotteiden määrä per sivu, esim 20/sivu. Voidaan myös muokata koodia ja sql-kyselyt. Sql-kyselyihin lisätään `LIMIT 20` ja http get parametreihin lisätään `page` argumentti jonka avulla voidaan määritellä sql-kyselyn mahdollinen _offset_ -arvo. 

Jos sivu = 2, niin sql-kysely = 

```sql
SELECT * 
FROM some_table
OFFSET 20
LIMIT 20
```
