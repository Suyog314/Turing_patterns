
from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import matplotlib.pyplot as plt
import io
import os

app = Flask(__name__)

OUTPUT_PATH = "static/generated/pattern.png"

def gray_scott(u, v, Du, Dv, F, k, dt, steps):
    for _ in range(steps):
        Lu = -4 * u + np.roll(u, 1, 0) + np.roll(u, -1, 0) + np.roll(u, 1, 1) + np.roll(u, -1, 1)
        Lv = -4 * v + np.roll(v, 1, 0) + np.roll(v, -1, 0) + np.roll(v, 1, 1) + np.roll(v, -1, 1)
        uvv = u * v * v
        u += (Du * Lu - uvv + F * (1 - u)) * dt
        v += (Dv * Lv + uvv - (F + k) * v) * dt
    return u, v

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        F = float(request.form['F'])
        k = float(request.form['k'])
        u_val = float(request.form['u_val'])
        v_val = float(request.form['v_val'])

        size = 100
        u = np.ones((size, size)) * u_val
        v = np.zeros((size, size)) * v_val
        u[45:55, 45:55] = 0.5
        v[45:55, 45:55] = 0.25

        Du, Dv, dt, steps = 0.16, 0.08, 1.0, 10000
        u, v = gray_scott(u, v, Du, Dv, F, k, dt, steps)

        plt.imsave(OUTPUT_PATH, u, cmap='plasma')
        return jsonify({'status': 'success', 'image_url': '/' + OUTPUT_PATH})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    os.makedirs("generated", exist_ok=True)
    app.run(debug=True)

