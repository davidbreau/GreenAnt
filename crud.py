import sqlite3
import datetime
from typing import Union

################# USER AUTH :


def get_jwt_from_mail_password(mail:str, password:str)-> Union[str, None]:
    """
    Gets a JSON Web Token (JWT) from the database using the email and password.

    Args:
        mail (str): The email of the user.
        password (str): The password of the user.

    Returns:
        The JWT if found, or None otherwise.
    """    
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT jwt FROM user WHERE mail=? AND password=?
                    """, (mail, password))
    result = curseur.fetchone()
    connexion.close()
    return result

# print(get_jwt_from_mail_password('dvdbr@googlemail.com', 'azerty2'))

########################################################################################################
########################################### CREATE #####################################################
########################################################################################################

def create_user(username: str, first_name:str, last_name:str, mail:str, password:str, jwt:str) -> int:
    """
    Creates a new user in the database with the given informations.

    Args:
        username (str): The username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        mail (str): The email of the user.
        password (str): The password of the user.
        jwt (str): The JSON Web Token (JWT) of the user.

    Returns:
        The ID of the new user as an integer.
    """
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

def create_action(company:str, value:float) -> None:
    """
    Creates a new action in the database with the given informations.

    Args:
        company(str): The name of the action based on the Company name as shown in actions courts.
        value(float): The initial value of the action (that will be set to updated values later on).
    """
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                 INSERT INTO action 
                 VALUES (NULL, ?, ?)
                 """, (company, value))
    connexion.commit()
    connexion.close()
    
def link_user_action(user_id:int, action_id:int) -> None:
    """
    Creates a new entry in the user_action association table to simulate the act to buy an action.

    Args:
        user_id (int): The ID of the user who's buying the action.
        action_id(int): The ID of the bought action.
    """
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()

    # Get action's actual value from its ID
    curseur.execute("""
                 SELECT value FROM action WHERE id = ?
                 """, (action_id,))
    value = curseur.fetchone()[0]

    # Save the bought action in the associatable with the user id, the action id, and the presearched action's value.
    # The null values are kept for the time the action will be sold
    curseur.execute("""
                 INSERT INTO user_action
                 VALUES (?, ?, ?, datetime('now'), NULL, NULL, NULL)
                 """, (user_id, action_id, value))

    connexion.commit()
    connexion.close()
    
# link_user_action(1,1)
# link_user_action(1,2)
# link_user_action(3,3)

def link_user_user(user_id_following:int, user_id_followed:int) -> None:
    """
    Creates a new entry in the user_user association table to simulate the action for one user to follow another user aiming to see his owned actions.

    Args:
        user_id_following(int): the id of the user who's following one other user.
        user_id_followed(int): the id of the user who's now followed by the previously specified user.
    """
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

def get_user_from_mail(mail:str) -> list :
    """
    Get all the informations of an user if it correlates to the specified email.
    
    Args:
        mail (str): The email of the user you want the complete informations of.

    Returns:
        A list containing a tuple with all the informations.
    """
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM user WHERE mail=?
                    """, (mail,))
    result = curseur.fetchall()
    connexion.close()
    return result

# print(get_user_from_mail('okot@live.fr'))

def get_user_id_from_mail(mail:str)-> tuple:
    """"
    Gets the id of the user if it correlated to the specified email
    
    Args:
        mail(str): The email of the user you want the id of.
    Returns :
        A tuple containing the ID of the corresponding user
    """
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM user WHERE mail=?
                    """, (mail,))
    result = curseur.fetchone()
    connexion.close()
    return result

# print(get_user_id_from_mail('davidbreau@live.fr'))

def get_actions_list():
    """
        Retrieves all actions from the database.
    Returns:
        A list of tuples representing each action with the company name and the actual value.
    """
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT company, value FROM action
                    """)
    result = curseur.fetchall()
    connexion.close()
    return result

# print(get_actions_list())

def get_users_list():
    """
    Retrieves all users from the database.
    Returns:
        A list of tuples representing each user.
    """
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id, first_name, last_name, mail FROM user
                    """)
    result = curseur.fetchall()
    connexion.close()
    return result

# print(get_users_list())

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

def get_user_s_actions_list(user_id:int)->list:
    """
    Shows all the action that are currently owned by the user detaining the specified ID, ignoring the actions that have been sold.
    
    Args:
        user_id(int): The id of the user you want to see the current actions
        
    Returns:
        A list of the actions bought but not yet sold.
    """
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT company, value FROM action
                        INNER JOIN user_action ON user_action.action_id = action.id
                        WHERE user_action.user_id = ? 
                            and user_action.sold != True
                    """, (user_id,))
    result = curseur.fetchall()
    connexion.close()
    return result

# print(get_user_s_actions_list(2))

def get_user_s_actions_sum(user_id:int)-> Union[int, None]:
    """
    Calculates the sum of the actions currently owned by the specified user to get the capital
    
    Args:
        user_id(int): The ID of the user
    Returns:
        The capital of the user as an integer, or None if the user don't have any action.
    """
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT SUM(action.value) AS capital
                        FROM action
                        INNER JOIN user_action ON user_action.action_id = action.id
                        WHERE user_action.user_id = ?
                            and user_action.sold != True 
                    """, (user_id,))
    result = curseur.fetchall()
    connexion.close()
    return result[0]

print(get_user_s_actions_sum(1))

def get_following_actions(user_id:int) -> list:
    """
    Shows individually all the actions that are owned by at least one followed user.
    
    Args:
        user_id(int): The id of the user you want to get the list of actions from followed users.
        
    Returns:
        A list of actions
    """
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

def get_action_id_from_company(company:str) -> int:
    """
    Returns the id of the actions that have the specified company name
    
    Args:
        company(str): Name of the company
        
    Returns:
        The ID as an integer
    """
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM action
                        WHERE company = ?
                    """, (company,))
    result = curseur.fetchone()
    connexion.close()
    return result[0]

def get_all_ids_followed(user_id:int) -> list:
    """
    Shows all the ids of the followed users from the specified user id.
    
    Args:
        user_id(int): id of the user
        
    Returns:
        A list containing a tuple of the ids
    """
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT user_id_followed from user_user
                        WHERE user_id_following = ?
                    """, (user_id,))
    result = curseur.fetchall()
    connexion.close()
    return result

# print(get_action_id_from_company('EDENRED'))

########################################################################################################
########################################### UPDATE #####################################################
########################################################################################################



def update_action_value(new_value:float, action_id:int) -> None:
    """
    Update the value of a specified action from its id, and stores the old value and the time it changed in the action_value_change table.
    
    Args:
        new_value(float): The value that will replaces its previous in the action table
        action_id(int): The id of the action
    """
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
    """
    Simulates the act from a user to sell it.
    Will look for the actual value of the specified action and store it as sold_value, automatically adding sold_time,
    And specifies that the action is now sold in the user_action table
    """
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
    """
    Changes the token of the specified user
    """
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE user
                        SET jwt = ?
                        WHERE id=?
                    """,(token, id))
    connexion.commit()
    connexion.close()
    
# update_token(1, 7878)
    
def update_mail(new_mail:str, user_id:int):
    """
    Updates the mail of the specified user.
    """
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE user 
                        SET mail = ?
                        WHERE id = ?
                    """, (new_mail, user_id))
    connexion.commit()
    connexion.close()

# update_mail('davidbr@live.fr', 1)

def update_password(new_password:str, user_id:int):
    """
    Updates the password of the specified user
    """
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE user 
                        SET password = ?
                        WHERE id = ?
                    """, (new_password, user_id))
    connexion.commit()
    connexion.close()

# update_password('azerty3', 1)

########################################################################################################
########################################### DELETE #####################################################
########################################################################################################

def delete_user(user_id:int):
    """
    Deletes specified user, will also delete all entries from the database where the user's id is used.
    """
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

def delete_action(action_id:int):
    """
    Deletes specified action, will also delete all entries from the database where the action's id is used.
    """
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    DELETE FROM action
                        WHERE id = ?
                    """, (action_id,))
    connexion.commit()
    connexion.close()
    
# delete_action(3)

def unlink_user_user(user_id_following:int, user_id_followed:int):
    """
    Simulates the the "unfollow" action.
    Deletes the link of the two users in the user_user action
    """
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




