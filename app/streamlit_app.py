import streamlit as st
import requests
import numpy as np

st.set_page_config(
    page_title="Smoking Status Predictor",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = "http://localhost:8000/predict"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0a0e1a; color: #e8eaf0; }
.hero {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a0a2e 50%, #0a1628 100%);
    border: 1px solid rgba(100,180,255,0.15); border-radius: 20px;
    padding: 48px 40px 36px; margin-bottom: 36px; position: relative; overflow: hidden;
}
.hero::before {
    content:''; position:absolute; top:-60px; right:-60px;
    width:300px; height:300px;
    background:radial-gradient(circle,rgba(80,140,255,0.12) 0%,transparent 70%);
    border-radius:50%;
}
.hero-title {
    font-family:'Syne',sans-serif; font-size:2.6rem; font-weight:800;
    background:linear-gradient(90deg,#64b4ff,#a78bfa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    margin:0 0 8px 0; line-height:1.1;
}
.hero-sub { color:#8899bb; font-size:1rem; font-weight:300; margin:0; }
.section-card {
    background:#111827; border:1px solid rgba(255,255,255,0.07);
    border-radius:16px; padding:28px 28px 20px; margin-bottom:20px;
}
.section-title {
    font-family:'Syne',sans-serif; font-size:0.75rem; font-weight:700;
    letter-spacing:0.15em; text-transform:uppercase; color:#64b4ff;
    margin:0 0 20px 0; padding-bottom:12px;
    border-bottom:1px solid rgba(100,180,255,0.15);
}
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label {
    color:#9aaac8 !important; font-size:0.82rem !important;
    font-weight:500 !important; letter-spacing:0.02em;
}
[data-testid="stNumberInput"] input {
    background:#1a2235 !important; border:1px solid rgba(255,255,255,0.1) !important;
    border-radius:8px !important; color:#e8eaf0 !important;
}
.stButton > button {
    background:linear-gradient(135deg,#3b6fd4,#7c3aed) !important;
    color:white !important; border:none !important; border-radius:12px !important;
    padding:16px 40px !important; font-family:'Syne',sans-serif !important;
    font-size:1rem !important; font-weight:700 !important;
    letter-spacing:0.05em !important; width:100% !important;
    box-shadow:0 4px 20px rgba(100,100,255,0.25) !important;
}
.result-box { border-radius:16px; padding:32px; text-align:center; margin-top:8px; }
.result-box.never  { background:linear-gradient(135deg,#0a2a1a,#0d3320); border:1px solid rgba(52,211,153,0.3); }
.result-box.former { background:linear-gradient(135deg,#1a1a0a,#2a2500); border:1px solid rgba(251,191,36,0.3); }
.result-box.current{ background:linear-gradient(135deg,#2a0a0a,#330d0d); border:1px solid rgba(248,113,113,0.3); }
.result-label { font-family:'Syne',sans-serif; font-size:0.7rem; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; opacity:0.6; margin-bottom:8px; }
.result-class { font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800; line-height:1.1; margin-bottom:6px; }
.result-confidence { font-size:0.9rem; opacity:0.55; }
.prob-row { display:flex; align-items:center; gap:12px; margin-bottom:10px; }
.prob-label { font-size:0.78rem; color:#8899bb; width:130px; flex-shrink:0; }
.prob-bar-bg { flex:1; height:6px; background:rgba(255,255,255,0.07); border-radius:99px; overflow:hidden; }
.prob-bar-fill { height:100%; border-radius:99px; }
.prob-val { font-size:0.78rem; color:#64b4ff; width:42px; text-align:right; flex-shrink:0; }
.info-note {
    background:rgba(100,180,255,0.06); border-left:3px solid #64b4ff;
    border-radius:0 8px 8px 0; padding:10px 14px;
    font-size:0.8rem; color:#7a9bbf; margin-top:12px;
}
</style>
""", unsafe_allow_html=True)

def calc_derived(weight, height, triglyceride, hdl):
    bmi = weight / ((height / 100) ** 2) if height > 0 else 0.0
    ath = np.log10(triglyceride / hdl) if hdl > 0 and triglyceride > 0 else 0.0
    return round(bmi, 2), round(ath, 4)

st.markdown("""
<div class="hero">
    <p class="hero-title">🫁 Smoking Status Predictor</p>
    <p class="hero-sub">Insira os indicadores biométricos do paciente para obter a predição do status de tabagismo.</p>
</div>
""", unsafe_allow_html=True)

col_form, col_result = st.columns([3, 2], gap="large")

with col_form:

    st.markdown('<div class="section-card"><p class="section-title">👤 Dados Pessoais</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    sex    = c1.selectbox("Sexo", options=[0,1], format_func=lambda x: "Feminino" if x==0 else "Masculino")
    age    = c2.number_input("Idade (anos)", min_value=1.0, max_value=120.0, value=40.0, step=1.0)
    drk_yn = c3.selectbox("Consome álcool?", options=[0,1], format_func=lambda x: "Não" if x==0 else "Sim")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><p class="section-title">📏 Medidas Antropométricas</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    weight    = c1.number_input("Peso (kg)",    min_value=20.0,  max_value=300.0, value=70.0,  step=0.5)
    height    = c2.number_input("Altura (cm)",  min_value=100.0, max_value=250.0, value=170.0, step=0.5)
    waistline = c3.number_input("Cintura (cm)", min_value=40.0,  max_value=200.0, value=80.0,  step=0.5)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><p class="section-title">❤️ Pressão Arterial</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    SBP = c1.number_input("Sistólica — SBP (mmHg)",  min_value=50.0,  max_value=250.0, value=120.0, step=1.0)
    DBP = c2.number_input("Diastólica — DBP (mmHg)", min_value=30.0,  max_value=180.0, value=80.0,  step=1.0)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><p class="section-title">🧪 Exames Laboratoriais</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    BLDS          = c1.number_input("Glicemia jejum — BLDS (mg/dL)", min_value=40.0,   max_value=500.0,  value=95.0,  step=1.0)
    tot_chole     = c2.number_input("Colesterol total (mg/dL)",       min_value=50.0,   max_value=600.0,  value=200.0, step=1.0)
    triglyceride  = c3.number_input("Triglicerídeos (mg/dL)",         min_value=10.0,   max_value=1000.0, value=150.0, step=1.0)

    c1, c2, c3 = st.columns(3)
    HDL_chole     = c1.number_input("HDL (mg/dL)",          min_value=5.0,  max_value=200.0, value=50.0,  step=1.0)
    LDL_chole     = c2.number_input("LDL (mg/dL)",          min_value=10.0, max_value=400.0, value=120.0, step=1.0)
    hemoglobin    = c3.number_input("Hemoglobina (g/dL)",   min_value=4.0,  max_value=25.0,  value=14.0,  step=0.1)

    c1, c2, c3 = st.columns(3)
    urine_protein    = c1.number_input("Proteína urina (1–6)", min_value=1.0,  max_value=6.0,   value=1.0,  step=1.0)
    serum_creatinine = c2.number_input("Creatinina (mg/dL)",   min_value=0.1,  max_value=20.0,  value=1.0,  step=0.1)
    SGOT_AST         = c3.number_input("AST/TGO (U/L)",        min_value=1.0,  max_value=500.0, value=25.0, step=1.0)

    c1, c2 = st.columns(2)
    SGOT_ALT  = c1.number_input("ALT/TGP (U/L)", min_value=1.0, max_value=500.0,  value=22.0, step=1.0)
    gamma_GTP = c2.number_input("GGT (U/L)",      min_value=1.0, max_value=1000.0, value=30.0, step=1.0)
    st.markdown('</div>', unsafe_allow_html=True)

    bmi, ath_index = calc_derived(weight, height, triglyceride, HDL_chole)
    st.markdown(f"""
    <div class="info-note">
        ✦ <strong>IMC calculado automaticamente:</strong> {bmi} kg/m²
        &nbsp;|&nbsp; <strong>Índice Aterogênico:</strong> {ath_index}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🔍 Analisar Paciente")

with col_result:
    st.markdown("<br><br>", unsafe_allow_html=True)

    if predict_btn:
        payload = {
            "sex": sex, "age": age, "waistline": waistline,
            "SBP": SBP, "DBP": DBP, "BLDS": BLDS,
            "tot_chole": tot_chole, "HDL_chole": HDL_chole,
            "LDL_chole": LDL_chole, "triglyceride": triglyceride,
            "hemoglobin": hemoglobin, "urine_protein": urine_protein,
            "serum_creatinine": serum_creatinine, "SGOT_AST": SGOT_AST,
            "SGOT_ALT": SGOT_ALT, "gamma_GTP": gamma_GTP,
            "DRK_YN": drk_yn, "BMI": bmi, "atherogenic_index": ath_index,
        }

        with st.spinner("Consultando modelo..."):
            try:
                resp = requests.post(API_URL, json=payload, timeout=10)
                resp.raise_for_status()
                data = resp.json()

                prediction = data["prediction"]
                confidence = data["confidence"]
                probs      = data["probabilities"]

                css_class = {"Nunca Fumou": "never", "Ex-Fumante": "former", "Fumante Atual": "current"}.get(prediction, "never")
                emoji     = {"Nunca Fumou": "🟢",    "Ex-Fumante": "🟡",     "Fumante Atual": "🔴"}.get(prediction, "⚪")
                color     = {"Nunca Fumou": "#34d399","Ex-Fumante": "#fbbf24","Fumante Atual": "#f87171"}.get(prediction, "#64b4ff")

                st.markdown(f"""
                <div class="result-box {css_class}">
                    <div class="result-label">Predição do Modelo</div>
                    <div class="result-class" style="color:{color}">{emoji} {prediction}</div>
                    <div class="result-confidence">Confiança: {confidence*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                st.markdown('<div class="section-card"><p class="section-title">📊 Distribuição de Probabilidades</p>', unsafe_allow_html=True)
                bar_colors = {"Nunca Fumou": "#34d399", "Ex-Fumante": "#fbbf24", "Fumante Atual": "#f87171"}
                for cls, prob in sorted(probs.items(), key=lambda x: -x[1]):
                    pct = prob * 100
                    bc  = bar_colors.get(cls, "#64b4ff")
                    st.markdown(f"""
                    <div class="prob-row">
                        <div class="prob-label">{cls}</div>
                        <div class="prob-bar-bg">
                            <div class="prob-bar-fill" style="width:{pct}%;background:{bc};"></div>
                        </div>
                        <div class="prob-val">{pct:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            except requests.exceptions.ConnectionError:
                st.error("❌ API offline. Inicie o servidor FastAPI em localhost:8000.")
            except requests.exceptions.Timeout:
                st.error("⏱️ Timeout. Tente novamente.")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")
    else:
        st.markdown("""
        <div style="border:1px dashed rgba(100,180,255,0.2);border-radius:16px;padding:48px 24px;text-align:center;color:#3a4a66;">
            <div style="font-size:3rem;margin-bottom:16px;">🫁</div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:600;margin-bottom:8px;color:#4a5a77;">Aguardando análise</div>
            <div style="font-size:0.82rem;">Preencha os dados e clique em <strong>Analisar Paciente</strong></div>
        </div>
        """, unsafe_allow_html=True)
