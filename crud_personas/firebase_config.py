import firebase_admin
from firebase_admin import credentials, db

# Inicializar la aplicación Firebase con las credenciales descargadas
cred = credentials.Certificate('apphornoporconveccion-firebase-adminsdk-cx87u-0de8e96d75.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://apphornoporconveccion-default-rtdb.firebaseio.com/'  # Cambia esto con tu URL de base de datos
})

# Obtener una referencia a la base de datos
def get_firebase_db():
    
    if not firebase_admin._apps:
        cred = credentials.Certificate("ruta/a/tu/archivo/firebase-adminsdk.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://tu-database.firebaseio.com/'
        })
    return db.reference('personas') # Cambia esto con la ruta de tu base de datos