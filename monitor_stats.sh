#!/usr/bin/env bash
# Uso: ./monitor_stats.sh <nombre_prueba>   (detener con Ctrl+C)
out="resultados/${1:?Falta el nombre de la prueba}_docker.csv"
echo "timestamp,contenedor,cpu_pct,mem_uso,mem_limite,mem_pct" > "$out"
echo "Grabando en $out ... (Ctrl+C para detener)"
while true; do
  ts=$(date +%s)
  docker stats --no-stream --format '{{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}}' \
    | sed -e "s/^/${ts},/" -e 's| / |,|' -e 's/%//g' >> "$out"
done
