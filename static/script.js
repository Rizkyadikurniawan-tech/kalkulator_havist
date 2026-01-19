// Data destinasi per daerah
const DESTINASI = {
    "Jawa Tengah": ["Yogyakarta", "Solo", "Semarang"],
    "Jawa Timur": ["Bromo", "Malang", "Surabaya"],
    "Bali": ["Kuta", "Ubud", "Seminyak"]
};

function updateDestinasi() {
    const daerah = document.getElementById('daerah').value;
    const destinasiSelect = document.getElementById('destinasi');
    
    destinasiSelect.innerHTML = '<option value="">Pilih Destinasi</option>';
    destinasiSelect.disabled = true;
    
    if (daerah && DESTINASI[daerah]) {
        DESTINASI[daerah].forEach(dest => {
            const option = document.createElement('option');
            option.value = dest;
            option.textContent = dest;
            destinasiSelect.appendChild(option);
        });
        destinasiSelect.disabled = false;
    }
    
    checkFormComplete();
}

function checkFormComplete() {
    const fields = ['daerah', 'destinasi', 'bus', 'hotel', 'peserta'];
    const allFilled = fields.every(id => document.getElementById(id).value);
    document.getElementById('hitungBtn').disabled = !allFilled;
}

document.getElementById('wisataForm').addEventListener('input', checkFormComplete);
document.getElementById('wisataForm').addEventListener('change', checkFormComplete);

document.getElementById('wisataForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        daerah: document.getElementById('daerah').value,
        destinasi: document.getElementById('destinasi').value,
        bus: document.getElementById('bus').value,
        hotel: document.getElementById('hotel').value,
        peserta: document.getElementById('peserta').value,
        malam: document.getElementById('malam').value
    };
    
    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        displayResult(result);
    } catch (error) {
        alert('Error menghitung biaya: ' + error.message);
    }
});

function displayResult(result) {
    document.getElementById('totalBiaya').textContent = result.total;
    document.getElementById('perOrang').textContent = result.per_orang;
    
    const rincianList = document.getElementById('rincianList');
    rincianList.innerHTML = '';
    
    for (const [kategori, harga] of Object.entries(result.rincian)) {
        const div = document.createElement('div');
        div.className = 'rincian-item';
        div.innerHTML = `
            <span>${kategori}</span>
            <span>${harga}</span>
        `;
        rincianList.appendChild(div);
    }
    
    document.getElementById('hasil').classList.remove('hidden');
}
