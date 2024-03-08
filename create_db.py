import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from faker import Faker
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

# https://simple.wikipedia.org/wiki/Voivodeships_of_Poland - for voivo

# Access environment variables
dotenv_path = 'env_var.env'
load_dotenv(dotenv_path)

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# Elements for faking data
fake = Faker()
voivodeships = [
    "Dolnośląskie",  # Wrocław
    "Kujawsko-pomorskie",  # Bydgoszcz
    "Lubelskie",  # Lublin
    "Lubuskie",  # Gorzów Wielkopolski
    "Łódzkie",  # Łódź
    "Małopolskie",  # Kraków
    "Mazowieckie",  # Warszawa
    "Opolskie",  # Opole
    "Podkarpackie",  # Rzeszów
    "Podlaskie",  # Białystok
    "Pomorskie",  # Gdańsk
    "Śląskie",  # Katowice
    "Świętokrzyskie",  # Kielce
    "Warmińsko-mazurskie",  # Olsztyn
    "Wielkopolskie",  # Poznań
    "Zachodniopomorskie"  # Szczecin
]
# To be sure that order has the same:
mapped_orders={i: [fake.random_element(elements=['completed', 'pending']), # status
                   fake.random_int(min=1, max=300), # same customer makes whole order 
                   fake.date_between(start_date='-2y', end_date='today')] # same date
                   for i in range(1, 1101)}

orders = []
n = 1
order = 1
while n < 1201:
    orders.append({
        'row_id': n,
        'order_id': order,
        'customer_id': mapped_orders[order][1],
        'product_id': fake.random_int(min=1, max=2),
        'quantity': fake.random_int(min=1, max=2),
        'order_date': mapped_orders[order][2],
        'status': mapped_orders[order][0]
    })
    n += 1
    if n % 15 == 0:
        orders.append({
            'row_id': n,
            'order_id': order,
            'customer_id': mapped_orders[order][1],
            'product_id': fake.random_int(min=1, max=2),
            'quantity': fake.random_int(min=1, max=2),
            'order_date': mapped_orders[order][2],
            'status': mapped_orders[order][0]
    })
    n += 1
    order += 1


customers = [
    {
        'customer_id': i + 1,
        'name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': f'{fake.random_element(elements=voivodeships)}'
    } for i in range(300)
]


products = [
    {
        'product_id': 1,
        'name': 'Smart Gardens',
        'price': round(fake.pyfloat(min_value=100.0, max_value=500.0), 2),
        'stock': fake.random_int(min=5, max=100)
    },
    {
        'product_id': 2,
        'name': 'Eco-Monitoring Systems',
        'price': round(fake.pyfloat(min_value=100.0, max_value=500.0),2),
        'stock': fake.random_int(min=5, max=100)
    }
]

orders_df = pd.DataFrame(orders)
products_df = pd.DataFrame(products)
customers_df = pd.DataFrame(customers)

# Create queries to add constrains for tables
queries = [
    "ALTER TABLE customers ADD CONSTRAINT pk_customers PRIMARY KEY (customer_id);",
    'ALTER TABLE products ADD CONSTRAINT pk_products PRIMARY KEY (product_id);',
    'ALTER TABLE orders ADD CONSTRAINT fk_orders_customers FOREIGN KEY (customer_id) REFERENCES customers(customer_id);',
    'ALTER TABLE orders ADD CONSTRAINT fk_orders_products FOREIGN KEY (product_id) REFERENCES products(product_id);'
]

# Establishing connection with DB and creating tables
try:
    engine = create_engine(f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
    orders_df.to_sql('orders', con=engine, if_exists='replace', index=False)
    products_df.to_sql('products', con=engine, if_exists='replace', index=False)
    customers_df.to_sql('customers', con=engine, if_exists='replace', index=False)

    # Add constrains
    with engine.connect() as connection:
        for query in queries:
            connection.execute(text(query))
except SQLAlchemyError as e:
    print(f'SQLAlchemy error: {e}')

