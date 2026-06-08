import sqlite3

def connexion():
    conn = sqlite3.connect('sobemat.db')
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
            revision  TEXT,
            photos    TEXT,
            boite     TEXT,
            puissance TEXT,
            equipements TEXT               
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Base de données créée avec succès !")

def ajouter_vehicule(marque, modele, annee, km, moteur, couleur, prix, etat, revision, boite, puissance,  equipements):
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vehicules 
        (marque, modele, annee, km, moteur, couleur, prix, etat, revision, boite, puissance, equipements )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (marque, modele, annee, km, moteur, couleur, prix, etat, revision, boite, puissance, equipements ))
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
    conn.commit()
    conn.close()

def get_couleurs():
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT couleur from vehicules')
    conn.commit()
    conn.close()    

def get_marques():
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT marque from vehicules')
    conn.commit()
    conn.close() 

def get_moteurs():
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT moteur from vehicules')
    conn.commit()
    conn.close() 

def get_etats():
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT etat from vehicules')
    conn.commit()
    conn.close()  
if __name__ == '__main__':
    creer_table()
