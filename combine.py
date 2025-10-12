import os
import csv
import glob


def find_columns(headers):
    lower = [h.lower() for h in headers]
    symbol_idx = None
    precision_idx = None
    for i, h in enumerate(lower):
        if h == "symbol" or h == "pair" or h == "coin":
            symbol_idx = i
        if h == "precision" or h == "price_precision" or h == "qty_precision" or h == "quantity_precision":
            if precision_idx is None:
                precision_idx = i
    if symbol_idx is None:
        for i, h in enumerate(lower):
            if "symbol" in h or "pair" in h or "coin" in h or "ticker" in h:
                symbol_idx = i
                break
    if precision_idx is None:
        for i, h in enumerate(lower):
            if "precision" in h:
                precision_idx = i
                break
    return symbol_idx, precision_idx


def read_csv_precisions(path):
    entries = {}
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        sample = f.read(2048)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
        except Exception:
            dialect = csv.excel
        reader = csv.reader(f, dialect)
        first_row = next(reader, None)
        if first_row is None:
            return entries
        # Try to detect headers first
        sym_i_opt, prec_i_opt = find_columns(first_row)
        if sym_i_opt is not None and prec_i_opt is not None:
            # Header present, continue with remaining rows
            sym_i, prec_i = sym_i_opt, prec_i_opt
            row_iter = reader
        else:
            # Assume first two columns are symbol and precision, and first_row is data
            sym_i, prec_i = 0, 1
            row_iter = [first_row]
            row_iter.extend(reader)
        for row in row_iter:
            if not row:
                continue
            if len(row) <= max(sym_i, prec_i):
                continue
            symbol = str(row[sym_i]).strip().upper()
            prec = str(row[prec_i]).strip()
            if symbol:
                entries[symbol] = prec
    return entries


def main():
    cwd = os.getcwd()
    csv_paths = [p for p in glob.glob(os.path.join(cwd, "*.csv"))]
    if not csv_paths:
        print("No CSV files found in working directory.")
        return
    output_name = "combined_precisions.csv"
    output_path = os.path.join(cwd, output_name)
    csv_paths = [p for p in csv_paths if os.path.basename(p).lower() != output_name.lower()]
    datasets = []
    for p in csv_paths:
        data = read_csv_precisions(p)
        if data:
            datasets.append((os.path.splitext(os.path.basename(p))[0], data))
        else:
            print(f"Skipped {os.path.basename(p)}: required columns not found or file empty")
    if not datasets:
        print("No valid CSV files with symbol and precision columns.")
        return
    symbols = set()
    for _, data in datasets:
        symbols.update(data.keys())
    symbols = sorted(symbols)
    headers = ["symbol"] + [name for name, _ in datasets]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for sym in symbols:
            row = [sym]
            for _, data in datasets:
                row.append(data.get(sym, ""))
            writer.writerow(row)
    print(f"Wrote {len(symbols)} symbols from {len(datasets)} files to {output_name}")


if __name__ == "__main__":
    main()

