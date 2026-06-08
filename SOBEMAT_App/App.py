from flask import Flask, render_template, request, redirect, url_for
import database
import qrcode
import os

from utils import HOST_IP
app = Flask(__name__)

# Dossier pour sauvegarder les QR Codes
QR_FOLDER = 'static/qrcodes'

# ── Page d'accueil — liste tous les véhicules ──────────────────
@app.route('/')
def index():
    vehicules = database.get_tous_vehicules()
    return render_template('index.html', vehicules=vehicules)

# ── Ajouter un véhicule ────────────────────────────────────────
@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    if request.method == 'POST':
        marque   = request.form['marque']
        modele   = request.form['modele']
        annee    = request.form['annee']
        km       = request.form['km']
        moteur   = request.form['moteur']
        couleur  = request.form['couleur']
        prix     = request.form['prix']
        etat     = request.form['etat']
        revision = request.form['revision']
        boite    = request.form['boite']
        puissance    = request.form['puissance']
        equipements = request.form['equipements']



        # Ajouter dans la base de données
        vehicule_id = database.ajouter_vehicule(
            marque, modele, annee, km, moteur, couleur, prix, etat, revision, boite, puissance, equipements
        )

        # Générer le QR Code
        generer_qrcode(vehicule_id)

        return redirect(url_for('index'))

    return render_template('ajouter.html')

# ── Fiche technique — vue client ───────────────────────────────
@app.route('/fiche/<int:vehicule_id>')
def fiche(vehicule_id):
    vehicule = database.get_vehicule(vehicule_id)
    if vehicule is None:
        return "Véhicule non trouvé", 404
    return render_template('fiche.html', vehicule=vehicule)

# ── Supprimer un véhicule ──────────────────────────────────────
@app.route('/supprimer/<int:vehicule_id>')
def supprimer(vehicule_id):
    database.supprimer_vehicule(vehicule_id)
    # Supprimer aussi le QR Code
    qr_path = f'{QR_FOLDER}/QR_{vehicule_id}.png'
    if os.path.exists(qr_path):
        os.remove(qr_path)
    return redirect(url_for('index'))

# ── Modifier un véhicule ──────────────────────────────────────
@app.route('/modifier/<int:vehicule_id>', methods=['GET', 'POST'])
def modifier(vehicule_id):
    vehicule = database.get_vehicule(vehicule_id)
    if vehicule is None:
        return "Véhicule non trouvé", 404
    # Récupérer les catégories pour les menus déroulants
    marques = database.get_marques()
    etats = database.get_etats()
    couleurs = database.get_couleurs()
    boites = database.get_boites()
    moteurs = database.get_moteurs()

    if request.method == 'POST':
        vehicule[1] = request.form['marque']
        vehicule[2] = request.form['modele']
        vehicule[3] = request.form['annee']
        vehicule[4] = request.form['km']
        vehicule[5] = request.form['moteur']
        vehicule[6] = request.form['couleur']
        vehicule[7] = request.form['prix']
        vehicule[8] = request.form['etat']
        vehicule[9] = request.form['revision']
        vehicule[10] = request.form['boite']
        vehicule[11] = request.form['puissance']
        vehicule[12] = request.form['equipements']
        vehicule[13] = request.form['tel']
        vehicule[14] = request.form['mail']

        # Mettre à jour dans la base de données
        database.modifier_vehicule(
            vehicule_id,
            vehicule[1], vehicule[2], vehicule[3], vehicule[4], vehicule[5],
            vehicule[6], vehicule[7], vehicule[8], vehicule[9], vehicule[10],
            vehicule[11], vehicule[12], vehicule[13], vehicule[14]
        )
        
        return redirect(url_for('index'))
    
    return render_template('modifier.html', 
                           vehicule=vehicule,
                           marques=marques,
                           etats=etats,
                           couleurs=couleurs,
                           boites=boites,
                           moteurs=moteurs)
                           
# ── Générer QR Code ────────────────────────────────────────────
def generer_qrcode(vehicule_id):
    # L'URL que le client verra en scannant
    url = f'{HOST_IP}/fiche/{vehicule_id}'
    
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="#1F3864", back_color="white")
    img.save(f'{QR_FOLDER}/QR_{vehicule_id}.png')
    print(f"✅ QR Code généré pour le véhicule {vehicule_id}")

# ── Lancer l'application ───────────────────────────────────────
if __name__ == '__main__':
    database.creer_table()
    os.makedirs(QR_FOLDER, exist_ok=True)
    app.run(debug=True, host='0.0.0.0')


