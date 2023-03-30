import sqlite3
import datetime


################# USER AUTH :

def get_jwt_from_mail_password(mail:str, password:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT jwt FROM user WHERE mail=? AND password=?
                    """, (mail, password))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat

# print(get_jwt_from_mail_password('dvdbr@googlemail.com', 'azerty2'))

########################################################################################################
########################################### CREATE #####################################################
########################################################################################################

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
    
# create_user('mrdjb','david','breau','dvdbr@googlemail.com','azerty2', '1234')
# create_user('av','arnaud', 'vila', 'arnaudvila@gmail.com', '5678', '12345')
# create_user('olive','olivier', 'kotwica', 'okot@live.fr', '900.', '123456')

def create_action(company:str, value:float):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                 INSERT INTO action 
                 VALUES (NULL, ?, ?)
                 """, (company, value))
    connexion.commit()
    connexion.close()
    
# create_action('mcdo', 50.0)
# create_action('LVMH', 700.45)
# create_action('Air France', '1600.13')
    

def link_user_action(user_id:int, action_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()

    # Récupérer la valeur de l'action
    curseur.execute("""
                 SELECT value FROM action WHERE id = ?
                 """, (action_id,))
    value = curseur.fetchone()[0]

    # Enregistrer l'achat de l'utilisateur pour cette action
    curseur.execute("""
                 INSERT INTO user_action
                 VALUES (?, ?, ?, datetime('now'), NULL, NULL, NULL)
                 """, (user_id, action_id, value))

    connexion.commit()
    connexion.close()
# link_user_action(2,1)
# link_user_action(1,2)
# link_user_action(3,3)

def link_user_user(user_id_following:int, user_id_followed:int):
    if user_id_following == user_id_followed:
        print("Erreur: un utilisateur ne peut pas se suivre lui-même.")
        return

    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                 INSERT INTO user_user
                 VALUES (?, ?)
                 """, (user_id_following, user_id_followed))
    connexion.commit()
    connexion.close()

# link_user_user(1,2)
# link_user_user(1,3)
# link_user_user(3,1)
# link_user_user(1,1)
    
########################################################################################################
########################################### READ #######################################################
########################################################################################################

def get_user_from_mail(mail:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM user WHERE mail=?
                    """, (mail,))
    result = curseur.fetchall()
    connexion.close()
    return result

# print(get_user_from_mail('okot@live.fr'))

def get_user_id_from_mail(mail:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM user WHERE mail=?
                    """, (mail,))
    result = curseur.fetchone()
    connexion.close()
    return result

# print(get_user_id_from_mail('okot@live.fr'))

def get_actions_list():
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT company, value FROM action
                    """)
    result = curseur.fetchall()
    connexion.close()
    return result

# print(get_actions_list())

def get_user_id_from_jwt(jwt:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM user WHERE jwt=?
                    """, (jwt,))
    result = curseur.fetchone()
    connexion.close()
    if result is None:
        return None
    else:
        return result[0]

# print(get_user_id_from_jwt('1234'))

def get_user_s_actions_list(user_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT company, value FROM action
                        INNER JOIN user_action ON user_action.action_id = action.id
                        WHERE user_action.user_id = ? 
                    """, (user_id,))
    result = curseur.fetchall()
    connexion.close()
    return result

# print(get_user_s_actions_list(2))

def get_user_s_actions_sum(user_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT SUM(action.value) AS capital
                        FROM action
                        INNER JOIN user_action ON user_action.action_id = action.id
                        WHERE user_action.user_id = ? 
                    """, (user_id,))
    result = curseur.fetchall()
    connexion.close()
    return result[0]

# print(get_user_s_actions_sum(1))

def get_following_actions(user_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()

    # Récupérer les identifiants des utilisateurs que l'utilisateur suit
    curseur.execute("""
                     SELECT user_id_followed FROM user_user WHERE user_id_following=?
                     """, (user_id,))
    followed_users = [x[0] for x in curseur.fetchall()]

    # Récupérer les actions associées à ces utilisateurs
    curseur.execute("""
                     SELECT DISTINCT action.id, action.company, action.value
                         FROM action
                         INNER JOIN user_action ON user_action.action_id = action.id
                         WHERE user_action.user_id IN ({})
                     """.format(",".join(["?"]*len(followed_users))), followed_users)
    actions = curseur.fetchall()

    connexion.close()
    return actions

# print(get_following_actions(3))

########################################################################################################
########################################### UPDATE #####################################################
########################################################################################################



def update_action_value(new_value:int, action_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT value FROM action 
                        WHERE id=?
                    """, (action_id,))
    action_value = curseur.fetchone()
    curseur.execute("""
                    INSERT INTO action_value_change
                    VALUES (?, datetime('now'), ?)
                    """, (action_id, action_value[0]))
    curseur.execute("""
                    UPDATE action 
                        SET value = ?
                        WHERE id = ?
                    """, (new_value, action_id))

    connexion.commit()
    connexion.close()
    
# update_action_value(76,1)
    
def update_user_action_sold(user_id:int, action_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT value FROM action 
                        WHERE id=?
                    """, (action_id,))
    action_value = curseur.fetchone()
    curseur.execute("""
                    UPDATE user_action
                        SET sold = True, sold_value = ?, sold_time = datetime('now')
                        WHERE user_id = ? 
                            AND action_id = ?
                    """, (action_value[0], user_id, action_id))
    connexion.commit()
    connexion.close()
    
# update_user_action_sold(1,2)
# update_user_action_sold(1,1)
    
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
    
# update_token(1, '7878')

########################################################################################################
########################################### DELETE #####################################################
########################################################################################################

def delete_user(user_id:int):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    DELETE FROM user
                        WHERE id = ?
                    """, (user_id,))
    connexion.commit()
    connexion.close()
    
# delete_user(4)
# delete_user(5)

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

# unlink_user_user(1,2)




