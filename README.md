# 🔊 Detector de Monedas de Oro o Plata por Sonido

Este proyecto permite **detectar si una moneda es de oro o plata auténtica** comparando el sonido que produce al golpearla. Utiliza análisis de frecuencia (FFT) para comparar una moneda de prueba con una grabación de referencia previamente autenticada.

## 🧠 ¿Cómo funciona?

1. Graba el sonido de una moneda auténtica (referencia).
2. Graba el sonido de una moneda que deseas probar.
3. Compara los espectros de frecuencia de ambos sonidos.
4. Si los sonidos son similares, se considera auténtica (o del mismo metal).
5. Visualiza las gráficas de la forma de onda y su análisis espectral.

## 📦 Requisitos

Asegúrate de tener instalado Python 3.8+ y las siguientes dependencias:

```bash
pip install numpy matplotlib scipy sounddevice

