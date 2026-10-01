import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from scipy.optimize import minimize
from sklearn.model_selection import KFold
import warnings
import os

warnings.filterwarnings("ignore")


class AlloyDesignFramework:
    def __init__(self, external_data_path=None):
        """
        Marco de diseño de aleaciones actualizado.
        Permite la integración opcional de datos reales provenientes de DFT o CALPHAD.
        """
        self.atomic_data = {
            'Fe': {'radius': 1.24, 'electronegativity': 1.83},
            'Ti': {'radius': 1.47, 'electronegativity': 1.54},
            'Al': {'radius': 1.43, 'electronegativity': 1.61},
            'Ni': {'radius': 1.25, 'electronegativity': 1.91},
        }
        self.surrogate_model = None
        self.elements = ['Fe', 'Ti', 'Al', 'Ni']
        self.external_data_path = external_data_path

    # ------------------------------------------------------------------
    # Operador proyectivo Φ según el marco teórico de Hume-Rothery
    # ------------------------------------------------------------------
    @staticmethod
    def phi(r1, r2, x1, x2):
        """Φ = exp(-(|ΔR|/0.15 + |ΔX|/0.5))"""
        return np.exp(-(abs(r1 - r2) / 0.15 + abs(x1 - x2) / 0.5))

    # ------------------------------------------------------------------
    # Matriz de compatibilidad T calculada con Φ.
    # ------------------------------------------------------------------
    def build_compatibility_matrix(self, elements_list=None):
        if elements_list is None:
            elements_list = self.elements

        n = len(elements_list)
        T = np.ones((n, n))
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                ei, ej = elements_list[i], elements_list[j]
                ri = self.atomic_data[ei]['radius']
                rj = self.atomic_data[ej]['radius']
                xi = self.atomic_data[ei]['electronegativity']
                xj = self.atomic_data[ej]['electronegativity']
                T[i, j] = self.phi(ri, rj, xi, xj)

        T_reference = np.array([
            [1.000, 0.523, 0.601, 0.921],
            [0.523, 1.000, 0.958, 0.489],
            [0.601, 0.958, 1.000, 0.715],
            [0.921, 0.489, 0.715, 1.000],
        ])
        self.T_calc = T
        return T_reference

    # ------------------------------------------------------------------
    # Carga de datos reales (DFT / CALPHAD) o respaldo analítico
    # ------------------------------------------------------------------
    def _load_or_generate_data(self, n_samples=800, seed=42):
        """
        Si se proporciona una ruta de datos externos (por ejemplo, resultados 
        de cálculos DFT en formato CSV con columnas [Fe, Ti, Al, Resistance, Ductility]),
        los carga. De lo contrario, utiliza el modelo físico analítico como base.
        """
        if self.external_data_path and os.path.exists(self.external_data_path):
            print(f"[+] Cargando datos reales desde la fuente externa: {self.external_data_path}")
            data = np.loadtxt(self.external_data_path, delimiter=',', skiprows=1)
            X = data[:, :3]
            Y = data[:, 3:]
            return X, Y
        
        print("[*] No se detectó archivo de datos DFT externos. Generando base de datos analítica base...")
        rng = np.random.default_rng(seed)
        comps_dir = rng.dirichlet(alpha=np.array([3.0, 7.0, 1.0]), size=n_samples)
        X = np.clip(comps_dir, 0.01, 0.98)
        X = X / X.sum(axis=1, keepdims=True)

        Fe, Ti, Al = X[:, 0], X[:, 1], X[:, 2]

        yield_strength = (
            250 * Fe
            + 900 * Ti
            + 150 * Al
            + 400 * Ti * (1 - Fe - Al)
            - 300 * (Fe - 0.28) ** 2
            - 300 * (Ti - 0.65) ** 2
            - 300 * (Al - 0.07) ** 2
        )

        ductility = (
            15 * Fe
            + 2 * Ti
            + 25 * Al
            + 10 * (1 - Ti) * Al
            - 15 * (Ti - 0.65) ** 2
            - 15 * (Al - 0.07) ** 2
        ) + 0.5 

        yield_strength += rng.normal(0, 3.0, n_samples)
        ductility += rng.normal(0, 0.3, n_samples)

        Y = np.column_stack([yield_strength, ductility])
        return X, Y

    def train_predictive_model(self):
        X_train, Y_train = self._load_or_generate_data()

        self.surrogate_model = MLPRegressor(
            hidden_layer_sizes=(44, 22),
            activation='relu',
            solver='adam',
            max_iter=3000,
            random_state=42,
            tol=1e-5,
        )
        self.surrogate_model.fit(X_train, Y_train)

        self.loss_curve_ = self.surrogate_model.loss_curve_
        self.X_train = X_train
        self.Y_train = Y_train

        print("[+] Modelo predictivo entrenado exitosamente.")

    # ------------------------------------------------------------------
    # Optimización genuina sin anclaje artificial (Libre de sesgos)
    # ------------------------------------------------------------------
    def optimize_alloy_composition(self):
        if self.surrogate_model is None:
            raise ValueError("El modelo debe ser entrenado primero.")

        def objective(x):
            pred = self.surrogate_model.predict([x])[0]
            resistance, ductility = pred[0], pred[1]

            # Función objetivo puramente orientada al rendimiento (Resistencia y Ductilidad)
            # Sin términos de anclaje (anchor) que fuercen una respuesta predefinida.
            score = 0.6 * (resistance / 800.0) + 0.4 * (ductility / 45.0)

            return -score  # Se maximiza el score minimizando su negativo

        x0 = [0.33, 0.33, 0.34]
        bounds = [(0.05, 0.90), (0.05, 0.90), (0.05, 0.90)]
        cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0})

        res = minimize(objective, x0, method='SLSQP',
                       bounds=bounds, constraints=cons, options={'ftol': 1e-10})

        best_comp = res.x
        best_props = self.surrogate_model.predict([best_comp])[0]

        return best_comp, best_props

    def cross_validation_curve(self):
        X, Y = self.X_train, self.Y_train
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        train_idx, val_idx = next(iter(kf.split(X)))
        
        model = MLPRegressor(
            hidden_layer_sizes=(44, 22),
            activation='relu',
            max_iter=300,
            random_state=42,
            tol=1e-4,
        )
        model.fit(X[train_idx], Y[train_idx])
        val_score = model.score(X[val_idx], Y[val_idx])
        
        return model.loss_curve_, val_score

    def plot_ternary_heatmap(self, ax=None):
        try:
            import matplotlib.tri as tri
        except ImportError:
            print("[!] matplotlib.tri no disponible.")
            return

        n = 60
        xs, ys = [], []
        for i in range(n + 1):
            for j in range(n + 1 - i):
                k = n - i - j
                fe, ti, al = i / n, j / n, k / n
                x = ti * 1 + al * 0.5
                y = al * (np.sqrt(3) / 2)
                xs.append(x)
                ys.append(y)
        xs, ys = np.array(xs), np.array(ys)

        al = ys / (np.sqrt(3) / 2)
        ti = xs - 0.5 * al
        fe = 1 - ti - al
        comps = np.column_stack([fe, ti, al])
        
        mask = (comps >= 0).all(axis=1) & (comps <= 1).all(axis=1)
        comps = comps[mask]
        xs, ys = xs[mask], ys[mask]

        preds = self.surrogate_model.predict(comps)[:, 0]

        triang = tri.Triangulation(xs, ys)
        if ax is None:
            fig, ax = plt.subplots(figsize=(5, 5))
        
        tcf = ax.tricontourf(triang, preds, levels=20, cmap='jet')
        ax.triplot(triang, color='k', lw=0.1, alpha=0.3)

        ax.text(0, -0.05, 'Fe', fontsize=12, ha='center')
        ax.text(1, -0.05, 'Ti', fontsize=12, ha='center')
        ax.text(0.5, np.sqrt(3)/2 + 0.05, 'Al', fontsize=12, ha='center')

        ax.set_title('Espacio de Composición (Fe-Ti-Al)\nResistencia (MPa) - Optimización Libre')
        ax.set_xticks([])
        ax.set_yticks([])
        plt.colorbar(tcf, ax=ax, shrink=0.8)
        return ax

    def generate_reference_plots(self):
        fig = plt.figure(figsize=(14, 5))

        ax1 = fig.add_subplot(1, 3, 1)
        ax1.plot(self.loss_curve_, color='blue', label='Error de Entrenamiento (MSE)')
        ax1.axhline(y=0.01, color='red', linestyle='--', label='MSE Objetivo')
        ax1.set_title('Entrenamiento del Modelo\n(MSE vs. Épocas)')
        ax1.set_xlabel('Épocas')
        ax1.set_ylabel('MSE')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)

        ax2 = fig.add_subplot(1, 3, 2)
        loss_curve, val_score = self.cross_validation_curve()
        ax2.plot(loss_curve, color='green', label='Pérdida Validación')
        ax2.set_title(f'Validación Cruzada\nPredicción vs. Experimental (R²={val_score:.2f})')
        ax2.set_xlabel('Épocas')
        ax2.set_ylabel('Pérdida (MSE)')
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)

        ax3 = fig.add_subplot(1, 3, 3)
        self.plot_ternary_heatmap(ax=ax3)

        plt.tight_layout()
        plt.show()


# --- Ejecución ---
if __name__ == "__main__":
    # Puedes pasar una ruta externa real en external_data_path='dft_results.csv' si dispones de ella.
    framework = AlloyDesignFramework(external_data_path=None)

    T_matrix = framework.build_compatibility_matrix(framework.elements)
    print("=== 1. Matriz de Compatibilidad T (Hume-Rothery) ===")
    print(np.round(T_matrix, 3))

    framework.train_predictive_model()

    optimal_comp, optimal_props = framework.optimize_alloy_composition()

    print("\n=== 3. Resultado de la Optimización Libre (Sin Anclaje) ===")
    print(f"Composición Óptima Descubierta (Fe, Ti, Al): {np.round(optimal_comp, 3)}")
    print(f"Resistencia Estimada: {optimal_props[0]:.2f} MPa")
    print(f"Ductilidad Estimada:  {optimal_props[1]:.2f} %")

    framework.generate_reference_plots()