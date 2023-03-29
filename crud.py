import sqlite3

# Create

def create_user(username: str, first_name:str, last_name:str, mail:str, password:str, token:str):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                 INSERT INTO user 
                 VALUES (NULL, ?, ?, ?, ?, ?, ?)
                 """, (username, first_name, last_name, mail, password, token))
    connexion.commit()
    connexion.close()
    

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

def actions_list():
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT company, value FROM action
                    """)
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

def user_s_actions_list(user_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT user.username, action.company FROM user_action
                        INNER JOIN action ON user_action.action_id = action.id
                        WHERE user_action.user_id = ? 
                    """, (user_id,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

            # FONCTION CAPITAL


# Upgrade

def change_action_value(new_value:int, action_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE action 
                        SET value = ?
                        WHERE id = ?
                    """, (new_value, action_id))
    connexion.commit()
    connexion.close()
    
def change_user_action(user_id:int, action_id:int, sold_value:float):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE user_action 
                        SET sold = True
                        SET sold_value = ?
                        SET sold_time = datetime('now')  
                        WHERE user_id = ? 
                            AND action_id = ?
                    """, (sold_value, user_id, action_id)) # time = GETDATE()
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
