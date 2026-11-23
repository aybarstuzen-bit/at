# ÖNERİLEN: Varyant Modu (indirim kurulumu gerekmez)

`snippets/bundle-offers-varyant.liquid` – her paket ürünün ayrı bir varyantıdır, sepete **doğrudan paket fiyatıyla** girer (2 Adet = 1.279,99 TL, 3 Adet = 1.879,99 TL). İndirim tanımlamaya gerek yoktur.

## 1. Ürün varyantlarını oluşturun
Admin → Ürünler → ürününüz → **Varyantlar → Seçenek ekle**
- Seçenek adı: **Paket**
- Değerler: **1 Adet**, **2 Adet**, **3 Adet**

| Varyant | Fiyat | Karşılaştırma fiyatı | Stok |
|---|---|---|---|
| 1 Adet | 779,99 | 1.210,00 | ayrı ayrı girin |
| 2 Adet | 1.279,99 | 2.420,00 | |
| 3 Adet | 1.879,99 | 3.630,00 | |

Ürünün renk vb. başka bir seçeneği varsa sorun değil; snippet seçili rengi koruyarak doğru paketi bulur.

## 2. Snippet'i ekleyin
1. Kodu düzenle → Snippets → **Yeni snippet** → adı `bundle-offers-varyant` → dosya içeriğini yapıştırın.
2. Özelleştir → Ürün şablonu → **Blok ekle → Özel Liquid**:
   ```liquid
   {% render 'bundle-offers-varyant', product: product %}
   ```
3. Bloğu "Satın al düğmeleri"nin üstüne taşıyın. Eski `bundle-offers` bloğunu ve önceden kurduysanız paket otomatik indirimlerini kaldırın.

Temanın kendi "Paket" seçicisi ve adet (+/-) alanı otomatik gizlenir; sepete her zaman seçili paket varyantından **1 adet** eklenir. Ayarlar snippet'in en üstündedir (`bo_option_name`, `bo_default_qty` vb.). Varyant değerlerini farklı yazdıysanız (örn. "2'li Paket"), `bo_tiers` listesindeki 2. alanı aynısıyla değiştirin.

---

# Alternatif: Adet Modu (otomatik indirim gerektirir)

Ücretli bundle uygulamasının "Birlikte al, daha çok kazan" paket görünümünü birebir veren, **uygulama gerektirmeyen** Liquid snippet'i.

## 1. Dosyayı temaya ekleyin
1. Shopify Admin → **Online Mağaza → Temalar → ⋯ → Kodu düzenle**
2. `Snippets` klasöründe **Yeni snippet ekle** → adı: `bundle-offers`
3. `snippets/bundle-offers.liquid` dosyasının tüm içeriğini yapıştırıp kaydedin.

## 2. Ürün sayfasına yerleştirin
1. **Özelleştir** → üstten **Ürünler → Varsayılan ürün** şablonunu açın.
2. Ürün bilgisi bölümünde **Blok ekle → Özel Liquid** seçin ve içine yazın:
   ```liquid
   {% render 'bundle-offers', product: product %}
   ```
3. Bloğu **"Satın al düğmeleri"** bloğunun hemen üstüne sürükleyin, kaydedin.
4. Bundle uygulamasının bloğunu kaldırın / uygulamayı silin.

## 3. Sepette indirimin düşmesi (ÜCRETSİZ otomatik indirim)
Snippet, seçilen paketin adedini sepete ekler. İndirimin ödeme sayfasında gerçekten uygulanması için Shopify'ın kendi (ücretsiz) otomatik indirimlerini kurun:

**Admin → İndirimler → İndirim oluştur → "Ürünlerde tutar indirimi"**

| | 2'li paket | 3'lü paket |
|---|---|---|
| Yöntem | Otomatik indirim | Otomatik indirim |
| Başlık (sepette görünür) | 2'li Paket İndirimi | 3'lü Paket İndirimi |
| İndirim değeri | **Sabit tutar: 279,99 TL** | **Sabit tutar: 459,98 TL** |
| "Sipariş başına bir kez uygula" | ✅ İşaretli | ✅ İşaretli |
| Geçerli ürünler | İlgili ürün(ler) | İlgili ürün(ler) |
| Minimum satın alma şartı | **Minimum ürün adedi: 2** | **Minimum ürün adedi: 3** |
| Kombinasyonlar | Hiçbiri işaretli değil | Hiçbiri işaretli değil |

İki indirim birbiriyle birleşmediğinden, 3 adette Shopify otomatik olarak daha avantajlı olanı (459,98 TL) uygular.

> Tutarlar snippet'in üstündeki `bo_tiers` listesindeki **İndirim (TL)** değeriyle aynı olmalı. Fiyatı değiştirirseniz ikisini birlikte güncelleyin:
> `İndirim = (ürün fiyatı × adet) − paket fiyatı` → 2 × 779,99 − 1.279,99 = **279,99**

**Ücretsiz kargo:** Admin → İndirimler → "Ücretsiz kargo" → Otomatik → Minimum ürün adedi: 2.
**Sürpriz hediye:** Sipariş notuna göre elle eklenebilir veya Shopify Flow ile etiketlenebilir.

## 4. Özelleştirme
Snippet'in en üstündeki **AYARLAR** bölümünden:
- `bo_heading` – başlık metni
- `bo_default_qty` – sayfa açıldığında seçili gelen paket (şu an `2` → "En Çok Satan" seçili gelir)
- `bo_hide_theme_qty` – temanın +/- adet seçicisini gizler
- `bo_tiers` – paket satırları: `Adet ~ Başlık ~ Alt yazı ~ İndirim TL ~ Üst etiket ~ Alt şerit ~ Rozet(evet/hayir)`
  - Alt yazıda `[birim]` adet başı fiyatı, `[adet]` adedi gösterir.
- Renkler: `<style>` içindeki `--bo-pink`, `--bo-cream`, `--bo-peach` değişkenleri.

## Özellikler
- Mobil ve masaüstü uyumlu, ekstra kütüphane yok, tema CSS'ini bozmaz.
- Üstü çizili fiyat, % rozet ve "tasarruf ediyorsunuz" tutarı ürünün **karşılaştırma fiyatından** otomatik hesaplanır.
- Varyant (renk/boy) değiştiğinde tüm fiyatlar anında güncellenir.
- Mağazanın para formatını (`{{amount}}TL` vb.) kullanır.
- Dawn ve Dawn tabanlı temalara (Sense, Craft, Refresh, Spotlight…) göre yazıldı; formu ve adet alanını otomatik bulur, yoksa gizli adet alanı ekler.
