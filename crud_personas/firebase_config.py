import firebase_admin
from firebase_admin import credentials, db

# Inicializar la aplicación Firebase con las credenciales descargadas
cred = credentials.Certificate('apphornoporconveccion-firebase-adminsdk-cx87u-0de8e96d75.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://apphornoporconveccion-default-rtdb.firebaseio.com/'  # Cambia esto con tu URL de base de datos
})

import pyrebase  # O cualquier librería que uses para interactuar con Firebase

def get_firebase_db():
    config = {
        "apiKey": "tu_api_key",
        "authDomain": "tu_auth_domain",
        "databaseURL": "tu_database_url",
        "projectId": "tu_project_id",
        "storageBucket": "tu_storage_bucket",
        "messagingSenderId": "tu_messaging_sender_id",
        "appId": "tu_app_id"
    }

    firebase = pyrebase.initialize_app(config)
    return firebase.database()
