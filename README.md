# 🏥 Sistema de Monitoramento de Pacientes IoT

Sistema de alertas em tempo real para monitoramento de pacientes críticos usando Big Data e visualização interativa.

## 🎯 Funcionalidades

- ✅ Processamento de 200.000+ registros com PySpark
- ✅ Limpeza e validação de dados em larga escala
- ✅ Classificação automática de níveis de risco
- ✅ Análise MapReduce para identificação de padrões
- ✅ Dashboard interativo com Streamlit
- ✅ Alertas em tempo real para casos críticos

## 🛠️ Tecnologias

- Python 3.11
- PySpark 3.5.0
- Apache Hadoop MapReduce
- Streamlit
- Plotly
- Pandas

## 🚀 Como Executar

### 1. Clone o repositório
\`\`\`bash
git clone https://github.com/seu-usuario/health-monitoring-system.git
cd health-monitoring-system
\`\`\`

### 2. Configure o ambiente
\`\`\`bash
conda create -n health-monitor python=3.11 -y
conda activate health-monitor
pip install -r requirements.txt
\`\`\`

### 3. Gere os dados
\`\`\`bash
python src/data_generation/gerar_dados.py
\`\`\`

### 4. Processe os dados com PySpark
\`\`\`bash
python src/processing/spark_processor.py
\`\`\`

### 5. Execute análise MapReduce (opcional)
\`\`\`bash
python src/processing/mapreduce_analyzer.py data/processed/pacientes_clean.csv > resultados_mapreduce.json
\`\`\`

### 6. Inicie o dashboard
\`\`\`bash
streamlit run src/dashboard/app.py
\`\`\`

## 📊 Estrutura dos Dados

### Dados de Entrada (Raw)
- **timestamp**: Data/hora da leitura
- **paciente_id**: Identificador único do paciente
- **nome_paciente**: Nome do paciente
- **idade**: Idade do paciente
- **bpm**: Batimentos por minuto
- **spo2**: Saturação de oxigênio (%)
- **pressao_sistolica**: Pressão arterial sistólica
- **pressao_diastolica**: Pressão arterial diastólica
- **temperatura**: Temperatura corporal (°C)
- **dispositivo_id**: ID do dispositivo IoT
- **localizacao**: Localização no hospital

### Dados Processados
Inclui todos os campos acima mais:
- **alerta_cardiaco**: Boolean
- **alerta_respiratorio**: Boolean
- **alerta_pressao**: Boolean
- **alerta_temperatura**: Boolean
- **total_alertas**: Contagem de alertas
- **nivel_risco**: NORMAL, MODERADO, ALTO, CRÍTICO

## 🎯 Regras de Classificação

### Alertas Individuais
- **Cardíaco**: BPM < 60 ou BPM > 100
- **Respiratório**: SpO2 < 95%
- **Pressão**: Sistólica > 140 ou Diastólica > 90
- **Temperatura**: < 36°C ou > 37.5°C

### Níveis de Risco
- **CRÍTICO**: 3+ alertas simultâneos
- **ALTO**: 2 alertas simultâneos
- **MODERADO**: 1 alerta
- **NORMAL**: Sem alertas

## 📈 Resultados Esperados

Com 200.000 registros:
- ~10% de dados sujos removidos na limpeza
- ~5-10% de pacientes em estado crítico
- ~15-20% de pacientes com risco alto/moderado
- Processamento completo em < 30 segundos


## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, abra uma issue ou pull request.

## 📄 Licença

MIT License

## 👤 Autor

Fabio Marques - www.linkedin.com/in/fabio-marques-a36725290

## 📚 Referências

- Apache Spark Documentation
- Hadoop MapReduce Guide
- Streamlit Documentation
\`\`\`

