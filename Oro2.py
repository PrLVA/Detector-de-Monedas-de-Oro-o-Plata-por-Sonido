import tkinter as tk
from tkinter import messagebox, filedialog
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

duration = 2
fs = 44100
audio_oro = None
fft_oro = None
audio_prueba = None
fft_prueba = None

def grabar_audio():
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    return audio.flatten()

def extraer_fragmento(audio, threshold=0.03, margen=1000):
    idx = np.where(np.abs(audio) > threshold)[0]
    if len(idx)==0: return audio
    ini = max(idx[0]-margen,0)
    fin = min(idx[-1]+margen, len(audio))
    return audio[ini:fin]

def graficar(audio, fs, titulo="Audio"):
    tiempo = np.arange(audio.size) / fs
    plt.figure(figsize=(10, 2.5))
    plt.plot(tiempo, audio)
    plt.title(f"Forma de onda - {titulo}")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.tight_layout()
    plt.show()

def graficar_fft(audio, fs, titulo="FFT"):
    N = len(audio)
    yf = fft(audio)
    xf = fftfreq(N, 1 / fs)
    idx = np.where(xf > 0)
    plt.figure(figsize=(10, 2.5))
    plt.plot(xf[idx], np.abs(yf[idx]))
    plt.title(f"Espectro de frecuencias - {titulo}")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Magnitud")
    plt.tight_layout()
    plt.show()
    return np.abs(yf[idx])

def comparar_fft(fft1, fft2):
    min_len = min(len(fft1), len(fft2))
    fft1 = fft1[:min_len]
    fft2 = fft2[:min_len]
    diferencia = np.mean(np.abs(fft1 - fft2) / (np.maximum(fft1, fft2)+1e-8))
    return diferencia

def grabar_referencia():
    global audio_oro, fft_oro
    messagebox.showinfo("Atención", "Presiona aceptar y GOLPEA la moneda auténtica cerca del micrófono...")
    audio_oro = grabar_audio()
    audio_oro = extraer_fragmento(audio_oro)
    graficar(audio_oro, fs, "Referencia Oro o plata")
    fft_oro = graficar_fft(audio_oro, fs, "Referencia Oro o plata")

def grabar_prueba():
    global audio_prueba, fft_prueba
    messagebox.showinfo("Atención", "Presiona aceptar y GOLPEA la moneda a PROBAR cerca del micrófono...")
    audio_prueba = grabar_audio()
    audio_prueba = extraer_fragmento(audio_prueba)
    graficar(audio_prueba, fs, "Moneda a Probar")
    fft_prueba = graficar_fft(audio_prueba, fs, "Moneda a Probar")

def comparar():
    if audio_oro is None or audio_prueba is None:
        messagebox.showwarning("Advertencia", "Graba primero los dos sonidos.")
        return
    diferencia = comparar_fft(fft_oro, fft_prueba)
    umbral = 0.25
    resultado = f"Resultado de la comparación: {diferencia:.3f}\n" 
    if diferencia < umbral:
        resultado += "¡La moneda probada suena SIMILAR al metal auténtico!"
    else:
        resultado += "El sonido DIFERE del metal auténtico (posible falso o diferente metal)."
    messagebox.showinfo("Resultado", resultado)

def guardar_referencia():
    if audio_oro is None:
        messagebox.showwarning("Advertencia", "Primero graba una referencia.")
        return
    archivo = filedialog.asksaveasfilename(defaultextension='.npy', filetypes=[("NumPy files", "*.npy")])
    if archivo:
        np.save(archivo, audio_oro)
        messagebox.showinfo("Éxito", "Referencia guardada.")

def cargar_referencia():
    global audio_oro, fft_oro
    archivo = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
    if archivo:
        audio_oro = np.load(archivo)
        graficar(audio_oro, fs, "Referencia Oro o plata(cargada)")
        fft_oro = graficar_fft(audio_oro, fs, "Referencia Oro o plata(cargada)")
        messagebox.showinfo("Éxito", "Referencia cargada.")

ventana = tk.Tk()
ventana.title("Detector de Oro por Sonido")
ventana.geometry("440x360")
tk.Label(ventana, text="Detector de monedas de oro o plata por sonido\nDONT TREAD ON ME", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(ventana, text="1. Grabar REFERENCIA (auténtico)", height=2, command=grabar_referencia, bg="#FFD700").pack(fill="x", padx=20, pady=4)
tk.Button(ventana, text="2. Grabar MONEDA A PROBAR", height=2, command=grabar_prueba, bg="#D3D3D3").pack(fill="x", padx=20, pady=4)
tk.Button(ventana, text="3. Comparar sonidos y mostrar resultado", height=2, command=comparar, bg="#ADD8E6").pack(fill="x", padx=20, pady=7)
tk.Button(ventana, text="Guardar referencia...", command=guardar_referencia, bg="#f2c800").pack(fill="x", padx=20, pady=1)
tk.Button(ventana, text="Cargar referencia...", command=cargar_referencia, bg="#c2e0f4").pack(fill="x", padx=20, pady=1)
tk.Label(ventana, text="Recomendado: guarda una referencia de oro o plata real.\nUsa siempre monedas de igual tipo.\nObserva las gráficas para comparar visualmente.", font=("Arial", 9)).pack(pady=12)
ventana.mainloop()