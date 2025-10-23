# MODERATE Innovathon - Analisis Energetico Simple

**Evento:** 24 octubre 2024 - Escuela Politecnica Gijon  
**Equipo:** Ana Belen + Profesora

---

## QUE HACE ESTE PROYECTO

Este proyecto analiza el consumo energetico de edificios para detectar **desperdicio de energia** y calcular el **ahorro potencial en euros**.

### PROBLEMA QUE RESUELVE:
- Las instalaciones consumen energia cuando estan vacias
- No hay control automatico del consumo
- Se pierde dinero en energia desperdiciada

### SOLUCION:
- Detecta cuando hay desperdicio (consumo sin ocupacion)
- Calcula cuanto dinero se puede ahorrar
- Genera graficos profesionales para presentar
- Da recomendaciones accionables

---

## COMO USAR

### 1. INSTALAR DEPENDENCIAS
```bash
pip install pandas matplotlib
```

### 2. EJECUTAR ANALISIS
```bash
python analisis_simple.py
```

### 3. GENERAR GRAFICOS DE PRESENTACION
```bash
python graficos_presentacion.py
```

---

## ARCHIVOS PRINCIPALES

### Scripts de Analisis:
- **`analisis_simple.py`** - Analisis principal con deteccion de desperdicio
- **`graficos_presentacion.py`** - Genera graficos para presentacion

### Datos:
- **`datos_energia.csv`** - Dataset con consumo, generacion y ocupacion

### Documentacion:
- **`GUIA_METER_DATOS.md`** - Como actualizar datos del evento
- **`GUION_PRESENTACION.md`** - Script de 2 minutos para presentar

### Visualizaciones:
- **`grafico_consumo.png`** - Analisis de desperdicio
- **`grafico_balance.png`** - Balance energetico
- **`presentacion_barras.png`** - Grafico de barras para presentacion
- **`presentacion_resumen.png`** - Dashboard ejecutivo

### Web:
- **`vision_produccion.html`** - Pagina web con dashboard visual

---

## METRICAS QUE DETECTA

- **Desperdicio:** Porcentaje de energia consumida sin ocupacion
- **Ahorro potencial:** Dinero que se puede ahorrar (en euros)
- **Autosuficiencia:** Porcentaje de energia renovable vs consumo
- **Balance energetico:** Diferencia entre generacion y consumo

---

## RESULTADOS ACTUALES

- **Desperdicio detectado:** 16.1% del consumo total
- **Ahorro potencial:** 32.73 euros en el periodo analizado
- **Autosuficiencia:** 56.1% (energia renovable)

---

## PARA EL EVENTO

1. **Actualizar datos:** Seguir `GUIA_METER_DATOS.md`
2. **Ejecutar analisis:** `python analisis_simple.py`
3. **Generar graficos:** `python graficos_presentacion.py`
4. **Presentar:** Usar `GUION_PRESENTACION.md`

---

## TECNOLOGIAS

- **Python** - Analisis de datos
- **Pandas** - Manipulacion de datos
- **Matplotlib** - Visualizaciones
- **HTML/CSS** - Dashboard web

---

**Simple pero efectivo. ROI inmediato. Entendible para cualquiera.**