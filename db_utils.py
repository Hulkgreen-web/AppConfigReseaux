import sqlite3
import bcrypt

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
                data TEXT NOT NULL,
                responsible_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (responsible_id) REFERENCES users(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                ip_entered TEXT NOT NULL,
                mask_entered TEXT NOT NULL,
                mode TEXT NOT NULL CHECK (mode IN ('classless', 'classful')),
                network_address TEXT NOT NULL,
                broadcast_address TEXT NOT NULL,
                subnet_mask TEXT NOT NULL,
                subnet TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ip_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                ip_to_check TEXT NOT NULL,
                network_ip TEXT NOT NULL,
                mask_str TEXT,
                mode TEXT NOT NULL CHECK (mode IN ('classless', 'classful')),
                belongs INTEGER,
                first_host TEXT,
                last_host TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
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
def check_password(password, hashed):
    # Vérifie si le mot de passe correspond au hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

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

# Point d'entrée pour tester les fonctions
if __name__ == "__main__":
    create_db()
    # Exemple d'ajout d'utilisateur (décommente pour tester)
    # add_user('test_user', 'test123')