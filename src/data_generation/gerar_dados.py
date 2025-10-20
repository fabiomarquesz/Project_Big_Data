import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker('pt_BR')
random.seed(42)
np.random.seed(42)

def gerar_dados_pacientes(num_pacientes=500, leituras_por_paciente=400):
    """
    Essa função, gera 200 mil registros de monitoramento de pacientes.
    Incluindo dados sujos para limpeza.
    """
    dados = []
    timestamp_base = datetime(2025, 1, 1, 0, 0, 0)

    for paciente_num in range(1, num_pacientes + 1):
        paciente_id = f'PAC{paciente_num:05d}'
        nome = fake.name()
        idade = random.randint(18, 95)

        #Definindo métricas de sáude
        if idade > 70:
            perfil = random.choice(['normal', 'risco_moderado', 'risco_alto', 'risco_alto'])
        
        elif idade > 50:
            perfil = random.choice(['normal', 'normal', 'risco_moderado', 'risco_alto'])
        else:
            perfil = random.choice(['normal', 'normal', 'normal', 'risco_moderado'])

        for i in range(leituras_por_paciente):
            timestamp = timestamp_base + timedelta(minutes=i * 15)

            #Gerando BPMs baseado nos perfis
            if perfil == 'normal':
                bpm = np.random.normal(75, 8)
                spo2 = np.random.normal(98, 1)
            elif perfil == 'risco_moderado':
                bpm = np.random.normal(85, 15)
                spo2 = np.random.normal(95, 2)
                if random.random() < 0.15:
                    bpm = np.random.choice([random.randint(45, 55), random.randint(105, 120)])
                    spo2 = np.random.normal(88, 94)
            else:
                bpm = np.random.normal(95, 20)
                spo2 = np.random.normal(93, 3)
                if random.random() < 0.35:
                    bpm = np.random.choice([random.randint(40, 50), random.randint(115, 140)])
                    spo2 = np.random.normal(85, 92)

            #Inserindo dados sujos para teste (10% dos dados)
            if random.random() < 0.10:
                bpm = random.choice([None, -1, 999, 0])
            if random.random() < 0.08:
                spo2 = random.choice([None, -1, 150, 0])

            # Pressão arterial
            pressao_sistolica = np.random.normal(120, 15)
            pressao_diastolica = np.random.normal(80, 10)

            #Temperatura
            temperatura = np.random.normal(36.5, 0.5)
            if perfil == 'risco_alto' and random.random() < 0.20:
                temperatura = random.uniform(38.0, 39.5)

            registro = {
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'paciente_id': paciente_id,
                'nome_paciente': nome,
                'idade': idade,
                'bpm': round(bpm, 1) if bpm is not None else None,
                'spo2': round(spo2, 1) if spo2 is not None else None,
                'pressao_sistolica': round(pressao_sistolica, 1),
                'pressao_diastolica': round(pressao_diastolica, 1),
                'temperatura': round(temperatura, 2),
                'dispositivo_id': f"DEV{random.randint(1000, 9999)}",
                'localizacao': random.choice(['UTI', 'Enfermaria', 'Semi-intensiva', 'Emergência'])
            }

            dados.append(registro)

    df = pd.DataFrame(dados)
    output_path = 'data/raw/pacientes_raw.csv'
    df.to_csv(output_path, index=False)

    print('Dados gerados com sucesso!')
    print(f'Total de registros: {len(df):,}')
    print(f'Total de pacientes: {num_pacientes}')
    print(f'Arquivo salvo em: {output_path}')
    print(f'Tamanho do arquivo: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB')
    print('\n Resumo dos dados: ')
    print(df.info)
    print('\n Valores nulos por coluna: ')
    print(df.isnull().sum())

    return df

if __name__ == '__main__':
    df = gerar_dados_pacientes(num_pacientes=500, leituras_por_paciente=400)