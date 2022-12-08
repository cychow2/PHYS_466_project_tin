
for T in range(1, 301):
    content = f"lmp -in T={T}/in.MD -screen T={T}/out.MD &\n"
    with open(f"T={T}/run", "w") as f:
        f.write(content)