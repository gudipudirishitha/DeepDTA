# DeepDTA: Deep Drug-Target Binding Affinity Prediction

A production-grade implementation of the deep learning architecture from **Öztürk et al. (Bioinformatics 2018)**: *"DeepDTA: deep drug–target binding affinity prediction"*.

---

## 🌟 Key Features & Requirements Addressed

1. **Effortless Biological Entity Entry**
   - Enter **plain drug names** (e.g. `Gefitinib`, `Imatinib`, `Sorafenib`, `Aspirin`) and **protein names / gene symbols** (e.g. `EGFR`, `ABL1`, `BRAF`, `HER2`, `FLT3`).
   - Integrated **Entity Resolution Engine**:
     - Fast local curated library for instant offline lookups.
     - Automated fallback to **PubChem PUG-REST API** (for small molecules) and **UniProtKB REST API** (for human protein targets).
     - Direct support for raw **SMILES** and raw **amino acid FASTA sequences**.

2. **Choice of Output Binding Affinity Metric**
   - **Davis Dataset Model ($pK_d$)**:
     $$\text{p}K_d = -\log_{10}\left(\frac{K_d}{10^9}\right)$$
     Directly predicts dissociation constant in logarithmic scale and automatically computes intuitive $K_d$ in nanomolar (nM) and micromolar ($\mu\text{M}$).
   - **KIBA Dataset Model (KIBA Score)**:
     Integrates multi-assay bioactivity ($K_i, K_d, \text{IC}_{50}$) into a standardized statistical metric.
   - **Consensus Dual-Evaluation**:
     Option to evaluate both models side-by-side on the same pair.

3. **Interpretability & Pharmacological Report**
   - Non-experts can immediately understand whether a pairing is **good or bad**:
     - **Executive Verdict Badge**: Color-coded rating (*"EXCELLENT PAIRING"*, *"GOOD PAIRING"*, *"MARGINAL PAIRING"*, *"POOR PAIRING (NON-BINDER)"*).
     - **Visual Gauge / Spectrum Bar**: Shows where the prediction lies compared to benchmark active thresholds ($pK_d \ge 7.0$ / $\text{KIBA} \ge 12.1$) and baseline negatives.
     - **Biochemical Meaning**: Explains the dissociation constant in plain English (e.g. *"Sub-10 nM potency indicates tight therapeutic inhibition"* vs *"Micromolar contact represents inert non-binding"*).
     - **Actionable Recommendation**: High priority drug candidate, chemical probe, or negligible interaction.

---

## 📐 DeepDTA Neural Architecture (Öztürk et al.)

```
  Drug (SMILES)               Target (Protein Sequence)
        │                                  │
  Embedding (65 -> 128)              Embedding (26 -> 128)
        │                                  │
  Conv1D (32 filters, k=6)           Conv1D (32 filters, k=8)
        │                                  │
  Conv1D (64 filters, k=6)           Conv1D (64 filters, k=8)
        │                                  │
  Conv1D (96 filters, k=6)           Conv1D (96 filters, k=8)
        │                                  │
  GlobalMaxPooling1D (96)            GlobalMaxPooling1D (96)
        └─────────────────┬────────────────┘
                    Concatenate (192)
                          │
                   Dense (1024, ReLU)
                          │
                     Dropout (0.1)
                          │
                   Dense (1024, ReLU)
                          │
                     Dropout (0.1)
                          │
                   Dense (512, ReLU)
                          │
                   Dense (1, Linear) ──> Predicted Affinity (pKd / KIBA)
```

---

## 🚀 Quickstart Guide

### 1. Command-Line Interface (CLI)

Run predictions directly from the command line:

```bash
# Predict Gefitinib + EGFR on Davis dataset (pKd)
python predict.py --drug "Gefitinib" --protein "EGFR" --dataset "davis"

# Predict Imatinib + ABL1 on KIBA dataset
python predict.py --drug "Imatinib" --protein "ABL1" --dataset "kiba"

# Negative control: Aspirin + EGFR
python predict.py --drug "Aspirin" --protein "EGFR" --dataset "davis"
```

### 2. Interactive Web Application

Launch the modern web interface:

```bash
python -m uvicorn web.app:app --host 0.0.0.0 --port 8000
```
Then navigate to `http://localhost:8000` in your web browser.

---

## 🧪 Testing

Execute the test suite verifying character encodings, entity resolvers, model inferences, and report generators:

```bash
python -m unittest discover tests
```

---

## 📂 Project Structure

```
DeepDTA-project-remastered/
├── saved_models/              # Keras native DeepDTA models (Davis & KIBA)
├── data/
│   ├── curated_drugs.json     # Curated drug library with SMILES
│   └── curated_proteins.json  # Curated target library with sequences
├── src/
│   ├── deepdta.py             # Dual CNN architecture & sequence encoders
│   ├── resolver.py            # Drug/Protein name resolver with PubChem/UniProt
│   ├── interpreter.py         # Report generator & Kd threshold calculations
│   └── predictor.py           # Unified inference pipeline
├── web/
│   ├── app.py                 # FastAPI backend server
│   └── templates/
│       └── index.html         # Responsive Tailwind CSS interactive UI
├── tests/
│   └── test_prediction.py     # Unit and integration test suite
├── predict.py                 # Command-line prediction tool
└── README.md                  # Project documentation
```

---

## 📚 References

- **DeepDTA Publication**: Öztürk, H., Özgür, A., & Ozkirimli, E. (2018). *DeepDTA: deep drug–target binding affinity prediction*. Bioinformatics, 34(17), i821–i829.
- **Davis Dataset**: Davis, M. I., et al. (2011). *Comprehensive analysis of kinase inhibitor selectivity*. Nature Biotechnology, 29(11), 1046–1051.
- **KIBA Dataset**: Tang, J., et al. (2014). *Making sense of large-scale kinase inhibitor bioactivity data sets*. J. Chem. Inf. Model., 54(3), 735–743.

