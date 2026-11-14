import json
import os
import glob
import math
import sys

def main():
    input_dir = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)

    in_files = sorted(glob.glob(os.path.join(input_dir, "*.in")))
    z_vals = [-1.644854, -0.67449, 0.0, 0.67449, 1.644854]

    for path in in_files:
        with open(path, "r") as f:
            case = json.load(f)

        case_id = case.get("case", os.path.splitext(os.path.basename(path))[0])
        horizon = max(1, int(case.get("horizon_minutes", 240)))
        markets = case.get("markets", [])

        forecasts = []
        for m in markets:
            m_id = m.get("id") or "unknown"
            raw_prices = m.get("prices", [])
            prices = [p for p in raw_prices if isinstance(p, (int, float)) and math.isfinite(p)]

            if not prices:
                prices = [0.5]

            x = prices[-1]

            sub_prices = prices[-360:] if len(prices) >= 360 else prices
            if len(sub_prices) < 2:
                sigma = 0.0002
            else:
                diffs = [sub_prices[i] - sub_prices[i-1] for i in range(1, len(sub_prices))]
                if not diffs:
                    sigma = 0.0002
                else:
                    mean_d = sum(diffs) / len(diffs)
                    var = sum((d - mean_d) ** 2 for d in diffs) / len(diffs)
                    sigma = 0.35 * math.sqrt(var)
                    sigma = max(0.0002, min(0.004, sigma))

            q_rows = []
            for h in range(1, horizon + 1):
                row = []
                sq_h = math.sqrt(h)
                for z in z_vals:
                    val = x + z * sigma * sq_h
                    val = max(0.0, min(1.0, val))
                    row.append(val)
                for j in range(1, 5):
                    if row[j] < row[j-1]:
                        row[j] = row[j-1]
                row = [round(v, 6) for v in row]
                for j in range(1, 5):
                    if row[j] < row[j-1]:
                        row[j] = row[j-1]
                q_rows.append(row)

            forecasts.append({
                "id": m_id,
                "q": q_rows
            })

        out_path = os.path.join(output_dir, f"{case_id}.out")
        with open(out_path, "w") as f:
            json.dump({"forecasts": forecasts}, f)

if __name__ == "__main__":
    main()
