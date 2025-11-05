from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, avg, count, lit
from pyspark.sql.types import *
import time

class HealthDataProcessor:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName =("HealthMonitorSystem") \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "4g") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")

    def carregar_dados(self, path='data/raw/pacientes_raw.csv'):
        """Carregando Dados Brutos"""
        print(f'Carregando dados de: {path}')
        df = self.spark.read.csv(path, header=True, inferSchema=True)
        print(f"{df.count():,} registros carregados")
        return df
    
    def limpar_dados(self, df):
        registro_inicial = df.count()

        #Removendo duplicatas
        df = df.dropDuplicates(['timestamp', 'paciente_id'])
        print(f' Quantidade de duplicadas removidas: {registro_inicial - df.count()}')

        #Validando BPM (40 - 200)
        df = df.filter(
            (col('bpm').isNotNull()) &
            (col('bpm') >= 40) &
            (col('bpm') <= 200)
        )

        #Valiando Spo2 (70 - 100)
        df = df.filter(
            (col('spo2').isNotNull()) &
            (col('spo2') >= 70) &
            (col('spo2') <= 100)
        )

        #Valiando pressão arterial
        df = df.filter(
            (col('pressao_sistolica') >= 80) &
            (col('pressao_sistolica') <= 200) & 
            (col('pressao_diastolica') >= 50) &
            (col('pressao_diastolica') <= 130)
        )

        #Valiando temperatura (35 - 42°C)
        df = df.filter(
            (col('temperatura') >= 35.0) &
            (col('temperatura') <= 42.0)
        )

        registros_final = df.count()
        removidos = registro_inicial - registros_final

        print(f'Registros inválidos removidos: {removidos} ({removidos / registro_inicial * 100:.2f}%)')
        print(f'Registos válidos: {registros_final:,}')

        return df
    
    def classificar_risco(self, df):
        print('Classificando pacientes por nível de risco...')

        df = df.withColumn('alerta_cardiaco',
                           when((col('bpm') < 60) | (col('bpm') > 100), True).otherwise(False))
        
        df = df.withColumn('alerta_pressao',
                           when((col('pressao_sistolica') > 140) | col('pressao_diastolica')))

        df = df.withColumn('alerta_temperatura',
                           when((col('temperatura') < 36.0) | (col('temperatura') > 37.5), True).otherwise(False))
        
        #Contagem total de alertas
        df = df.withColumn('total_alertas',
                           col('alerta_cardiaco').cast('int') +
                           col('alerta_respiratorio').cas('int') + 
                           col('alerta_pressao').cast('int') +
                           col('alerta_temperatura').cast('int')
                           )

        #Classificnado níveis de risco
        df = df.withColumn('nivel_risco',
                           when(col('total_alertas') >= 3, 'CRÍTICO')
                           .when(col('total_alertas') == 2, 'ALTO')
                           .when(col('total_alertas') == 1, 'MODERADO')
                           .otherwise('NORMAL')
                           )
        
        print('Classificação de risco aplicada!')
        return df
    
    def salvar_dados_limpos(self, df, path='data/processed/pacientes_clean.csv'):
        print(f'\nSalvando dados processados em: {path}')
        
        df_pandas = df.toPandas()
        df_pandas.to_csv(path, index=False)

        print(f'\n{df.count():,} registros salvos com sucesso!')
        return df_pandas
    
    def gerar_estatisticas(self, df):
        print('\nESTATÍSTICAS DO PROCESSAMENTO')
        print('=' * 60)

        total = df.count()
        print(f'\nTotal de registros processados: {total:,}')

        #Distribuição por nível de risco
        print('\nDistribuição por Nível de Risco: ')
        df.groupBy('nivel_risco').count().orderBy('count', ascending=False).show()
        
        #Pacientes críticos
        criticos = df.filter(col('nivel_risco') == 'CRÍTICO').select('paciente_id').distinct().count()
        print(f'\nNúmero de pacientes em estado CRÍTICO: {criticos}')

        #Média gerais
        print('\n Médias Gerais: ')

        df.select(
            avg('bpm').alias('BPM Médio'),
            avg('spo2').alis('SpO2 Médio'),
            avg('temperatura').alias('Temperatura Média')
        ).show()

    def processar_pipeline_completo(self):
        inicio = time.time()

        print('=' * 60)
        print('SISTEMA DE MONITORAMENTO DE PACIENTES IoT')
        print('=' * 60)

        #Pipeline
        df = self.carregar_dados()
        df = self.limpar_dados()
        df = self.classificar_risco()
        self.gerar_estatisticas(df)
        df_pandas = self.salvar_dados_limpos(df)

        tempo_total = time.time() - inicio

        print('=' * 60)
        print(f'Pipeline concluída em {tempo_total:.2f} segundos')
        print('=' * 60)

        self.spark.stop()
        return df_pandas
    
if __name__ == '__main__':
    processador = HealthDataProcessor()
    df = processador.processar_pipeline_completo()