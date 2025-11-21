import funções as fn;
import numpy as np

#CODIFICADORES

# Configurações globais
SAMPLE_RATE = 44100  # Taxa de amostragem
BIT_DURATION = 1.0   # 1 segundo por bit
FREQ_LOW = 440       # Frequência para '0' (Lá)
FREQ_HIGH = 880      # Frequência para '1' (Lá oitava)

def encode_nrz(data_bits,debug=False):
    """
    Codifica dados usando NRZ
    
    Args:
        data_bits: string de bits (ex: "10110")
    
    Returns:
        array: Sinal de áudio codificado
    """
    audio_signal = np.array([])
    
    fn.show(f"Codificando NRZ: {data_bits}",debug)
    
    for i, bit in enumerate(data_bits):
        if bit == '1':
            freq = FREQ_HIGH
            fn.show(f"Bit {i}: '1' -> {freq} Hz",debug)
        else:
            freq = FREQ_LOW
            fn.show(f"Bit {i}: '0' -> {freq} Hz",debug)
        
        tone = fn.generate_tone(freq, BIT_DURATION)
        audio_signal = np.concatenate([audio_signal, tone])
    
    return audio_signal

def encode_nrzi(data_bits,debug=False):
    """
    Codifica dados usando NRZI
    
    Args:
        data_bits: string de bits
    
    Returns:
        array: Sinal de áudio codificado
    """
    pass
    
    return '0'

def encode_manchester(data_bits,debug=False):
    """
    Codifica dados usando Manchester
    
    Args:
        data_bits: string de bits
    
    Returns:
        array: Sinal de áudio codificado
    """
    audio_signal = np.array([])
    
    fn.show(f"Codificando Manchester: {data_bits}",debug)
    
    for i, bit in enumerate(data_bits):
        if bit == '1':
            # Bit '1': alto->baixo (primeira metade alta, segunda baixa)
            tone1 = fn.generate_tone(FREQ_HIGH, BIT_DURATION/2)
            tone2 = fn.generate_tone(FREQ_LOW, BIT_DURATION/2)
            fn.show(f"Bit {i}: '1' -> {FREQ_HIGH}Hz -> {FREQ_LOW}Hz",debug)
        else:
            # Bit '0': baixo->alto (primeira metade baixa, segunda alta)
            tone1 = fn.generate_tone(FREQ_LOW, BIT_DURATION/2)
            tone2 = fn.generate_tone(FREQ_HIGH, BIT_DURATION/2)
            fn.show(f"Bit {i}: '0' -> {FREQ_LOW}Hz -> {FREQ_HIGH}Hz",debug)
        
        bit_signal = np.concatenate([tone1, tone2])
        audio_signal = np.concatenate([audio_signal, bit_signal])
    
    return audio_signal