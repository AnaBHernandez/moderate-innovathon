"""
ANALISIS ENERGETICO SIMPLE
==========================
Para MODERATE Innovathon - Equipo Ana + Profesora
Ana: Responsable de analisis de negocio y presentacion
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Configurar estilo general mas profesional
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#f8f9fa'

# =============================================
# 1. CARGAR DATOS (Lo mas simple)
# =============================================
print("=" * 50)
print("CARGANDO DATOS DE ENERGIA")
print("=" * 50)

# Leer archivo CSV
df = pd.read_csv('datos_energia.csv')

print(f"\nDatos cargados: {len(df)} registros")
print(f"Desde {df['fecha'].min()} hasta {df['fecha'].max()}")
print("\nPrimeras filas:")
print(df.head())

# =============================================
# 2. CALCULAR METRICAS BASICAS (Facil)
# =============================================
print("\n" + "=" * 50)
print("CALCULANDO METRICAS DE NEGOCIO")
print("=" * 50)

# Consumo total
consumo_total = df['consumo_kwh'].sum()
print(f"\nConsumo total: {consumo_total:.1f} kWh")

# Generacion total (si hay paneles solares)
if 'generacion_kwh' in df.columns:
    generacion_total = df['generacion_kwh'].sum()
    print(f"Generacion total: {generacion_total:.1f} kWh")
    
    # Autosuficiencia = cuanto generamos vs consumimos
    autosuficiencia = (generacion_total / consumo_total) * 100
    print(f"Autosuficiencia: {autosuficiencia:.1f}%")
    
    # Balance = diferencia
    balance = generacion_total - consumo_total
    if balance > 0:
        print(f"EXCEDENTE: +{balance:.1f} kWh")
    else:
        print(f"DEFICIT: {balance:.1f} kWh")

# =============================================
# 3. DETECTAR DESPERDICIO (Simple pero util)
# =============================================
print("\n" + "=" * 50)
print("DETECTANDO DESPERDICIO")
print("=" * 50)

# Si hay columna de ocupacion
if 'ocupacion' in df.columns:
    # Desperdicio = consumo cuando no hay nadie
    df['desperdicio'] = df.apply(
        lambda row: row['consumo_kwh'] if row['ocupacion'] == 0 else 0,
        axis=1
    )
    
    desperdicio_total = df['desperdicio'].sum()
    porcentaje_desperdicio = (desperdicio_total / consumo_total) * 100
    
    print(f"\nDesperdicio detectado: {desperdicio_total:.1f} kWh")
    print(f"Porcentaje de desperdicio: {porcentaje_desperdicio:.1f}%")
    
    # Calcular ahorro potencial en euros
    precio_kwh = 0.15  # 15 centimos por kWh (precio tipico)
    ahorro_eur = desperdicio_total * precio_kwh
    
    print(f"Ahorro potencial: {ahorro_eur:.2f} euros")

# =============================================
# 4. GRAFICOS MEJORADOS (Mas claros y bonitos)
# =============================================
print("\n" + "=" * 50)
print("GENERANDO VISUALIZACIONES")
print("=" * 50)

# Grafico 1: Consumo con zonas marcadas
fig, ax = plt.subplots(figsize=(14, 6))

# Separar datos por ocupacion
if 'ocupacion' in df.columns:
    df_ocupado = df[df['ocupacion'] == 1]
    df_vacio = df[df['ocupacion'] == 0]
    
    # Plot con colores diferentes
    ax.plot(df_ocupado['fecha'], df_ocupado['consumo_kwh'], 
            marker='o', linewidth=3, markersize=6, color='#2ecc71', 
            label='Consumo con ocupacion', alpha=0.8)
    ax.plot(df_vacio['fecha'], df_vacio['consumo_kwh'], 
            marker='o', linewidth=3, markersize=6, color='#e74c3c', 
            label='DESPERDICIO (sin ocupacion)', alpha=0.8)
else:
    ax.plot(df['fecha'], df['consumo_kwh'], 
            marker='o', linewidth=3, markersize=6, color='#3498db', alpha=0.8)

ax.set_title('Consumo Energetico: Donde Perdemos Dinero?', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Fecha y Hora', fontsize=14, fontweight='bold')
ax.set_ylabel('Consumo (kWh)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=12, loc='upper right')

# Rotar etiquetas
plt.xticks(rotation=45, ha='right')

# Anadir anotacion
if 'ocupacion' in df.columns and desperdicio_total > 0:
    ax.text(0.5, 0.95, f'Desperdicio total: {porcentaje_desperdicio:.1f}% = {ahorro_eur:.2f} euros',
            transform=ax.transAxes, fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#ffe5e5', alpha=0.8),
            horizontalalignment='center', verticalalignment='top')

plt.tight_layout()
plt.savefig('grafico_consumo.png', dpi=200, bbox_inches='tight')
print("Guardado: grafico_consumo.png")
plt.close()

# Grafico 2: Comparacion mejorada (si hay generacion)
if 'generacion_kwh' in df.columns:
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot de consumo y generacion
    ax.fill_between(range(len(df)), df['consumo_kwh'], 
                     alpha=0.3, color='#e74c3c', label='Consumo')
    ax.plot(df['fecha'], df['consumo_kwh'], 
            linewidth=3, color='#c0392b', marker='o', markersize=5)
    
    ax.fill_between(range(len(df)), df['generacion_kwh'], 
                     alpha=0.3, color='#2ecc71', label='Generacion')
    ax.plot(df['fecha'], df['generacion_kwh'], 
            linewidth=3, color='#27ae60', marker='s', markersize=5, linestyle='--')
    
    ax.set_title('Balance Energetico: Generamos lo Suficiente?', 
                 fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Fecha y Hora', fontsize=14, fontweight='bold')
    ax.set_ylabel('Energia (kWh)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Rotar etiquetas
    plt.xticks(rotation=45, ha='right')
    
    # Anadir anotaciones
    ax.text(0.5, 0.95, f'Autosuficiencia: {autosuficiencia:.1f}% | Balance: {balance:.1f} kWh',
            transform=ax.transAxes, fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#e8f4f8', alpha=0.8),
            horizontalalignment='center', verticalalignment='top')
    
    plt.tight_layout()
    plt.savefig('grafico_balance.png', dpi=200, bbox_inches='tight')
    print("Guardado: grafico_balance.png")
    plt.close()

# =============================================
# 5. RESUMEN EJECUTIVO (Para presentar)
# =============================================
print("\n" + "=" * 50)
print("RESUMEN EJECUTIVO")
print("=" * 50)

print(f"""
SITUACION ACTUAL:
• Consumo analizado: {consumo_total:.1f} kWh
• Periodo: {len(df)} registros
""")

if 'generacion_kwh' in df.columns:
    print(f"""• Generacion solar: {generacion_total:.1f} kWh
• Autosuficiencia: {autosuficiencia:.1f}%""")

if 'ocupacion' in df.columns:
    print(f"""
OPORTUNIDADES DETECTADAS:
• Desperdicio: {porcentaje_desperdicio:.1f}% del consumo
• Ahorro potencial: {ahorro_eur:.2f} euros en este periodo

RECOMENDACION:
• Implementar control automatico cuando edificio vacio
• Monitoreo en tiempo real para detectar anomalias
• Objetivo: Reducir desperdicio a <10%
""")

print("\nANALISIS COMPLETADO")
print("=" * 50)
