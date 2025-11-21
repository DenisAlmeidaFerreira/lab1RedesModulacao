import numpy as np
import matplotlib.pyplot as plt
import codificadores as codificadores
import decodificadores as decodificadores

mensagem_bits = "000011101101011100010111001"
num_bits = len(mensagem_bits)

sinais = {
    "NRZ": codificadores.encode_nrz(mensagem_bits),
    "Manchester": codificadores.encode_manchester(mensagem_bits)
}

SNR_values = np.arange(-1, -301, -1)

for mod, sinal_limpo in sinais.items():
    num_erros = []
    primeiros_bits_snr = None
    todos_bits_snr = None
    bits_comprometidos = np.zeros(num_bits, dtype=bool)
    
    for snr in SNR_values:
        sinal_ruidoso = sinal_limpo + np.random.normal(0, np.sqrt(np.mean(sinal_limpo**2)/ (10**(snr/10))), len(sinal_limpo))
        
        if mod == "NRZ":
            mensagem_decodificada = decodificadores.decode_nrz(sinal_ruidoso, num_bits)
        elif mod == "Manchester":
            mensagem_decodificada = decodificadores.decode_manchester(sinal_ruidoso, num_bits)
        
        erros = sum([1 for a, b in zip(mensagem_bits, mensagem_decodificada) if a != b])
        num_erros.append(erros)
        
        for i, (orig, dec) in enumerate(zip(mensagem_bits, mensagem_decodificada)):
            if orig != dec:
                bits_comprometidos[i] = True
        
        if erros > 0 and primeiros_bits_snr is None:
            primeiros_bits_snr = snr
        if todos_bits_snr is None and bits_comprometidos.all():
            todos_bits_snr = snr
    
    plt.figure(figsize=(10,6))
    plt.plot(-SNR_values, num_erros, marker='o')
    plt.axvline(x=-primeiros_bits_snr, color='orange', linestyle='--', label='Primeiros bits comprometidos')
    plt.axvline(x=-todos_bits_snr, color='red', linestyle='--', label='Todos os bits comprometidos')
    plt.xlabel("SNR (dB) – maior à direita = menos ruído")
    plt.ylabel("Número de bits errados")
    plt.title(f"Número de erros vs SNR para {mod}")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print(f"{mod}: Primeiros bits comprometidos em SNR = {primeiros_bits_snr} dB")
    print(f"{mod}: Todos os bits comprometidos em SNR = {todos_bits_snr} dB")
