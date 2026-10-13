import random
from locust import HttpUser, task, between

# Pinguinos reales del dataset (uno por especie).
# Se rotan para que no siempre se pida la misma prediccion.
MUESTRAS = [
    {"culmen_length_mm": 39.1, "culmen_depth_mm": 18.7, "flipper_length_mm": 181,
     "body_mass_g": 3750, "island": "Torgersen", "sex": "MALE"},      # Adelie
    {"culmen_length_mm": 46.5, "culmen_depth_mm": 17.9, "flipper_length_mm": 192,
     "body_mass_g": 3500, "island": "Dream", "sex": "FEMALE"},        # Chinstrap
    {"culmen_length_mm": 49.1, "culmen_depth_mm": 14.8, "flipper_length_mm": 220,
     "body_mass_g": 5150, "island": "Biscoe", "sex": "FEMALE"},       # Gentoo
]


class UsuarioInferencia(HttpUser):
    # Igual al ejemplo del profe. NO se cambia entre 1 y 3 replicas.
    wait_time = between(1, 2.5)

    @task
    def predecir(self):
        payload = random.choice(MUESTRAS)
        with self.client.post("/predict", json=payload, name="/predict",
                              catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"HTTP {resp.status_code}: {resp.text[:200]}")
                return
            try:
                body = resp.json()
            except ValueError:
                resp.failure("Respuesta sin JSON valido")
                return
            if "especie_predicha" not in body:
                resp.failure("Falta el campo 'especie_predicha'")
                return
            resp.success()
