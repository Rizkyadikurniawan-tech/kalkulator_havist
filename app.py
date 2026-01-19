from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'wisata_admin_2026'

# Data harga (persistent di memory)
DAERAH_WISATA = {"Jawa Tengah": {"Yogyakarta": 500000, "Solo": 450000}, "Bali": {"Kuta": 800000}}
BUS_OPSI = {"Economy": 150000, "VIP": 350000}
HOTEL_OPSI = {"1 Bintang": 200000, "3 Bintang": 500000}
ADMIN_CREDENTIALS = {'havist': 'havist123'}

# Filter format angka
def format_number(value):
    return f'{value:,.0f}'
app.jinja_env.filters['format_number'] = format_number

@app.route('/')
def index():
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect(url_for('wisata'))
        return render_template('admin_login.html', error='Username atau password salah!')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    
    return render_template('admin_dashboard.html', 
                         username=session['admin_username'],
                         daerah_wisata=DAERAH_WISATA,
                         bus_opsi=BUS_OPSI,
                         hotel_opsi=HOTEL_OPSI)

@app.route('/wisata')
def wisata():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('index.html', 
                         daerah_wisata=DAERAH_WISATA,
                         bus_opsi=BUS_OPSI,
                         hotel_opsi=HOTEL_OPSI)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    daerah = data['daerah']
    destinasi = data['destinasi']
    bus = data['bus']
    hotel = data['hotel']
    peserta = int(data['peserta'])
    malam = int(data['malam'])
    
    biaya_wisata = DAERAH_WISATA.get(daerah, {}).get(destinasi, 0)
    biaya_bus = BUS_OPSI.get(bus, 0)
    biaya_hotel = HOTEL_OPSI.get(hotel, 0) * malam
    
    total = (biaya_wisata + biaya_bus + biaya_hotel) * peserta
    per_orang = total / peserta
    
    return jsonify({
        'total': f'Rp {total:,.0f}',
        'per_orang': f'Rp {per_orang:,.0f}',
        'rincian': {
            'Wisata': f'Rp {biaya_wisata:,.0f}',
            'Bus': f'Rp {biaya_bus:,.0f}',
            'Hotel': f'Rp {biaya_hotel * peserta:,.0f}'
        }
    })

# ===== KELOLA HARGA WISATA =====
@app.route('/admin/wisata')
def admin_wisata():
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    return render_template('admin_wisata.html', daerah_wisata=DAERAH_WISATA)

@app.route('/admin/wisata/add', methods=['GET', 'POST'])
def wisata_add():
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        daerah = request.form['daerah']
        destinasi = request.form['destinasi']
        harga = int(request.form['harga'])
        
        if daerah not in DAERAH_WISATA:
            DAERAH_WISATA[daerah] = {}
        DAERAH_WISATA[daerah][destinasi] = harga
        flash('Destinasi wisata berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_wisata'))
    
    return render_template('wisata_form.html', title="Tambah Destinasi Wisata", 
                         daerah="", destinasi="", harga="")

@app.route('/admin/wisata/delete/<daerah>/<destinasi>')
def wisata_delete(daerah, destinasi):
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    
    if daerah in DAERAH_WISATA and destinasi in DAERAH_WISATA[daerah]:
        del DAERAH_WISATA[daerah][destinasi]
        if not DAERAH_WISATA[daerah]:  # Hapus daerah jika kosong
            del DAERAH_WISATA[daerah]
        flash('Destinasi wisata berhasil dihapus!', 'success')
    return redirect(url_for('admin_wisata'))

# ===== KELOLA BUS & HOTEL =====
@app.route('/admin/transport')
def admin_transport():
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    return render_template('admin_transport.html', bus_opsi=BUS_OPSI, hotel_opsi=HOTEL_OPSI)

@app.route('/admin/bus/add', methods=['GET', 'POST'])
def bus_add():
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        nama = request.form['nama']
        harga = int(request.form['harga'])
        BUS_OPSI[nama] = harga
        flash('Opsi bus berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_transport'))
    
    return render_template('admin_form.html', title="Tambah Bus", 
                         form_type="bus_add", nama="", harga="")

@app.route('/admin/hotel/add', methods=['GET', 'POST'])
def hotel_add():
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        nama = request.form['nama']
        harga = int(request.form['harga'])
        HOTEL_OPSI[nama] = harga
        flash('Opsi hotel berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_transport'))
    
    return render_template('admin_form.html', title="Tambah Hotel", 
                         form_type="hotel_add", nama="", harga="")

@app.route('/admin/bus/delete/<nama>')
def bus_delete(nama):
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    if nama in BUS_OPSI: 
        del BUS_OPSI[nama]
        flash('Opsi bus berhasil dihapus!', 'success')
    return redirect(url_for('admin_transport'))

@app.route('/admin/hotel/delete/<nama>')
def hotel_delete(nama):
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    if nama in HOTEL_OPSI: 
        del HOTEL_OPSI[nama]
        flash('Opsi hotel berhasil dihapus!', 'success')
    return redirect(url_for('admin_transport'))

# ===== STATISTIK =====
@app.route('/admin/statistik')
def admin_statistik():
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    
    # Hitung statistik
    total_destinasi = sum(len(dest) for dest in DAERAH_WISATA.values())
    total_bus = len(BUS_OPSI)
    total_hotel = len(HOTEL_OPSI)
    
    return render_template('admin_statistik.html', 
                         total_destinasi=total_destinasi,
                         total_bus=total_bus,
                         total_hotel=total_hotel,
                         daerah_wisata=DAERAH_WISATA,
                         bus_opsi=BUS_OPSI,
                         hotel_opsi=HOTEL_OPSI)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Anda telah logout!', 'info')
    return redirect(url_for('admin_login'))

