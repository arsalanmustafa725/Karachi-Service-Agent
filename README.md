# 🏙️ Karachi Service Agent (KSA)
> **AI Seekho Google Antigravity National Hackathon 2026 Project**  
> **Team:** Team KSA Orchestrator  
> **Author:** Arsalan (Team Lead)  

---

## 📌 About The Project

**Karachi Service Agent (KSA)** is an AI-powered, multi-lingual location and service orchestration system built specifically for the residents of Karachi, Pakistan.

Finding reliable service providers (such as **plumbers, electricians, AC repair technicians, and tutors**) across different neighborhoods in Karachi can be challenging. KSA solves this problem by using an **LLM-driven Agent Orchestrator (Groq Llama 3.3 70B)** that dynamically understands user queries in **Urdu Script, Roman Urdu, or English**, maps them to local service providers, and integrates with **Google Maps** for real-time location tracing and direct communication.

---

## ✨ Key Features

* 🧠 **Smart Language Orchestrator:** Automatically detects the input script (Urdu Script, Roman Urdu, or English) and responds strictly in the exact same script/language without code-mixing.
* 📍 **Karachi Service Database & Location Tracing:** Maps user requirements to local mechanics, electricians, and plumbers across areas like Gulshan-e-Iqbal, Saddar, Nazimabad, and DHA.
* 📲 **Click-to-Call Link Integration:** Generates direct dial links (`tel:`) and Google Maps search buttons for quick contact.
* 💬 **Session Memory:** Retains multi-turn conversation context so users can ask follow-up questions seamlessly.
* 🛠️ **Real-Time Technical Monitoring:** Built-in sidebar state logger displaying agent status, active model parameters, and stack telemetry.

---

## 🧬 Core Technical Stack

* **Frontend / UI:** [Streamlit](https://streamlit.io/)
* **AI Orchestrator Engine:** Groq REST API (`llama-3.3-70b-versatile`)
* **Location & Vision Mapping:** Google Places & Maps API
* **Language / Environment:** Python 3.x (`requests`, `json`, `streamlit`)

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system:
```bash
python --version
