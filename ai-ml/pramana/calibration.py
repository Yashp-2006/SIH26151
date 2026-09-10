"""
Empirical Calibration & Forensic Evaluation Engine.

Provides statistical proof that PRAMANA's Evidence Balance Sheet generates 
calibrated log-likelihood ratios, avoiding the overconfidence common in black-box AI.
Outputs Expected Calibration Error (ECE) and Tippett Plot coordinates.
"""

import math
from typing import List, Tuple, Dict

def log10_lr_to_prob(log_lr: float, prior_odds: float = 1.0) -> float:
    """
    Converts a base-10 log likelihood ratio to a posterior probability.
    Assuming given prior odds (default 1:1 / neutral prior).
    """
    # Prevent math overflow for massive definitive LRs
    if log_lr > 100:
        return 1.0
    if log_lr < -100:
        return 0.0
    
    lr = math.pow(10, log_lr)
    odds = lr * prior_odds
    return odds / (1.0 + odds)

def expected_calibration_error(predictions: List[Tuple[float, bool]], num_bins: int = 10) -> float:
    """
    Calculates Expected Calibration Error (ECE) for the attribution engine.
    
    Args:
        predictions: List of tuples (log10_lr, ground_truth_boolean)
        num_bins: Number of probability bins (default: 10)
        
    Returns:
        float: The ECE score (lower is better, 0.0 is perfect calibration).
    """
    if not predictions:
        return 0.0

    # Convert Log-LRs to Probabilities
    probs = [(log10_lr_to_prob(ll), gt) for ll, gt in predictions]
    
    # Sort predictions by confidence
    probs.sort(key=lambda x: x[0])
    
    bin_size = len(probs) // num_bins
    if bin_size == 0:
        bin_size = 1
        num_bins = len(probs)
        
    ece = 0.0
    total_samples = len(probs)
    
    for i in range(num_bins):
        start_idx = i * bin_size
        # The last bin takes the remainder
        end_idx = total_samples if i == num_bins - 1 else (i + 1) * bin_size
        
        bin_data = probs[start_idx:end_idx]
        if not bin_data:
            continue
            
        bin_len = len(bin_data)
        
        # Average predicted probability in bin
        avg_conf = sum(p for p, _ in bin_data) / bin_len
        # Actual accuracy (proportion of true matches) in bin
        avg_acc = sum(1.0 for _, gt in bin_data if gt) / bin_len
        
        # Weighted error for this bin
        ece += (bin_len / total_samples) * abs(avg_acc - avg_conf)
        
    return ece

def generate_tippett_coordinates(predictions: List[Tuple[float, bool]], num_points: int = 100) -> Dict[str, List[float]]:
    """
    Generates coordinates for a Tippett Plot. 
    A standard forensic science metric evaluating the discriminative power of Likelihood Ratios.
    
    Returns cumulative proportions of same-source and different-source comparisons 
    exceeding given log-LR thresholds.
    """
    if not predictions:
        return {"thresholds": [], "y_same_source": [], "y_diff_source": []}
        
    lrs = [ll for ll, _ in predictions]
    min_lr, max_lr = min(lrs), max(lrs)
    
    # Create threshold grid across the observed LR range
    step = (max_lr - min_lr) / num_points if num_points > 1 else 1.0
    thresholds = [min_lr + i * step for i in range(num_points + 1)]
    
    same_source_lrs = [ll for ll, gt in predictions if gt]
    diff_source_lrs = [ll for ll, gt in predictions if not gt]
    
    n_same = len(same_source_lrs) if same_source_lrs else 1
    n_diff = len(diff_source_lrs) if diff_source_lrs else 1
    
    y_same, y_diff = [], []
    
    for t in thresholds:
        # Proportion of True Positives exceeding threshold
        prop_same = sum(1 for ll in same_source_lrs if ll >= t) / n_same
        # Proportion of False Positives exceeding threshold (should drop rapidly)
        prop_diff = sum(1 for ll in diff_source_lrs if ll >= t) / n_diff
        
        y_same.append(prop_same)
        y_diff.append(prop_diff)
        
    return {
        "thresholds": thresholds,
        "y_same_source": y_same,
        "y_diff_source": y_diff
    }
