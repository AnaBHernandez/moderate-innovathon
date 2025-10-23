import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('datos_energia.csv')

consumo_total = df['consumo_kwh'].sum()
generacion_total = df['generacion_kwh'].sum()
autosuficiencia = (generacion_total / consumo_total) * 100
balance = generacion_total - consumo_total

df['desperdicio'] = df.apply(lambda row: row['consumo_kwh'] if row['ocupacion'] == 0 else 0, axis=1)
desperdicio_total = df['desperdicio'].sum()
porcentaje_desperdicio = (desperdicio_total / consumo_total) * 100
ahorro_eur = desperdicio_total * 0.15

print("=" * 60)
print("GENERANDO GRAFICOS PARA PRESENTACION")
print("=" * 60)

# GRAFICO 1: BARRAS COMPARATIVAS
fig, ax = plt.subplots(figsize=(14, 8))

categorias = ['Consumo\nTotal', 'Generacion\nSolar', 'DESPERDICIO\n(edificio vacio)']
valores = [consumo_total, generacion_total, desperdicio_total]
colores = ['#e74c3c', '#2ecc71', '#f39c12']

barras = ax.bar(categorias, valores, color=colores, alpha=0.8, edgecolor='black', linewidth=2)

for i, (barra, valor) in enumerate(zip(barras, valores)):
    height = barra.get_height()
    ax.text(barra.get_x() + barra.get_width()/2., height,
            f'{valor:.1f} kWh',
            ha='center', va='bottom', fontsize=20, fontweight='bold')

ax.set_ylabel('Energia (kWh)', fontsize=18, fontweight='bold')
ax.set_title('COMPARACION ENERGETICA: Donde esta el problema?', 
             fontsize=24, fontweight='bold', pad=30)
ax.tick_params(axis='both', labelsize=16)
ax.grid(axis='y', alpha=0.3, linestyle='--')

ax.axhline(y=desperdicio_total, color='#f39c12', linestyle='--', linewidth=3, alpha=0.5)

plt.tight_layout()
plt.savefig('presentacion_barras.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Guardado: presentacion_barras.png")
plt.close()

# GRAFICO 2: RESUMEN VISUAL
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor('white')

gs = fig.add_gridspec(2, 3, hspace=0.4, wspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])
ax1.text(0.5, 0.55, f'{porcentaje_desperdicio:.1f}%', 
         ha='center', va='center', fontsize=55, fontweight='bold', color='#e74c3c')
ax1.text(0.5, 0.25, 'DESPERDICIO', 
         ha='center', va='center', fontsize=22, fontweight='bold', color='#2c3e50')
ax1.text(0.5, 0.1, f'{desperdicio_total:.1f} kWh perdidos', 
         ha='center', va='center', fontsize=16, color='#7f8c8d')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')
ax1.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, 
              fill=False, edgecolor='#e74c3c', linewidth=4))

ax2 = fig.add_subplot(gs[0, 1])
ax2.text(0.5, 0.55, f'{ahorro_eur:.2f} €', 
         ha='center', va='center', fontsize=50, fontweight='bold', color='#27ae60')
ax2.text(0.5, 0.25, 'AHORRO POTENCIAL', 
         ha='center', va='center', fontsize=18, fontweight='bold', color='#2c3e50')
ax2.text(0.5, 0.1, 'en este periodo', 
         ha='center', va='center', fontsize=16, color='#7f8c8d')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')
ax2.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, 
              fill=False, edgecolor='#27ae60', linewidth=4))

ax3 = fig.add_subplot(gs[0, 2])
ax3.text(0.5, 0.55, f'{autosuficiencia:.1f}%', 
         ha='center', va='center', fontsize=55, fontweight='bold', color='#3498db')
ax3.text(0.5, 0.25, 'AUTOSUFICIENCIA', 
         ha='center', va='center', fontsize=18, fontweight='bold', color='#2c3e50')
ax3.text(0.5, 0.1, 'energia renovable', 
         ha='center', va='center', fontsize=16, color='#7f8c8d')
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')
ax3.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, 
              fill=False, edgecolor='#3498db', linewidth=4))

ax4 = fig.add_subplot(gs[1, :])
categorias_mini = ['Consumo', 'Generacion', 'Desperdicio']
valores_mini = [consumo_total, generacion_total, desperdicio_total]
colores_mini = ['#e74c3c', '#2ecc71', '#f39c12']

barras_mini = ax4.barh(categorias_mini, valores_mini, color=colores_mini, alpha=0.8, edgecolor='black', linewidth=2)

for i, (barra, valor) in enumerate(zip(barras_mini, valores_mini)):
    width = barra.get_width()
    ax4.text(width, barra.get_y() + barra.get_height()/2.,
            f'  {valor:.1f} kWh',
            ha='left', va='center', fontsize=18, fontweight='bold')

ax4.set_xlabel('Energia (kWh)', fontsize=16, fontweight='bold')
ax4.tick_params(axis='both', labelsize=14)
ax4.grid(axis='x', alpha=0.3, linestyle='--')
ax4.set_title('Distribucion Energetica', fontsize=20, fontweight='bold', pad=15)

plt.suptitle('RESUMEN EJECUTIVO - Analisis Energetico', 
             fontsize=28, fontweight='bold', y=0.98)

plt.savefig('presentacion_resumen.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Guardado: presentacion_resumen.png")
plt.close()

print("\n" + "=" * 60)
print("GRAFICOS LISTOS PARA PRESENTACION")
print("=" * 60)
print("\nArchivos creados:")
print("  - presentacion_barras.png")
print("  - presentacion_resumen.png")
print("\nUsa estos PNG en tu presentacion")
print("=" * 60)