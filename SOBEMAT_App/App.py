from flask import Flask, render_template, request, redirect, url_for
import database
import qrcode
import os

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

# ── Générer QR Code ────────────────────────────────────────────
def generer_qrcode(vehicule_id):
    # L'URL que le client verra en scannant
    url = f'http://192.168.1.121:5000/fiche/{vehicule_id}'
    
    
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


