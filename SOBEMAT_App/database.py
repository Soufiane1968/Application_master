import sqlite3

def connexion():
    conn = sqlite3.connect('sobemat.db', check_same_thread=False)
    return conn

def creer_table():
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicules (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            marque    TEXT NOT NULL,
            modele    TEXT NOT NULL,
            annee     INTEGER,
            km        INTEGER,
            moteur    TEXT,
            couleur   TEXT,
            prix      REAL,
            etat      TEXT,
            photos    TEXT,
            boite     TEXT,
            puissance TEXT,
            equipements  TEXT,
            nb_portes    TEXT,
            nb_places    TEXT               
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Base de données créée avec succès !")


def ajouter_vehicule(marque, modele, annee, km, moteur, couleur, prix, etat, boite, puissance, equipements, nb_portes, nb_places):
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vehicules 
        (marque, modele, annee, km, moteur, couleur, prix, etat, boite, puissance, equipements, nb_portes, nb_places)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (marque, modele, annee, km, moteur, couleur, prix, etat, boite, puissance, equipements, nb_portes, nb_places))
    conn.commit()
    vehicule_id = cursor.lastrowid
    conn.close()
    return vehicule_id

def get_vehicule(vehicule_id):
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicules WHERE id = ?', (vehicule_id,))
    vehicule = cursor.fetchone()
    conn.close()
    return vehicule

def get_tous_vehicules():
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicules')
    vehicules = cursor.fetchall()
    conn.close()
    return vehicules

def supprimer_vehicule(vehicule_id):
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vehicules WHERE id = ?', (vehicule_id,))
    conn.commit()
    conn.close()


def get_boites():
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT boite from vehicules')
    boites = cursor.fetchall()
    conn.close()
    return boites

def get_couleurs():
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT couleur from vehicules')
    couleurs = cursor.fetchall()
    conn.close()
    return couleurs    

def get_marques():
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT marque from vehicules')
    marques = cursor.fetchall()
    conn.close()
    return marques    

def get_moteurs():
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT moteur from vehicules')
    moteurs = cursor.fetchall()
    conn.close()
    return moteurs

def get_modeles():
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT modele from vehicules')
    modeles = cursor.fetchall()
    conn.close()
    return modeles

def get_etats():
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT etat from vehicules')
    etats = cursor.fetchall()
    conn.close()
    return etats
    
if __name__ == '__main__':
    creer_table()
