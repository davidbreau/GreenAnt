import sqlite3
import datetime
# Create

def create_user(username: str, first_name:str, last_name:str, mail:str, password:str, jwt:str):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                 INSERT INTO user 
                 VALUES (NULL, ?, ?, ?, ?, ?, 1, ?)
                 """, (username, first_name, last_name, mail, password, jwt))
    user_id = curseur.lastrowid
    connexion.commit()
    connexion.close()
    return user_id
    

def create_action(company:str, value:float):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                 INSERT INTO action 
                 VALUES (NULL, ?, ?)
                 """, (company, value))
    connexion.commit()
    connexion.close()
    
def link_user_action(user_id:int, action_id:int, bought_value:float):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                 INSERT INTO user_action
                 VALUES (?, ?, ?, datetime('now'))
                 """, (user_id, action_id, bought_value))
    connexion.commit()
    connexion.close()
    
def link_user_user(user_id_following:int, user_id_followed:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                 INSERT INTO user_user
                 VALUES (?, ?)
                 """, (user_id_following, user_id_followed))
    connexion.commit()
    connexion.close()
    
def store_value_change(action_id:int, new_value:float):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                 INSERT INTO action_value_change
                 VALUES (?, datetime('now'), ?)
                 """, (action_id, new_value))
    connexion.commit()
    connexion.close()
    
# Read

def get_user_from_mail(mail:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM user WHERE mail=?
                    """, (mail,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

def get_user_id_from_mail(mail:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM user WHERE mail=?
                    """, (mail,))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat

def get_actions_list():
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT company, value FROM action
                    """)
    result = curseur.fetchall()
    connexion.close()
    return result

def get_user_s_actions_list(user_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT user.username, action.company FROM user_action
                        INNER JOIN action ON user_action.action_id = action.id
                        WHERE user_action.user_id = ? 
                    """, (user_id,))
    result = curseur.fetchall()
    connexion.close()
    return result

def get_user_s_actions_sum(user_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT user.username, action.company, SUM(action.value) AS capital
                        FROM user_action
                        INNER JOIN action ON user_action.action_id = action.id
                        INNER JOIN user ON user_action.user_id = user.id
                        WHERE user_action.user_id = ? 
                    GROUP BY user.username, action.company
                    """, (user_id,))
    result = curseur.fetchall()
    connexion.close()
    return result



# Update

def update_action_value(new_value:int, action_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE action 
                        SET value = ?
                        WHERE id = ?
                    """, (new_value, action_id))
    connexion.commit()
    connexion.close()
    
def update_user_action(user_id:int, action_id:int, sold_value:float):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE user_action 
                        SET sold = True
                        SET sold_value = ?
                        SET sold_time = datetime('now')  
                        WHERE user_id = ? 
                            AND action_id = ?
                    """, (sold_value, user_id, action_id))
    connexion.commit()
    connexion.close()
    
def update_token(id, token:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE user
                        SET jwt = ?
                        WHERE id=?
                    """,(token, id))
    connexion.commit()
    connexion.close()
    

# Delete

def delete_user(user_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    DELETE FROM user
                        WHERE user_id = ?
                    """, (user_id,))
    connexion.commit()
    connexion.close()

def unlink_user_user(user_id_following:int, user_id_followed:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    DELETE FROM user_user
                        WHERE user_id_following = ?
                        AND user_id_followed = ?
                    """, (user_id_following, user_id_followed))
    connexion.commit()
    connexion.close()

# USER AUTH :

def get_jwt_from_mail_password(mail:str, password:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT jwt FROM user WHERE mail=? AND password=?
                    """, (mail, password))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat



