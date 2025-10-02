import sqlite3
import hashlib

DB_FILE = 'network_admin.db'  # Nom du fichier de la base de données

def create_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Création de la table users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')

    # Création de la table decoupes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decoupes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            data TEXT NOT NULL,
            responsible_id INTEGER NOT NULL,
            FOREIGN KEY (responsible_id) REFERENCES users(id)
        )
    ''')

    # Création de la table des calculs réseau
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
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Création de la table de vérification des IPs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ip_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            ip_to_check TEXT NOT NULL,
            network_ip TEXT NOT NULL,
            mask_str TEXT,
            mode TEXT NOT NULL CHECK (mode IN ('classless', 'classful')),
            belongs INTEGER, -- BOOLEAN stocké comme 0 ou 1
            first_host TEXT,
            last_host TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de données créée avec succès !")

# Hashage du mot de passe pour la sécurité
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Ajout d'un utilisateur avec le mot de passe hashé
def add_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hash_password(password)))
        conn.commit()
        print(f"Utilisateur '{username}' ajouté !")
    except sqlite3.IntegrityError:
        print("Erreur : Nom d'utilisateur déjà pris.")
    finally:
        conn.close()

# Nouvelle fonction pour afficher le schéma
def show_schema():
    #ligne pour se connécter a la db
    conn = sqlite3.connect(DB_FILE)
    #on creé un cursor
    cursor = conn.cursor()
    # Cette commande SQL demande à SQLite de lister tous les noms des tables
    # Elle regarde dans une table spéciale appelée sqlite_master qui contient
    # les informations sur la structure de la base
    #elle récupere le nom des tables avec "type table"
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #recupère tous les noms des tables trouvé dans par la requête précédente stocké dans une liste de tuples
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for column in columns:
            print(f"  {column[1]} ({column[2]}) {'PRIMARY KEY' if column[5] else ''}")
    conn.close()

if __name__ == "__main__":
    create_db()  # Crée le schéma et les tables
    add_user('admin', 'password123')  # Ajoute un utilisateur test
    show_schema()  # Affiche le schéma