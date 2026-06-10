# 🤖 E-Hand — Bionic Robotic Hand

> Main bionique robotique téléopérée par vision par ordinateur

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-orange)
![SolidWorks](https://img.shields.io/badge/SolidWorks-2024-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Description

**E-Hand** est une main bionique robotique conçue et simulée sous SolidWorks,
couplée à un système de vision par ordinateur (OpenCV + MediaPipe) permettant
de téléopérer la main en temps réel — ma main bouge, la main robotique reproduit
exactement le même geste.

---

## ✨ Fonctionnalités

- ✅ Conception mécanique complète sous SolidWorks
- ✅ 14 articulations — anatomiquement fidèle à la main humaine
- ✅ Simulation Motion — flexion/extension validée
- ✅ Détection 21 landmarks en temps réel (MediaPipe)
- ✅ Calcul d'angle de flexion par doigt
- ✅ Génération signal PWM pour 5 servo-moteurs indépendants
- 🔄 ROS2 + RViz2 — en cours
- 🔄 Arduino — commande hardware réelle

---
E-Hand/
│
├── ehand.py              # Script principal MediaPipe + PWM
├── solidworks/           # Fichiers de conception .SLDPRT / .SLDASM
├── docs/                 # Images et documentation
└── README.md
---

## 📸 Démonstration

| Conception SolidWorks | Vision temps réel |
|---|---|
| ![solidworks](#) | ![mediapipe](#) |

---

## 🎯 Applications visées

- 🦾 Téléopération en milieux dangereux
- 🏥 Prothèse bionique intelligente
- 🧠 Rééducation motrice assistée par IA

---

## 👤 Auteur

**Amir Mokhtar Ben Dhiab** — Étudiant ingénieur en électromécanique  
amirbendhiab0@gmail.com

---

## 📄 License

MIT License — libre d'utilisation avec attribution.

## 🏗️ Architecture
