#!/usr/bin/env python3
"""
DeepDTA Command Line Prediction Tool
Predicts Drug-Target Binding Affinity and generates a detailed report.
Paper: Öztürk et al., Bioinformatics 2018 (DeepDTA)
"""

import sys
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from src.predictor import DeepDTAPipeline


def print_banner():
    banner = """
================================================================================
    DEEPDTA: DEEP DRUG-TARGET BINDING AFFINITY PREDICTION
    Convolutional Neural Networks for Sequence-Based Bioactivity Modeling
================================================================================
"""
    print(banner)


def display_report(report: dict):
    eval_info = report['evaluation']
    drug_info = report['drug']
    prot_info = report['protein']

    print("-" * 80)
    print(f"  VERDICT: {eval_info['verdict']} [{eval_info['tier']}]")
    print("-" * 80)
    print(f"  Target Pairing Status : {eval_info['status_badge']}")
    print(f"  Predicted {eval_info['metric_name']}: {eval_info['formatted_value']}")

    if eval_info.get('kd_nm') is not None:
        print(f"  Estimated Dissociation Const (Kd): {eval_info['formatted_kd']}")

    print(f"  Benchmark Active Threshold       : {eval_info['threshold_label']}")
    print(f"  Estimated Binding Percentile     : ~Top {100 - eval_info['percentile_est']}%")
    print("\n[SCIENTIFIC INTERPRETATION]")
    print(f"  {eval_info['summary']}")
    print(f"\n[RECOMMENDATION]")
    print(f"  {eval_info['recommendation']}")

    print("\n[RESOLVED MOLECULE DETAILS]")
    print(f"  Drug Name       : {drug_info['name']}")
    print(f"  PubChem CID     : {drug_info.get('cid', 'N/A')}")
    print(f"  SMILES String   : {drug_info['smiles'][:75]}{'...' if len(drug_info['smiles']) > 75 else ''}")
    print(f"  Resolution Source: {drug_info['source']}")

    print("\n[RESOLVED TARGET DETAILS]")
    print(f"  Target Protein  : {prot_info['name']}")
    print(f"  Gene Symbol     : {prot_info['gene_symbol']}")
    print(f"  Sequence Length : {prot_info['length']} residues")
    print(f"  Resolution Source: {prot_info['source']}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Predict Drug-Target binding affinity using the DeepDTA deep learning model."
    )
    parser.add_argument(
        '--drug', '-d',
        type=str,
        required=True,
        help="Name of the drug (e.g., 'Gefitinib', 'Imatinib', 'Afatinib') or raw SMILES string."
    )
    parser.add_argument(
        '--protein', '-p',
        type=str,
        required=True,
        help="Name of the protein/gene symbol (e.g., 'EGFR', 'ABL1', 'BRAF') or amino acid sequence."
    )
    parser.add_argument(
        '--dataset', '-s',
        type=str,
        choices=['davis', 'kiba'],
        default='davis',
        help="Target dataset/affinity metric: 'davis' (pKd) or 'kiba' (KIBA score). Default is 'davis'."
    )

    args = parser.parse_args()

    print_banner()
    print(f"[*] Initializing DeepDTA pipeline...")
    print(f"[*] Query Drug    : {args.drug}")
    print(f"[*] Query Protein : {args.protein}")
    print(f"[*] Target Metric : {'Davis (pKd / Dissociation Constant)' if args.dataset == 'davis' else 'KIBA (Bioactivity Score)'}")
    print("[*] Resolving biological entities and running neural inference...\n")

    pipeline = DeepDTAPipeline()
    result = pipeline.predict(args.drug, args.protein, dataset=args.dataset)

    if not result.get('success'):
        print(f"\n[ERROR] {result.get('error')}", file=sys.stderr)
        sys.exit(1)

    display_report(result)


if __name__ == '__main__':
    main()
