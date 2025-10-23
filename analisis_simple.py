"""
📊 ANÁLISIS ENERGÉTICO SIMPLE
================================
Para MODERATE Innovathon - Equipo Ana + Profesora
Ana: Responsable de análisis de negocio y presentación
"""

import pandas as pd
import matplotlib.pyplot as plt

# =============================================
# 1. CARGAR DATOS (Lo más simple)
# =============================================
print("=" * 50)
print("📂 CARGANDO DATOS DE ENERGÍA")
print("=" * 50)

# Leer archivo CSV
df = pd.read_csv('datos_energia.csv')

print(f"\n✅ Datos cargados: {len(df)} registros")
print(f"📅 Desde {df['fecha'].min()} hasta {df['fecha'].max()}")
print("\n🔍 Primeras filas:")
print(df.head())

# =============================================
# 2. CALCULAR MÉTRICAS BÁSICAS (Fácil)
# =============================================
print("\n" + "=" * 50)
print("📊 CALCULANDO MÉTRICAS DE NEGOCIO")
print("=" * 50)

# Consumo total
consumo_total = df['consumo_kwh'].sum()
print(f"\n💡 Consumo total: {consumo_total:.1f} kWh")

# Generación total (si hay paneles solares)
if 'generacion_kwh' in df.columns:
    generacion_total = df['generacion_kwh'].sum()
    print(f"⚡ Generación total: {generacion_total:.1f} kWh")
    
    # Autosuficiencia = cuánto generamos vs consumimos
    autosuficiencia = (generacion_total / consumo_total) * 100
    print(f"🎯 Autosuficiencia: {autosuficiencia:.1f}%")
    
    # Balance = diferencia
    balance = generacion_total - consumo_total
    if balance > 0:
        print(f"✅ EXCEDENTE: +{balance:.1f} kWh")
    else:
        print(f"⚠️ DÉFICIT: {balance:.1f} kWh")

# =============================================
# 3. DETECTAR DESPERDICIO (Simple pero útil)
# =============================================
print("\n" + "=" * 50)
print("🔍 DETECTANDO DESPERDICIO")
print("=" * 50)

# Si hay columna de ocupación
if 'ocupacion' in df.columns:
    # Desperdicio = consumo cuando no hay nadie
    df['desperdicio'] = df.apply(
        lambda row: row['consumo_kwh'] if row['ocupacion'] == 0 else 0,
        axis=1
    )
    
    desperdicio_total = df['desperdicio'].sum()
    porcentaje_desperdicio = (desperdicio_total / consumo_total) * 100
    
    print(f"\n🚫 Desperdicio detectado: {desperdicio_total:.1f} kWh")
    print(f"📉 Porcentaje de desperdicio: {porcentaje_desperdicio:.1f}%")
    
    # Calcular ahorro potencial en €
    precio_kwh = 0.15  # 15 céntimos por kWh (precio típico)
    ahorro_eur = desperdicio_total * precio_kwh
    
    print(f"💰 Ahorro potencial: {ahorro_eur:.2f} €")

# =============================================
# 4. GRÁFICOS SIMPLES (Visual pero claro)
# =============================================
print("\n" + "=" * 50)
print("📈 GENERANDO VISUALIZACIONES")
print("=" * 50)

# Gráfico 1: Consumo a lo largo del tiempo
plt.figure(figsize=(12, 5))
plt.plot(df['fecha'], df['consumo_kwh'], marker='o', linewidth=2, markersize=4)
plt.title('📊 Consumo Energético en el Tiempo', fontsize=14, fontweight='bold')
plt.xlabel('Fecha')
plt.ylabel('Consumo (kWh)')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico_consumo.png', dpi=150)
print("✅ Guardado: grafico_consumo.png")

# Gráfico 2: Comparación (si hay generación)
if 'generacion_kwh' in df.columns:
    plt.figure(figsize=(12, 5))
    plt.plot(df['fecha'], df['consumo_kwh'], label='Consumo', linewidth=2)
    plt.plot(df['fecha'], df['generacion_kwh'], label='Generación', linewidth=2, linestyle='--')
    plt.title('⚡ Consumo vs Generación', fontsize=14, fontweight='bold')
    plt.xlabel('Fecha')
    plt.ylabel('Energía (kWh)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('grafico_balance.png', dpi=150)
    print("✅ Guardado: grafico_balance.png")

# =============================================
# 5. RESUMEN EJECUTIVO (Para presentar)
# =============================================
print("\n" + "=" * 50)
print("📋 RESUMEN EJECUTIVO")
print("=" * 50)

print(f"""
SITUACIÓN ACTUAL:
• Consumo analizado: {consumo_total:.1f} kWh
• Período: {len(df)} registros
""")

if 'generacion_kwh' in df.columns:
    print(f"""• Generación solar: {generacion_total:.1f} kWh
• Autosuficiencia: {autosuficiencia:.1f}%""")

if 'ocupacion' in df.columns:
    print(f"""
OPORTUNIDADES DETECTADAS:
• Desperdicio: {porcentaje_desperdicio:.1f}% del consumo
• Ahorro potencial: {ahorro_eur:.2f} € en este período

RECOMENDACIÓN:
• Implementar control automático cuando edificio vacío
• Monitoreo en tiempo real para detectar anomalías
• Objetivo: Reducir desperdicio a <10%
""")

print("\n✅ ANÁLISIS COMPLETADO")
print("=" * 50)