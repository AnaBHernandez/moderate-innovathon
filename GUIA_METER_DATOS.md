# 📥 GUÍA RÁPIDA: CÓMO METER DATOS NUEVOS DEL EVENTO

## ⏱️ TIEMPO TOTAL: 5 MINUTOS

---

## 📋 PASO 1: GUARDAR EL ARCHIVO DE DATOS (30 segundos)

**Te darán un archivo:** `datos_evento.csv` o `datos_energia_real.xlsx`

### Si es CSV:
1. Copiar a: `C:\Users\AnaJoseValeria\Documents\Proyectos\moderate-innovathon`
2. ✅ Listo

### Si es Excel (.xlsx):
1. Abrir en Excel
2. Archivo → Guardar como
3. Tipo: **CSV (delimitado por comas)**
4. Nombre: `datos_evento.csv`
5. Guardar en la carpeta del proyecto
6. ✅ Listo

---

## 📋 PASO 2: CAMBIAR NOMBRE EN LOS SCRIPTS (2 minutos)

### 🔹 SCRIPT 1: analisis_simple.py

**Abrir:**
```bash
notepad analisis_simple.py
Buscar (Ctrl+F):

pd.read_csv('datos_energia.csv')
Cambiar datos_energia.csvpordatos_evento.csv