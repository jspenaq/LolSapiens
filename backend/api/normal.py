import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Crea el dataset
dataset = [
    ["PTA", 0.0, 8],
    ["Lethal", 43.8, 16],
    ["Fleet", 60.0, 10],
    ["Conqueror", 31.3, 16],
    ["Electrocute", 53.2, 5229],
    ["Predator", 52.2, 295],
    ["Harvest", 53.3, 287],
    ["HOB", 46.3, 41],
    ["Aery", 56.3, 21236],
    ["Comet", 53.4, 1591],
    ["Phase", 43.2, 37],
    ["Grasp", 50.0, 8],
    ["Aftershock", 62.8, 86],
    ["Guardian", 58.2, 220],
    ["Glacial", 59.5, 1962],
    ["Spellbook", 70, 10],
    ["First", 52.2, 293],
    # ["PTA", 0.0, 7],
    # ["Lethal", 43.8, 16],
    # ["Fleet", 60.0, 10],
    # ["Conqueror", 31.3, 16],
    # ["Electrocute", 53.2, 5229],
    # ["Predator", 52.2, 295],
    # ["Harvest", 53.3, 287],
    # ["HOB", 46.3, 41],
    # ["Aery", 56.3, 21236],
    # ["Comet", 53.4, 1591],
    # ["Phase", 43.2, 37],
    # ["Grasp", 50.0, 8],
    # ["Aftershock", 62.8, 86],
    # ["Guardian", 58.2, 220],
    # ["Glacial", 59.5, 1962],
    # ["Spellbook", 70, 10],
    # ["First", 52.2, 293],
    # ["Ril", 75, 4],
    # ["Mej", 50, 2],
    # ["Overgrowth", 47.6, 21],
    # ["Revitalize", 62.5, 8],
    # ["Unflinching", 100, 2],
    # ["WQE", 83.3, 12],
    # ["QEW", 57.7, 168],
]

# Crea el dataframe
df = pd.DataFrame(dataset, columns=["Runa", "Valor_Victoria", "Numero_Veces_Usada"])
standard = df["Numero_Veces_Usada"].std(ddof=0)  # Normalize by N instead of N-1
mean = df["Numero_Veces_Usada"].mean()
cv = standard / mean
maximum = df["Numero_Veces_Usada"].max()
p20 = df["Numero_Veces_Usada"].quantile(0.20)
q1 = df["Numero_Veces_Usada"].quantile(0.25)
q2 = df["Numero_Veces_Usada"].quantile(0.50)
p60 = df["Numero_Veces_Usada"].quantile(0.60)
q3 = df["Numero_Veces_Usada"].quantile(0.75)
minimum = df["Numero_Veces_Usada"].min()
maximum = df["Numero_Veces_Usada"].max()
iqr = q3 - q1

print(f"{standard=}")
print(f"{mean=}")
print(f"{cv=}")
print(f"{maximum=}")
print(f"{p20=}")
print(f"{q1=}")
print(f"{q2=}")
print(f"{q3=}")
print(f"{iqr=}")

df = df[df["Numero_Veces_Usada"] >= q1]

# Crea un objeto MinMaxScaler
scaler = MinMaxScaler()

# Aplica la normalización a la columna 'Numero_Veces_Usada'
df["Numero_Veces_Usada_Normalizada"] = scaler.fit_transform(df[["Numero_Veces_Usada"]])


def f(w1: float, w2: float):
    # Definir los pesos
    peso1 = w1
    peso2 = w2

    # Calcular la puntuación ponderada
    df["Puntuacion_ponderada"] = (
        df["Valor_Victoria"] * peso1 + df["Numero_Veces_Usada_Normalizada"] * peso2
    )

    # Caalcular la media ponderada
    # df["Valor_Victoria_Ponderada"] = (
    #     df["Valor_Victoria"] * df["Numero_Veces_Usada"] / df["Numero_Veces_Usada"].sum()
    # )
    # media_ponderada = df["valor_victoria_ponderada"].sum()

    # Imprime los resultados
    print(df.sort_values(by="Valor_Victoria", ascending=False))
    print()


# f(0.7, 0.3)
f(0.6, 0.4)
f(0.5, 0.5)
# f(0.4, 0.6)
# print(df.sort_values(by="Valor_Victoria", ascending=False))
print(df)
