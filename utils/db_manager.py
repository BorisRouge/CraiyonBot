import psycopg2




class Database:
    """Менеджер базы данных."""
    def __init__(self, db_conf: str, log):
        self.db_conf = db_conf
        self.log = log
        self.start_up()

    def start_up(self):
        con = psycopg2.connect(self.db_conf)
        cur = con.cursor()
        try:
            cur.execute("""SELECT * FROM users""")
            self.log.warning("Таблица users - OK")
        except psycopg2.Error:
            self.log.warning("Таблицы users не существует. Создается...")
            con.rollback()
            self.create_table_users()
        con.close()

    def create_table_users(self):
        """Создать таблицу пользователей."""
        con = psycopg2.connect(self.db_conf)
        cur = con.cursor()
        try:
            cur.execute(    # TODO: add picname to the table (consider also distinction of NNs)
                """CREATE TABLE users (
                user_id BIGINT,
                pic_id SERIAL,
                filepath VARCHAR);"""
            )
            con.commit()
            self.log.warning("Таблица users создана.")
        except psycopg2.Error as e:
            self.log.error(f"Таблица users не создана, по причине {e.pgerror}")
            con.rollback()

    def user_info(self, user_id: int):
        """Проверка наличия пользователя в базе.
        Возращает текущий баланс счета или ложное значение."""

        con = psycopg2.connect(self.db_conf)
        cur = con.cursor()
        try:
            cur.execute(
                        f"""SELECT *
                            FROM users
                            WHERE user_id = '{user_id}';"""
            )
            user_data = cur.fetchone()
            if user_data == None:
                raise TypeError
            self.log.info('Успешный запрос данных о пользователе.')
            return user_data

        except (psycopg2.Error, TypeError) as e:
            self.log.error('При поиске в базе данных '
                     +'не найден идентификатор пользователя.', e
                     )
            return False

    def user_create(self, user_id: int):
        """Создание пользователя с указанным идентификатором."""
        con = psycopg2.connect(self.db_conf)
        cur = con.cursor()
        cur.execute(
                        f"""INSERT INTO users(user_id)
                         VALUES({user_id});"""
        )
        con.commit()
        con.close()
        self.log.info(f'Пользователь {user_id} внесен в базу данных.')

    def save_image_paths(self, user_id, paths: list):
        con = psycopg2.connect(self.db_conf)
        cur = con.cursor()
        for path in paths:
            cur.execute(
                f"""INSERT INTO users(user_id, filepath)
                                     VALUES({user_id},'{path}');"""
            )
        con.commit()
        con.close()

