import pandas as pd
import matplotlib.pyplot as plt

"""
plot_results.py
CSC 746 - High Performance Computing
Assignment: Matrix Multiplication Performance Study

This script reads performance results from all_results.csv,
computes MFLOP/s, and generates four plots:
1. Basic vs BLAS
2. Blocked vs BLAS
3. All Implementations
4. Basic vs Blocked

Author: Guiran Liu
Date: september 21, 2025

Notes on authorship:
- The overall design and plotting logic were developed by me.
- I used AI assistance to help refine the code structure and
  ensure clarity and correctness in the implementation.
"""

rows = []
with open("all_results.csv") as f:
    for line in f:
        line = line.strip()
        if not line.startswith("CSV"):
            continue
        parts = line.split(",")
        if len(parts) < 5:
            continue
        N = int(parts[-3])
        B = int(parts[-2])
        t = float(parts[-1])
        impl_raw = ",".join(parts[1:-3]).strip().lower()

    
        if "blocked" in impl_raw:
            impl = "blocked"
        elif "reference" in impl_raw or "blas" in impl_raw:
            impl = "blas"
        elif "basic" in impl_raw:
            impl = "basic"
        else:
            impl = impl_raw

        rows.append({"impl": impl, "N": N, "B": B, "time": t})

df = pd.DataFrame(rows)
df["mflops"] = 2 * (df["N"]**3) / (df["time"] * 1e6)

# ---- 1: Basic vs BLAS ----
plt.figure()
for impl in ["basic","blas"]:
    sub = df[df["impl"]==impl].sort_values("N")
    plt.plot(sub["N"], sub["mflops"], marker="o", label=impl)
plt.xlabel("Problem size N"); plt.ylabel("MFLOP/s")
plt.title("Basic vs BLAS"); plt.legend(); plt.grid(True)
plt.savefig("basic_vs_blas.png", dpi=150)

# ---- 2: Blocked vs BLAS ----
plt.figure()
sub = df[df["impl"]=="blas"].sort_values("N")
plt.plot(sub["N"], sub["mflops"], marker="o", label="blas")
for b in [2,16,32,64]:
    sub = df[(df["impl"]=="blocked") & (df["B"]==b)].sort_values("N")
    plt.plot(sub["N"], sub["mflops"], marker="o", label=f"blocked B={b}")
plt.xlabel("Problem size N"); plt.ylabel("MFLOP/s")
plt.title("Blocked vs BLAS"); plt.legend(); plt.grid(True)
plt.savefig("blocked_vs_blas.png", dpi=150)

# ---- 3: All implementations ----
plt.figure()
for impl in ["blas","basic"]:
    sub = df[df["impl"]==impl].sort_values("N")
    plt.plot(sub["N"], sub["mflops"], marker="o", label=impl)
for b in [2,16,32,64]:
    sub = df[(df["impl"]=="blocked") & (df["B"]==b)].sort_values("N")
    plt.plot(sub["N"], sub["mflops"], marker="o", label=f"blocked B={b}")
plt.xlabel("Problem size N"); plt.ylabel("MFLOP/s")
plt.title("All Implementations"); plt.legend(); plt.grid(True)
plt.savefig("all_impls.png", dpi=150)

# ---- 4: Basic vs Blocked ----
plt.figure()
sub = df[df["impl"]=="basic"].sort_values("N")
plt.plot(sub["N"], sub["mflops"], marker="o", label="basic")
for b in [2,16,32,64]:
    sub = df[(df["impl"]=="blocked") & (df["B"]==b)].sort_values("N")
    plt.plot(sub["N"], sub["mflops"], marker="o", label=f"blocked B={b}")
plt.xlabel("Problem size N"); plt.ylabel("MFLOP/s")
plt.title("Basic vs Blocked"); plt.legend(); plt.grid(True)
plt.savefig("basic_vs_blocked.png", dpi=150)

plt.show()