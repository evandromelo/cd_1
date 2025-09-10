# Análise Completa de Experimento de Secagem de Folhas de Planta Medicinal
# Disciplina: ENG6001 - Introdução à Ciência de Dados com Python Aplicada à Engenharia Agrícola
# Aluno: Pós-graduação em Engenharia Agrícola

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuração para gráficos em português
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
sns.set_style("whitegrid")

# 1. GERAÇÃO DE DADOS SIMULADOS DE SECAGEM
print("="*60)
print("ANÁLISE DE EXPERIMENTO DE SECAGEM DE FOLHAS")
print("Planta Medicinal: Melissa officinalis (Erva-cidreira)")
print("="*60)

# Parâmetros do experimento simulado
np.random.seed(42)  # Para reprodutibilidade
temperaturas = [40, 50, 60, 70]  # °C
n_repeticoes = 5
tempo_max = 300  # minutos

dados_simulados = []

for temp in temperaturas:
    for rep in range(1, n_repeticoes + 1):
        # Parâmetros do modelo de Henderson e Pabis modificado
        # MR = a * exp(-k * t) + c
        if temp == 40:
            a, k, c = 0.95 + np.random.normal(0, 0.02), 0.008 + np.random.normal(0, 0.001), 0.05
        elif temp == 50:
            a, k, c = 0.96 + np.random.normal(0, 0.02), 0.012 + np.random.normal(0, 0.001), 0.04
        elif temp == 60:
            a, k, c = 0.97 + np.random.normal(0, 0.02), 0.018 + np.random.normal(0, 0.002), 0.03
        else:  # 70°C
            a, k, c = 0.98 + np.random.normal(0, 0.02), 0.025 + np.random.normal(0, 0.002), 0.02
        
        # Tempos de amostragem (minutos)
        tempos = np.array([0, 15, 30, 45, 60, 90, 120, 150, 180, 210, 240, 270, 300])
        
        for t in tempos:
            # Razão de umidade (MR) com ruído
            mr = a * np.exp(-k * t) + c + np.random.normal(0, 0.01)
            mr = max(0.02, mr)  # Limitar valor mínimo
            
            # Umidade inicial típica: 80-85% (base úmida)
            umidade_inicial = 82 + np.random.normal(0, 1)
            # Umidade de equilíbrio típica: 3-8% (base úmida)
            umidade_equilibrio = 5 + np.random.normal(0, 0.5)
            
            # Umidade atual
            umidade_atual = (mr * (umidade_inicial - umidade_equilibrio)) + umidade_equilibrio
            
            # Massa atual (considerando massa seca constante de 10g)
            massa_seca = 10  # g
            massa_atual = massa_seca * (1 + umidade_atual/100) / (1 - umidade_atual/100)
            
            dados_simulados.append({
                'temperatura': temp,
                'repeticao': rep,
                'tempo_min': t,
                'umidade_percentual': round(umidade_atual, 2),
                'massa_g': round(massa_atual, 3),
                'razao_umidade': round(mr, 4)
            })

# Criação do DataFrame
df = pd.DataFrame(dados_simulados)

# Salvando os dados simulados em CSV
df.to_csv('dados_secagem_simulados.csv', index=False)
print("✓ Dados simulados gerados e salvos em 'dados_secagem_simulados.csv'")

# 2. IMPORTAÇÃO DOS DADOS
print("\n" + "="*50)
print("2. IMPORTAÇÃO DOS DADOS")
print("="*50)

# Carregando os dados do CSV
df_raw = pd.read_csv('dados_secagem_simulados.csv')
print(f"✓ Dados importados: {df_raw.shape[0]} linhas, {df_raw.shape[1]} colunas")
print(f"✓ Temperaturas testadas: {sorted(df_raw['temperatura'].unique())}°C")
print(f"✓ Número de repetições: {df_raw['repeticao'].nunique()}")
print(f"✓ Tempo máximo: {df_raw['tempo_min'].max()} minutos")

# 3. LIMPEZA DOS DADOS
print("\n" + "="*50)
print("3. LIMPEZA E PREPARAÇÃO DOS DADOS")
print("="*50)

# Verificação de valores ausentes
print("Valores ausentes por coluna:")
print(df_raw.isnull().sum())

# Verificação de outliers usando Z-score
def detectar_outliers(df, coluna, threshold=3):
    z_scores = np.abs(stats.zscore(df[coluna]))
    return df[z_scores > threshold]

outliers_umidade = detectar_outliers(df_raw, 'umidade_percentual')
outliers_massa = detectar_outliers(df_raw, 'massa_g')

print(f"\n✓ Outliers detectados em umidade: {len(outliers_umidade)}")
print(f"✓ Outliers detectados em massa: {len(outliers_massa)}")

# Limpeza: remover valores inconsistentes
df_clean = df_raw.copy()

# Filtrar valores fisicamente impossíveis
df_clean = df_clean[df_clean['umidade_percentual'] >= 0]
df_clean = df_clean[df_clean['umidade_percentual'] <= 100]
df_clean = df_clean[df_clean['massa_g'] > 0]
df_clean = df_clean[df_clean['razao_umidade'] >= 0]

print(f"✓ Dados após limpeza: {df_clean.shape[0]} linhas")

# 4. ANÁLISE EXPLORATÓRIA DOS DADOS
print("\n" + "="*50)
print("4. ANÁLISE EXPLORATÓRIA DOS DADOS")
print("="*50)

# Estatísticas descritivas
print("Estatísticas descritivas:")
print(df_clean.describe())

# Análise por temperatura
print("\nResumo por temperatura:")
resumo_temp = df_clean.groupby('temperatura').agg({
    'umidade_percentual': ['mean', 'std', 'min', 'max'],
    'massa_g': ['mean', 'std'],
    'razao_umidade': ['mean', 'std']
}).round(3)

for temp in sorted(df_clean['temperatura'].unique()):
    dados_temp = df_clean[df_clean['temperatura'] == temp]
    print(f"{temp}°C: Umidade final média = {dados_temp[dados_temp['tempo_min'] == dados_temp['tempo_min'].max()]['umidade_percentual'].mean():.2f}%")

# 5. VISUALIZAÇÃO DOS DADOS
print("\n" + "="*50)
print("5. VISUALIZAÇÃO DOS DADOS")
print("="*50)

# Configuração da figura
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Análise de Secagem de Folhas de Planta Medicinal\n(Melissa officinalis)', 
             fontsize=16, fontweight='bold')

# Gráfico 1: Curvas de secagem (Razão de Umidade vs Tempo)
ax1 = axes[0, 0]
cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
for i, temp in enumerate(sorted(df_clean['temperatura'].unique())):
    dados_temp = df_clean[df_clean['temperatura'] == temp]
    # Calcular médias por tempo
    medias = dados_temp.groupby('tempo_min')['razao_umidade'].mean()
    stds = dados_temp.groupby('tempo_min')['razao_umidade'].std()
    
    ax1.errorbar(medias.index, medias.values, yerr=stds.values, 
                label=f'{temp}°C', marker='o', capsize=5, color=cores[i])

ax1.set_xlabel('Tempo (minutos)')
ax1.set_ylabel('Razão de Umidade (MR)')
ax1.set_title('Curvas de Secagem')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Gráfico 2: Perda de massa
ax2 = axes[0, 1]
for i, temp in enumerate(sorted(df_clean['temperatura'].unique())):
    dados_temp = df_clean[df_clean['temperatura'] == temp]
    medias = dados_temp.groupby('tempo_min')['massa_g'].mean()
    stds = dados_temp.groupby('tempo_min')['massa_g'].std()
    
    ax2.errorbar(medias.index, medias.values, yerr=stds.values, 
                label=f'{temp}°C', marker='s', capsize=5, color=cores[i])

ax2.set_xlabel('Tempo (minutos)')
ax2.set_ylabel('Massa (g)')
ax2.set_title('Perda de Massa Durante Secagem')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Gráfico 3: Taxa de secagem
ax3 = axes[1, 0]
for i, temp in enumerate(sorted(df_clean['temperatura'].unique())):
    dados_temp = df_clean[df_clean['temperatura'] == temp]
    medias = dados_temp.groupby('tempo_min')['umidade_percentual'].mean()
    
    # Calcular taxa de secagem (derivada numérica)
    tempos = medias.index.values
    umidades = medias.values
    taxa_secagem = -np.gradient(umidades, tempos)  # Negativo porque umidade diminui
    
    ax3.plot(tempos[1:-1], taxa_secagem[1:-1], 
            label=f'{temp}°C', marker='^', color=cores[i])

ax3.set_xlabel('Tempo (minutos)')
ax3.set_ylabel('Taxa de Secagem (%/min)')
ax3.set_title('Taxa de Secagem')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Gráfico 4: Boxplot da umidade final por temperatura
ax4 = axes[1, 1]
dados_final = df_clean[df_clean['tempo_min'] == df_clean['tempo_min'].max()]
sns.boxplot(data=dados_final, x='temperatura', y='umidade_percentual', ax=ax4)
ax4.set_xlabel('Temperatura (°C)')
ax4.set_ylabel('Umidade Final (%)')
ax4.set_title('Distribuição da Umidade Final')

plt.tight_layout()
plt.show()

# 6. AJUSTE DE MODELOS COM SCIPY
print("\n" + "="*50)
print("6. AJUSTE DE MODELOS MATEMÁTICOS")
print("="*50)

# Definição dos modelos matemáticos
def henderson_pabis(t, a, k):
    """Modelo de Henderson e Pabis: MR = a * exp(-k * t)"""
    return a * np.exp(-k * t)

def page(t, a, k, n):
    """Modelo de Page: MR = a * exp(-k * t^n)"""
    return a * np.exp(-k * np.power(t, n))

def newton(t, a, k, b):
    """Modelo de Newton: MR = a * exp(-k * t) + b"""
    return a * np.exp(-k * t) + b

# Dicionário para armazenar resultados
resultados_modelos = {}

# Ajuste para cada temperatura
for temp in sorted(df_clean['temperatura'].unique()):
    print(f"\nAjuste para {temp}°C:")
    print("-" * 30)
    
    # Dados para a temperatura específica
    dados_temp = df_clean[df_clean['temperatura'] == temp]
    dados_medios = dados_temp.groupby('tempo_min')['razao_umidade'].mean().reset_index()
    
    t_data = dados_medios['tempo_min'].values
    mr_data = dados_medios['razao_umidade'].values
    
    # Ajuste dos modelos
    modelos = {
        'Henderson-Pabis': (henderson_pabis, [1.0, 0.01]),
        'Page': (page, [1.0, 0.01, 1.0]),
        'Newton': (newton, [1.0, 0.01, 0.05])
    }
    
    temp_resultados = {}
    
    for nome_modelo, (func, p0) in modelos.items():
        try:
            # Ajuste da curva
            popt, pcov = curve_fit(func, t_data, mr_data, p0=p0, maxfev=5000)
            
            # Predição
            mr_pred = func(t_data, *popt)
            
            # Cálculo de métricas
            r2 = 1 - np.sum((mr_data - mr_pred)**2) / np.sum((mr_data - np.mean(mr_data))**2)
            rmse = np.sqrt(np.mean((mr_data - mr_pred)**2))
            mae = np.mean(np.abs(mr_data - mr_pred))
            
            # Erro padrão dos parâmetros
            param_errors = np.sqrt(np.diag(pcov))
            
            temp_resultados[nome_modelo] = {
                'parametros': popt,
                'erro_parametros': param_errors,
                'r2': r2,
                'rmse': rmse,
                'mae': mae,
                'predicao': mr_pred
            }
            
            # Exibir resultados
            print(f"{nome_modelo}:")
            for i, (param, erro) in enumerate(zip(popt, param_errors)):
                print(f"  Parâmetro {i+1}: {param:.6f} ± {erro:.6f}")
            print(f"  R²: {r2:.4f}")
            print(f"  RMSE: {rmse:.6f}")
            print(f"  MAE: {mae:.6f}")
            print()
            
        except Exception as e:
            print(f"Erro no ajuste do modelo {nome_modelo}: {e}")
    
    resultados_modelos[temp] = temp_resultados

# Identificar melhor modelo para cada temperatura
print("RESUMO DOS MELHORES MODELOS:")
print("=" * 50)
for temp in sorted(resultados_modelos.keys()):
    temp_res = resultados_modelos[temp]
    if temp_res:
        melhor_modelo = max(temp_res.keys(), key=lambda k: temp_res[k]['r2'])
        r2_melhor = temp_res[melhor_modelo]['r2']
        print(f"{temp}°C: {melhor_modelo} (R² = {r2_melhor:.4f})")

# Visualização dos ajustes
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Ajuste de Modelos Matemáticos de Secagem', fontsize=16, fontweight='bold')

for i, temp in enumerate(sorted(df_clean['temperatura'].unique())):
    ax = axes[i//2, i%2]
    
    # Dados experimentais
    dados_temp = df_clean[df_clean['temperatura'] == temp]
    dados_medios = dados_temp.groupby('tempo_min')['razao_umidade'].mean().reset_index()
    
    t_data = dados_medios['tempo_min'].values
    mr_data = dados_medios['razao_umidade'].values
    
    # Plotar dados experimentais
    ax.scatter(t_data, mr_data, color='black', s=50, alpha=0.7, label='Dados Experimentais')
    
    # Plotar ajustes dos modelos
    cores_modelo = ['#1f77b4', '#ff7f0e', '#2ca02c']
    for j, (nome_modelo, cor) in enumerate(zip(resultados_modelos[temp].keys(), cores_modelo)):
        if nome_modelo in resultados_modelos[temp]:
            mr_pred = resultados_modelos[temp][nome_modelo]['predicao']
            r2 = resultados_modelos[temp][nome_modelo]['r2']
            ax.plot(t_data, mr_pred, color=cor, linewidth=2, 
                   label=f'{nome_modelo} (R²={r2:.3f})')
    
    ax.set_xlabel('Tempo (minutos)')
    ax.set_ylabel('Razão de Umidade (MR)')
    ax.set_title(f'Temperatura: {temp}°C')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Análise da influência da temperatura nos parâmetros
print("\n" + "="*50)
print("7. ANÁLISE DA INFLUÊNCIA DA TEMPERATURA")
print("="*50)

# Extrair constante de secagem (k) do modelo de Henderson-Pabis
k_values = []
temperaturas_k = []

for temp in sorted(resultados_modelos.keys()):
    if 'Henderson-Pabis' in resultados_modelos[temp]:
        k = resultados_modelos[temp]['Henderson-Pabis']['parametros'][1]
        k_values.append(k)
        temperaturas_k.append(temp)

if len(k_values) > 1:
    # Ajuste da equação de Arrhenius: k = k0 * exp(-Ea/(R*T))
    # Linearização: ln(k) = ln(k0) - Ea/(R*T)
    T_kelvin = np.array(temperaturas_k) + 273.15
    ln_k = np.log(k_values)
    
    # Regressão linear
    slope, intercept, r_value, p_value, std_err = stats.linregress(1/T_kelvin, ln_k)
    
    R = 8.314  # J/(mol·K)
    Ea = -slope * R  # Energia de ativação (J/mol)
    k0 = np.exp(intercept)
    
    print(f"Análise de Arrhenius:")
    print(f"Energia de ativação (Ea): {Ea:.2f} J/mol ({Ea/1000:.2f} kJ/mol)")
    print(f"Fator pré-exponencial (k0): {k0:.6f} min⁻¹")
    print(f"Coeficiente de correlação (R): {r_value:.4f}")
    
    # Gráfico de Arrhenius
    plt.figure(figsize=(10, 6))
    plt.scatter(1/T_kelvin, ln_k, s=100, color='red', alpha=0.7, label='Dados experimentais')
    
    # Linha de ajuste
    x_fit = np.linspace(min(1/T_kelvin), max(1/T_kelvin), 100)
    y_fit = slope * x_fit + intercept
    plt.plot(x_fit, y_fit, 'b-', linewidth=2, 
             label=f'Ajuste linear (R = {r_value:.4f})')
    
    plt.xlabel('1/T (K⁻¹)')
    plt.ylabel('ln(k)')
    plt.title('Gráfico de Arrhenius - Dependência da Temperatura')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Relatório final
print("\n" + "="*60)
print("RELATÓRIO FINAL DA ANÁLISE")
print("="*60)
print(f"✓ Total de dados analisados: {df_clean.shape[0]} pontos")
print(f"✓ Temperaturas testadas: {sorted(df_clean['temperatura'].unique())}")
print(f"✓ Tempo de secagem: 0 a {df_clean['tempo_min'].max()} minutos")
print(f"✓ Umidade inicial média: {df_clean[df_clean['tempo_min'] == 0]['umidade_percentual'].mean():.2f}%")

# Umidade final por temperatura
print("\n✓ Umidade final por temperatura:")
for temp in sorted(df_clean['temperatura'].unique()):
    dados_final = df_clean[(df_clean['temperatura'] == temp) & 
                          (df_clean['tempo_min'] == df_clean['tempo_min'].max())]
    umidade_final = dados_final['umidade_percentual'].mean()
    print(f"  {temp}°C: {umidade_final:.2f}%")

print("\n✓ Modelos matemáticos testados: Henderson-Pabis, Page, Newton")
print("✓ Todos os gráficos e análises foram gerados com sucesso!")
print("✓ Dados salvos em 'dados_secagem_simulados.csv'")

print("\nEste script está pronto para uso na disciplina ENG6001!")
print("Desenvolvido para análise completa de experimentos de secagem.")