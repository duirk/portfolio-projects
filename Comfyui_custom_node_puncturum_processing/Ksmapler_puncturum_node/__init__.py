import torch
import numpy as np
import networkx as nx
from scipy.integrate import quad
import comfy.sample
import comfy.samplers
import nodes  # Importamos el módulo principal de nodos de ComfyUI

class CustomKSamplerNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0, "step": 0.1, "round": 0.01}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "latent_image": ("LATENT",),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "puncturum": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 5.0, "step": 0.1}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "sample"
    CATEGORY = "custom"

    def sample(self, model, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise, puncturum):
        # ==========================================
        # INTEGRACIÓN DE NODOS Y RED COMPLEJA
        # ==========================================
        safe_seed = int(seed) % 4294967296
        np.random.seed(safe_seed)
        
        num_nodos = 40
        G = nx.erdos_renyi_graph(n=num_nodos, p=0.3, seed=safe_seed)

        for u, v in G.edges():
            G[u][v]['weight'] = np.random.uniform(0.1, 1.0)

        L = nx.laplacian_matrix(G, weight='weight').toarray()
        autovalores, autovectores = np.linalg.eigh(L)
        lambda_fiedler = autovalores[1] if len(autovalores) > 1 else 1.0

        def densidad_energia_continua(x, autovalor_laminrar):
            return np.exp(-x) * np.cos(autovalor_laminrar * np.pi * x) ** 2

        energia_integral, _ = quad(densidad_energia_continua, 0, 1, args=(lambda_fiedler,))

        vector_fiedler = autovectores[:, 1] if autovectores.shape[1] > 1 else np.ones(num_nodos)
        f_spectral = {i: 1 if vector_fiedler[i] >= 0 else -1 for i in range(num_nodos)}
        f_vector = np.array([f_spectral[i] for i in range(num_nodos)])
        energia_matricial = np.dot(f_vector.T, np.dot(L, f_vector))

        # CORRECCIÓN: No alteramos los tensores de 'positive'. 
        # Utilizamos puncturum y la energía matricial de la red exclusivamente para modular los pasos.
        factor_red = max(0.1, energia_matricial / (num_nodos * max(1.0, puncturum)))
        optimized_steps = max(1, int(steps / factor_red))

        # Ejecutamos el muestreo con los pasos optimizados y el conditioning limpio
        return nodes.common_ksampler(
            model, seed, optimized_steps, cfg, sampler_name, scheduler, 
            positive, negative, latent_image, denoise=denoise
        )

NODE_CLASS_MAPPINGS = {
    "CustomKSampler": CustomKSamplerNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CustomKSampler": "Custom KSampler Node optimizado con Nodos y Puncturum"
}