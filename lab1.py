import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import sounddevice as sd
from scipy import signal
from scipy.io import wavfile
import time
import os
import codificadores as codificadores;
import decodificadores as decodificadores;

# Configurações globais
SAMPLE_RATE = 44100  # Taxa de amostragem
BIT_DURATION = 1.0   # 1 segundo por bit
FREQ_LOW = 440       # Frequência para '0' (Lá)
FREQ_HIGH = 880      # Frequência para '1' (Lá oitava)

#print(sd.query_devices())

# Definir dispositivos de entrada/saída
input_device = 1    # Microfone do notebook
output_device = 3   # Alto-falantes do notebook, MME
sd.default.device = (input_device, output_device)

# Gravação de áudio
DURATION = 3  # duração em segundos
FILENAME = "captura.wav"

#Adicionando Ruido
def adicionar_ruido(audio_signal, snr_db=-12):
    """
    Adiciona ruído gaussiano ao sinal
    
    Args:
        audio_signal: Sinal original
        snr_db: Relação sinal-ruído em dB
    
    Returns:
        array: Sinal com ruído
    """
    # Calcula potência do sinal
    signal_power = np.mean(audio_signal ** 2)
    
    # Calcula potência do ruído baseada no SNR
    snr_linear = 10 ** (snr_db / 10)
    noise_power = signal_power / snr_linear
    
    # Gera ruído gaussiano
    noise = np.random.normal(0, np.sqrt(noise_power), len(audio_signal))
    
    return audio_signal + noise

# Captura de áudio do microfone
def capturar_do_microfone(duracao_segundos):
    """
    Captura áudio do microfone
    
    Args:
        duracao_segundos: Duração da captura
    
    Returns:
        array: Áudio capturado
    """
    print(f"Iniciando captura por {duracao_segundos} segundos...")
    print("Reproduza o áudio no seu celular AGORA!")
    
    # Captura áudio
    audio_capturado = sd.rec(
        int(duracao_segundos * SAMPLE_RATE), 
        samplerate=SAMPLE_RATE, 
        channels=1
    )
    sd.wait()  # Aguarda terminar a captura
    
    print("Captura concluída!")
    return audio_capturado.flatten()

# LABORATÓRIO

mensagem_bits = "000011101101011100010111001"
num_bits = len(mensagem_bits)

sinal_limpo = codificadores.encode_nrz(mensagem_bits)

SNR_values = np.arange(-1, -301, -1)
num_erros = []

primeiros_bits_snr = None
todos_bits_snr = None

bits_comprometidos = np.zeros(num_bits, dtype=bool)

for snr in SNR_values:
    sinal_ruidoso = adicionar_ruido(sinal_limpo, snr_db=snr)
    mensagem_decodificada = decodificadores.decode_nrz(sinal_ruidoso, num_bits)
    
    erros = sum([1 for a, b in zip(mensagem_bits, mensagem_decodificada) if a != b])
    num_erros.append(erros)
    
    for i, (orig, dec) in enumerate(zip(mensagem_bits, mensagem_decodificada)):
        if orig != dec:
            bits_comprometidos[i] = True
    
    if erros > 0 and primeiros_bits_snr is None:
        primeiros_bits_snr = snr
    
    if todos_bits_snr is None and bits_comprometidos.all():
        todos_bits_snr = snr

print(f"Primeiros bits comprometidos em SNR = {primeiros_bits_snr} dB")
print(f"Todos os bits comprometidos em SNR = {todos_bits_snr} dB")

plt.plot(-SNR_values, num_erros, marker='o')
plt.xlabel("SNR (dB) – maior à direita = menos ruído")
plt.ylabel("Número de bits errados")
plt.title("Número de erros vs SNR")
plt.grid(True)
plt.show()