from flask import Flask, request, render_template, session, redirect, url_for
import re
import os

app = Flask(__name__)
# Gunakan secret key tetap untuk CTF agar session tidak expire saat restart
app.secret_key = os.urandom(24)

# SECURITY PROTOCOL: REGEX AEGIS
# Memblokir keyword berbahaya agar player harus kreatif pakai chr() atau teknik lain
KEYWORDS = r'os|eval|exec|bind|connect|python|socket|ls|cat|shell'
REGEX_FILTER = r'0x[0-9A-Fa-f]+|\\u[0-9A-Fa-f]{4}|%[0-9A-Fa-f]{2}|\.[A-Za-z0-9]{1,3}\b|[\\\/]|\.\.|' + KEYWORDS

@app.route('/')
def index():
    user_info = session.get('user_data', {})
    return render_template('index.html', user=user_info, registered=bool(user_info))

@app.route('/update-profile', methods=['POST'])
def update_profile():
    name = request.form.get('name')
    nim = request.form.get('nim')
    ipk = request.form.get('ipk')
    bio = request.form.get('bio', '')
    
    error_msg = None
    # Proteksi Regex Aegis
    if re.search(REGEX_FILTER, bio, re.IGNORECASE):
        error_msg = "Regex Aegis: Malicious Activity Detected!"

    # Aktivasi Eval Mode via Header
    if request.headers.get('X-Activate-Eval') == 'true':
        session['eval_enabled'] = True

    session['user_data'] = {
        "name": name, "nim": nim, "ipk": ipk, "bio": bio, "error": error_msg
    }
    return redirect(url_for('preview'))

@app.route('/preview')
def preview():
    data = session.get('user_data')
    if not data:
        return redirect(url_for('index'))
    
    eval_mode = session.get('eval_enabled', False)
    payload = data.get('bio', '')
    
    if data.get('error'):
        output = data['error']
    elif eval_mode:
        try:
            # 1. Tentukan fungsi yang diizinkan untuk dipakai player
            safe_functions = {
                "open": open, 
                "chr": chr, 
                "str": str, 
                "len": len,
                "join": "".join, 
                "range": range, 
                "list": list,
                "dict": dict
            }
            
            # 2. FIXED: Inject safe_functions ke __builtins__
            # Ini supaya list comprehension [chr(x) for x in ...] bisa jalan
            # tanpa kena error 'name not defined'
            custom_globals = {
                "__builtins__": safe_functions
            }
            
            # 3. Eksekusi dengan globals yang sudah dimodifikasi
            res = eval(payload, custom_globals, {})
            output = str(res)
        except Exception as e:
            output = f"Python Execution Error: {str(e)}"
    else:
        output = payload

    return render_template('preview.html', user=data, rendered_bio=output, eval_active=eval_mode)

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Pastikan file flag.txt sudah ada di direktori yang sama
    app.run(host='0.0.0.0', port=5000, debug=True)