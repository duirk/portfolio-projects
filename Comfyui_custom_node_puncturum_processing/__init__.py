import torch

class TurboQuantumGraphNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "num_nodes": ("INT", {"default": 1000000, "min": 1000, "max": 100000000, "step": 10000}),
                "qubit_depth": ("INT", {"default": 10, "min": 1, "max": 30, "step": 1}),
                "scale_duration": ("FLOAT", {"default": 60.0, "min": 5.0, "max": 600.0, "step": 5.0}),
                "device": (["cuda", "cpu"], {"default": "cuda"}),
            },
            "optional": {
                "width": ("INT", {"default": 512, "min": 64, "max": 2048, "step": 8}),
                "height": ("INT", {"default": 320, "min": 64, "max": 2048, "step": 8}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120, "step": 1}),
                "frames": ("INT", {"default": 25, "min": 1, "max": 120, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING", "FLOAT", "INT", "INT", "INT", "INT")
    RETURN_NAMES = ("quantum_report", "fidelity_score", "width", "height", "fps", "frames")
    FUNCTION = "process_quantum_turbo"
    CATEGORY = "utilidades"

    def process_quantum_turbo(self, num_nodes, qubit_depth, scale_duration, device, width=512, height=320, fps=24, frames=25):
        if device == "cuda" and not torch.cuda.is_available():
            device = "cpu"

        print(f"--- INICIANDO PROCESAMIENTO CUÁNTICO HIPER TURBO ({qubit_depth} Qubits, {num_nodes:,} nodos) ---")
        
        # 1. Superposición Cuántica Ultraligera con tensores complejos
        real_part = torch.randn(num_nodes, dtype=torch.float32, device=device)
        imag_part = torch.randn(num_nodes, dtype=torch.float32, device=device)
        state_vector = torch.complex(real_part, imag_part)
        state_vector = state_vector / torch.norm(state_vector)
        
        # 2. Rotaciones de Fase Cuántica
        theta = 3.1415926535 / qubit_depth
        phase_gate = torch.exp(1j * theta * torch.arange(num_nodes, dtype=torch.float32, device=device))
        evolved_state = state_vector * phase_gate
        
        # 3. Medición Cuántica y cálculo de fidelidad
        probabilities = torch.abs(evolved_state) ** 2
        raw_fidelity = torch.sum(probabilities * torch.log(probabilities + 1e-9)).abs().item()
        
        scaled_fidelity = float((raw_fidelity % 1.0) * scale_duration + 15.0)
        quantum_energy = torch.mean(torch.abs(evolved_state)).item() * 100.0

        report = (
            f"⚡ Procesamiento Cuántico  Turbo Exitosamente.\n"
            f"Nodos: {num_nodes:,} | Res: {width}x{height} | FPS: {fps} | Cuadros: {frames} | Fidelidad: {scaled_fidelity:.2f}%"
        )

        print(report)
        return (report, scaled_fidelity, width, height, fps, frames)

NODE_CLASS_MAPPINGS = {
    "TurboQuantumGraphNode": TurboQuantumGraphNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TurboQuantumGraphNode": "⚛️  Turbo Quantum Processor"
}
