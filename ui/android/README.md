# Android (Kotlin / APK) UI Workspace

Direktori basis untuk pengembangan antarmuka **aplikasi Android** berbasis **Kotlin / Jetpack Compose** dalam ekosistem Prototype.

## 📁 Struktur

```text
ui/android/
├── components/   # Preview komponen UI Compose / XML (Button, Card, Nav, dll.)
├── apps/         # Aplikasi APK utuh (project Gradle / module)
└── README.md     # Manifest cabang platform Android
```

## 🚀 Menambahkan Aplikasi Kotlin Android

1. Letakkan proyek Gradle (`*.gradle.kts`, `settings.gradle.kts`, `src/`) di bawah `ui/android/apps/<nama-aplikasi>/`.
2. Aktifkan preview penamaan: `ui/android/components/<nama-komponen>/` untuk komponen UI yang bisa dibagikan.
3. Baca tokens desain bersama dari `ui/web/components/glass/css.css` untuk menjaga konsistensi palet antar platform.