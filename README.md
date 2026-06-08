# Projeto Inteligência Artificial e Data Science

# 🚬 Smoking Status Predictor

Sistema de predição de status de fumante (**Never Smoked**, **Former Smoker** ou **Current Smoker**) utilizando Machine Learning com XGBoost treinado sobre o dataset da Korean National Health Insurance Service (NHIS).

---

## 📋 Visão Geral

O projeto utiliza indicadores biométricos para prever o status de tabagismo de um paciente.

### Tecnologias Utilizadas

| Componente   | Tecnologia             | Finalidade                    |
| ------------ | ---------------------- | ----------------------------- |
| Modelo ML    | Scikit-Learn (XGBoost) | Predição de status de fumante |
| Backend      | FastAPI + Uvicorn      | API REST                      |
| Frontend     | Streamlit              | Interface Web                 |
| Serialização | Joblib (.pkl)          | Persistência do modelo        |

---

## 📁 Estrutura do Projeto

```text
project-root/
│
├── api/
│   ├── main.py
│   └── requirements.txt
│
├── app/
│   ├── app.py
│   └── requirements.txt
│
├── model_artifacts/
│   ├── smoking_model.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── feature_names.pkl
│
├── notebook/
│   └── Cópia_de_Equipe_04_smoking_driking_dataset.ipynb
│
└── README.md
```

---

## ✅ Pré-requisitos

Certifique-se de possuir:

- Python 3.10 ou superior
- pip
- Git

### Downloads

- Python: https://www.python.org/downloads/
- Git: https://git-scm.com/

---

# 🚀 Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/Rafaelsn11/smoking_driking_dataset.git
cd smoking_driking_dataset
```

---

## 2. Instalar dependências da API

```bash
cd api
pip install -r requirements.txt
```

---

## 3. Instalar dependências do Frontend

```bash
cd ../app
pip install -r requirements_streamlit.txt
```

---

## 4. Gerar os artefatos do modelo

> Necessário apenas na primeira execução.

Abra o notebook:

```text
Cópia_de_Equipe_04_smoking_driking_dataset.ipynb
```

Execute todas as células em sequência.

Ao final serão gerados:

```text
model_artifacts/
├── smoking_model.pkl
├── scaler.pkl
├── label_encoder.pkl
└── feature_names.pkl
```

---

# ▶️ Executando a Aplicação

A aplicação necessita de dois serviços executando simultaneamente.

Abra dois terminais.

---

## Terminal 1 — Backend FastAPI

```bash
cd api
python -m uvicorn main:app --reload
```

API disponível em:

```text
http://localhost:8000
```

Documentação Swagger:

```text
http://localhost:8000/docs
```

---

## Terminal 2 — Frontend Streamlit

```bash
cd app
python -m streamlit run app.py
```

Interface disponível em:

```text
http://localhost:8501
```

---

# 🖥️ Como Utilizar

1. Acesse:

```text
http://localhost:8501
```

2. Preencha os dados biométricos do paciente:

- Personal Data
- Anthropometric Measurements
- Blood Pressure
- Lab Results

3. Os seguintes índices são calculados automaticamente:

- BMI (Body Mass Index)
- Atherogenic Index

4. Clique em:

```text
Analisar Paciente
```

5. O sistema retornará:

- Classe prevista
- Percentual de confiança
- Distribuição de probabilidade para todas as classes

---

# 🔌 API Reference

| Método | Endpoint    | Descrição                     |
| ------ | ----------- | ----------------------------- |
| GET    | `/`         | Health Check                  |
| GET    | `/features` | Lista das features do modelo  |
| POST   | `/predict`  | Predição do status de fumante |
| GET    | `/docs`     | Swagger UI                    |

---

## Exemplo de Requisição

### POST `/predict`

```json
{
  "age": 35,
  "height_cm": 175,
  "weight_kg": 80,
  "waist_cm": 85,
  "systolic": 120,
  "relaxation": 80,
  "fasting_blood_sugar": 95,
  "cholesterol": 180,
  "triglyceride": 120,
  "hdl": 55,
  "ldl": 100,
  "hemoglobin": 14.5,
  "serum_creatinine": 1.0,
  "ast": 20,
  "alt": 25,
  "gtp": 30
}
```

### Exemplo de Resposta

```json
{
  "prediction": "Never Smoked",
  "confidence": 92.4,
  "probabilities": {
    "Never Smoked": 0.924,
    "Former Smoker": 0.053,
    "Current Smoker": 0.023
  }
}
```

---

# 🛠️ Troubleshooting

## 500 Internal Server Error

O scaler e o modelo devem possuir exatamente o mesmo número de features (19).

Execute novamente as células responsáveis pela geração dos artefatos.

---

## InconsistentVersionWarning

Os arquivos `.pkl` foram gerados em uma versão diferente do Scikit-Learn.

Para corrigir:

```bash
pip install scikit-learn==1.4.2
```

---

## API Offline no Streamlit

Verifique se o backend FastAPI está executando na porta 8000 antes de clicar em:

```text
Analisar Paciente
```

---

## ModuleNotFoundError

Instale as dependências em cada módulo:

```bash
cd api
pip install -r requirements.txt

cd ../app
pip install -r requirements.txt
```

---

## model_artifacts não encontrado

Execute todas as células do notebook para gerar os arquivos:

```text
model_artifacts/
```

---

## 📊 Dataset

**Korean National Health Insurance Service (NHIS)**

Aproximadamente **1 milhão de registros** contendo indicadores biométricos e hábitos relacionados ao tabagismo.

---

## 🤖 Modelo Utilizado

- Random Forest Classifier
- Scikit-Learn
- Classificação Multiclasse

Classes previstas:

- Never Smoked
- Former Smoker
- Current Smoker

---

## 👥 Equipe

Projeto acadêmico desenvolvido para estudo de Machine Learning aplicado à área da saúde.

---

**Smoking Status Predictor**  
Dataset: Korean NHIS Smoking & Drinking  
Modelo: XGBoost Classifier  
2026
