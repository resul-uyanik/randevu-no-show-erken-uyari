# 🏥 Sağlıkta Randevu İptalleri ve Gelmeme (No-Show) Erken Uyarı Sistemi

Bu proje, poliklinik randevularına gelmeyen hastaları (**No-Show**) makine öğrenmesi teknikleriyle önceden tahmin ederek hastane kapasite kaybını ve atıl zamanı en aza indirmeyi hedefleyen uçtan uca bir veri bilimi çalışmasıdır.

---

## 📌 Proje Özeti ve İş Problemi
* **Problem:** Randevulara gelinmemesi hekimlerin takviminde boşluklara, gelir kaybına ve randevu sırası bekleyen diğer hastaların sağlık hizmetine erişiminin gecikmesine yol açmaktadır.
* **Çözüm:** Hastanın demografik bilgileri, sağlık koşulları ve randevu planlama dinamikleri üzerinden gelmeme olasılığını hesaplayan bir Random Forest modeli geliştirilmiş ve operasyonel aksiyon önerileri üreten interaktif bir erken uyarı paneli tasarlanmıştır.

---

## 📊 Öne Çıkan Bulgular (EDA)
* **Randevu Bekleme Süresi (Lead Time):** Randevunun oluşturulduğu tarih ile muayene tarihi arasındaki gün farkı arttıkça randevuya gelmeme oranı belirgin şekilde yükselmektedir.
* **Aynı Gün Randevuları:** Aynı güne alınan randevularda gelme sadakati en yüksek seviyededir.
* **SMS Bildirimi:** Hatırlatma SMS'lerinin etkisi bekleme süresine ve hedef kitleye göre değişkenlik göstermektedir.

---

## 🛠️ Kullanılan Teknolojiler
* **Programlama Dili:** Python 3.x
* **Veri Analizi & Görselleştirme:** Pandas, NumPy, Matplotlib, Seaborn
* **Makine Öğrenmesi:** Scikit-Learn (Random Forest Classifier, ROC-AUC, Sınıf Dengeleme)
* **Arayüz Geliştirme:** Streamlit
* **Model Dağıtımı & Serileştirme:** Joblib

---

## 🚀 Kurulum ve Yerel Çalıştırma

Projeyi yerel makinenizde çalıştırmak için:

```bash
# 1. Repoyu klonlayın
git clone [https://github.com/resul-uyanik/randevu-no-show-erken-uyari.git](https://github.com/resul-uyanik/randevu-no-show-erken-uyari.git)
cd randevu-no-show-erken-uyari

# 2. Sanal ortamı oluşturun ve aktif edin
python -m venv venv
# Windows için:
venv\Scripts\activate

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Streamlit erken uyarı panelini başlatın
streamlit run app.py