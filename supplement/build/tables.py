"""Builds Markdown tables for the supplementary report from the exported CSVs."""
import math, os, sys
import pandas as pd

IN = sys.argv[1] if len(sys.argv) > 1 else '.'
def rd(f): return pd.read_csv(os.path.join(IN, f), low_memory=False)

MINUS = '−'
DEC = ['Jev', 'Laya', 'Decider', 'SemIf-2B', 'SemIf-4B', 'Bespoke-Nimble', 'Luna Decisions']
OTH = ['CoPE', 'BART', 'GPT-5.6 Luna', 'GPT-6 Sol']
SUP = ['TF-IDF+LR', 'DistilBERT']
ALL = DEC + OTH
DS = ['Dynamic', 'MHS', 'HateXplain', 'HateCheck']

def isnan(v):
    try: return v is None or (isinstance(v, float) and math.isnan(v))
    except Exception: return False

def f3(v):
    if isnan(v): return '–'
    s = f'{v:.3f}'
    return s[1:] if s.startswith('0') else s

def pp(v, nd=1, sig=False):
    if isnan(v): return '–'
    r = round(v, nd)
    s = f'{abs(r):.{nd}f}'
    if v > 0: s = '+' + s
    elif v < 0: s = MINUS + s
    return f'**{s}**' if sig else s

def pct(v, nd=0):
    if isnan(v): return '–'
    return f'{v:.{nd}f}'

def ci(lo, hi, nd=1):
    if isnan(lo) or isnan(hi): return '–'
    return f'[{pp(lo, nd)}, {pp(hi, nd)}]'

def excl0(lo, hi):
    return (not isnan(lo)) and (not isnan(hi)) and (lo > 0 or hi < 0)

def md(header, rows, align=None):
    align = align or (['l'] + ['r'] * (len(header) - 1))
    sep = ['---:' if a == 'r' else (':---:' if a == 'c' else '---') for a in align]
    out = ['| ' + ' | '.join(header) + ' |', '| ' + ' | '.join(sep) + ' |']
    out += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out)

T = {}   # name -> markdown
N = {}   # name -> numbers for prose checks

# ---------------------------------------------------------------- classification
cl = rd('classification.csv')
main = cl[cl.cohort == 'main']
def cval(model, ds, cond, metric, src=main):
    x = src[(src.model == model) & (src.dataset == ds) & (src.condition == cond) & (src.metric == metric)]
    return x.value.iloc[0] if len(x) else float('nan')

early = cl[cl.cohort == 'early_1000']
for ds in DS:
    rows = []
    for m in ALL:
        gen = cval(m, ds, 'generic_definition', 'macro_f1')
        mark = ''
        if ds == 'HateXplain' and isnan(gen):
            g2 = cval(m, ds, 'generic_definition', 'macro_f1', early)
            if not isnan(g2): gen, mark = g2, '†'
        rows.append([m, f3(cval(m, ds, 'no_definition', 'macro_f1')), f3(gen) + mark,
                     f3(cval(m, ds, 'benchmark_direct', 'macro_f1')),
                     f3(cval(m, ds, 'benchmark_direct', 'hate_precision')),
                     f3(cval(m, ds, 'benchmark_direct', 'hate_recall')),
                     f3(cval(m, ds, 'A', 'macro_f1')), f3(cval(m, ds, 'B', 'macro_f1'))])
    for m in SUP:
        x = cl[(cl.cohort == 'binary_transfer') & (cl.model == m) & (cl.dataset == ds) & (cl.metric == 'macro_f1')]
        # in-domain value only (trained on same dataset) is in transfer.csv; here report nothing
    T[f'class_{ds}'] = md(['Model', 'No def.', 'Generic', 'Bench.', 'Bench. P', 'Bench. R', 'A', 'B'], rows)

# all-non-hate baseline from decomposition file
dc = rd('decomposition_cells.csv')
N['all_non_hate'] = {ds: dc[(dc.dataset == ds) & (dc.metric == 'all_non_hate_macro_f1')].value.iloc[0] for ds in DS}

# ---------------------------------------------------------------- generic definition effect
rows = []
for m in ALL:
    r = [m]
    for ds in DS:
        src = early if ds == 'HateXplain' else main
        g = cval(m, ds, 'generic_definition', 'macro_f1', src)
        n0 = cval(m, ds, 'no_definition', 'macro_f1', src)
        r.append(pp(100 * (g - n0)) if not (isnan(g) or isnan(n0)) else '–')
    if any(c != '–' for c in r[1:]): rows.append(r)
T['generic'] = md(['Model'] + DS, rows)

# ---------------------------------------------------------------- three-class
tc = rd('three_class.csv')
tcm = tc[tc.cohort == 'main']
rows = []
for m in ALL + SUP:
    x = tcm[(tcm.model == m) & (tcm.condition == 'benchmark_direct')]
    if not len(x): continue
    g = lambda met, cls=None: (x[(x.metric == met) & ((x.class_label == cls) if cls else x.class_label.isna())].value.iloc[0]
                               if len(x[(x.metric == met) & ((x.class_label == cls) if cls else x.class_label.isna())]) else float('nan'))
    rows.append([m, f3(g('macro_f1')), f3(g('f1', 'hatespeech')), f3(g('f1', 'offensive')), f3(g('f1', 'normal')),
                 f3(g('recall', 'hatespeech')), f3(g('recall', 'offensive')),
                 pct(100 * g('offensive_to_hate_share')), pct(100 * g('offensive_to_normal_share'))])
T['three'] = md(['Model', 'Macro-F1', 'F1 hate', 'F1 off.', 'F1 normal', 'R hate', 'R off.', 'Off.→hate %', 'Off.→normal %'], rows)

# ---------------------------------------------------------------- transfer
tr = rd('transfer.csv')
tb = tr[(tr.cohort == 'binary_transfer') & (tr.metric == 'macro_f1')]
rows = []
for m in SUP:
    for src in ['Dynamic', 'MHS', 'HateXplain']:
        r = [m if src == 'Dynamic' else '', src]
        for ds in DS:
            x = tb[(tb.model == m) & (tb.trained_on == src) & (tb.dataset == ds)]
            v = x.value.iloc[0] if len(x) else float('nan')
            s = f3(v)
            r.append(f'**{s}**' if ds == src else s)
        rows.append(r)
T['transfer'] = md(['Classifier', 'Trained on'] + DS, rows, ['l', 'l', 'r', 'r', 'r', 'r'])
hp = tr[(tr.cohort == 'binary_transfer')].drop_duplicates(['model', 'trained_on'])
rows = []
for _, r in hp.sort_values(['model', 'trained_on']).iterrows():
    if r.model == 'DistilBERT':
        rows.append([r.model, r.trained_on, f'epoch {int(r.selected_epoch)}', f3(r.selected_source_validation_macro_f1)])
    else:
        rows.append([r.model, r.trained_on, f'C = {r.selected_C:g}', f3(r.selected_source_validation_macro_f1)])
T['transfer_hp'] = md(['Classifier', 'Trained on', 'Selected', 'Validation macro-F1'], rows, ['l', 'l', 'l', 'r'])
tn = tr[(tr.cohort == 'native') & (tr.metric == 'macro_f1')]
N['transfer_native'] = tn[['model', 'task', 'trained_on', 'value']].to_dict('records')

# ---------------------------------------------------------------- attributes
at = rd('attributes.csv')
def amf(m, task, cond='benchmark_direct'):
    x = at[(at.model == m) & (at.task == task) & (at.condition == cond) & (at.metric == 'macro_f1')]
    return x.value.iloc[0] if len(x) else float('nan')
rows = []
for m in ALL + SUP:
    vals = [amf(m, 'hatecheck_target'), amf(m, 'hatecheck_direction'), amf(m, 'dynamic_type')]
    vals0 = [amf(m, 'hatecheck_target', 'no_definition'), amf(m, 'hatecheck_direction', 'no_definition'), amf(m, 'dynamic_type', 'no_definition')]
    if all(isnan(v) for v in vals + vals0): continue
    rows.append([m] + [f3(v) for v in vals0] + [f3(v) for v in vals])
T['attr'] = md(['Model', 'Group, no def.', 'Direction, no def.', 'Conduct, no def.', 'Group, Bench.', 'Direction, Bench.', 'Conduct, Bench.'], rows)
# conduct per class F1 under benchmark-direct
cls = ['none', 'animosity', 'derogation', 'dehumanization', 'threatening', 'support']
rows = []
for m in ALL + SUP:
    x = at[(at.model == m) & (at.task == 'dynamic_type') & (at.condition == 'benchmark_direct') & (at.metric == 'f1')]
    if not len(x): continue
    rows.append([m] + [f3(x[x.class_label == c].value.iloc[0]) if len(x[x.class_label == c]) else '–' for c in cls])
sup = at[(at.task == 'dynamic_type') & (at.metric == 'support') & (at.condition == 'benchmark_direct')].drop_duplicates('class_label')
supd = {r.class_label: int(r.value) for _, r in sup.iterrows()}
tot = sum(supd.values())
T['conduct'] = md(['Model'] + [f'{c} ({100*supd.get(c,0)/tot:.1f}%)' for c in cls], rows)
grp = ['women', 'trans people', 'gay people', 'black people', 'disabled people', 'Muslims', 'immigrants']
rows = []
for m in ALL + SUP:
    x = at[(at.model == m) & (at.task == 'hatecheck_target') & (at.condition == 'benchmark_direct') & (at.metric == 'f1')]
    if not len(x): continue
    rows.append([m] + [f3(x[x.class_label == c].value.iloc[0]) if len(x[x.class_label == c]) else '–' for c in grp])
T['group'] = md(['Model'] + grp, rows)

# ---------------------------------------------------------------- definition effects
de = rd('definition_effects.csv')
rows = []
cnt = {'gain': 0, 'loss': 0, 'inc': 0}
for m in DEC + ['CoPE', 'GPT-5.6 Luna', 'GPT-6 Sol']:
    for ds in DS:
        x = de[(de.model == m) & (de.dataset == ds)]
        d = x[x.metric == 'delta_macro_f1_pp']
        if not len(d): continue
        d = d.iloc[0]
        g = lambda met: x[x.metric == met].value.iloc[0] if len(x[x.metric == met]) else float('nan')
        intro = g('introduced_percent')
        if isnan(intro): intro = g('broken_percent')
        s = excl0(d.adj_low, d.adj_high)
        if d.family == 'family2':
            cnt['gain' if s and d.value > 0 else ('loss' if s else 'inc')] += 1
        n0 = x[(x.metric == 'macro_f1') & (x.condition == 'no_definition')].value
        n1 = x[(x.metric == 'macro_f1') & (x.condition == 'benchmark_direct')].value
        rows.append([m if ds == 'Dynamic' else '', ds, f3(n0.iloc[0]) if len(n0) else '–', f3(n1.iloc[0]) if len(n1) else '–',
                     pp(d.value, sig=s), ci(d.adj_low, d.adj_high), pct(g('changed_percent'), 1),
                     pct(g('corrected_percent'), 1), pct(intro, 1), int(d.family_size)])
T['defeff'] = md(['Model', 'Dataset', 'No def.', 'Bench.', 'ΔF1', 'Adjusted 95% CI', 'Changed %', 'Corrected %', 'Broken %', 'Family'],
                 rows, ['l', 'l'] + ['r'] * 8)
N['defeff_counts'] = cnt

# ---------------------------------------------------------------- ablation
ab = rd('ablation.csv')
abc = ab[ab.metric == 'delta_macro_f1_pp']
rows = []
cnt = {}
for m in [x for x in DEC + OTH if x in set(abc.model)]:
    for ds in DS:
        r = [m if ds == 'Dynamic' else '', ds]
        for c in ['C2-C1', 'C3-C2']:
            x = abc[(abc.model == m) & (abc.dataset == ds) & (abc.contrast == c)]
            if not len(x): r += ['–', '–']; continue
            x = x.iloc[0]; s = excl0(x.adj_low, x.adj_high)
            k = (c, 'cope' if m == 'CoPE' else 'main')
            cnt.setdefault(k, [0, 0, 0])
            cnt[k][0 if (s and x.value > 0) else (1 if s else 2)] += 1
            r += [pp(x.value, sig=s), ci(x.adj_low, x.adj_high)]
        # absolute macro-F1 on three-way intersection
        y = ab[(ab.model == m) & (ab.dataset == ds) & (ab.metric == 'macro_f1') & (ab.scope == 'three_way_valid_intersection')]
        vv = [y[y.variant == v].value.iloc[0] if len(y[y.variant == v]) else float('nan') for v in ['label_only', 'plus_definition', 'benchmark_direct']]
        rows.append(r[:2] + [f3(v) for v in vv] + r[2:])
fam = abc[['model', 'family_size']].drop_duplicates()
T['ablation'] = md(['Model', 'Dataset', 'C1', 'C2', 'C3', 'C2−C1', 'Adjusted CI', 'C3−C2', 'Adjusted CI'], rows, ['l', 'l'] + ['r'] * 7)
N['ablation_counts'] = {f'{k[0]}/{k[1]}': v for k, v in cnt.items()}
N['ablation_fam'] = fam.to_dict('records')

# ---------------------------------------------------------------- robustness
rb = rd('robustness.csv')
rows = []
order = ['Laya', 'Decider', 'SemIf-2B', 'SemIf-4B', 'Bespoke-Nimble', 'Jev', 'Luna Decisions', 'CoPE', 'GPT-5.6 Luna', 'GPT-6 Sol']
for m in order:
    r = [m]
    orig = rb[(rb.model == m) & (rb.metric == 'macro_f1') & (rb.variant == 'original')]
    r.append(f3(orig.value.iloc[0]) if len(orig) else '–')
    for c in ['neutral-original', 'reversed-original', 'P1-original', 'P2-original']:
        x = rb[(rb.model == m) & (rb.variant == c.split('-')[0])]
        d = x[x.metric == 'delta_macro_f1_pp']
        if not len(d): r += ['–', '–']; continue
        d = d.iloc[0]
        ch = x[x.metric == 'changed_percent'].value.iloc[0]
        r += [pp(d.value, sig=excl0(d.adj_low, d.adj_high)), pct(ch, 1)]
    rows.append(r)
T['robust'] = md(['Model', 'Orig.', 'A/B Δ', 'A/B chg. %', 'Rev. Δ', 'Rev. chg. %', 'P1 Δ', 'P1 chg. %', 'P2 Δ', 'P2 chg. %'], rows)
rho = rb[rb.metric == 'spearman_rho'][['variant', 'value']]
N['rho'] = rho.to_dict('records')
N['robust_fam'] = rb[rb.metric == 'delta_macro_f1_pp'][['study', 'family_size']].drop_duplicates().to_dict('records')
# corrected/introduced fp/fn for robustness
rows = []
for m in order:
    for c, lab in [('neutral-original', 'A/B'), ('reversed-original', 'Rev.'), ('P1-original', 'P1'), ('P2-original', 'P2')]:
        x = rb[(rb.model == m) & (rb.variant == c.split('-')[0])]
        if not len(x[x.metric == 'changed_count']): continue
        g = lambda met: int(x[x.metric == met].value.iloc[0])
        rows.append([m, lab, g('changed_count'), g('corrected_fp_count'), g('corrected_fn_count'), g('introduced_fp_count'), g('introduced_fn_count')])
T['robust_flips'] = md(['Model', 'Variant', 'Changed', 'Corr. FP', 'Corr. FN', 'Intr. FP', 'Intr. FN'], rows, ['l', 'l'] + ['r'] * 5)


# ================================================================ PART 2
# ---------------------------------------------------------------- decomposition cells
rows = []
dd = dc[dc.metric == 'delta_macro_f1_pp']
dorder = ['Jev', 'Laya', 'Decider', 'SemIf-2B', 'SemIf-4B', 'Bespoke-Nimble', 'Luna Decisions', 'CoPE', 'BART', 'GPT-5.6 Luna', 'GPT-6 Sol']
for ds in DS:
    for m in dorder:
        x = dd[(dd.model == m) & (dd.dataset == ds)]
        if not len(x): continue
        x = x.iloc[0]
        y = dc[(dc.model == m) & (dc.dataset == ds)]
        g = lambda met: y[y.metric == met].value.iloc[0] if len(y[y.metric == met]) else float('nan')
        flag = '§' if x.excluded_degenerate_baseline else ''
        rows.append([m, ds, f'{int(x.n):,}', f3(x.reference_macro_f1), f3(x.comparison_macro_f1),
                     pp(x.value, sig=excl0(x.adj_low, x.adj_high)) + flag, ci(x.adj_low, x.adj_high),
                     pp(g('delta_hate_precision_pp')), pp(g('delta_hate_recall_pp'))])
T['decomp'] = md(['Model', 'Dataset', 'N', 'A', 'B', 'B−A', 'Adjusted 95% CI', 'ΔP', 'ΔR'], rows, ['l', 'l'] + ['r'] * 7)
N['decomp_counts'] = dd.groupby(['family', 'decision']).size().to_dict()
nd = dd[(dd.family == 'historical_primary30') & (~dd.excluded_degenerate_baseline.astype(bool))]
N['decomp_nondegenerate'] = nd.decision.value_counts().to_dict()

# ---------------------------------------------------------------- threshold control
th = rd('threshold_control.csv')
POST = 'post-hoc complete-case sensitivity (199 development outputs)'
def thsel(m, ds):
    y = th[(th.model == m) & (th.dataset == ds)]
    if (y.analysis_mode == POST).any(): return y[y.analysis_mode == POST], True
    return y, False
torder = ['Laya', 'SemIf-4B', 'Jev', 'Luna Decisions', 'Decider', 'SemIf-2B', 'Bespoke-Nimble', 'BART']
rows, rows2 = [], []
tc_cnt = {}
for m in torder:
    for ds in ['Dynamic', 'MHS', 'HateXplain']:
        y, post = thsel(m, ds)
        fam = y.family.iloc[0]
        mf = lambda c: y[(y.metric == 'macro_f1') & (y.condition == c)].value.iloc[0]
        def con(c):
            z = y[(y.metric == 'delta_macro_f1_pp') & (y.contrast == c)]
            if not len(z): return '–'
            z = z.iloc[0]; s = excl0(z.adj_low, z.adj_high)
            k = (c, fam); tc_cnt.setdefault(k, [0, 0, 0]); tc_cnt[k][0 if (s and z.value > 0) else (1 if s else 2)] += 1
            return pp(z.value, sig=s)
        lab = (m if ds == 'Dynamic' else '')
        rows.append([lab, ds + ('§' if post else ''), 'P' if fam == 'primary' else 'E', f3(mf('A')), f3(mf('B')), f3(mf('Astar')), f3(mf('Bstar')), f3(mf('soft')),
                     con('Astar-minus-A'), con('Bstar-minus-B'), con('soft-Astar'), con('soft-Bstar')])
        t = y[y.metric == 'selected_threshold']; v = y[y.metric == 'validation_macro_f1']
        ta = t[t.condition == 'Astar'].value.iloc[0]
        tb = t[t.condition == 'Bstar'].sort_values('component', key=lambda s: s.map({'scope': 0, 'targeting': 0, 'intentional': 1, 'abuse': 1}))
        ts = t[t.condition == 'soft'].value.iloc[0]
        comps = ', '.join(f'{r.component} {r.value:.3f}' for _, r in tb.iterrows())
        vv = lambda c: v[v.condition == c].value.iloc[0] if len(v[v.condition == c]) else float('nan')
        rows2.append([lab, ds + ('§' if post else ''), f'{ta:.3f}', comps, f'{ts:.3f}', f3(vv('Astar')), f3(vv('Bstar')), f3(vv('soft'))])
T['thresh'] = md(['Model', 'Dataset', 'Fam.', 'A', 'B', 'A*', 'B*', 'Soft', 'A*−A', 'B*−B', 'Soft−A*', 'Soft−B*'], rows, ['l', 'l', 'c'] + ['r'] * 9)
T['thresh_sel'] = md(['Model', 'Dataset', 'A* threshold', 'B* thresholds', 'Soft threshold', 'Val. A*', 'Val. B*', 'Val. soft'], rows2, ['l', 'l', 'r', 'l', 'r', 'r', 'r', 'r'])
N['thresh_counts'] = {f'{k[0]}/{k[1]}': v for k, v in tc_cnt.items()}

# ---------------------------------------------------------------- corrected pairs
cp = rd('corrected_pairs.csv')
rows = []
for m in dorder:
    x = cp[cp.model == m]
    if not len(x): continue
    rows.append([m, len(x), int((x.all_components_correct == True).sum()), int((x.all_components_correct == False).sum()),
                 int(x.all_components_correct.isna().sum()), int((x.A == 'hate').sum()), int((x.A == 'non-hate').sum())])
rows.append(['Total', len(cp), int((cp.all_components_correct == True).sum()), int((cp.all_components_correct == False).sum()),
             int(cp.all_components_correct.isna().sum()), int((cp.A == 'hate').sum()), int((cp.A == 'non-hate').sum())])
T['corrected'] = md(['Model', 'Corrected pairs', 'All components correct', 'Some component wrong', 'Unresolved', 'FP corrected', 'FN corrected'], rows)
N['corrected_by_ds'] = cp.groupby('dataset').size().to_dict()

# ---------------------------------------------------------------- refusals
rf = rd('refusals.csv')
cov = rf[rf.record_type == 'coverage']
rows = []
for ds in DS:
    for cond in ['benchmark_direct', 'no_definition', 'A', 'B']:
        x = cov[(cov.dataset == ds) & (cov.condition == cond)]
        if not len(x): continue
        g = lambda met: x[x.metric == met].value.iloc[0] if len(x[x.metric == met]) else float('nan')
        rows.append([ds, {'benchmark_direct': 'Bench.', 'no_definition': 'No def.'}.get(cond, cond), f'{int(g("requested")):,}', f'{int(g("refused")):,}' if not isnan(g('refused')) else '–'])
T['ref_cov'] = md(['Dataset', 'Condition', 'Requested', 'Refusals'], rows, ['l', 'l', 'r', 'r'])
N['ref_cov_metrics'] = sorted(cov.metric.unique().tolist())
sc = rf[rf.record_type == 'sensitivity_contrast']
rows = []
for _, r in sc.iterrows():
    rows.append([r.dataset, r.scenario.replace('refusal_as_wrong_gold_opposite', 'as error').replace('refusal_as_hate', 'as hate').replace('exclude', 'excluded'),
                 f3(r.left_f1), f3(r.right_f1), pp(r.value, sig=bool(r.significant)), ci(r.adj_low, r.adj_high)])
T['ref_sens'] = md(['Dataset', 'Refusals', 'A', 'B', 'B−A', 'Adjusted 95% CI'], rows, ['l', 'l', 'r', 'r', 'r', 'r'])
N['ref_sens_cols'] = sc[['dataset', 'scenario', 'contrast', 'refused_in_either_A_B', 'significance_changed']].to_dict('records')


# ================================================================ PART 3
# ---------------------------------------------------------------- efficiency
ef = rd('efficiency.csv')
GPU_USD_H = 0.20
LD_BILL = {'A': '04', 'B': '05'}
costs = rd('costs.csv')
def ld_cost(ds, cond):
    cell = f"{LD_BILL[cond]}/{ds}/evaluation"
    x = costs[(costs.experiment == 'Luna_Decisions_main') & (costs.billing_cell == cell)]
    g = lambda met: float(x[x.metric == met].value.iloc[0])
    return g('known_charge_usd') / g('attempted') * 1000
PRI = {'HateCheck': ['hatecheck_decomposition_3728', 'decomposition_additional_original_population', 'shared_population_fresh_attempts_including_refusals'],
       'other': ['decomposition_additional_original_population', 'corrected_validation_common800', 'sol_common800', 'shared_population_fresh_attempts_including_refusals']}
def first(x, mets):
    for m in mets:
        y = x[x.metric == m].value
        if len(y) and not isnan(y.iloc[0]): return float(y.iloc[0])
    return float('nan')
def eff(m, ds, cond):
    for co in PRI['HateCheck' if ds == 'HateCheck' else 'other']:
        x = ef[(ef.model == m) & (ef.dataset == ds) & (ef.condition == cond) & (ef.cohort == co)]
        if len(x): break
    else: return None
    n = first(x, ['n', 'requested', 'complete', 'attempted'])
    if isnan(n) and co == 'hatecheck_decomposition_3728': n = 3728.0
    r = dict(cohort=co, n=n,
             med=first(x, ['median_wall_seconds', 'wall_median_seconds', 'median_complete_worker_seconds']),
             p95=first(x, ['p95_wall_seconds', 'wall_p95_seconds', 'p95_complete_worker_seconds']),
             tput=first(x, ['observed_complete_posts_per_second', 'observed_posts_per_second', 'worker_service_posts_per_second', 'complete_posts_per_wall_second', 'complete_posts_per_second']),
             usd=first(x, ['accounted_usd', 'known_accounted_usd']), conc=first(x, ['concurrency']))
    if m == 'Luna Decisions': r['usd1k'] = ld_cost(ds, cond); r['hosted'] = True
    elif not isnan(r['usd']): r['usd1k'] = r['usd'] / n * 1000; r['hosted'] = True
    else:
        r['hosted'] = False
        r['usd1k'] = GPU_USD_H / 3600 / r['tput'] * 1000 if not isnan(r['tput']) else float('nan')
    return r
EFF = {}
for ds in DS:
    for m in ALL:
        for cond in 'AB':
            r = eff(m, ds, cond)
            if r: EFF[(m, ds, cond)] = r
def ms(v): return '–' if isnan(v) else f'{1000*v:,.0f}'
def usd(v, hosted):
    if isnan(v): return '–'
    s = f'{v:.3f}' if v >= 0.001 else f'{v:.4f}'
    return s if hosted else s + '*'
eorder = ['Laya', 'BART', 'SemIf-2B', 'Decider', 'SemIf-4B', 'CoPE', 'Bespoke-Nimble', 'Luna Decisions', 'Jev', 'GPT-5.6 Luna', 'GPT-6 Sol']
rows = []
for m in eorder:
    a, b = EFF.get((m, 'HateCheck', 'A')), EFF.get((m, 'HateCheck', 'B'))
    if not a: continue
    fa, fb = cval(m, 'HateCheck', 'A', 'macro_f1'), cval(m, 'HateCheck', 'B', 'macro_f1')
    dl = 100 * (b['med'] / a['med'] - 1); dcst = 100 * (b['usd1k'] / a['usd1k'] - 1)
    rows.append([m, f3(fa), f3(fb), ms(a['med']), ms(a['p95']), ms(b['med']), ms(b['p95']), pp(dl, 0) + '%',
                 f"{a['tput']:.1f}" if not isnan(a['tput']) else '–', usd(a['usd1k'], a['hosted']), usd(b['usd1k'], b['hosted']), pp(dcst, 0) + '%'])
T['eff_hc'] = md(['Model', 'F1 A', 'F1 B', 'A med.', 'A p95', 'B med.', 'B p95', 'Δ med.', 'Texts/s A', '$/1K A', '$/1K B', 'Δ cost'], rows)
rows = []
for ds in ['Dynamic', 'MHS', 'HateXplain']:
    for m in eorder:
        a, b = EFF.get((m, ds, 'A')), EFF.get((m, ds, 'B'))
        if not a or not b: continue
        lab = {'decomposition_additional_original_population': 'full', 'corrected_validation_common800': '800', 'sol_common800': '800',
               'shared_population_fresh_attempts_including_refusals': 'full'}[a['cohort']]
        rows.append([ds if m == eorder[0] or not rows or rows[-1][0] != ds and False else '', m, lab, ms(a['med']), ms(b['med']), pp(100 * (b['med'] / a['med'] - 1), 0) + '%',
                     usd(a['usd1k'], a['hosted']), usd(b['usd1k'], b['hosted']), pp(100 * (b['usd1k'] / a['usd1k'] - 1), 0) + '%'])
# set dataset label on first row of each block
last = None
for r, ds in zip(rows, [d for d in ['Dynamic', 'MHS', 'HateXplain'] for m in eorder if EFF.get((m, d, 'A')) and EFF.get((m, d, 'B'))]):
    r[0] = ds if ds != last else ''; last = ds
T['eff_other'] = md(['Dataset', 'Model', 'Texts', 'A med.', 'B med.', 'Δ med.', '$/1K A', '$/1K B', 'Δ cost'], rows, ['l', 'l'] + ['r'] * 7)
N['EFF'] = EFF

# ---------------------------------------------------------------- cascades
ca = rd('cascades.csv'); cc = rd('cascade_contrasts.csv')
fz = ca[ca.frozen_operating_point == True]
pairs = [('Laya', 'Jev'), ('Laya', 'Luna Decisions'), ('Laya', 'GPT-5.6 Luna'), ('Laya', 'GPT-6 Sol'), ('Jev', 'Luna Decisions'), ('Jev', 'GPT-5.6 Luna'), ('Jev', 'GPT-6 Sol')]
short = {'GPT-5.6 Luna': 'Luna', 'GPT-6 Sol': 'Sol', 'Luna Decisions': 'Luna Dec.'}
rows = []
for f_, s_ in pairs:
    for ds in DS:
        z = fz[(fz.model == f_) & (fz.second_model == s_) & (fz.dataset == ds)].iloc[0]
        k = cc[(cc.model == f_) & (cc.second_model == s_) & (cc.dataset == ds)]
        def kd(ref):
            y = k[k.reference == ref]
            if not len(y): return '–', None
            y = y.iloc[0]; return pp(y.value, sig=excl0(y.adj_low, y.adj_high)), y
        v1, _ = kd(f_); v2, y2 = kd(s_); vr, _ = kd('random')
        tost = '–'
        if y2 is not None and not isnan(y2.tost_ci90_low):
            eq = '≤1' if y2.equivalent_1pp else ('≤2' if y2.equivalent_2pp else 'no')
            tost = f'[{pp(y2.tost_ci90_low, 2)}, {pp(y2.tost_ci90_high, 2)}] {eq}'
        rows.append([f'{f_}→{short.get(s_, s_)}' if ds == 'Dynamic' else '', ds, f'{int(round(100*z.referral_rate))}%', f3(z.value), v1, v2, vr, tost,
                     f'{z.hosted_cost_per_1000_usd:.3f}'])
T['cascade'] = md(['Cascade', 'Dataset', 'Referred', 'Macro-F1', 'vs first', 'vs second', 'vs random', 'TOST 90% CI vs second', 'Hosted $/1K'], rows, ['l', 'l'] + ['r'] * 7)
N['cascade_tost'] = cc[cc.equivalent_1pp.notna()][['model', 'second_model', 'dataset', 'referral_rate', 'equivalent_1pp', 'equivalent_2pp', 'tost_ci90_low', 'tost_ci90_high']].to_dict('records')
# second-model standalone
# routing (earlier cohort, A prompt)
ro = rd('routing.csv')
rows = []
for ds in ['Dynamic', 'MHS', 'HateXplain']:
    y = ro[(ro.dataset == ds) & (ro.second_model == 'GPT-6 Sol')]
    for rr in sorted(y.referral_rate.unique()):
        z = y[y.referral_rate == rr]; g = lambda met: z[z.metric == met].value.iloc[0]
        rows.append([ds if rr == 0 else '', f'{int(round(100*rr))}%', f3(g('macro_f1')), f3(g('hate_precision')), f3(g('hate_recall')), int(g('corrected')), int(g('introduced')), f"{g('estimated_hosted_usd'):.3f}"])
T['routing'] = md(['Dataset', 'Referred', 'Macro-F1', 'P', 'R', 'Corrected', 'Introduced', 'Hosted $ (800 texts)'], rows, ['l'] + ['r'] * 7)

# ---------------------------------------------------------------- audit
pa = rd('audit/pairwise_agreement.csv')
pa = pa[pa.uncertainty_treatment == 'mutually_definite'].copy()
PMAP = {'P1': 'Dynamic', 'P2': 'MHS', 'P3': 'HateXplain', 'P4': 'HateCheck'}
def norm_field(f):
    f = f.replace('audit/', '').replace('audit_', '')
    parts = f.split('/')
    if parts[0] in PMAP and len(parts) == 2: return (PMAP[parts[0]], 'policy')
    if parts[0] in PMAP and parts[1] == 'component': return (PMAP[parts[0]], parts[2])
    if parts[0] == 'policy' and len(parts) == 2: return (parts[1], 'policy')
    if parts[0] == 'component': return (PMAP[parts[1]], parts[2])
    return ('All', parts[0].replace('components', 'all components'))
pa['ds'], pa['fld'] = zip(*pa.field.map(norm_field))
RATERS = [('expert/opus', 'Expert–Opus'), ('expert/gemini', 'Expert–Gemini'), ('opus/gemini', 'Opus–Gemini')]
keys = [('All', 'policy'), ('All', 'all components')] + [(d, f) for d in DS for f in (['policy', 'scope', 'intentional', 'conduct'] if d == 'Dynamic' else ['policy', 'targeting', 'abuse'])]
rows = []
for d, f in keys:
    r = [d if (f == 'policy' or d == 'All') else '', f]
    for rk, _ in RATERS:
        y = pa[(pa.raters == rk) & (pa.ds == d) & (pa.fld == f)]
        a = y[y.metric == 'agreement']; k = y[y.metric == 'cohen_kappa']
        if not len(a): r.append('–'); continue
        kk = k.value.iloc[0] if len(k) else float('nan')
        r.append(f"{int(a.agree_n.iloc[0])}/{int(a.n.iloc[0])}" + ('' if isnan(kk) else f" (κ {kk:.2f})"))
    rows.append(r)
T['audit_pair'] = md(['Dataset', 'Judgment'] + [lab for _, lab in RATERS], rows, ['l', 'l', 'r', 'r', 'r'])
ma = rd('audit/model_agreement.csv')
rows = []
for m in ALL:
    r = [m]
    for ref in ['majority', 'expert']:
        y = ma[(ma.model == m) & (ma.reference == ref)]
        for met in ['agree_pct', 'conflicts_pct', 'comp_pct']:
            z = y[y.metric == met]
            if not len(z): r.append('–'); continue
            z = z.iloc[0]
            r.append(f'{z.value:.0f} ({z.ci_low:.0f}–{z.ci_high:.0f})')
    rows.append(r)
T['audit_models'] = md(['Model', 'Agree (maj.)', 'Conflicts (maj.)', 'Comp. (maj.)', 'Agree (expert)', 'Conflicts (expert)', 'Comp. (expert)'], rows)
N['ma_refs'] = ma.reference.unique().tolist(); N['ma_metrics'] = ma.metric.unique().tolist()
N['ma_n'] = ma[['reference', 'metric', 'n']].drop_duplicates().to_dict('records')
cr = rd('audit/conflict_rates.csv')
rows = []
for ds in DS:
    r = [ds]
    for ref in ['majority', 'expert']:
        for w in ['raw', 'reweighted']:
            z = cr[(cr.dataset == ds) & (cr.reference == ref) & (cr.weighting == w)]
            if not len(z): r.append('–'); continue
            z = z.iloc[0]
            r.append((f'{int(z.k)}/{int(z.n)} = ' if w == 'raw' else '') + f'{z.value:.0f} ({z.ci_low:.0f}–{z.ci_high:.0f})')
    rows.append(r)
T['audit_conf'] = md(['Dataset', 'Majority, raw', 'Majority, reweighted', 'Expert, raw', 'Expert, reweighted'], rows)
cw = rd('audit/conflict_wilson.csv')
N['cw'] = cw[['model', 'k', 'n', 'ci_low', 'ci_high', 'reference', 'status']].to_dict('records')
dcz = rd('audit/disputed_cases.csv')
rows = []
for _, r in dcz.iterrows():
    rows.append([r.item_id, r.dataset_label, r.expert_policy, r.opus_policy, r.gemini_policy, r.reference_policy, r.reference_components.replace(';', '; ')])
T['disputed'] = md(['Item', 'Dataset label', 'Expert', 'Opus', 'Gemini', 'Reference', 'Reference components'], rows, ['l'] * 7)
N['disputed_reasons'] = dcz.selection_reason.value_counts().to_dict()

# ---------------------------------------------------------------- policy contrast
pc = rd('policy_contrast/model_results.csv')
porder = ['Jev', 'Laya', 'Decider', 'SemIf-2B', 'SemIf-4B', 'Bespoke-Nimble', 'Luna Decisions', 'CoPE', 'BART', 'GPT-5.6 Luna', 'GPT-6 Sol']
rows = []
PC = {}
for m in porder:
    r = [m]
    for idn in ['men', 'white people', 'straight people', 'overall']:
        z = pc[(pc.model == m) & (pc.cohort == 'full') & (pc.identity == idn)]
        g = lambda met: z[z.metric == met].iloc[0]
        a, c_, u = g('pin_accuracy'), g('conditional_switch'), g('unconditional_switch')
        PC[(m, idn)] = (a.value, c_.value, u.value)
        cs = '–' if isnan(c_.value) else f'{100*c_.value:.0f}'
        r.append(f'{100*a.value:.0f} / {cs} / {100*u.value:.0f}')
    rows.append(r)
T['policy_id'] = md(['Model', 'Men', 'White people', 'Straight people', 'All 90'], rows)
rows = []
for m in porder:
    def gs(co, grp, met='success_rate'):
        z = pc[(pc.model == m) & (pc.cohort == co) & (pc.group == grp) & (pc.metric == met)]
        return z.iloc[0] if len(z) else None
    s, h, n_ = gs('full', 'switch'), gs('full', 'hateful_controls'), gs('full', 'neutral_controls')
    sa = gs('accepted', 'switch')
    hf, nf = gs('full', 'hateful_controls', 'false_flip_rate'), gs('full', 'neutral_controls', 'false_flip_rate')
    dz = pc[(pc.model == m) & (pc.cohort == 'accepted_minus_full') & (pc.metric == 'Correct switch')]
    dz = dz.iloc[0] if len(dz) else None
    rows.append([m, f'{100*s.value:.0f} ({100*s.ci_low:.0f}–{100*s.ci_high:.0f})', f'{100*h.value:.0f}', f'{100*n_.value:.0f}',
                 f'{100*hf.value:.0f}', f'{100*nf.value:.0f}', f'{100*sa.value:.0f}', pp(dz.value) if dz is not None else '–'])
T['policy_main'] = md(['Model', 'Switch % (95% CI)', 'Hateful controls %', 'Neutral controls %', 'Hateful false flips %', 'Neutral false flips %', 'Switch %, 234 accepted', 'Δ (pp)'], rows)
N['PC'] = PC

# ---------------------------------------------------------------- exposure
ex = rd('exposure.csv')
g = lambda met, co=None: ex[(ex.metric == met) & ((ex.cohort == co) if co else True)]
rows = []
for co, lab in [('training_selection', 'Replayed training selection'), ('evaluation_partition', 'Replayed evaluation partition'), ('neither', 'Neither')]:
    rows.append([lab, int(g('n', co).value.iloc[0]), int(g('hate', co).value.iloc[0]), int(g('non_hate', co).value.iloc[0])])
T['exp_split'] = md(['Partition of our MHS test set', 'Comments', 'Hate', 'Non-hate'], rows)
rows = []
for m in ['Decider', 'TF-IDF+LR', 'DistilBERT', 'Jev', 'GPT-6 Sol']:
    z = ex[(ex.model == m) & (ex.metric == 'macro_f1')].iloc[0]
    rows.append([m, f3(float(z.value)), f'[{f3(z.ci_low)}, {f3(z.ci_high)}]'])
T['exp_f1'] = md(['Model', 'Macro-F1', '95% CI'], rows)
rows = []
for _, z in ex[ex.metric == 'difference_pp'].iterrows():
    rows.append([z.contrast.replace('-minus-', ' − '), pp(float(z.value)), ci(z.ci_low, z.ci_high), ci(z.adj_low, z.adj_high)])
T['exp_diff'] = md(['Contrast', 'Δ (pp)', 'Unadjusted 95% CI', 'Adjusted 95% CI (2 contrasts)'], rows)
N['exp_replay'] = {r.metric: r.value for _, r in ex[ex.metric.str.startswith('replay')].iterrows()}

if __name__ == '__main__':
    import json
    want = sys.argv[2].split(',') if len(sys.argv) > 2 else list(T)
    for k in want:
        print(f'\n### {k}\n{T[k]}')
