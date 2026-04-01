from obspy import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from obspy.signal.spectral_estimation import welch

filePath = "C:\\Users\\sabrahar\\Desktop\\ML\\segy\\line5raw.sgy"

stream = read(filePath)
trace = stream[0]

# Создаем фигуру для всех графиков
plt.figure(figsize=(15, 10))

# 1. Исходный сигнал
plt.subplot(4, 2, 1)
plt.plot(trace.data[:1000])
plt.title('Исходный сигнал')
plt.grid(True)

exit(2)
# 2. Применяем полосовой фильтр
trace_filtered = trace.copy()
trace_filtered.filter('bandpass', freqmin=1.0, freqmax=20.0, corners=2, zerophase=True)
plt.subplot(4, 2, 2)
plt.plot(trace_filtered.data[:1000])
plt.title('После полосовой фильтрации')
plt.grid(True)

# 3. Нормализация
trace_norm = trace.copy()
trace_norm.normalize()
plt.subplot(4, 2, 3)
plt.plot(trace_norm.data[:1000])
plt.title('После нормализации')
plt.grid(True)

# 4. Удаление тренда
trace_detrend = trace.copy()
trace_detrend.detrend(type='linear')
plt.subplot(4, 2, 4)
plt.plot(trace_detrend.data[:1000])
plt.title('После удаления тренда')
plt.grid(True)

# 5. Применение окна
trace_tapered = trace.copy()
trace_tapered.taper(max_percentage=0.05, type='hann')
plt.subplot(4, 2, 5)
plt.plot(trace_tapered.data[:1000])
plt.title('После применения окна Ханна')
plt.grid(True)

# 6. Спектральный анализ
freq, power = welch(trace.data, fs=trace.stats.sampling_rate)
plt.subplot(4, 2, 6)
plt.semilogy(freq, power)
plt.title('Спектр сигнала')
plt.xlabel('Частота (Гц)')
plt.ylabel('Мощность')
plt.grid(True)

# 7. Автокорреляция
autocorr = trace.correlate(trace)
plt.subplot(4, 2, 7)
plt.plot(autocorr.data[:1000])
plt.title('Автокорреляция')
plt.grid(True)

# 8. Сглаживание
trace_smooth = trace.copy()
trace_smooth.smooth(window_len=5)
plt.subplot(4, 2, 8)
plt.plot(trace_smooth.data[:1000])
plt.title('После сглаживания')
plt.grid(True)

plt.tight_layout()
plt.show()

# Дополнительные примеры обработки

# 1. Интерполяция
trace_interp = trace.copy()
trace_interp.interpolate(sampling_rate=1000.0)
print(f"Частота дискретизации после интерполяции: {trace_interp.stats.sampling_rate} Гц")

# 2. Вычисление огибающей
trace_env = trace.copy()
trace_env.envelope()
plt.figure(figsize=(10, 4))
plt.plot(trace_env.data[:1000])
plt.title('Огибающая сигнала')
plt.grid(True)
plt.show()

# # 3. Спектрограмма
# trace.spectrogram()
# plt.title('Спектрограмма')
# plt.show()

# Сохранение обработанного сигнала
trace_filtered.write("processed_trace.sac", format="SAC")
