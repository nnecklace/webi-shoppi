
# CREATE TABLE -lauseet

```sql
CREATE TABLE categories (
        id SERIAL NOT NULL,
        created_at TIMESTAMP WITHOUT TIME ZONE,
        modified_at TIMESTAMP WITHOUT TIME ZONE,
        name VARCHAR(100) NOT NULL,
        PRIMARY KEY (id)
)

CREATE TABLE users (
        created_at TIMESTAMP WITHOUT TIME ZONE,
        modified_at TIMESTAMP WITHOUT TIME ZONE,
        id UUID NOT NULL,
        first_name VARCHAR(150) NOT NULL,
        last_name VARCHAR(150) NOT NULL,
        email VARCHAR(150) NOT NULL,
        username VARCHAR(150) NOT NULL,
        password VARCHAR(150) NOT NULL,
        balance INTEGER,
        PRIMARY KEY (id),
        UNIQUE (id),
        UNIQUE (username)
)

CREATE TABLE products (
        id SERIAL NOT NULL,
        created_at TIMESTAMP WITHOUT TIME ZONE,
        modified_at TIMESTAMP WITHOUT TIME ZONE,
        name VARCHAR(150) NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER,
        user_id UUID NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
)

CREATE TABLE categories_products (
        category_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        PRIMARY KEY (category_id, product_id),
        FOREIGN KEY(category_id) REFERENCES categories (id),
        FOREIGN KEY(product_id) REFERENCES products (id) ON DELETE CASCADE
)

CREATE TABLE comments (
        id SERIAL NOT NULL,
        created_at TIMESTAMP WITHOUT TIME ZONE,
        modified_at TIMESTAMP WITHOUT TIME ZONE,
        content TEXT NOT NULL,
        product_id INTEGER NOT NULL,
        user_id UUID NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(product_id) REFERENCES products (id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
)
```
