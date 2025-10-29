from flask import Flask, request, render_template, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os, re, json

app = Flask(__name__)
app.secret_key = '12345678'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

USERS_DB = 'users.json'
if not os.path.exists(USERS_DB):
    with open(USERS_DB, 'w', encoding='utf-8') as f:
        json.dump([], f)

email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
password_re = re.compile(r'(?=.*[A-Z])(?=.*\d).{8,}')
phone_re = re.compile(r'^[0-9+\-\s]{7,15}$')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_user(data):
    with open(USERS_DB, 'r+', encoding='utf-8') as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            users = []
        users.append(data)
        f.seek(0)
        json.dump(users, f, ensure_ascii=False, indent=2)
        f.truncate()
@app.route('/')
def home():
    """Redirige al login al abrir la app"""
    return redirect(url_for('login'))


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener los campos según los name del HTML
        full_name = request.form.get('fullName', '').strip()
        doc_type = request.form.get('docType', '').strip()
        doc_number = request.form.get('docNumber', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        phone = request.form.get('phone', '').strip()
        city = request.form.get('city', '').strip()
        bio = request.form.get('bio', '').strip()
        skills = request.form.get('skills', '').strip()
        terms = request.form.get('terms')
        privacy = request.form.get('privacy')

        errors = []

        # Validaciones
        if not full_name:
            errors.append('El nombre completo es obligatorio.')
        if not doc_type or not doc_number:
            errors.append('Tipo y número de documento son obligatorios.')
        if not email or not email_re.match(email):
            errors.append('Correo electrónico inválido.')
        if not password or not password_re.match(password):
            errors.append('Contraseña inválida. Debe tener mínimo 8 caracteres, 1 número y 1 mayúscula.')
        if not phone or not phone_re.match(phone):
            errors.append('Número de teléfono inválido.')
        if not city:
            errors.append('Ciudad/Localidad es obligatoria.')
        if not terms:
            errors.append('Debe aceptar los términos y condiciones.')
        if not privacy:
            errors.append('Debe aceptar la política de tratamiento de datos personales.')

        # Manejo de foto
        photo = request.files.get('profilePhoto')
        photo_filename = None
        if photo and photo.filename:
            if allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                photo_filename = os.path.join(UPLOAD_FOLDER, filename)
                photo.save(photo_filename)
            else:
                errors.append('Tipo de archivo para la foto no permitido.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('registro.html')

        # Guardar usuario
        user_data = {
            'full_name': full_name,
            'doc_type': doc_type,
            'doc_number': doc_number,
            'email': email,
            'password_hash': generate_password_hash(password),
            'phone': phone,
            'city': city,
            'bio': bio,
            'skills': skills,
            'photo': photo_filename
        }
        save_user(user_data)
        flash('✅ Registro exitoso. ¡Bienvenido(a) a Ofilink!', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')
# Fin del codigo Registrar
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Muestra el login y valida las credenciales"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Por favor ingresa tu correo y contraseña.', 'error')
            return render_template('login.html')

        try:
            with open(USERS_DB, 'r', encoding='utf-8') as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        user = next((u for u in users if u['email'] == email), None)
        if user and check_password_hash(user['password_hash'], password):
            session['user'] = user['full_name']
            flash(f'✅ Bienvenido(a), {user["full_name"]}', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Correo o contraseña incorrectos.', 'error')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    """Página después del login"""
    if 'user' not in session:
        flash('Debes iniciar sesión primero.', 'error')
        return redirect(url_for('login'))
    return f"<h1>Bienvenido, {session['user']} 👋</h1><p><a href='/logout'>Cerrar sesión</a></p>"


@app.route('/logout')
def logout():
    """Cierra la sesión"""
    session.clear()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
# Fin del codigo del Login
