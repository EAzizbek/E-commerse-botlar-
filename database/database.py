import asyncpg
from config import config
class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
    
    async def add_user(self, telegram_id, name, surename, age, phone):
        query = """
        INSERT INTO users (telegram_id, name, surename, age, phone_number)
        VALUES ($1, $2, $3, $4, $5)
        """
        await self.pool.execute(
            query, telegram_id, name, surename, int(age), phone
        )
    
    async def is_user_exists(self, telegram_id: int) -> bool:
        query = """
        SELECT EXISTS (
        SELECT 1 FROM users WHERE telegram_id = $1
        );
        """
        return await self.pool.fetchval(query, telegram_id)
    
    async def user_profile(self,telegram_id):
        query="""
        select name,age,phone_number,role from users where telegram_id=$1;
        """
        return await self.pool.fetchrow(query,telegram_id)
    
    async def get_user_role(self,telegram_id):
        query="""
        select role from users where telegram_id=$1;
        """
        return await self.pool.fetchval(query,telegram_id)
    
    async def get_users(self):
        query="""
        select name,role,telegram_id from users order by id;
        """
        return await self.pool.fetch(query)
    
    async def get_user_id(self,telegram_id):
        query="""
        select id from users where telegram_id=$1;
        """
        return await self.pool.fetchval(query,telegram_id)
    
    
    async def set_user_role(self,telegram_id,role):
        query="""
        update users set role=$1 where telegram_id=$2;
        """
        await self.pool.execute(query,role,telegram_id)

    #Products

    async def get_products(self):
        query="""
        select id,name,price,description from products order by id;
        """
        return await self.pool.fetch(query)
    
    async def add_product(self,name,price,description):
        query="""
        insert into products(name,price,description) values($1,$2,$3);
        """
        await self.pool.execute(query,name,int(price),description)

    async def delete_product(self,product_id):
        query="""
        delete from products where id=$1;"""
        await self.pool.execute(query,product_id)
    
    async def update_product(self,name,price,description,product_id):
        query="""
        update products set name=$1,price=$2,description=$3 where id=$4;
        """
        await self.pool.execute(query,name,int(price),description,product_id)
    
    #orders
    async def get_or_create_cart(self, user_id):

        order = await self.pool.fetchrow(
            """
            SELECT * FROM orders
            WHERE user_id=$1 AND order_status='cart'
            """,
            user_id
        )

        if order:
            return order["id"]

        order = await self.pool.fetchrow(
            """
            INSERT INTO orders(user_id)
            VALUES($1)
            RETURNING id
            """,
            user_id
        )

        return order["id"]
    

    async def add_product_to_cart(self, user_id, product_id):

        order_id = await self.get_or_create_cart(user_id)

        await self.pool.execute(
            """
            INSERT INTO order_items(order_id, product_id)
            VALUES($1,$2)
            """,
            order_id,
            product_id
        )
    
    async def get_cart_products(self, user_id):

        return await self.pool.fetch(
            """
            SELECT p.id, p.name, p.price
            FROM order_items oi
            JOIN orders o ON oi.order_id=o.id
            JOIN products p ON oi.product_id=p.id
            WHERE o.user_id=$1 AND o.order_status='cart'
            """,
            user_id
        )