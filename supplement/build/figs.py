"""New figures for the supplement. Run after tables.py logic (imports it)."""
import sys, os
sys.argv = [sys.argv[0], sys.argv[1], 'none'] if len(sys.argv) > 1 else sys.argv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tables as tb

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'figures')
BLUE, ORANGE, GREEN = '#2a78d6', '#eb6834', '#1baf7a'
INK, MUTED, GRID = '#1f1f1f', '#5c5c5c', '#e6e6e6'
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['DejaVu Serif'], 'font.size': 8.5,
                     'axes.edgecolor': MUTED, 'axes.labelcolor': INK, 'xtick.color': MUTED, 'ytick.color': MUTED,
                     'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.color': GRID,
                     'grid.linewidth': 0.6, 'axes.axisbelow': True, 'legend.frameon': False})
GROUP = {m: BLUE for m in tb.DEC}
GROUP.update({'CoPE': ORANGE, 'BART': ORANGE, 'GPT-5.6 Luna': GREEN, 'GPT-6 Sol': GREEN})
SHORT = {'GPT-5.6 Luna': 'Luna', 'GPT-6 Sol': 'Sol', 'Luna Decisions': 'Luna Dec.', 'Bespoke-Nimble': 'Nimble'}

def save(fig, name):
    for ext in ('png', 'pdf'):
        fig.savefig(os.path.join(OUT, f'{name}.{ext}'), dpi=200, bbox_inches='tight')
    plt.close(fig)

# ---------------------------------------------------------------- 1. quality vs latency and cost, HateCheck, all models
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), sharey=True)
LOFF = {  # label offsets (points) per panel to avoid collisions
    0: {'Laya': (6, -3), 'BART': (6, 2), 'SemIf-2B': (-8, -10), 'Decider': (6, -10), 'SemIf-4B': (-44, 4), 'CoPE': (-14, 6),
        'Bespoke-Nimble': (6, -10), 'Luna Decisions': (-46, -3), 'Jev': (-8, 7), 'GPT-5.6 Luna': (-6, 7), 'GPT-6 Sol': (4, -11)},
    1: {'Laya': (6, -3), 'BART': (6, 2), 'SemIf-2B': (6, 3), 'Decider': (6, -10), 'SemIf-4B': (-44, 4), 'CoPE': (-14, 6),
        'Bespoke-Nimble': (6, -10), 'Luna Decisions': (-44, -10), 'Jev': (-8, 7), 'GPT-5.6 Luna': (-6, 7), 'GPT-6 Sol': (-8, -11)},
}
for k, ax in enumerate(axes):
    for m in tb.eorder:
        a, b = tb.EFF.get((m, 'HateCheck', 'A')), tb.EFF.get((m, 'HateCheck', 'B'))
        fa, fbb = tb.cval(m, 'HateCheck', 'A', 'macro_f1'), tb.cval(m, 'HateCheck', 'B', 'macro_f1')
        xa, xb = (a['med'] * 1000, b['med'] * 1000) if k == 0 else (a['usd1k'], b['usd1k'])
        c = GROUP[m]
        ax.plot([xa, xb], [fa, fbb], color=c, lw=1.2, alpha=0.8, zorder=2)
        ax.scatter([xa], [fa], s=34, color=c, edgecolor='white', linewidth=1.2, zorder=3)
        ax.scatter([xb], [fbb], s=34, facecolor='white', edgecolor=c, linewidth=1.4, zorder=3)
        dx, dy = LOFF[k].get(m, (6, 0))
        ax.annotate(SHORT.get(m, m), (xa, fa), xytext=(dx, dy), textcoords='offset points', fontsize=7.2, color=INK)
    ax.set_xscale('log')
    ax.set_xlabel('Median latency per text (ms, log)' if k == 0 else 'Cost per 1K texts (USD, log)')
axes[0].set_ylabel('Macro-F1, HateCheck')
axes[0].set_title('(a) Quality and latency', loc='left', fontsize=9, color=INK)
axes[1].set_title('(b) Quality and cost', loc='left', fontsize=9, color=INK)
from matplotlib.lines import Line2D
h = [Line2D([], [], color=BLUE, marker='o', ls='-', label='Decision models'), Line2D([], [], color=ORANGE, marker='o', ls='-', label='CoPE, BART'),
     Line2D([], [], color=GREEN, marker='o', ls='-', label='Commercial LLMs'),
     Line2D([], [], color=MUTED, marker='o', ls='', label='Direct (A)'), Line2D([], [], color=MUTED, marker='o', mfc='white', ls='', label='Decomposed (B)')]
fig.legend(handles=h, loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.13), fontsize=7.5)
save(fig, 'quality-efficiency-all')

# ---------------------------------------------------------------- 2. policy contrast: detection vs adherence
order = sorted(tb.porder, key=lambda m: tb.PC[(m, 'overall')][2])
fig, ax = plt.subplots(figsize=(6.4, 3.4))
for i, m in enumerate(order):
    acc, cond, unc = tb.PC[(m, 'overall')]
    ax.plot([0, 100], [i, i], color=GRID, lw=0.6, zorder=1)
    ax.plot([100 * unc, 100 * acc], [i, i], color=MUTED, lw=1.2, zorder=2)
    ax.scatter(100 * acc, i, s=38, color=BLUE, edgecolor='white', linewidth=1.2, zorder=3)
    ax.scatter(100 * cond, i, s=38, color=ORANGE, marker='D', edgecolor='white', linewidth=1.0, zorder=4)
    ax.scatter(100 * unc, i, s=30, facecolor='white', edgecolor=INK, linewidth=1.2, zorder=5)
ax.set_yticks(range(len(order))); ax.set_yticklabels(order, color=INK)
ax.set_xlim(-3, 103); ax.set_xlabel('% of the 90 switch texts'); ax.grid(axis='y', visible=False)
h = [Line2D([], [], color=BLUE, marker='o', ls='', label='Labeled hate under P$_\\mathrm{in}$ (detection)'),
     Line2D([], [], color=ORANGE, marker='D', ls='', label='Switched, among those (adherence)'),
     Line2D([], [], color=INK, marker='o', mfc='white', ls='', label='Switched, all texts')]
ax.legend(handles=h, loc='lower center', bbox_to_anchor=(0.45, 1.0), ncol=3, fontsize=7.3)
save(fig, 'policy-detection-adherence')

# ---------------------------------------------------------------- 3. definition effects: changed predictions vs macro-F1 change
de = tb.de
fig, ax = plt.subplots(figsize=(6.0, 3.2))
pts = []
for m in tb.DEC + ['CoPE', 'GPT-5.6 Luna', 'GPT-6 Sol']:
    for ds in tb.DS:
        x = de[(de.model == m) & (de.dataset == ds)]
        d = x[x.metric == 'delta_macro_f1_pp']
        if not len(d): continue
        d = d.iloc[0]; ch = x[x.metric == 'changed_percent'].value.iloc[0]
        sig = tb.excl0(d.adj_low, d.adj_high)
        pts.append((m, ds, ch, d.value, sig))
for m, ds, ch, dv, sig in pts:
    ax.scatter(ch, dv, s=34, color=BLUE if sig else 'white', edgecolor=BLUE, linewidth=1.3, zorder=3)
ax.axhline(0, color=MUTED, lw=0.8, zorder=1)
for m, ds, ch, dv, sig in pts:
    if ch > 15 or abs(dv) > 6:
        off = {('Decider', 'HateCheck'): (-30, 7), ('SemIf-4B', 'MHS'): (4, 3)}.get((m, ds), (5, -3))
        ax.annotate(f'{SHORT.get(m, m)}, {ds}', (ch, dv), xytext=off, textcoords='offset points', fontsize=7, color=INK)
ax.set_xlabel('Predictions changed by the definition (%)'); ax.set_ylabel('Change in macro-F1 (points)')
h = [Line2D([], [], color=BLUE, marker='o', ls='', label='Adjusted interval excludes zero'),
     Line2D([], [], color=BLUE, marker='o', mfc='white', ls='', label='Inconclusive')]
ax.legend(handles=h, loc='upper left', fontsize=7.5)
save(fig, 'definition-flips')
print('figures ok')
