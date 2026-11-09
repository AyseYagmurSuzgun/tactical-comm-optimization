# Problem Tanımı

## 1. Amaç
Taktik sahada kara unsurlarına veya İHA'lara entegre edilen baz istasyonu ve
radyo link cihazlarının konumlarını, haberleşme kapsaması ve toplam sistem
verimi (throughput) açısından en iyi olacak şekilde belirlemek.

## 2. Simülasyon Ortamı
- Alan: 5 km x 5 km, hücre boyutu 50 m (100 x 100 grid)
- Arazi: yükseklik haritası ve engel (bina/orman) bilgisi
- Frekans: 900 MHz (hassasiyet analizinde 2.4 GHz de denenecek)
- Yayılım modeli: log-distance yol kaybı + log-normal gölgeleme +
  arazi kaynaklı görüş hattı (LOS) kontrolü ve bıçak sırtı difraksiyon kaybı

## 3. Düğümler
- Sabit baz istasyonu: 1-3 adet
- Hareketli röle (kara aracı veya İHA): 2-5 adet
- Kullanıcı/terminal: 20-100 adet

## 4. Karar Değişkenleri
- Hareketli rölelerin (x, y) konumları
- İHA için ek olarak irtifa (anten yüksekliği)

## 5. Amaç Fonksiyonu
Kapsama oranı ve toplam throughput'un birlikte maksimize edilmesi:

    J = w1 * kapsama + w2 * throughput - ceza(kısıt ihlali)

- Kapsama: SINR değeri eşiğin üstünde olan alan/kullanıcı yüzdesi
- Throughput: kullanıcı başına B * log2(1 + SINR), toplamı alınır
- Ek metrik: en düşük kullanıcı throughput'u (adalet)

## 6. Kısıtlar
- Röleler simülasyon alanı içinde kalmalı
- Minimum SINR eşiği (başlangıçta 5 dB)
- Hareket hızı ve adım büyüklüğü sınırlı (dinamik senaryoda)
- İHA irtifa aralığı sınırlı

## 7. Yöntemler
- Referans (baseline): rastgele yerleşim, düzgün grid, k-means tabanlı yerleşim
- Optimizasyon: PSO ve Genetik Algoritma
- Pekiştirmeli öğrenme: PPO (hareketli kullanıcı senaryosu)

## 8. Değerlendirme
Her yöntem birden fazla rastgele tohum (seed) ile tekrarlanır. Elde edilen
yerleşimin kapsama ve throughput değerleri, referans yerleşimlere göre yüzde
kazanç olarak raporlanır.

## 9. Çıktılar
- Simülasyon ortamı
- Konumlandırma algoritması
- Kapsama-verim karşılaştırması