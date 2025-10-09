import json
import sqlite3
import bcrypt
from typing import Dict, Any

# Fichier de la base de données
DB_FILE = 'network_admin.db'

# Fonction pour créer la base de données
def create_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS decoupes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                ip_entered TEXT NOT NULL,
                mask_entered TEXT NOT NULL,
                nb_sr_entered INTEGER NOT NULL,
                data TEXT NOT NULL,
                responsible_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (responsible_id) REFERENCES users(id)
            )
        ''')
        conn.commit()
        print("Base de données créée avec succès !")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la base : {e}")
    finally:
        conn.close()

# Fonction pour hacher le mot de passe avec bcrypt
def hash_password(password):
    # Convertit le mot de passe en bytes et génère un hash avec un sel
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# Fonction pour vérifier un mot de passe
def check_password(username,password):
    # Vérifie si le mot de passe correspond au hash
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        return bcrypt.checkpw(password.encode('utf-8'), result[0])
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return None
    finally:
        conn.close()

# Fonction pour récupérer le nom d'utilisateur dans la DB
def check_username(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return row[0] if row else None
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return None
    finally:
        conn.close()

def get_user_id(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return row[0] if row else None
    except sqlite3.Error as e:
        print("SQLite error: ", e)
        return None
    finally:
        conn.close()


# Fonction pour ajouter un utilisateur
def add_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        # Hache le mot de passe avec bcrypt
        password_hash = hash_password(password)
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        print(f"Utilisateur '{username}' ajouté !")
        return True
    except sqlite3.IntegrityError:
        print("Erreur : Nom d'utilisateur déjà pris.")
        return False
    finally:
        conn.close()

def add_decoupe(user_id, name,ip_entered,mask_entered,nb_sr_entered, data : Dict[int, Any]):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO decoupes (name,ip_entered,mask_entered,nb_sr_entered, data, responsible_id) "
                       "VALUES (?, ?, ?, ?, ?, ?)",
                       (name,ip_entered,mask_entered,nb_sr_entered, json.dumps(data, ensure_ascii=False, indent=4), user_id))
        conn.commit()
        print(f"Découpe '{name}' ajoutée !")
        return True
    except sqlite3.IntegrityError:
        print(f"Erreur: Une découpe existe déjà avec le nom {name} !")
        return False
    finally:
        conn.close()


def get_decoupe_by_name(name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT data FROM decoupes WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row is None:
            return None
        return json.loads(row[0])
    finally:
        conn.close()


def get_decoupes_by_id(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM decoupes WHERE responsible_id = ?", (user_id,))
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    finally:
        conn.close()

def get_info_entered(responsible_id, name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ip_entered, mask_entered, nb_sr_entered FROM decoupes WHERE responsible_id = ?"
                       " AND name = ?", (responsible_id, name))
        row = cursor.fetchone()
        return tuple(row) if row else None
    finally:
        conn.close()


def update_decoupe(responsible_id, name,ip_entered,mask_entered,nb_sr_entered, data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE decoupes SET ip_entered = ?, mask_entered = ?, nb_sr_entered = ?, data = ?"
            "WHERE name = ? AND responsible_id = ?",
            (ip_entered, mask_entered, nb_sr_entered,json.dumps(data,ensure_ascii=False,indent=4),
             name, responsible_id))
        conn.commit()
        print(f"Modification de la découpe '{name}' effectuée avec succès !")
        return True
    except sqlite3.IntegrityError:
        print(f"Erreur, une donnée est erronée")
        return False
    finally:
        conn.close()


# Point d'entrée pour tester les fonctions
if __name__ == "__main__":
    create_db()
    # Exemple d'ajout d'utilisateur (décommente pour tester)
    # add_user('test_user', 'test123')