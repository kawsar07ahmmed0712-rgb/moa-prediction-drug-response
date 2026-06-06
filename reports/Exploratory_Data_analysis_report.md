# Research-based EDA Blueprint for the MoA Project

## What top EDA practice shows

The strongest public notebooks do not behave like scratchpads; they behave like **computational narratives**. Research on highly rated Kaggle notebooks shows that community value is not driven by leaderboard score alone: the most accurate notebooks are often *not* the most upvoted ones, because readability, completeness, and narrative quality matter independently. In that work, the authors explicitly describe notebooks as a medium that should combine code, results, and explanation into a form another analyst can follow and reuse. citeturn48view0turn35view0turn18view0

A detailed study of 80 highly voted Kaggle notebooks found a very consistent documentation pattern: rich markdown, strong section headings, explanation of adjacent code, interpretation of outputs, and explicit summaries. Quantitatively, those notebooks averaged 55.3 code cells and 45.1 markdown cells, had a median of 95 total cells, and contained far more markdown text than a large GitHub comparison set. Their markdown was used mostly for **process explanation** and **section structure/navigation**, with additional cells for results, reasons, references, and summaries. The same study also found that documentation tends to follow the lifecycle of a data project, with heavy emphasis on exploratory analysis and later model training sections, plus a problem overview at the beginning and a summary at the end. citeturn36view1turn36view2turn37view0turn37view1

Notebook and visualisation research points to the same conclusion from a different angle: notebooks become hard to read when they look like one long stream of unrelated cells, and high-dimensional EDA becomes overwhelming when users are forced to inspect every possible plot. WHATSNEXT argues for making the analysis thread visible and for showing the reader what question comes next, while Foresight argues for a **guidepost-based** style of EDA that starts from the strongest statistical patterns rather than plotting everything. SuperNOVA adds that notebook visualisations work best when they are well integrated into the notebook and not so exotic that they break the reading flow. citeturn19view2turn19view3turn19view4turn38view0turn19view0turn19view1

Professional project structure reinforces those notebook-level lessons. Cookiecutter Data Science recommends numbered notebooks, separate `raw / interim / processed` data layers, and dedicated `reports / figures` outputs; a workflow paper distinguishes **Exploratory**, **Refinement**, and **Polishing** phases so that a notebook does not try to do everything at once; and scikit-learn explicitly warns that transformations such as scaling, feature selection, and PCA must be fit on training data only to avoid leakage. citeturn15view3turn39view0turn43view1turn43view4

The practical summary is straightforward:

1. Good EDA notebooks explain decisions, not just calculations. citeturn36view1turn37view1  
2. Good notebooks are lifecycle-ordered, with a clear beginning, middle, and end. citeturn37view0turn39view0  
3. High-dimensional EDA should be **selective** and **ranked**, not exhaustive. citeturn38view0  
4. Visuals should earn their place by creating a next step or a decision. citeturn19view3turn19view4turn37view1  
5. Competition-grade notebooks still need reproducible structure and leakage discipline. citeturn15view3turn43view1

## Why basic EDA plans fail

A basic or messy EDA plan usually breaks down in this project for six reasons.

1. It starts with a generic “numerical versus categorical” split, which is the wrong abstraction for MoA. Your data is not a normal business table; it is an **experimental design dataset** with metadata, two different biological feature blocks, a sparse multi-label target matrix, control samples, and repeated drugs. If the plan ignores that structure, the notebook becomes technically correct but strategically weak.

2. It creates **chart walls**. In a high-dimensional dataset, a feature-by-feature tour is not exploration; it is visual inventory. Guidepost-based EDA exists precisely because forcing analysts through the full space of attributes and encodings is overwhelming and low-yield. citeturn38view0

3. It has no visible narrative thread. Notebook research shows that interleaved code, charts, and tables can easily become an unorganised single stream, which makes the analysis workflow hard to review and hard to continue. citeturn19view2turn19view3

4. It underuses markdown. The strongest Kaggle notebooks do not dump code and hope the figures explain themselves. They use markdown for section headlines, process description, interpretation, rationale, and summary. Without that, the notebook is harder to audit and far less useful to your future self. citeturn36view1turn37view1turn48view0

5. It repeats the same analysis mechanically. A weak plan often runs the same generic histogram/correlation routine for every block. A stronger plan reuses an *analytic stencil* but changes the question. For MoA, gene features, cell features, labels, metadata, and repeated drugs each support different modelling decisions.

6. It mixes exploration with modelling and transforms, which is dangerous. Scikit-learn’s documentation is very clear: split first, fit transforms on training data only, and keep PCA, selection, scaling, and similar steps inside a safe pipeline. If EDA quietly fits reusable transforms on full data, the notebook stops being exploratory and starts leaking information. citeturn43view1turn15view0turn15view2

## Upgraded competition-grade EDA structure

This structure is stronger because it follows the **true geometry of the MoA problem**: experimental design first, label space second, biological feature blocks third, global representation and modelling risk after that, and a decision register at the end. That ordering matches the lifecycle logic seen in well-documented notebooks while keeping this notebook firmly in the exploratory phase rather than slipping into premature modelling. citeturn37view1turn39view0turn38view0

Before the numbered sections, use one consistent **section contract** throughout the notebook:

- **Markdown heading** with the analysis question and its scope  
- **Short explanation** of why the section matters  
- **Code cell(s)** only for the specific diagnostic being run  
- **Insight block** immediately after the output: *Finding → Why it matters → Action*  
- **Section-end summary** with at most three decisions or open questions  

That pattern mirrors how strong notebooks use process, result, reason, and summary markdown rather than leaving the reader to infer the meaning of a chart. citeturn36view1turn37view1

### The structure to use

**1. Notebook contract and scope**

1.1 Objective, audience, and non-goals  
1.2 Loaded assets and feature dictionary  
1.3 Leakage guardrails for all descriptive transforms  
1.4 Plotting rules, top-*k* rules, and summary template  

**Analyse:** what this notebook must answer and what it must not attempt.  
**Why:** a strong notebook begins with a visible contract; this prevents drift into modelling and keeps the exploration phase clean.  
**Plots:** none beyond a compact asset inventory table.  
**Decisions:** fix notebook scope, helper function conventions, and the summary format used later.

**2. Experimental design and metadata audit**

2.1 Table inventory and feature-block map  
2.2 Metadata balance in train and test  
2.2.1 `cp_type` distribution  
2.2.2 `cp_time` distribution  
2.2.3 `cp_dose` distribution  
2.3 Metadata interaction structure  
2.3.1 `cp_type × cp_time`  
2.3.2 `cp_type × cp_dose`  
2.3.3 `cp_time × cp_dose`  
2.4 Control-versus-treated protocol  
2.4.1 Control row frequency  
2.4.2 Active-label sanity view for controls  
2.5 Section summary and actions  

**Analyse:** whether the experimental design is balanced, whether train and test look aligned, and whether the control/treated split behaves exactly as expected.  
**Why:** in MoA, metadata is not decoration; it encodes the perturbation setting and directly informs modelling rules, especially the control-sample constraint.  
**Plots:** proportional train/test bars, normalised interaction heatmaps, and one compact control-versus-treated comparison.  
**Decisions:** metadata encoding strategy, whether interaction features are worth testing later, and the control-row post-processing rule.

**3. Label-space analysis**

3.1 Global target geometry  
3.1.1 Scored target density and sparsity  
3.1.2 Positives per target  
3.1.3 Positives per sample  
3.1.4 Zero-label versus multi-label prevalence  
3.2 Long-tail diagnostics  
3.2.1 Rank-frequency curve for targets  
3.2.2 Cumulative positive coverage curve  
3.2.3 Rare-target risk bands  
3.3 Label dependence  
3.3.1 Top-*k* co-occurrence matrix  
3.3.2 Clustered label-correlation view  
3.3.3 Frequent label-combination analysis  
3.4 Auxiliary label block  
3.4.1 Scored versus nonscored density  
3.4.2 Whether auxiliary learning looks promising  
3.5 Section summary and actions  

**Analyse:** how sparse the target matrix is, how long-tailed the 206 scored labels are, how many labels are active per sample, and which labels tend to appear together.  
**Why:** this is the section that determines evaluation realism, fold strategy, rare-label monitoring, and whether auxiliary nonscored targets deserve later modelling effort.  
**Plots:** rank-frequency, cumulative coverage, ECDF of sample label cardinality, top-*k* clustered heatmaps, and an UpSet-style view for the most common label combinations.  
**Decisions:** choose multi-label-aware validation, define rare-target monitoring, and decide whether nonscored targets belong only in advanced experiments.

**4. Biological feature block analysis**

4.1 Gene-expression block  
4.1.1 Per-feature location, spread, and shape  
4.1.2 Per-sample gene response intensity  
4.1.3 Gene response conditioned on metadata  
4.1.4 High-variance and extreme-tail genes  
4.1.5 Train/test shift within the gene block  

4.2 Cell-viability block  
4.2.1 Per-feature location, spread, and shape  
4.2.2 Per-sample cell response intensity  
4.2.3 Cell response conditioned on metadata  
4.2.4 High-variance and extreme-tail cell features  
4.2.5 Train/test shift within the cell block  

4.3 Cross-block coupling  
4.3.1 Gene-versus-cell response strength  
4.3.2 Cross-block ratios and differences as candidate features  
4.3.3 Block comparison by magnitude, skew, and stability  

4.4 Section summary and actions  

**Analyse:** the internal behaviour of the 772 gene and 100 cell features as *blocks*, not as 872 unrelated columns. Use the same analytic stencil for both blocks so the notebook stays consistent without becoming repetitive.  
**Why:** MoA feature engineering usually comes from block-level understanding: sample-level summary features, block-wise transforms, PCA, outlier handling, and gene/cell interaction ideas.  
**Plots:** distributions of per-feature summary statistics, per-sample summary distributions, metadata-conditioned response plots, and a gene-versus-cell coupling plot.  
**Decisions:** which summary statistics to create later, whether gene and cell blocks should be transformed separately, and whether block-wise PCA is worth testing.

**5. Representation structure and distribution shift**

5.1 PCA on the gene block  
5.1.1 Scree and explained variance  
5.1.2 PCA scatter by metadata  
5.1.3 PCA scatter by sample label density  

5.2 PCA on the cell block  
5.2.1 Scree and explained variance  
5.2.2 PCA scatter by metadata  
5.2.3 PCA scatter by sample label density  

5.3 Combined representation view  
5.3.1 PCA on combined biological features  
5.3.2 Control-versus-treated separation  
5.3.3 Optional local manifold view on a stratified subsample  

5.4 Shift diagnostics  
5.4.1 Feature-level divergence ranking  
5.4.2 Sample-level drift proxies  
5.4.3 Most unstable features or directions  

5.5 Section summary and actions  

**Analyse:** whether the main variation directions line up with metadata, control structure, and label activity, and whether train/test differences appear concentrated in a small set of features or in broader representation space.  
**Why:** this section tells you whether dimensionality reduction is merely aesthetic or genuinely useful, and whether there are unstable regions of feature space you should treat carefully.  
**Plots:** scree plots, PCA scatters with density-aware rendering, and ranked divergence charts.  
**Decisions:** whether to create separate PCA features for gene and cell blocks, whether to add sample-level outlier indicators, and whether any feature shifts deserve monitoring later.

**6. Validation and modelling-risk diagnostics**

6.1 Repeated-drug structure  
6.1.1 Drug frequency distribution  
6.1.2 High-repeat drugs and potential fold contamination risk  

6.2 Multi-label fold risk  
6.2.1 Rare labels across candidate folds  
6.2.2 Label-pair preservation need  
6.2.3 Sample-label cardinality balance across folds  

6.3 Leakage-sensitive transformations  
6.3.1 Scaling and clipping  
6.3.2 PCA  
6.3.3 Feature selection or filtering  
6.3.4 Any target-aware aggregation checks  

6.4 Inference constraints  
6.4.1 Control rows and zero predictions  
6.4.2 Submission-target alignment reminder  

6.5 Section summary and actions  

**Analyse:** whether standard folds would be too optimistic because of repeated drugs, whether label pairs need preservation, and which later transformations are most leakage-sensitive.  
**Why:** competition-level EDA should reduce modelling risk *before* training starts.  
**Plots:** repeated-drug Pareto chart, fold-risk tables, label-pair coverage summaries, and a leakage checklist.  
**Decisions:** whether to test drug-aware validation later, whether iterative stratification should be the default, and which transforms must be locked inside cross-validation only.

**7. EDA decision register and handoff**

7.1 Baseline feature-engineering candidates  
7.2 Advanced feature candidates  
7.3 Validation design decisions  
7.4 Inference-time rules  
7.5 Saved artefacts for the next notebook  

**Analyse:** the output of the whole notebook, converted into an action list.  
**Why:** the point of EDA is not to accumulate plots; it is to create a clean backlog for feature engineering and modelling.  
**Plots:** none required; this section should be mainly a concise decision table.  
**Decisions:** baseline versus advanced backlog, figures to save, and the exact handoff to `03_feature_engineering.ipynb`.

## Advanced plots that earn their place

I would keep only plots that surface a pattern you can plausibly act on. That is exactly the logic of guidepost-based EDA and notebook-integrated visual design: show the strongest patterns, keep the notebook readable, and avoid detached visual gimmicks unless they materially improve interpretation. citeturn38view0turn19view0turn19view1

**For experimental design and metadata**

1. **Normalised train-versus-test proportion bars** for `cp_type`, `cp_time`, and `cp_dose`  
   Purpose: reveal drift immediately without overloading the reader.

2. **Delta bars** showing percentage-point differences between train and test  
   Purpose: makes small distribution shifts visible faster than side-by-side counts.

3. **Normalised interaction heatmaps** for metadata pairs  
   Purpose: exposes whether time/dose combinations are balanced or structurally sparse.

4. **Compact mosaic / UpSet-style view for metadata combinations**  
   Purpose: useful if you want one view of the full experimental design intersection.

**For the label space**

1. **Rank-frequency plot on a log scale**  
   Purpose: best view of target long-tail shape.

2. **Cumulative positive-coverage curve**  
   Purpose: shows how much of the positive mass sits in the head versus the tail.

3. **ECDF or histogram of active labels per sample**  
   Purpose: distinguishes zero-label, single-label, and true multi-label regimes.

4. **Clustered co-occurrence heatmap for top-*k* labels only**  
   Purpose: readable dependence structure without a useless 206×206 wall.

5. **UpSet plot for the most common label combinations**  
   Purpose: far more interpretable than a raw combination table.

**For gene and cell feature blocks**

1. **Distribution-of-distributions plots**  
   Examples: histogram of per-feature means, standard deviations, skewness, kurtosis.  
   Purpose: summarises hundreds of features without plotting each one.

2. **Ridgeline / violin / raincloud plots of per-sample summary features by metadata**  
   Purpose: shows treatment-response strength and metadata-conditioned shifts.

3. **Top-variance or top-tail lollipop charts**  
   Purpose: identifies candidate features for closer inspection without pretending every feature deserves the same attention.

4. **Hexbin plot of gene-versus-cell sample summaries**  
   Purpose: reveals whether the two biological blocks move together or carry different signal.

5. **Ranked shift chart using KS/Wasserstein/mean-difference proxies**  
   Purpose: prioritises which features deserve later robustness checks.

**For representation structure**

1. **Scree plots** for gene PCA, cell PCA, and combined PCA  
   Purpose: judge whether block-wise compression is meaningful.

2. **PCA scatter with transparency or density contours**  
   Purpose: show structure without overplotting.

3. **PCA scatter coloured by metadata and by active-label count**  
   Purpose: links representation structure back to experimental design and target behaviour.

4. **Optional UMAP on a stratified subsample**  
   Purpose: only if it reveals local neighbourhood structure that PCA misses. Use sparingly.

**For validation and risk**

1. **Pareto chart of repeated drug frequencies**  
   Purpose: immediately conveys group leakage risk.

2. **Fold-risk heatmap**  
   Purpose: rare-label or label-pair coverage by fold candidate.

3. **Leakage checklist table**  
   Purpose: not visually glamorous, but extremely valuable in a competition notebook.

What I would **not** keep in the main narrative:

1. A histogram for every gene or cell feature  
2. A full 206×206 label heatmap  
3. A full all-feature correlation matrix  
4. Repeated versions of the same plot with only minor cosmetic changes  
5. Interactive widgets that do not materially improve interpretation

## How this notebook feeds feature engineering

For a competition notebook, EDA should end as a **feature-engineering and validation brief**. In multi-label problems, preserving label relationships across folds matters, and preprocessing must stay inside train-only fitting; the literature on second-order multi-label stratification and scikit-learn’s leakage guidance both support turning EDA observations directly into validation and transformation rules. citeturn47view0turn43view1turn43view4

Here is how each EDA block should drive downstream work.

1. **Experimental design and metadata audit**  
   This section should decide how you encode `cp_type`, `cp_time`, and `cp_dose`, whether interaction terms are worth trying, and enforce the structural rule that control rows deserve special treatment at inference time.

2. **Label-space analysis**  
   This section should decide whether the validation strategy must be multi-label-aware, how rare targets will be monitored, whether label-pair preservation matters, and whether nonscored targets are worth using later as auxiliary outputs rather than baseline targets.

3. **Biological feature block analysis**  
   This section should produce candidate engineered features such as sample-level gene summaries, sample-level cell summaries, and cross-block ratios or differences. It should also tell you whether gene and cell blocks ought to be transformed separately.

4. **Representation structure and shift**  
   This section should decide whether block-wise PCA is justified, whether sample-level outlier flags are worth testing, and whether any unstable features should be monitored rather than dropped blindly.

5. **Validation and modelling-risk diagnostics**  
   This section should decide whether later experiments need drug-aware grouping, whether iterative multi-label stratification should be used by default, and which transforms must be strictly confined inside cross-validation folds.

6. **Inference constraints**  
   This section should formalise downstream rules such as zeroing control predictions and never using `drug_id` as a baseline feature if it is unavailable at test time.

7. **Decision register**  
   This final section should split your backlog into **baseline** and **advanced** actions. For your project, that would likely mean:  
   - **Baseline:** metadata encoding, leakage-safe preprocessing, block summary features, and a clean validation plan  
   - **Advanced:** block-wise PCA, auxiliary nonscored learning, drug-aware validation experiments, and richer cross-block features

## Execution strategy for the notebook

Treat `02_eda.ipynb` as a pure **exploratory-phase notebook**, not as a mixed exploration-modelling document. The workflow literature explicitly separates exploratory work from later refinement/polishing, while project templates recommend numbered notebooks and clear output directories so the notebook remains easy to rerun and review. citeturn39view0turn15view3

Use this execution order.

1. **Create the notebook contract first.**  
   Open with the objective, non-goals, loaded assets, and the reusable section template.

2. **Load only clean interim assets.**  
   Do not redo data integration here. That belongs to the earlier notebook.

3. **Define a small helper layer before any section starts.**  
   Helpers for summary tables, top-*k* selection, train/test proportion comparison, and reusable block diagnostics.

4. **Start with metadata and experimental design before touching the large numeric blocks.**  
   This gives context for every later plot.

5. **Run label-space analysis before feature-block analysis.**  
   In MoA, the label matrix is one of the main reasons the modelling problem is hard; understand it early.

6. **Use one reusable analytic stencil for the gene and cell blocks.**  
   The questions should be the same, but the interpretation can differ. This keeps the notebook clean and avoids copy-paste clutter.

7. **Prefer summary statistics and ranked diagnostics over exhaustive per-feature plots.**  
   If a plot does not change a later decision, it belongs in an appendix at most.

8. **After every major section, add an insight block with three lines only.**  
   - **Finding**  
   - **Why it matters**  
   - **Action for feature engineering / validation**

9. **Do not fit reusable transforms on the full dataset in EDA.**  
   If you inspect a transform descriptively, make it clear that the real fitted version will live inside the training pipeline later. This matters especially for scaling, PCA, and any feature filtering. citeturn43view1turn43view4

10. **Maintain a live decision register as you go.**  
    Do not wait until the last cell to remember what mattered.

11. **Save only high-value artefacts.**  
    Store the most useful tables and figures in `reports/figures` or a similar project location, not every temporary plot. That keeps the notebook readable and the project reproducible. citeturn15view3

12. **End with a clean handoff.**  
    The final cells should answer one question only: *what will be implemented in `03_feature_engineering.ipynb`, and in what order?*

If you follow this blueprint, your EDA notebook will read like a competition-grade technical narrative rather than a temporary scratch file: MoA-specific, strongly numbered, selective in its visualisations, safe against leakage, and directly connected to downstream feature-engineering and validation choices.