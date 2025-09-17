# -*- coding: utf-8 -*-
"""
Análise Completa do Dataset Titanic (dados_titanic.csv)
Autor: Gerado por ChatGPT (para Evandro de Castro Melo)
Descrição:
    Script detalhado e comentado, cobrindo:
    1) Carregamento e inspeção dos dados
    2) Tratamento de dados faltantes
    3) Análise Exploratória (estatísticas e gráficos)
    4) Engenharia de atributos
    5) Modelagem preditiva (Regressão Logística) para prever sobrevivência
    6) Geração de arquivos de saída: figuras PNG, CSV limpo e um resumo em TXT

Uso:
    python analise_dados_titanic.py
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    roc_auc_score,
    roc_curve,
    confusion_matrix
)


# ---------------------------
# Funções auxiliares
# ---------------------------

def ensure_dir(path: str):
    """Cria diretório se não existir"""
    if not os.path.exists(path):
        os.makedirs(path)


def carregar_dados(caminho_csv: str) -> pd.DataFrame:
    """
    Carrega o dataset Titanic
    - caminho_csv: nome do arquivo (na mesma pasta do script)
    """
    df = pd.read_csv(caminho_csv, sep=",", encoding="utf-8")
    # padroniza nomes de colunas
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def faltantes(df: pd.DataFrame) -> pd.DataFrame:
    total = df.isna().sum()
    perc = (total / len(df) * 100).round(2)
    out = pd.DataFrame({"faltantes": total, "percentual": perc}).sort_values("percentual", ascending=False)
    return out


def estatisticas_numericas(df: pd.DataFrame) -> pd.DataFrame:
    num_cols = df.select_dtypes(include=[np.number]).columns
    return df[num_cols].describe(percentiles=[.05, .25, .5, .75, .95]).T


def estatisticas_categoricas(df: pd.DataFrame, top_n=10) -> dict:
    cat_cols = df.select_dtypes(exclude=[np.number]).columns
    info = {}
    for c in cat_cols:
        info[c] = df[c].value_counts(dropna=False).head(top_n)
    return info


def tratar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estratégias simples:
    - sex, embarked → moda
    - age, fare → mediana
    - flags para presença de infos textuais (cabin, boat, home_dest etc.)
    - extração de títulos do nome
    - family_size e is_alone
    """
    dfc = df.copy()

    if "home.dest" in dfc.columns and "home_dest" not in dfc.columns:
        dfc = dfc.rename(columns={"home.dest": "home_dest"})

    for col in ["sex", "embarked"]:
        if col in dfc.columns:
            moda = dfc[col].mode(dropna=True)
            if len(moda) > 0:
                dfc[col] = dfc[col].fillna(moda.iloc[0])

    for col in ["age", "fare"]:
        if col in dfc.columns:
            med = dfc[col].median()
            dfc[col] = dfc[col].fillna(med)

    for col in ["cabin", "boat", "home_dest", "ticket", "name"]:
        if col in dfc.columns:
            dfc[f"has_{col}"] = (~dfc[col].isna()).astype(int)

    if "name" in dfc.columns:
        dfc["title"] = (
            dfc["name"]
            .astype(str)
            .str.extract(r",\s*([^\.]+)\.", expand=False)
            .str.strip()
        )
        title_counts = dfc["title"].value_counts(dropna=False)
        raros = set(title_counts[title_counts < 10].index.tolist())
        dfc["title"] = dfc["title"].apply(lambda x: "Rare" if x in raros else x)

    if set(["sibsp", "parch"]).issubset(dfc.columns):
        dfc["family_size"] = dfc["sibsp"].fillna(0) + dfc["parch"].fillna(0) + 1
        dfc["is_alone"] = (dfc["family_size"] == 1).astype(int)

    return dfc


def criar_graficos_basicos(df: pd.DataFrame, figdir: str):
    ensure_dir(figdir)

    if "age" in df.columns:
        plt.figure()
        df["age"].dropna().plot(kind="hist", bins=30, title="Distribuição de Idade")
        plt.xlabel("Idade")
        plt.tight_layout()
        plt.savefig(os.path.join(figdir, "hist_idade.png"))
        plt.close()

    if "fare" in df.columns:
        plt.figure()
        df["fare"].dropna().plot(kind="hist", bins=30, title="Distribuição de Tarifa (Fare)")
        plt.xlabel("Tarifa")
        plt.tight_layout()
        plt.savefig(os.path.join(figdir, "hist_fare.png"))
        plt.close()

    if set(["survived", "sex"]).issubset(df.columns):
        taxa = df.groupby("sex")["survived"].mean()
        plt.figure()
        taxa.plot(kind="bar", title="Taxa de sobrevivência por sexo")
        plt.ylabel("Taxa de sobrevivência")
        plt.tight_layout()
        plt.savefig(os.path.join(figdir, "sobrevivencia_por_sexo.png"))
        plt.close()

    if set(["survived", "pclass"]).issubset(df.columns):
        taxa = df.groupby("pclass")["survived"].mean()
        plt.figure()
        taxa.plot(kind="bar", title="Taxa de sobrevivência por classe")
        plt.ylabel("Taxa de sobrevivência")
        plt.tight_layout()
        plt.savefig(os.path.join(figdir, "sobrevivencia_por_classe.png"))
        plt.close()


def preparar_modelagem(df: pd.DataFrame):
    if "survived" not in df.columns:
        return None, None

    y = df["survived"].astype(int)

    possiveis = [
        "pclass", "sex", "age", "sibsp", "parch", "fare", "embarked",
        "family_size", "is_alone", "title",
        "has_cabin", "has_boat", "has_home_dest", "has_ticket", "has_name"
    ]
    cols = [c for c in possiveis if c in df.columns]

    X = df[cols].copy()

    cat_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()
    X = pd.get_dummies(X, columns=cat_cols, drop_first=True)

    num_cols = X.select_dtypes(include=[np.number]).columns
    scaler = StandardScaler()
    X[num_cols] = scaler.fit_transform(X[num_cols])

    return X, y


def modelar_e_avaliar(X, y, figdir: str):
    ensure_dir(figdir)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    clf = LogisticRegression(max_iter=200)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    # curva ROC
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    plt.figure()
    plt.plot(fpr, tpr, label=f"ROC AUC = {auc:.3f}")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.xlabel("Falso Positivo")
    plt.ylabel("Verdadeiro Positivo")
    plt.title("Curva ROC")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(figdir, "roc_curve.png"))
    plt.close()

    cm = confusion_matrix(y_test, y_pred)
    plt.figure()
    plt.imshow(cm, interpolation="nearest")
    plt.title("Matriz de Confusão")
    plt.colorbar()
    plt.xticks([0, 1], ["Não Sobreviveu", "Sobreviveu"])
    plt.yticks([0, 1], ["Não Sobreviveu", "Sobreviveu"])
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], "d"),
                     ha="center", va="center")
    plt.tight_layout()
    plt.savefig(os.path.join(figdir, "confusion_matrix.png"))
    plt.close()

    clf_report = classification_report(y_test, y_pred, digits=3)

    return acc, auc, clf_report, clf


# ---------------------------
# Programa principal
# ---------------------------

def main():
    arquivo_csv = "dados_titanic.csv"          # dataset na mesma pasta
    figdir = "figures"
    relatorio = "resumo_analise.txt"
    csv_limpo = "dados_titanic_clean.csv"

    # 1) Carregar
    df = carregar_dados(arquivo_csv)

    # 2) Análises básicas
    falt_txt = faltantes(df)
    est_num = estatisticas_numericas(df)
    est_cat = estatisticas_categoricas(df)

    # 3) Tratar
    df_clean = tratar_dados(df)

    # 4) Gráficos
    criar_graficos_basicos(df_clean, figdir)

    # 5) Modelagem
    X, y = preparar_modelagem(df_clean)

    with open(relatorio, "w", encoding="utf-8") as f:
        f.write("==== DADOS FALTANTES ====\n")
        f.write(falt_txt.to_string() + "\n\n")

        f.write("==== ESTATÍSTICAS NUMÉRICAS ====\n")
        f.write(est_num.to_string() + "\n\n")

        f.write("==== ESTATÍSTICAS CATEGÓRICAS (top 10 cada) ====\n")
        for col, vc in est_cat.items():
            f.write(f"\nColuna: {col}\n{vc.to_string()}\n")

        if X is not None and y is not None:
            acc, auc, clf_report, clf = modelar_e_avaliar(X, y, figdir)
            f.write("\n==== MODELAGEM ====\n")
            f.write(f"Acurácia: {acc:.4f}\n")
            f.write(f"ROC AUC: {auc:.4f}\n")
            f.write(clf_report + "\n")

            coefs = pd.Series(clf.coef_[0], index=X.columns).sort_values(ascending=False)
            coefs.to_csv("coeficientes_logistica.csv", encoding="utf-8")
            f.write("\nCoeficientes salvos em coeficientes_logistica.csv\n")

    df_clean.to_csv(csv_limpo, index=False, encoding="utf-8")
    print("Análise concluída! Arquivos gerados:")
    print(f"- {relatorio}")
    print(f"- {csv_limpo}")
    print(f"- figuras em {figdir}/")
    print("- coeficientes_logistica.csv (se modelagem rodou)")


if __name__ == "__main__":
    main()
