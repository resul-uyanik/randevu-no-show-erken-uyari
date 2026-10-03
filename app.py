import streamlit as st
import pandas as pd
import joblib

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Randevu Erken Uyarı Sistemi",
    page_icon="🏥",
    layout="wide"
)

# Kaydedilen model ve sütunları yükleme
@st.cache_resource
def load_model():
    model = joblib.load('no_show_rf_model.pkl')
    features = joblib.load('model_features.pkl')
    return model, features

model, model_features = load_model()

st.title("🏥 Randevu İptal / No-Show Erken Uyarı Sistemi")
st.markdown("Hasta ve randevu parametrelerini girerek randevuya **gelmeme olasılığını** ve **operasyonel risk seviyesini** hesaplayın.")

st.divider()

# Giriş Alanları (2 Kolon)
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Hasta Bilgileri")
    gender = st.selectbox("Cinsiyet", ["Kadın (F)", "Erkek (M)"])
    age = st.slider("Yaş", min_value=0, max_value=115, value=30)
    scholarship = st.checkbox("Sosyal Yardım / Burs Alıyor mu? (Bolsa Família)")
    hypertension = st.checkbox("Hipertansiyon Var mı?")
    diabetes = st.checkbox("Diyabet Var mı?")
    alcoholism = st.checkbox("Alkolizm Geçmişi Var mı?")
    handicap = st.selectbox("Engellilik Düzeyi (0-4)", [0, 1, 2, 3, 4])

with col2:
    st.subheader("📅 Randevu Koşulları")
    lead_time = st.number_input("Randevu Bekleme Süresi (Gün Farkı)", min_value=0, max_value=180, value=7,
                                help="Randevunun alındığı tarih ile muayene günü arasındaki gün sayısı.")
    day_of_week = st.selectbox("Randevu Günü", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    sms_received = st.radio("Hatırlatma SMS'i Gönderildi mi?", ["Evet", "Hayır"])

st.divider()

# Tahmin Butonu
if st.button("🚨 Riski Hesapla ve Öneri Üret", type="primary", use_container_width=True):
    # Veri hazırlığı
    input_dict = {
        'Age': age,
        'Scholarship': int(scholarship),
        'Hypertension': int(hypertension),
        'Diabetes': int(diabetes),
        'Alcoholism': int(alcoholism),
        'Handicap': handicap,
        'SMS_received': 1 if sms_received == "Evet" else 0,
        'LeadTime': lead_time,
        'IsSameDay': 1 if lead_time == 0 else 0,
        'Gender_M': 1 if "Erkek" in gender else 0,
        'AppointmentDayOfWeek_Monday': 1 if day_of_week == "Monday" else 0,
        'AppointmentDayOfWeek_Saturday': 1 if day_of_week == "Saturday" else 0,
        'AppointmentDayOfWeek_Thursday': 1 if day_of_week == "Thursday" else 0,
        'AppointmentDayOfWeek_Tuesday': 1 if day_of_week == "Tuesday" else 0,
        'AppointmentDayOfWeek_Wednesday': 1 if day_of_week == "Wednesday" else 0
    }
    
    # Model sütun hizalaması
    input_df = pd.DataFrame([input_dict])
    for col in model_features:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model_features]

    # Model Tahmini
    risk_prob = model.predict_proba(input_df)[0][1] * 100

    # Sonuç ve Karar Destek Çıktısı
    st.subheader("🎯 Tahmin ve Aksiyon Raporu")
    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        st.metric(label="Gelmeme (No-Show) Riski", value=f"%{risk_prob:.1f}")

    with res_col2:
        if risk_prob >= 65:
            st.error("⚠️ **YÜKSEK RİSK:** Hastanın randevuya gelmeme ihtimali çok yüksek.")
            st.markdown("""
            * **Aksiyon Önerisi:**
              - Hastayı 24 saat önce teyit için telefonla doğrudan arayın.
              - Bu randevu slotunu acil/yedek liste (overbooking) için işaretleyin.
            """)
        elif risk_prob >= 35:
            st.warning("⚡ **ORTA RİSK:** Gelmeme ihtimali kayda değer.")
            st.markdown("""
            * **Aksiyon Önerisi:**
              - Randevudan 1 gün önce interaktif teyit SMS'i (Örn: 'EVET' yazarak onaylayın) gönderin.
            """)
        else:
            st.success("✅ **DÜŞÜK RİSK:** Hastanın gelme olasılığı yüksek.")
            st.markdown("""
            * **Aksiyon Önerisi:**
              - Standart randevu hatırlatma prosedürü yeterlidir.
            """)