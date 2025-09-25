import sqlite3
import hashlib

DB_FILE = 'network_admin.db'  # Nom du fichier de la base de données


def create_db():

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    # Création de la table users
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Création de la table decoupes
    cur.execute('''
        CREATE TABLE IF NOT EXISTS decoupes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            data TEXT NOT NULL,
            responsible_id INTEGER NOT NULL,
            FOREIGN KEY (responsible_id) REFERENCES users (id)
        )
    ''')

    con.commit()
    con.close()
    print("Base de données créée avec succès !")

#hashage du mdp pour la sécurité
def hash_password(password):
    #.encode convertis le mot de passe en octet binaire car la librairie hash du binaire
    return hashlib.sha256(password.encode()).hexdigest()

#on ajoute un utilisateur avec le mdp hashé
def add_user(username, password):

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    try:
        cur.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',(username, hash_password(password)))
        con.commit()
        print(f"Utilisateur '{username}' ajouté !")
    except sqlite3.IntegrityError:
        print("Erreur : Nom d'utilisateur déjà pris.")
    finally:
        con.close()


# Test initial
if __name__ == "__main__":
    create_db()
    add_user('admin', 'password123')  # Ajoute un utilisateur test