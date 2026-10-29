"""Figure del paper (PDF in paper/figure/), dai risultati e dalla cache del pilota.

    python paper/figure.py           figure in italiano in paper/figure/
    python paper/figure.py en        figure in inglese in paper_en/figures/ (versione per la rivista)

Palette validata (validate_palette.js, sfondo bianco, tutte le coppie): blu, arancione, verde acqua per le tre
famiglie di modelli; i due Timestral sono due toni dello stesso blu (chiaro = 28M, scuro = 209M). Benchmark in
grigio. Ogni figura con piu' serie ha la legenda.
"""

import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pilota"))
import covariate as C  # noqa: E402
import pilota as P  # noqa: E402
import vol_implicita as V  # noqa: E402

LANG = sys.argv[1] if len(sys.argv) > 1 else "it"
RIS = P.RIS
OUT = ROOT / "paper_en" / "figures" if LANG == "en" else Path(__file__).resolve().parent / "figure"
TAG = "2024-01-01_c4096_p1"
MODELLI = ["Timestral-28M", "Timestral-209M", "TimesFM-3", "Chronos-2"]
COL = {"Timestral-28M": "#86b6ef", "Timestral-209M": "#1c5cab", "TimesFM-3": "#eb6834", "Chronos-2": "#1baf7a"}
MARK = {"Timestral-28M": "o", "Timestral-209M": "o", "TimesFM-3": "s", "Chronos-2": "D"}
INK, INK2, GRID, AXIS = "#0b0b0b", "#52514e", "#e1e0d9", "#c3c2b7"
GRIGIO, GRIGIO_SCURO, GRIGIO_CHIARO = "#7a7974", "#3a3a37", "#b9b8b0"
W = 6.3  # larghezza del testo in pollici
NOME = {"Caffe": "Caffè"}
if LANG == "en":
    NOME = {"Gasolio": "Heating oil", "Benzina": "Gasoline", "Gas naturale": "Natural gas", "Oro": "Gold",
            "Argento": "Silver", "Rame": "Copper", "Grano": "Wheat", "Mais": "Corn", "Soia": "Soybeans",
            "Caffe": "Coffee", "Zucchero": "Sugar", "Cacao": "Cocoa", "Bestiame": "Live cattle"}
EN = {
    "CRPS rispetto al random walk, $h=1$ (sotto 1 = meglio; frecce: valori fuori scala)":
        "CRPS relative to the random walk, $h=1$ (below 1 = better; arrows: values off scale)",
    "Mediana prevista a un giorno meno ultimo prezzo, in % (WTI)":
        "One-day-ahead median minus last price, in % (WTI)",
    "Origini": "Forecast origins",
    "Rendimento giornaliero": "Daily return",
    "Simulazione storica": "Historical simulation",
    "Violazioni Timestral": "Timestral violations",
    "Rendimento (%)": "Return (%)",
    "Realizzata (Garman-Klass)": "Realized (Garman-Klass)",
    "Foundation model": "Foundation models",
    "Benchmark classici": "Econometric benchmarks",
    "Volatilità annualizzata (%)": "Annualized volatility (%)",
    "Prezzo: CRPS / random walk, $h=20$": "Price: CRPS / random walk, $h=20$",
    "Volatilità: QLIKE / HAR, $h=20$": "Volatility: QLIKE / HAR, $h=20$",
    "Contesto (giorni)": "Context length (days)",
    "Prezzo: CRPS / random walk, $h=5$": "Price: CRPS / random walk, $h=5$",
    "Volatilità: QLIKE / HAR, $h=5$": "Volatility: QLIKE / HAR, $h=5$",
    "QLIKE con l'indice / QLIKE senza (sotto 1 = l'indice aiuta)":
        "QLIKE with the index / QLIKE without (below 1 = the index helps)",
}


def T(s: str) -> str:
    """Traduzione delle etichette per la versione inglese."""
    return EN.get(s, s) if LANG == "en" else s

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": (["Times New Roman", "DejaVu Serif"] if LANG == "en"
                   else ["Latin Modern Roman", "CMU Serif", "DejaVu Serif"]),
    "mathtext.fontset": "cm", "font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9, "legend.fontsize": 8,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False, "lines.linewidth": 1.2,
    "axes.titlecolor": INK, "axes.titleweight": "normal", "savefig.bbox": "tight", "pdf.fonttype": 42,
})


def salva(fig, nome):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{nome}.pdf")
    fig.savefig(OUT / f"{nome}.png", dpi=160)
    plt.close(fig)
    print("  ", nome)


def riferimento(ax, x=1.0, vertical=True):
    (ax.axvline if vertical else ax.axhline)(x, color=GRIGIO, lw=0.8, zorder=1)


# --------------------------------------------------------------------------- dati
def fig_prezzi():
    fig, axes = plt.subplots(5, 3, figsize=(W, 7.2), sharex=True)
    for ax, a in zip(axes.ravel(), P.ASSETS):
        df = P.load_asset(a)
        p = df["prezzo"].where(df["prezzo"] > 0)
        ax.plot(p.index, p, color=COL["Timestral-209M"], lw=0.7)
        ax.axvspan(pd.Timestamp("2024-01-01"), p.index[-1], color=GRID, alpha=0.7, lw=0, zorder=0)
        ax.set_title(NOME.get(a, a), loc="left", pad=2)
        ax.grid(axis="x", visible=False)
        ax.tick_params(length=0)
    for ax in axes[-1]:
        ax.xaxis.set_major_locator(mpl.dates.YearLocator(6))
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter("%Y"))
    fig.tight_layout(h_pad=0.6, w_pad=0.8)
    salva(fig, "prezzi")


# --------------------------------------------------------------------------- prezzo
def legenda_sopra(fig_or_ax, handles=None, labels=None, ncol=5):
    """Legenda su una riga sopra il grafico, allineata a sinistra, senza cornice."""
    kw = dict(ncol=ncol, loc="lower left", bbox_to_anchor=(0, 1.01), handletextpad=0.3, columnspacing=1.2,
              borderaxespad=0, handlelength=1.4)
    if handles is not None:
        return fig_or_ax.legend(handles, labels, **kw)
    return fig_or_ax.legend(**kw)


def fig_prezzo_asset():
    d = pd.read_csv(RIS / "prezzo.csv")
    d = d[d["h"] == 1]
    assets = P.ASSETS[::-1]
    y = {a: i for i, a in enumerate(assets)}
    xmin, xmax = 0.93, 1.06
    fig, ax = plt.subplots(figsize=(W, 5.3))
    # fasce alterne per settore
    settori = [P.UNIVERSE[a][1] for a in assets]
    blocchi, inizio = [], 0
    for i in range(1, len(assets) + 1):
        if i == len(assets) or settori[i] != settori[inizio]:
            blocchi.append((inizio, i - 1, settori[inizio]))
            inizio = i
    nomi_settore = {"Energia": "Energy", "Metalli preziosi": "Precious metals", "Metalli industriali": "Industrial metals",
                    "Cereali": "Grains", "Soft e bestiame": "Softs and livestock"}
    for k, (a, b, s) in enumerate(blocchi):
        if k % 2 == 0:
            ax.axhspan(a - 0.5, b + 0.5, color="#f3f2ee", lw=0, zorder=0)
        ax.text(0.006, b + 0.45, nomi_settore[s] if LANG == "en" else s, fontsize=7, color=GRIGIO,
                style="italic", va="top", ha="left", transform=ax.get_yaxis_transform())
    off = {"ETS": -0.28, "Timestral-28M": -0.14, "Timestral-209M": 0.0, "TimesFM-3": 0.14, "Chronos-2": 0.28}
    for m, o in off.items():
        s = d[d["modello"] == m].set_index("asset")["CRPS/RW"]
        ys = np.array([y[a] + o for a in s.index])
        if m == "ETS":
            ax.scatter(s.values, ys, marker="o", s=20, facecolor="white", edgecolor=GRIGIO_SCURO, lw=0.9,
                       label="AutoETS", zorder=3)
            continue
        dentro = s.values <= xmax
        ax.scatter(s.values[dentro], ys[dentro], marker=MARK[m], s=24, color=COL[m], edgecolor="white", lw=0.5,
                   label=m, zorder=3)
        for v, yy in zip(s.values[~dentro], ys[~dentro]):  # fuori scala: freccia sul bordo e valore
            ax.scatter([xmax - 0.002], [yy], marker=">", s=26, color=COL[m], zorder=3, clip_on=False)
            ax.text(xmax - 0.006, yy, f"{v:.2f}", fontsize=7, color=INK2, ha="right", va="center")
    riferimento(ax)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(-0.6, len(assets) - 0.4)
    ax.set_yticks(range(len(assets)), [NOME.get(a, a) for a in assets])
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel(T("CRPS rispetto al random walk, $h=1$ (sotto 1 = meglio; frecce: valori fuori scala)"))
    legenda_sopra(ax)
    salva(fig, "prezzo_asset")


def fig_chronos_mediana():
    df, orig, _, _ = P.setup_asset("WTI", "2024-01-01", 4096, 1)
    x = P.model_input(df, "prezzo")
    last = x[orig - 1].astype(float)
    fig, ax = plt.subplots(figsize=(W, 2.4))
    bins = np.linspace(-1.5, 1.5, 61)
    for m in ["Timestral-209M", "TimesFM-3", "Chronos-2"]:
        q = np.load(P.CACHE / f"{m}_WTI_prezzo_{TAG}.npy")
        lv = P.levels_of(m)
        med = q[:, 0, int(np.argmin(np.abs(lv - 0.5)))]
        dev = 100 * (med - last) / last
        ax.hist(dev, bins=bins, histtype="step", color=COL[m], lw=1.4,
                label=f"{m}: {np.abs(dev).mean():.2f}%")
    ax.axvline(0, color=GRIGIO, lw=0.8)
    ax.set_xlabel(T("Mediana prevista a un giorno meno ultimo prezzo, in % (WTI)"))
    ax.set_ylabel(T("Origini"))
    legenda_sopra(ax, ncol=3)
    salva(fig, "chronos_mediana")


# --------------------------------------------------------------------------- VaR
def fig_var_wti():
    df, orig, _, _ = P.setup_asset("WTI", "2024-01-01", 4096, 1)
    r = df["rendimento"].to_numpy(float)
    y, date = r[orig], df.index[orig]
    q = np.load(P.CACHE / f"Timestral-209M_WTI_rendimento_{TAG}.npy")[:, 0, 0]  # quantile 0.01
    g = np.load(P.CACHE / f"bench_GARCH-t_WTI_rendimento_2024-01-01_p1_o{orig[0]}-{len(orig)}.npy")[:, 0]
    hs = np.array([np.nanquantile(r[max(0, o - P.WINDOW): o], 0.01) for o in orig])
    fig, ax = plt.subplots(figsize=(W, 2.8))
    ax.bar(date, y, width=1.6, color="#a3a29a", lw=0, label=T("Rendimento giornaliero"))
    ax.plot(date, hs, color=GRIGIO_SCURO, lw=1.0, ls=(0, (4, 2)), label=T("Simulazione storica"))
    ax.plot(date, g, color=GRIGIO, lw=1.0, label="GARCH-t")
    ax.plot(date, q, color=COL["Timestral-209M"], lw=1.2, label="Timestral-209M")
    hit = y < q
    ax.scatter(date[hit], y[hit], s=14, color=COL["Timestral-209M"], zorder=4, edgecolor="white", lw=0.5,
               label=f"{T('Violazioni Timestral')} ({hit.sum()})")
    ax.set_ylabel(T("Rendimento (%)"))
    ax.grid(axis="x", visible=False)
    legenda_sopra(ax, ncol=3)
    salva(fig, "var_wti")


# --------------------------------------------------------------------------- volatilita'
def fig_vol_wti():
    df, orig, _, _ = P.setup_asset("WTI", "2024-01-01", 4096, 1)
    h = 5
    v = df["var_gk"].to_numpy(float)
    o = orig[orig + h <= len(v)]
    real = np.array([np.nanmean(v[i: i + h]) for i in o])
    ok = np.isfinite(real)
    o, real = o[ok], real[ok]
    sel = np.searchsorted(orig, o)
    ann = lambda var: np.sqrt(252 * var) * 100  # noqa: E731

    def fm(path):
        q = P.common(np.load(path), P.levels_of("Timestral-209M"))[sel, :h]
        return np.mean((np.maximum(q, 1e-3) / 100) ** 2 / 252, axis=(1, 2))

    ovx = V.serie_indice("OVX", df.index).astype(float) ** 2 / 252 / 1e4
    serie = [
        (T("Realizzata (Garman-Klass)"), ann(real), dict(color=GRIGIO_CHIARO, lw=0.9)),
        ("HAR", ann(P.har_forecast(v, o, h)), dict(color=GRIGIO_SCURO, lw=1.0, ls=(0, (4, 2)))),
        ("Log-HAR-X (OVX)", ann(C.loghar_forecast(v, ovx, o, h)), dict(color=GRIGIO, lw=1.0)),
        ("Timestral-209M", ann(fm(P.CACHE / f"Timestral-209M_WTI_volatilita_{TAG}.npy")),
         dict(color=COL["Timestral-28M"], lw=1.1)),
        ("Timestral-209M + OVX", ann(fm(P.CACHE / f"Timestral-209M_WTI_volatilita_iv-Propria_{TAG}.npy")),
         dict(color=COL["Timestral-209M"], lw=1.2)),
    ]
    fig, axes = plt.subplots(2, 1, figsize=(W, 4.4), sharex=True, sharey=True)
    for ax, idx, tit in [(axes[0], [0, 3, 4], T("Foundation model")),
                             (axes[1], [0, 1, 2], T("Benchmark classici"))]:
        for i in idx:
            lab, s, kw = serie[i]
            ax.plot(df.index[o], s, label=lab, **kw)
        ax.set_title(tit, loc="left")
        ax.set_ylabel(T("Volatilità annualizzata (%)"))
        ax.grid(axis="x", visible=False)
        ax.legend(loc="upper left")
    fig.tight_layout(h_pad=1.0)
    salva(fig, "vol_wti")


def fig_contesto():
    d = pd.read_csv(RIS / "robustezza" / "contesto.csv")
    fig, axes = plt.subplots(1, 2, figsize=(W, 2.5))
    for ax, col, lab in [(axes[0], "CRPS/RW h=20", "Prezzo: CRPS / random walk, $h=20$"),
                         (axes[1], "QLIKE/HAR h=20", "Volatilità: QLIKE / HAR, $h=20$")]:
        for m in ["Timestral-28M", "TimesFM-3"]:
            g = d[d["modello"] == m].dropna(subset=[col]).groupby("contesto")[col].apply(P.geo_mean)
            ax.plot(g.index, g.values, marker=MARK[m], ms=5, color=COL[m], label=m)
        ax.axhline(1, color=GRIGIO, lw=0.8)
        ax.set_xscale("log", base=2)
        ax.set_xticks([256, 512, 1024, 4096], ["256", "512", "1024", "4096"])
        ax.minorticks_off()
        ax.set_title(T(lab), loc="left")
        ax.set_xlabel(T("Contesto (giorni)"))
    fig.tight_layout(w_pad=2)
    legenda_sopra(fig, *axes[0].get_legend_handles_labels(), ncol=2).set_bbox_to_anchor((0.0, 1.0),
                                                                                    transform=fig.transFigure)
    salva(fig, "contesto")


def fig_anni():
    d = pd.read_csv(RIS / "sottoperiodi_regimi.csv")
    anni = ["2024", "2025", "2026"]
    fig, axes = plt.subplots(1, 2, figsize=(W, 2.5), sharex=True)
    for ax, (task, h, lab) in zip(axes, [("prezzo", 5, "Prezzo: CRPS / random walk, $h=5$"),
                                         ("volatilita", 5, "Volatilità: QLIKE / HAR, $h=5$")]):
        g = d[(d["compito"] == task) & (d["h"] == h) & d["gruppo"].astype(str).isin(anni)]
        for m in MODELLI:
            s = g[g["modello"] == m].set_index(g[g["modello"] == m]["gruppo"].astype(str))["rel"].reindex(anni)
            ax.plot(anni, s.values, marker=MARK[m], ms=5, color=COL[m], label=m)
        ax.axhline(1, color=GRIGIO, lw=0.8)
        ax.set_title(T(lab), loc="left")
    fig.tight_layout(w_pad=2)
    legenda_sopra(fig, *axes[0].get_legend_handles_labels(), ncol=4).set_bbox_to_anchor((0.0, 1.0),
                                                                                    transform=fig.transFigure)
    salva(fig, "anni")


def fig_vol_implicita():
    d = pd.read_csv(RIS / "vol_implicita" / "con_contro_senza.csv")
    d = d[(d["compito"] == "volatilita") & (d["covariata"] == "Propria")]
    assets = ["WTI", "Brent", "Gasolio", "Benzina", "Oro"][::-1]
    y = {a: i for i, a in enumerate(assets)}
    fig, axes = plt.subplots(1, 3, figsize=(W, 2.9), sharey=True)
    off = {"Log-HAR-X": -0.28, "Timestral-28M": -0.14, "Timestral-209M": 0.0, "TimesFM-3": 0.14, "Chronos-2": 0.28}
    for ax, h in zip(axes, P.HORIZONS):
        g = d[d["h"] == h]
        for i in range(0, len(assets), 2):
            ax.axhspan(i - 0.5, i + 0.5, color="#f3f2ee", lw=0, zorder=0)
        for m, o in off.items():
            s = g[g["modello"] == m].set_index("asset")["rapporto"].reindex(assets).dropna()
            ys = [y[a] + o for a in s.index]
            if m == "Log-HAR-X":
                ax.scatter(s.values, ys, marker="o", s=18, facecolor="white", edgecolor=GRIGIO_SCURO, lw=0.9,
                           label="Log-HAR-X vs Log-HAR", zorder=3)
            else:
                ax.scatter(s.values, ys, marker=MARK[m], s=20, color=COL[m], edgecolor="white", lw=0.5, label=m,
                           zorder=3)
        riferimento(ax)
        ax.set_xlim(0.69, 1.03)
        ax.set_ylim(-0.6, len(assets) - 0.4)
        ax.set_title(f"$h={h}$", loc="left")
        ax.grid(axis="y", visible=False)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(range(len(assets)), [f"{NOME.get(a, a)} ({'GVZ' if a == 'Oro' else 'OVX'})" for a in assets])
    axes[1].set_xlabel(T("QLIKE con l'indice / QLIKE senza (sotto 1 = l'indice aiuta)"))
    fig.tight_layout(w_pad=1.2)
    legenda_sopra(fig, *axes[0].get_legend_handles_labels(), ncol=5).set_bbox_to_anchor((0.0, 1.0),
                                                                                    transform=fig.transFigure)
    salva(fig, "vol_implicita")


if __name__ == "__main__":
    for f in [fig_prezzi, fig_prezzo_asset, fig_chronos_mediana, fig_var_wti, fig_vol_wti, fig_contesto, fig_anni,
              fig_vol_implicita]:
        f()
