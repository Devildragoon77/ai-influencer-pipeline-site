# Konten panduan Bahasa Indonesia. Body berupa fragmen HTML.

KIT = '<a href="https://lionheart886.gumroad.com/l/ai-influencer-pipeline-kit">AI Influencer Pipeline Kit</a>'
DNA = '<a href="https://lionheart886.gumroad.com/l/reel-dna-extractor">Reel DNA Extractor</a>'

GUIDES = {

"cara-membuat-ai-influencer": {
"title": "Cara Membuat AI Influencer di 2026 (Arsitektur Lengkap + Biaya Nyata)",
"desc": "Panduan lengkap membuat AI influencer yang posting otomatis ke Instagram: desain persona, pipeline n8n, API resmi Instagram, quality control, dan biaya bulanan sebenarnya.",
"h1": "Cara Membuat AI Influencer di 2026",
"cta": f"Lewati 6 bulan ngoding — sistem produksi yang dijelaskan di sini sudah dipaketkan sebagai {KIT} (dokumentasi bahasa Inggris).",
"body": """
<p>Kebanyakan tutorial "cara bikin AI influencer" berhenti di generate wajah cantik. Padahal yang menentukan sukses adalah sistem produksinya: pipeline yang posting setiap hari tanpa kamu, dengan kualitas yang cukup tinggi supaya akunnya benar-benar tumbuh.</p>

<h2>Arsitektur yang terbukti jalan</h2>
<ol>
<li><strong>Riset</strong> — scrape akun-akun benchmark di niche kamu dan ekstrak apa yang bikin konten mereka perform: pose, framing, pencahayaan, color grade. Kami menyebutnya "Visual DNA". Generate dari prompt kosong hasilnya generik; mereplikasi format yang terbukti hasilnya nyambung dengan selera niche.</li>
<li><strong>Generasi</strong> — model image dengan face reference yang dikunci. Aset terpenting adalah SATU foto portrait persona yang bersih dan pencahayaannya netral: semua gambar berikutnya dikondisikan dari situ. Wajah yang berubah-ubah adalah pembunuh kualitas nomor satu.</li>
<li><strong>Quality control</strong> — gerbang AI (kami pakai Claude) yang menilai tiap hasil PASS/FAIL terhadap spesifikasi, dan alasan gagalnya dimasukkan kembali ke prompt berikutnya. Maksimal 3 percobaan. Tanpa ini, feed kamu penuh tangan berjari enam.</li>
<li><strong>Persetujuan manusia</strong> — setiap konten masuk ke Telegram dengan tombol approve/reject. Cuma ~5 menit per hari dan ini wajib: konten AI tanpa review adalah jalan tercepat akun kena masalah kebijakan.</li>
<li><strong>Publishing</strong> — Instagram Graph API resmi dengan Meta developer app milikmu sendiri. Otomasi akun sendiri tidak perlu app review. Bot browser bikin akun kena banned; API resmi tidak.</li>
</ol>

<h2>Keputusan desain persona yang penting</h2>
<ul>
<li><strong>Buka-bukaan bahwa persona ini AI.</strong> Ini kebijakan Instagram, dan persona yang ketahuan belakangan kehilangan semua peluang brand deal. Audiens Gen-Z 2026 tidak masalah dengan AI yang jujur.</li>
<li><strong>Kunci identitas di fitur wajah, bukan ekspresi.</strong> Blok identitas mendeskripsikan rambut, mata, kulit, postur — sementara pose, arah pandang, dan ekspresi mengikuti foto benchmark. Ekspresi yang di-hardcode bikin semua post terlihat sama.</li>
<li><strong>Pilih niche dengan format visual yang bisa direplikasi</strong> — fashion, fitness, lifestyle. Niche tutorial atau talking-head tidak cocok dengan pipeline ini.</li>
</ul>

<h2>Biaya bulanan (terverifikasi Juni 2026)</h2>
<table>
<tr><th>Komponen</th><th>Per bulan</th></tr>
<tr><td>n8n (self-hosted, mesin otomasinya)</td><td>Rp 0</td></tr>
<tr><td>VPS 24/7 (opsional)</td><td>~Rp 100rb ($6)</td></tr>
<tr><td>Claude API (caption, Visual DNA, QC)</td><td>Rp 50–160rb</td></tr>
<tr><td>Apify (scraping benchmark)</td><td>~Rp 80rb</td></tr>
<tr><td>Kredit generate gambar/video</td><td>Rp 0–500rb tergantung frekuensi</td></tr>
</table>
<p>Total kasar: Rp 250rb–800rb/bulan untuk akun yang posting harian. Yang mahal adalah video (reels) — lihat <a href="kling-motion-control.html">panduan Kling motion control</a>.</p>

<h2>Ekspektasi waktu</h2>
<p>Setup: satu akhir pekan kalau kamu teknis. Pertumbuhan: berbulan-bulan — otomasi menyelesaikan produksi, bukan audiens. Akun yang menang memperlakukan pipeline sebagai mesin konsistensi: tidak pernah bolong posting, tidak pernah burnout, dan jam manusiamu bebas untuk hal yang tidak bisa diotomasi (pilihan niche, kolab, outreach brand).</p>
"""},

"otomatisasi-posting-instagram-n8n": {
"title": "Auto-Posting Instagram dengan Graph API Resmi + n8n (Panduan 2026)",
"desc": "Cara posting otomatis ke Instagram (feed, story, reels) pakai Graph API resmi dan n8n — setup token, alur publish dua langkah, dan jebakan-jebakan yang bikin gagal.",
"h1": "Auto-Posting Instagram: Graph API Resmi + n8n",
"cta": f"Semua ini sudah jadi di {KIT} — 13 workflow n8n siap import, termasuk publisher untuk post, story, dan reels.",
"body": """
<p>Kamu tidak butuh tools penjadwalan berbayar atau bot browser yang berisiko untuk auto-posting ke Instagram. Graph API resmi bisa handle post, story, dan reels — gratis, legal, dan stabil. Ini setup yang terbukti jalan.</p>

<h2>Prasyarat</h2>
<ul>
<li>Akun Instagram <strong>profesional</strong> (creator/bisnis) yang terhubung ke Facebook Page</li>
<li>Meta developer app rasa Instagram-Login dengan use case "Manage messaging & content"</li>
<li>Long-lived token dengan <code>instagram_business_basic</code> dan <code>instagram_business_content_publish</code></li>
</ul>
<p>Dua fakta yang menghemat berjam-jam: token jenis ini memanggil <code>graph.instagram.com</code> (bukan graph.facebook.com), dan otomasi akun sendiri cukup standard access — <strong>tidak perlu Meta app review</strong>.</p>

<h2>Alur publish dua langkah</h2>
<pre><code>POST https://graph.instagram.com/v23.0/{ig-user-id}/media
     ?image_url={url-publik}&caption={caption}&access_token={token}
# balikannya {"id": "container-id"}

POST https://graph.instagram.com/v23.0/{ig-user-id}/media_publish
     ?creation_id={container-id}&access_token={token}</code></pre>
<p>Di n8n ini dua node HTTP Request dengan Wait pendek di antaranya (container butuh beberapa detik diproses; untuk reels, poll <code>status_code</code> container sampai <code>FINISHED</code>).</p>
<ul>
<li><strong>Story:</strong> alur sama dengan <code>media_type=STORIES</code></li>
<li><strong>Reels:</strong> <code>media_type=REELS</code> + <code>video_url</code> (harus .mp4 yang bisa diakses publik)</li>
<li><strong>Hosting gambar:</strong> API mengambil media lewat URL, jadi hasil generate harus di-host dulu — akun gratis Cloudinary cukup.</li>
</ul>

<h2>Jebakan dari pengalaman produksi</h2>
<ul>
<li><strong>Timezone default n8n adalah America/New_York.</strong> Kalau instance-mu belum diset, cron "jam 8 malam" jalan jam 8 malam waktu New York — set <code>GENERIC_TIMEZONE=Asia/Jakarta</code> atau per-workflow <code>settings.timezone</code>.</li>
<li><strong>Page token kedaluwarsa (~60 hari).</strong> Pasang reminder rotasi; token mati diam-diam adalah penyebab "kok berhenti posting" paling umum.</li>
<li><strong>Pakai content queue, jangan posting langsung.</strong> Google Sheet dengan kolom <code>id | status | image_url | caption | scheduled_time</code> memungkinkan approval sebelum workflow publisher mengambil baris <code>approved</code>. Memisahkan generasi dari publishing inilah yang bikin sistem aman ditinggal.</li>
<li><strong>Link sticker di story tidak bisa lewat API</strong> — tetap manual. Highlights juga tidak ada API publiknya.</li>
</ul>
"""},

"cara-ai-influencer-menghasilkan-uang": {
"title": "Cara AI Influencer Menghasilkan Uang di 2026 (Versi Jujur, Konteks Indonesia)",
"desc": "Jalur monetisasi AI influencer yang realistis di Indonesia: UGC ads, affiliate Shopee/Tokopedia/TikTok Shop, endorse UMKM, subscription — dengan ambang follower yang jujur.",
"h1": "Cara AI Influencer Menghasilkan Uang (Konteks Indonesia)",
"cta": f"Sisi produksinya sudah terpecahkan — {KIT} adalah mesin posting/reels/balasan lengkapnya, jadi jam kerjamu fokus ke deal.",
"body": """
<p>Kenyataan yang jarang dibilang: AI influencer adalah bisnis media, dan bisnis media memonetisasi audiens — yang butuh berbulan-bulan dibangun. Ini jalur yang benar-benar menghasilkan, diurutkan dari yang paling realistis untuk akun kecil, lengkap dengan ambang yang tidak pernah disebut di thread-thread hype.</p>

<h2>1. Jasa UGC ads untuk brand (jalan dari 0 follower)</h2>
<p>Brand butuh materi iklan lebih dari mereka butuh audiensmu. Persona AI yang bisa "memakai" produk dan tampil di reels adalah kapasitas produksi iklan — Rp 800rb–5jt per video lewat marketplace UGC atau outreach langsung ke brand DTC. Satu-satunya jalur yang dibayar SEBELUM punya audiens, karena yang dijual produksi, bukan reach.</p>

<h2>2. Affiliate marketplace lokal (jalan dari ~100 follower)</h2>
<p>Ini keunggulan pasar Indonesia: <strong>Shopee Affiliate, Tokopedia Affiliate, dan TikTok Shop Affiliate approve hampir instan</strong> — bandingkan dengan Amazon yang ada masa probation 180 hari. Komisi per penjualan dari link di bio atau konten. Awalnya recehan, tapi nilai sebenarnya di fase ini adalah <em>data konversi</em>: produk apa yang diklik audiensmu memberi tahu apa yang layak dijual nanti.</p>
<p>Khusus TikTok Shop: format video commerce-nya persis output pipeline reels — produk + persona + motion. Pipeline yang sama yang bikin konten Instagram bisa memproduksi konten affiliate TikTok Shop secara massal, dengan gerbang approval tetap jalan.</p>

<h2>3. Endorse / paid promote UMKM lokal (realistis dari ~1.000 follower engaged)</h2>
<p>Di bawah 1.000 follower dengan engagement nyata, outreach justru membakar kontak — tunggu ambangnya. Dua hal wajib untuk persona AI: <strong>buka status AI di media kit sejak awal</strong> (ketahuan belakangan = deal batal + risiko akun), dan bawa statistik engagement, bukan jumlah follower. Brand lokal/UMKM di niche persona jauh lebih sering closing daripada brand besar — dan rate Rp 200rb–1jt per post untuk micro-influencer adalah pasar yang sangat hidup di Indonesia.</p>

<h2>4. Subscription dan konten eksklusif (realistis dari ~10rb follower)</h2>
<p>Baru masuk akal setelah audiens besar dan hangat. Data lapangan: perbedaan akun persona $1k/bulan vs $5k+/bulan biasanya 4+ aliran pendapatan paralel — tapi tiap aliran baru dinyalakan setelah audiensnya sanggup menopang.</p>

<h2>5. Menjual mesinnya (jalan hari ini juga, bukan pendapatan influencer)</h2>
<p>Skill yang membangun AI influencer — otomasi n8n, pipeline generasi, quality control — laku dijual ke kreator dan bisnis lain sebagai produk dan jasa, berapapun follower-mu. Banyak operasi "AI influencer" diam-diam menghasilkan lebih banyak dari sini daripada dari personanya sendiri.</p>

<h2>Urutan yang jujur</h2>
<p>Pendapatan kapasitas-produksi dulu (UGC, jasa/produk), affiliate sebagai pengumpulan data kedua, endorse UMKM di 1k, subscription di 10k. Siapapun yang menjual jalur "brand deal di 200 follower" sedang menjual mimpi, bukan matematika.</p>
"""},

"analisis-reel-viral": {
"title": "Kenapa Reel Bisa Viral: Membedah Struktur, Gerakan, dan Bahasa Kamera Jadi Data",
"desc": "Metode membedah reel viral menjadi struktur yang bisa dipakai ulang: timeline cut, energi gerakan, bahasa kamera, pencahayaan — dan cara memakai blueprint-nya untuk kontenmu.",
"h1": "Membedah Reel Viral Menjadi Blueprint",
"cta": f"{DNA} mengotomasi seluruh analisis ini — masukkan URL reel, keluar blueprint JSON terstruktur, termasuk motion prompt Kling.",
"body": """
<p>"Pelajari yang works di niche kamu" adalah nasihat yang semua orang kasih tapi tidak ada yang operasionalkan. Ini cara mengubah reel yang perform jadi data terstruktur yang benar-benar bisa dipakai ulang — kami menyebutnya DNA reel.</p>

<h2>Lima lapisan yang layak diekstrak</h2>
<ol>
<li><strong>Timeline cut.</strong> Berapa shot, berapa lama masing-masing bertahan, di mana ritme berubah. Mayoritas short-form viral ada di 1–4 cut — dan timing cut pertama adalah pengait retensi.</li>
<li><strong>Gerakan subjek.</strong> Apa yang dilakukan performer secara fisik, ketukan demi ketukan, plus kurva energinya. Lapisan ini yang paling buruk dideskripsikan prompt teks dan paling menentukan hasil.</li>
<li><strong>Bahasa kamera.</strong> Jarak (close/medium/full), sudut, dan gerakan (terkunci, handheld, push-in). "Handheld setinggi dada gaya HP" terbaca sangat berbeda dari "tripod terkunci full-body".</li>
<li><strong>Pencahayaan dan grade.</strong> Arah sumber, keras/lembutnya, suhu warna, dan finishing-nya. Konsistensi estetika antar-post datang dari menyalin lapisan ini dengan presisi.</li>
<li><strong>Kerangka format.</strong> Hook (1,5 detik pertama), pengembangan, payoff. Lepaskan subjek spesifiknya dan kerangkanya bisa dipindah antar-niche.</li>
</ol>

<h2>Metode praktisnya</h2>
<p>Ekstrak 6–10 frame berjarak rata dari reel, lalu minta model vision mendeskripsikan tiap lapisan dalam JSON terstruktur. Detail prompt yang krusial: minta <em>fakta yang bisa diamati</em> (durasi shot dalam detik, arah cahaya), bukan interpretasi ("vibe-nya energik") — fakta bisa dipakai ulang, vibe tidak.</p>

<h2>Memakai blueprint</h2>
<ul>
<li><strong>Untuk generasi AI:</strong> buat ulang frame pertama dengan karaktermu (pose, framing, cahaya dari blueprint), lalu gerakkan dengan deskripsi motion-nya — atau dengan video aslinya via motion control Kling.</li>
<li><strong>Untuk kreator manusia:</strong> blueprint adalah shot list. Cut yang sama, posisi kamera yang sama, subjekmu.</li>
<li><strong>Untuk strategi:</strong> bedah 50 reel teratas di niche-mu dan polanya langsung kelihatan — kerangka yang berulang, pencahayaan dominan, 2–3 format yang benar-benar menopang niche itu. Bikin yang itu dulu sebelum menciptakan format baru.</li>
</ul>

<p>Satu garis etika: blueprint mendeskripsikan struktur, bukan menyalin konten. Replikasi <em>format</em> dengan subjek dan styling-mu sendiri — jangan reproduksi footage atau identitas orang.</p>
"""},

"kling-motion-control": {
"title": "Kling Motion Control: Transfer Gerakan Reel Asli ke Karakter AI (2026)",
"desc": "Cara kerja Kling V3 Omni motion control, biayanya, dan cara memakai video referensi untuk menggerakkan karakter AI untuk reels Instagram/TikTok.",
"h1": "Kling Motion Control: Gerakan Asli di Karakter AI",
"cta": f"{DNA} mengubah reel apapun jadi blueprint gerakan siap pakai — termasuk motion prompt Kling-nya.",
"body": """
<p>Video AI dari teks punya plafon: kamu bisa mendeskripsikan koreografi, tapi model yang mengarang performanya, dan identitas wajah cenderung bergeser tiap detik. Motion control membaliknya — kamu memberi <em>video referensi</em> dan model mentransfer gerakan performer aslinya ke karaktermu.</p>

<h2>Apa yang dilakukan Kling V3 Omni</h2>
<p>Dua input: <strong>gambar frame awal</strong> (karaktermu — identitas, outfit, scene) dan <strong>video referensi</strong> (3–30 detik performa nyata). Output mempertahankan identitas karaktermu sambil mereproduksi gerakan tubuh, timing gestur, dan energi referensinya. Di tes produksi kami, identitas bertahan jauh lebih baik daripada koreografi teks.</p>

<h2>Realita biaya (Juni 2026)</h2>
<table>
<tr><th>Mode</th><th>Biaya</th><th>Catatan</th></tr>
<tr><td>Image-to-video biasa (koreografi teks)</td><td>~13 kredit/detik</td><td>5 dtk ≈ 65 kredit</td></tr>
<tr><td>V3 Omni motion control</td><td>15 kredit/detik</td><td>5 dtk = 75, 10 dtk = 150</td></tr>
</table>
<p>Biaya mengikuti panjang output, bukan kerumitan. Mulai dari klip 5 detik: panjang jarang jadi alasan reel gagal, dan biayanya setengah.</p>

<h2>Alur kerja yang hasilnya meyakinkan</h2>
<ol>
<li><strong>Pilih reel benchmark</strong> dengan subjek manusia dan cut sedikit (≤4). Cut adalah musuh: mendorong gerakan melewati batas cut bikin karakter "teleport" antar-pose.</li>
<li><strong>Replikasi frame pertamanya</strong> dengan karaktermu: pose, framing, scene, cahaya sama, identitas karaktermu. Generate di 9:16 (1080×1920) — Kling mengikuti rasio gambar sumbernya.</li>
<li><strong>Jalankan motion control</strong> dengan gambar itu + video benchmark, dengan prompt menjaga identitas dan mentransfer gerakan N detik pertama.</li>
<li><strong>Tetap pakai approval manusia</strong> sebelum publish. Motion transfer itu bagus, bukan sempurna — tangan dan putaran cepat masih kadang gagal.</li>
</ol>

<h2>Peringatan praktis</h2>
<ul>
<li>Generasi tetap jalan di server walau client-mu timeout — poll hasilnya, jangan retry (retry = bayar dua kali).</li>
<li>Reel panjang: potong di batas cut, generate per segmen, gabungkan dengan ffmpeg.</li>
<li>Etika/kebijakan: transfer <em>gaya gerakan</em>, buka status AI kontenmu, dan jangan mereproduksi orang yang bisa dikenali. Gerakannya adalah teknik; identitasnya harus milikmu.</li>
</ul>
"""},

}
