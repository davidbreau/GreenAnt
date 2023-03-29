import sqlite3  

connexion = sqlite3.connect('bdd.db')
curseur = connexion.cursor()

# TABLES

curseur.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    mail TEXT NOT NULL,
                    password TEXT NOT NULL,
                    token TEXT NOT NULL 
                )
                """)

curseur.execute("""
                CREATE TABLE IF NOT EXISTS action (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    value FLOAT NOT NULL
                )
                """)

# TABLES D'ASSOCIATIONS

curseur.execute("""
                CREATE TABLE IF NOT EXISTS user_action (
                    user_id INTEGER,
                    action_id INTEGER,
                    bought_value FLOAT NOT NULL,
                    bought_time TEXT NOT NULL,
                    sold BOOLEAN DEFAULT FALSE,
                    sold_value FLOAT DEFAULT NULL,
                    sold_time TEXT DEFAULT NULL,
                    FOREIGN KEY (user_id) REFERENCES user(id),
                    FOREIGN KEY (action_id) REFERENCES action(id)
                )
                """)

curseur.execute("""
                CREATE TABLE IF NOT EXISTS user_user (
                    user_id_following INTEGER,
                    user_id_followed INTEGER,
                    FOREIGN KEY (user_id_following) REFERENCES user(id),
                    FOREIGN KEY (user_id_followed) REFERENCES user(id)
                )
                """)

curseur.execute("""
                CREATE TABLE IF NOT EXISTS action_value_change (
                    action_id INTEGER,
                    time TEXT NOT NULL,
                    value FLOAT NOT NULL,
                    FOREIGN KEY (action_id) REFERENCES action(id)
                )
                """)

connexion.commit()
connexion.close()