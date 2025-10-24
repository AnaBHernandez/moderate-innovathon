from pathlib import Path
import openpyxl

BASE = Path('/workspace/datos_originales')


def preview_xlsx(path: Path, nrows: int = 10):
    print(f"\n=== Preview: {path.name} ===")
    try:
        wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    except Exception as e:
        print(f"Error abriendo {path}: {e}")
        return
    try:
        for ws in wb.worksheets:
            print(f"-- Hoja: {ws.title} --")
            rows = ws.iter_rows(values_only=True)
            shown = 0
            for r in rows:
                if r is None:
                    continue
                if all(v is None for v in r):
                    continue
                print(r)
                shown += 1
                if shown >= nrows:
                    break
    finally:
        wb.close()


def main():
    # HDD
    hdd_dir = BASE / 'hdd-anual'
    for f in sorted(hdd_dir.glob('*.xlsx'))[:2]:
        preview_xlsx(f)

    # Producción energética
    prod_dir = BASE / 'produccion-energetica'
    for f in sorted(prod_dir.glob('*.xlsx'))[:3]:
        preview_xlsx(f)

    # Consumo biomasa
    consumo = BASE / 'consumo-biomasa.xlsx'
    if consumo.exists():
        preview_xlsx(consumo)


if __name__ == '__main__':
    main()
