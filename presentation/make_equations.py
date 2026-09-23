"""Render the Algorithm 1 objectives (paper eqs. 5-11) as PNGs with matplotlib mathtext for the 'Algorithm 1 in full' slides.
Output: assets/eq_*.png (transparent background, navy ink). Called by make_assets.py."""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets") + "/"
os.makedirs(A, exist_ok=True)
INK = "#14213D"
plt.rcParams["mathtext.fontset"] = "cm"

EQS = {
    # (5) tokenizer
    "eq5": r"$\mathcal{L}_{\mathrm{tok}}(\theta) \;=\; \mathcal{L}_{\mathrm{MSE}}(\theta) \;+\; 0.2\,\mathcal{L}_{\mathrm{LPIPS}}(\theta)$",
    # (6) corruption and prediction
    "eq6": r"$z_0 \sim \mathcal{N}(0, I),\quad z_1 \sim \mathcal{D},\quad (\tau, d) \sim p(\tau, d),\quad "
           r"\tilde{z} = (1-\tau)\,z_0 + \tau\,z_1,\quad \hat{z}_1 = f_\theta(\tilde{z}, \tau, d, a)$",
    # (7) flow term
    "eq7a": r"$\mathcal{L}(\theta) \;=\; \Vert \hat{z}_1 - z_1 \Vert_2^2 \qquad \mathrm{if}\ d = d_{\min}$",
    # (7) bootstrap term
    "eq7b": r"$\mathcal{L}(\theta) \;=\; (1-\tau)^2\,\left\Vert \dfrac{\hat{z}_1 - \tilde{z}}{1-\tau} \;-\; "
            r"\mathrm{sg}\left(\dfrac{b' + b''}{2}\right) \right\Vert_2^2 \qquad \mathrm{otherwise}$",
    # (7) half-step definitions
    "eq7c": r"$b' = \dfrac{f_\theta(\tilde{z}, \tau, d/2, a) - \tilde{z}}{1-\tau},\qquad "
            r"z' = \tilde{z} + b'\,d/2,\qquad "
            r"b'' = \dfrac{f_\theta(z', \tau + d/2, d/2, a) - z'}{1 - (\tau + d/2)}$",
    # (8) ramp weight
    "eq8": r"$w(\tau) \;=\; 0.9\,\tau + 0.1$",
    # (9) behaviour cloning + reward, multi-token prediction
    "eq9": r"$\mathcal{L}(\theta) \;=\; -\sum_{n=0}^{L} \ln p_\theta(a_{t+n} \mid h_t) \;-\; "
           r"\sum_{n=0}^{L} \ln p_\theta(r_{t+n} \mid h_t),\qquad L = 8$",
    # (10) value head
    "eq10": r"$\mathcal{L}(\theta) \;=\; -\sum_{t=1}^{T} \ln p_\theta(R^\lambda_t \mid s_t),\qquad "
            r"R^\lambda_t = r_t + \gamma\, c_t\,\left[(1-\lambda)\,v_t + \lambda\,R^\lambda_{t+1}\right],\qquad R^\lambda_T = v_T$",
    # (11) PMPO
    "eq11": r"$\mathcal{L}(\theta) \;=\; \dfrac{1-\alpha}{|\mathcal{D}^-|}\sum_{i \in \mathcal{D}^-} \ln \pi_\theta(a_i \mid s_i) \;-\; "
            r"\dfrac{\alpha}{|\mathcal{D}^+|}\sum_{i \in \mathcal{D}^+} \ln \pi_\theta(a_i \mid s_i) \;+\; "
            r"\dfrac{\beta}{N}\sum_{i=1}^{N} \mathrm{KL}\left[\pi_\theta(\cdot \mid s_i)\,\Vert\,\pi_{\mathrm{prior}}\right]$",
    "eq11b": r"$A_t = R^\lambda_t - v_t,\qquad \mathcal{D}^+ = \{s_i : A_i \geq 0\},\qquad \mathcal{D}^- = \{s_i : A_i < 0\},\qquad "
             r"\alpha = 0.5,\quad \beta = 0.3,\quad \gamma = 0.997$",
}

def render(name, tex, size=20):
    fig = plt.figure(figsize=(0.1, 0.1))
    fig.text(0, 0, tex, fontsize=size, color=INK)
    out = A + f"{name}.png"
    fig.savefig(out, dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    return out

if __name__ == "__main__":
    for k, v in EQS.items():
        render(k, v)
    print("equations rendered:", ", ".join(EQS))
