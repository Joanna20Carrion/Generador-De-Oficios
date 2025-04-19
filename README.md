# 📨 Generador de Oficios Personalizados

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-App-lightgrey?style=flat&logo=flask)
![HTML5](https://img.shields.io/badge/HTML5-Bootstrap-orange?style=flat&logo=html5)
![Estado](https://img.shields.io/badge/Deploy-Railway-green?style=flat&logo=railway)

---

## 📝 Descripción

Aplicación web desarrollada en **Flask** que permite generar **oficios personalizados en Word** a partir de una **plantilla `.docx`**, utilizando información extraída de un archivo **Excel**.  
Los documentos generados se empaquetan automáticamente en un **archivo ZIP para descarga inmediata**, sin guardar nada en el servidor.

---

## 🎯 Funcionalidades

- Subida de archivos `.xlsx` y `.docx`
- Procesamiento de múltiples códigos de empresa
- Reemplazo automático de campos en la plantilla:
  - `[Nombre del Destinatario]`
  - `[Cargo]`
  - `[Entidad]`
  - `[Dirección]`
  - `[Distrito]`
- Adjunta un PDF específico según la **actividad** (Transmisión, Generación, Distribución, Cliente Libre)
- Descarga final de **ZIP** con todos los documentos por carpeta

---

## 💻 Tecnologías utilizadas

- ![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)  
- ![Flask](https://img.shields.io/badge/Flask-Web_App-black?style=flat&logo=flask)  
- ![Pandas](https://img.shields.io/badge/Pandas-Data--Processing-purple?style=flat&logo=pandas)  
- ![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel_Reader-yellowgreen?style=flat)  
- ![python-docx](https://img.shields.io/badge/python--docx-Word_Generator-blueviolet?style=flat)  
- ![HTML5](https://img.shields.io/badge/HTML5-+Bootstrap-orange?style=flat&logo=html5)  
- ![Railway](https://img.shields.io/badge/Deploy-Railway-green?style=flat&logo=railway)

---

## ⚙️ Requisitos

Asegúrate de tener estas dependencias en tu entorno:

```bash
pip install -r requirements.txt
```

---

## 👤 Autora

**Joanna Alexandra Carrión Pérez**  
🎓 Bachiller en Ingeniería Electrónica  
🚀 Apasionada por la ciencia de datos y sistemas inteligentes  
📧 joannacarrion14@gmail.com  
🔗 ![LinkedIn](https://img.shields.io/badge/LinkedIn-Joanna%20Carrión%20Pérez-blue?style=flat&logo=linkedin) [LinkedIn](https://www.linkedin.com/in/joanna-carrion-perez/)

---

## 🧩 Contribuciones

¿Ideas o mejoras?  
Haz un **fork**, mejora lo que gustes y envía un **pull request**. ¡Las contribuciones son bienvenidas! 
