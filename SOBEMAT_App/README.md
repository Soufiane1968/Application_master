# SOBEMAT — Vehicle Management System

SOBEMAT is a Flask-based web application designed to manage a vehicle inventory. The application allows administrators to list, add, modify, and delete vehicles. It automatically generates custom QR codes pointing to client-facing technical specification sheets (fiche technique) for each vehicle.

---

## 📁 Project Structure

Below is the directory structure of the repository:

```text
Application_master/
├── README.md                  # Main repository documentation
└── SOBEMAT_App/               # Main application directory
    ├── App.py                 # Flask application (routes and web server entry point)
    ├── database.py            # SQLite database initialization and helper functions
    ├── utils.py               # Shared utility/configuration variables (e.g. HOST_IP)
    ├── sobemat.db             # SQLite database storing vehicle records
    ├── static/                # Static assets (stylesheets, images, QR codes)
    │   ├── css/
    │   │   └── style.css      # Core styles for layouts, forms, and pages
    │   ├── qrcodes/           # Generated QR codes for vehicles (PNG format)
    │   └── logo_sobemat.png   # SOBEMAT branding logo
    └── templates/             # HTML templates for rendering pages
        ├── index.html         # Admin dashboard (listing all vehicles)
        ├── ajouter.html       # Interface/form to add new vehicles
        ├── modifier.html      # Interface/form to edit existing vehicles
        └── fiche.html         # Customer-facing detailed vehicle technical sheet
```

---

## 🐍 Python Files & Main Functions

### 1. `App.py`
This file serves as the web application entry point. It manages routing, form submissions, and QR code generation.

*   **`index()`** (Route: `/`): Fetches all vehicle records and renders the admin dashboard (`index.html`).
*   **`ajouter()`** (Route: `/ajouter`): Handles both `GET` (displays the add-vehicle form populated with existing choices) and `POST` (saves vehicle details, triggers QR code generation, and redirects to dashboard).
*   **`fiche(vehicule_id)`** (Route: `/fiche/<id>`): Public specification sheet view for clients. Displays vehicle data.
*   **`modifier(vehicule_id)`** (Route: `/modifier/<id>`): Displays the edit form filled with current vehicle data (`GET`) and saves edits to the database (`POST`).
*   **`supprimer(vehicule_id)`** (Route: `/supprimer/<id>`): Deletes the specified vehicle from the database and removes its generated QR code image from the file system.
*   **`QR_gen(vehicule_id)`** (Route: `/QR_gen/<id>`): Triggers regeneration of the QR code for a specific vehicle.
*   **`generer_qrcode(vehicule_id)`**: Helper function that creates a high-quality QR code pointing to the vehicle's public page (`{HOST_IP}/fiche/{vehicule_id}`) and saves it to `static/qrcodes/QR_{id}.png`.

### 2. `database.py`
Contains helper functions to interact with the SQLite database (`sobemat.db`).

*   **`connexion()`**: Establishes and returns a connection to the SQLite database.
*   **`creer_table()`**: Runs on startup to create the `vehicules` table if it does not exist.
*   **`ajouter_vehicule(...)`**: Inserts a new vehicle record into the database and returns its new ID.
*   **`get_vehicule(vehicule_id)`**: Fetches a single vehicle record by ID.
*   **`get_tous_vehicules()`**: Fetches all vehicles from the database.
*   **`supprimer_vehicule(vehicule_id)`**: Deletes a vehicle record by ID.
*   **Category Getters** (`get_marques()`, `get_modeles()`, `get_etats()`, `get_boites()`, `get_moteurs()`, `get_couleurs()`): Fetch distinct lists of values from existing records to populate dropdown lists dynamically in forms.

### 3. `utils.py`
A simple configuration file.
*   **`HOST_IP`**: Configures the base URL/IP (e.g., `http://172.22.74.250:5000`) used for generating QR codes, ensuring they point to the correct network address.

---

## 🚀 Git Operations (Pulling & Pushing)

### How to Pull Changes
Before starting to work, make sure you pull the latest version of the code from the remote repository:

```bash
# Fetch and merge changes from the remote main branch
git pull origin main
```

### How to Push Changes
When you are ready to share your changes, follow these steps:

1.  **Stage your changes**:
    ```bash
    git add .
    ```
    *(Note: `.gitignore` is configured to automatically ignore python caches like `__pycache__/` and compilation files like `*.pyc` to keep the repository clean).*

2.  **Commit the staged changes**:
    ```bash
    git commit -m "Describe the changes you made clearly"
    ```

3.  **Push to the remote repository**:
    ```bash
    git push origin main
    ```
