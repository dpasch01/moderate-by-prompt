import sys, re, os
IN = sys.argv[1]
sys.argv = [sys.argv[0], IN, 'none']
import pandas as pd
import tables as tb
from tables import T, N, f3, isnan
V = {}
for ds in tb.DS: V[f'nonhate_{ds}'] = f3(N['all_non_hate'][ds])
# generic max abs
gm = 0
for m in tb.ALL:
    for ds in tb.DS:
        src = tb.early if ds == 'HateXplain' else tb.main
        g, n0 = tb.cval(m, ds, 'generic_definition', 'macro_f1', src), tb.cval(m, ds, 'no_definition', 'macro_f1', src)
        if not (isnan(g) or isnan(n0)): gm = max(gm, abs(100 * (g - n0)))
V['gen_max'] = f'{gm:.1f}'
sh = {m: tb.tcm[(tb.tcm.model == m) & (tb.tcm.condition == 'benchmark_direct') & (tb.tcm.metric == 'offensive_to_hate_share')].value.iloc[0] for m in tb.DEC}
V['off_lo'], V['off_hi'] = f'{100*min(sh.values()):.0f}', f'{100*max(sh.values()):.0f}'
assert min(sh, key=sh.get) == 'Luna Decisions' and max(sh, key=sh.get) == 'Bespoke-Nimble'
c = N['defeff_counts']; V.update(de_gain=c['gain'], de_loss=c['loss'], de_inc=c['inc'])
a = N['ablation_counts']; V.update(ab_def_gain=a['C2-C1/main'][0], ab_def_loss=a['C2-C1/main'][1], ab_desc_gain=a['C3-C2/main'][0], ab_desc_loss=a['C3-C2/main'][1])
rho = {r['variant']: r['value'] for r in N['rho']}
V.update(rho_o1=f"{rho['original/P1']:.2f}"[1:], rho_o2=f"{rho['original/P2']:.2f}"[1:], rho_12=f"{rho['P1/P2']:.2f}"[1:])
d = N['decomp_counts']
V.update(dc_gain=d[('historical_primary30', 'gain')], dc_loss=d[('historical_primary30', 'loss')], dc_inc=d[('historical_primary30', 'inconclusive')])
V.update(dc_nd_gain=N['decomp_nondegenerate']['gain'], dc_nd_loss=N['decomp_nondegenerate']['loss'])
t = N['thresh_counts']
sumk = lambda c, i: t[f'{c}/primary'][i] + t[f'{c}/exploratory'][i]
V.update(th_aa=sumk('Astar-minus-A', 0), th_bb=sumk('Bstar-minus-B', 0), th_sa_gain=sumk('soft-Astar', 0), th_sa_loss=sumk('soft-Astar', 1),
         th_sb_gain=sumk('soft-Bstar', 0), th_sb_loss=sumk('soft-Bstar', 1))
rp = N['exp_replay']
V.update(replay_rows=f"{int(float(rp['replay_dataset_rows'])):,}", replay_ids=f"{int(float(rp['replay_eligible_ids'])):,}", replay_cap=f"{int(float(rp['replay_train_cap'])):,}")
cs = tb.costs
num = lambda x: pd.to_numeric(x, errors='coerce').sum()
def money(v): return f'{v:.2f}' if v >= 0.1 else f'{v:.3f}'
def ce(exp, model, met): return money(num(cs[(cs.experiment == exp) & (cs.model == model) & (cs.metric == met)].value))
V.update(cost_hist_jev=ce('main_experiments_historical_catalog', 'Jev', 'accounted_or_estimated_usd'),
         cost_hist_luna=ce('main_experiments_historical_catalog', 'GPT-5.6 Luna', 'accounted_or_estimated_usd'),
         cost_hist_sol=ce('main_experiments_historical_catalog', 'GPT-6 Sol', 'accounted_or_estimated_usd'),
         cost_inc_jev=ce('main_experiments_later_increment', 'Jev', 'new_accounted_usd'),
         cost_inc_luna=ce('main_experiments_later_increment', 'GPT-5.6 Luna', 'new_accounted_usd'),
         cost_inc_sol=ce('main_experiments_later_increment', 'GPT-6 Sol', 'new_accounted_usd'),
         cost_ld=money(num(cs[(cs.experiment == 'Luna_Decisions_main') & (cs.metric == 'known_charge_usd')].value)),
         cost_sol_nodef=ce('Sol_no_definition', 'GPT-6 Sol', 'spent_or_reserved_usd'),
         cost_par_jev=ce('paraphrases', 'Jev', 'recorded_usd'), cost_par_ld=ce('paraphrases', 'Luna Decisions', 'recorded_usd'),
         cost_par_luna=ce('paraphrases', 'GPT-5.6 Luna', 'recorded_usd'), cost_par_sol=ce('paraphrases', 'GPT-6 Sol', 'recorded_usd'),
         cost_bstar_jev=ce('Bstar_validation', 'Jev', 'recorded_cost_usd'), cost_bstar_ld=ce('Bstar_validation', 'Luna Decisions', 'recorded_cost_usd'))
src = open('SUPPLEMENT.tmpl.md').read()
def sub_t(m): return T[m.group(1)]
def sub_n(m): return str(V[m.group(1)])
out = re.sub(r'\{\{T:([a-zA-Z0-9_]+)\}\}', sub_t, src)
out = re.sub(r'\{\{N:([a-zA-Z0-9_]+)\}\}', sub_n, out)
assert '{{' not in out, re.findall(r'\{\{[^}]*\}\}', out)
open('out/SUPPLEMENT.md', 'w').write(out)
print('rendered', len(out)); print(V)
