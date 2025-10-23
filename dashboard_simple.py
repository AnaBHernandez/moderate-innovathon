import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar datos
df = pd.read_csv('datos_energia.csv')

# Calcular metricas
consumo_total = df['consumo_kwh'].sum()
generacion_total = df['generacion_kwh'].sum()
autosuficiencia = (generacion_total / consumo_total) * 100
balance = generacion_total - consumo_total

df['desperdicio'] = df.apply(lambda row: row['consumo_kwh'] if row['ocupacion'] == 0 else 0, axis=1)
desperdicio_total = df['desperdicio'].sum()
porcentaje_desperdicio = (desperdicio_total / consumo_total) * 100
ahorro_eur = desperdicio_total * 0.15

print("=" * 60)
print("GENERANDO DASHBOARD ULTRA SIMPLE")
print("=" * 60)

# Crear figura con 4 subplots
fig = plt.figure(figsize=(20, 16))
fig.patch.set_facecolor('white')

# Configurar grid 2x2
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# =============================================
# GRAFICO 1: BARRAS COMPARATIVAS (Problema) - MANTENER
# =============================================
ax1 = fig.add_subplot(gs[0, 0])

categorias = ['Consumo\nTotal', 'Generacion\nSolar', 'DESPERDICIO\n(edificio vacio)']
valores = [consumo_total, generacion_total, desperdicio_total]
colores = ['#e74c3c', '#2ecc71', '#f39c12']

barras = ax1.bar(categorias, valores, color=colores, alpha=0.8, edgecolor='black', linewidth=2)

for i, (barra, valor) in enumerate(zip(barras, valores)):
    height = barra.get_height()
    ax1.text(barra.get_x() + barra.get_width()/2., height,
            f'{valor:.1f} kWh',
            ha='center', va='bottom', fontsize=16, fontweight='bold')

ax1.set_ylabel('Energia (kWh)', fontsize=14, fontweight='bold')
ax1.set_title('COMPARACION ENERGETICA: Donde esta el problema?', 
             fontsize=16, fontweight='bold', pad=15)
ax1.tick_params(axis='both', labelsize=12)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# =============================================
# GRAFICO 2: RESUMEN EJECUTIVO (Solucion) - MANTENER
# =============================================
ax2 = fig.add_subplot(gs[0, 1])

# Crear dashboard ejecutivo
ax2.text(0.5, 0.8, f'{porcentaje_desperdicio:.1f}%', 
         ha='center', va='center', fontsize=40, fontweight='bold', color='#e74c3c')
ax2.text(0.5, 0.65, 'DESPERDICIO', 
         ha='center', va='center', fontsize=18, fontweight='bold', color='#2c3e50')
ax2.text(0.5, 0.55, f'{desperdicio_total:.1f} kWh perdidos', 
         ha='center', va='center', fontsize=14, color='#7f8c8d')

ax2.text(0.5, 0.35, f'{ahorro_eur:.2f} €', 
         ha='center', va='center', fontsize=35, fontweight='bold', color='#27ae60')
ax2.text(0.5, 0.25, 'AHORRO POTENCIAL', 
         ha='center', va='center', fontsize=16, fontweight='bold', color='#2c3e50')
ax2.text(0.5, 0.15, 'en este periodo', 
         ha='center', va='center', fontsize=12, color='#7f8c8d')

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')
ax2.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, 
              fill=False, edgecolor='#e74c3c', linewidth=3))

# =============================================
# GRAFICO 3: ULTRA SIMPLE - ANTES vs DESPUES
# =============================================
ax3 = fig.add_subplot(gs[1, 0])

# Crear grafico de antes vs despues
situaciones = ['SITUACION\nACTUAL', 'SITUACION\nOPTIMIZADA']
desperdicio_actual = porcentaje_desperdicio
desperdicio_optimizado = 5.0  # Objetivo: 5% de desperdicio
ahorro_actual = ahorro_eur
ahorro_optimizado = ahorro_actual * (desperdicio_optimizado / desperdicio_actual)

# Crear grafico de barras
x = np.arange(len(situaciones))
width = 0.35

# Barras de desperdicio
barras1 = ax3.bar(x - width/2, [desperdicio_actual, desperdicio_optimizado], 
                  width, label='Desperdicio (%)', color=['#e74c3c', '#2ecc71'], alpha=0.8)

# Barras de ahorro (escala diferente)
ax3_twin = ax3.twinx()
barras2 = ax3_twin.bar(x + width/2, [ahorro_actual, ahorro_optimizado], 
                       width, label='Ahorro (€)', color=['#f39c12', '#27ae60'], alpha=0.8)

# Anadir valores en las barras
for i, (barra, valor) in enumerate(zip(barras1, [desperdicio_actual, desperdicio_optimizado])):
    height = barra.get_height()
    ax3.text(barra.get_x() + barra.get_width()/2., height,
            f'{valor:.1f}%', ha='center', va='bottom', fontsize=14, fontweight='bold')

for i, (barra, valor) in enumerate(zip(barras2, [ahorro_actual, ahorro_optimizado])):
    height = barra.get_height()
    ax3_twin.text(barra.get_x() + barra.get_width()/2., height,
            f'{valor:.1f}€', ha='center', va='bottom', fontsize=14, fontweight='bold')

ax3.set_xlabel('Situacion', fontsize=12, fontweight='bold')
ax3.set_ylabel('Desperdicio (%)', fontsize=12, fontweight='bold', color='#e74c3c')
ax3_twin.set_ylabel('Ahorro (€)', fontsize=12, fontweight='bold', color='#f39c12')
ax3.set_title('ANTES vs DESPUES: Impacto de la solucion', 
             fontsize=14, fontweight='bold', pad=10)
ax3.set_xticks(x)
ax3.set_xticklabels(situaciones)
ax3.grid(axis='y', alpha=0.3, linestyle='--')

# =============================================
# GRAFICO 4: ULTRA SIMPLE - ROI Y PAYBACK
# =============================================
ax4 = fig.add_subplot(gs[1, 1])

# Crear grafico de ROI simple
categorias_roi = ['Inversion\nInicial', 'Ahorro\nAnual', 'ROI\nAnual']
valores_roi = [1000, ahorro_eur * 365, (ahorro_eur * 365 / 1000) * 100]  # Asumiendo 1000€ de inversion
colores_roi = ['#3498db', '#27ae60', '#2ecc71']

barras_roi = ax4.bar(categorias_roi, valores_roi, color=colores_roi, alpha=0.8, edgecolor='black', linewidth=2)

for i, (barra, valor) in enumerate(zip(barras_roi, valores_roi)):
    height = barra.get_height()
    if i == 2:  # ROI en porcentaje
        ax4.text(barra.get_x() + barra.get_width()/2., height,
                f'{valor:.1f}%', ha='center', va='bottom', fontsize=16, fontweight='bold')
    else:  # Valores en euros
        ax4.text(barra.get_x() + barra.get_width()/2., height,
                f'{valor:.0f}€', ha='center', va='bottom', fontsize=16, fontweight='bold')

ax4.set_ylabel('Valor (€)', fontsize=12, fontweight='bold')
ax4.set_title('ROI Y PAYBACK: Cuanto se recupera?', 
             fontsize=14, fontweight='bold', pad=10)
ax4.tick_params(axis='both', labelsize=12)
ax4.grid(axis='y', alpha=0.3, linestyle='--')

# Anadir texto explicativo
ax4.text(0.5, 0.95, f'Payback: {1000 / (ahorro_eur * 365):.1f} años', 
         transform=ax4.transAxes, fontsize=12, fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='#e8f4f8', alpha=0.8),
         horizontalalignment='center', verticalalignment='top')

# =============================================
# TITULO PRINCIPAL
# =============================================
plt.suptitle('DASHBOARD ULTRA SIMPLE - MODERATE Innovathon', 
             fontsize=24, fontweight='bold', y=0.98)

# Guardar
plt.savefig('dashboard_simple.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Guardado: dashboard_simple.png")

plt.close()

print("\n" + "=" * 60)
print("DASHBOARD ULTRA SIMPLE GENERADO")
print("=" * 60)
print("\nArchivo creado: dashboard_simple.png")
print("Contiene los 4 graficos ultra simples:")
print("  - Grafico 1: Comparacion energetica (MANTENIDO)")
print("  - Grafico 2: Resumen ejecutivo (MANTENIDO)")
print("  - Grafico 3: Antes vs Despues (NUEVO - SIMPLE)")
print("  - Grafico 4: ROI y Payback (NUEVO - SIMPLE)")
print("=" * 60)
