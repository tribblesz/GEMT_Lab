---
date created: 2026-04-10
author: "StarDustX"
note type: pdf-summary
resource type: apt-fim-literature
source pdf: "[[Resources/APT-FIM/PDFs/atomic-scale-phase-composition-through-multivariate-statistical-analysis-of-atom-probe-tomography-data-duplicate.pdf]]"
provider: "lmstudio"
model: "gemma-4-26B-A4B-it-Q4_K_M"
tags:
  - "#resource/pdf-summary"
  - "#apt"
  - "#fim"
---

# atomic-scale-phase-composition-through-multivariate-statistical-analysis-of-atom-probe-tomography-data-duplicate

## Source PDF

[[Resources/APT-FIM/PDFs/atomic-scale-phase-composition-through-multivariate-statistical-analysis-of-atom-probe-tomography-data-duplicate.pdf]]

## Overview
The study demonstrates the application of Multivariate Statistical Analysis (MVSA)—specifically Principal Component Analysis (PCA) and "Poisson-scaled PCA"—to estimate chemical phase composition in Atom Probe Tomography (APT) at the instrument's full spatial resolution ($\sim$0.2 nm). The approach aims to extract chemical information directly from atomic-scale spectral-image datasets, avoiding the $\sim$125-fold loss of volumetric resolution typically caused by aggregating ions into $1\text{ nm}^3$ voxels.

## Key Findings
* **Automated Phase Discovery:** MVSA allows for the automated, unbiased discovery of chemical phases and spatial distributions without *a priori* knowledge of species or manual Region of Interest (ROI) selection.
* **Interface & Trace Detection:** The method is highly sensitive to subtle variations and low-concentration species; it successfully identified unexpected interfacial chemistry in Ni-base superalloys, including metal oxides and increased singly charged metal ions.
* **Elemental Partitioning:** PCA scores revealed phase-specific partitioning, specifically that Nb and Ta are more prevalent in the Ni-rich phase than in the Cr/Co-rich phase.
* **Isotope Recovery:** Poisson-scaled PCA successfully recovers quantitatively correct isotope distributions even when data is binned at the single-atom or sub-atomic scale.
* **Noise vs. Signal:** In highly binned volumes (0.2 nm cubes), noise constitutes the vast majority of total variance ($\sim$93.7%), with only $\sim$6.3% representing the underlying chemical composition.

## Methods And Instrumentation Notes
* **Instrumentation:** Data were acquired using a **Cameca LEAP 3000X HR** (voltage-pulsed mode) on Ni-base superalloys prepared via the matchstick method and electropolishing ($10\% \text{HClO}_4$ in acetic acid).
* **Precision & Efficiency:** The instrument provides $<1\text{ nm}$ lateral and up to $0.06\text{ nm}$ longitudinal precision, with a detection efficiency of 37% for all ion types.
* **Data Processing:** Mass spectra were constructed using $0.5\text{ Da}$ width bins. For computational efficiency, the study utilized MATLAB with sparse-matrix operations and custom C/MEX-files to manage massive datasets (e.g., $\sim$190 million voxels). 
* **Pre-processing:** A critical step involves scaling data by the inverse square root of the mean spectrum to transform the Poisson noise covariance matrix toward an identity matrix. Voxels with only a single count should be ignored as they provide no information regarding interatom correlations.
* **Computational Scaling:** To handle datasets too large for core memory, "out-of-core" algorithms and software like AXSIA can be used to compute only the most significant eigenvalues.

## Relevance To APT/FIM
* **Statistical Modeling of Sparsity:** Because APT detection efficiency is low, data is extremely sparse (often $<1$ ion per voxel). The MVSA model treats detected ions as random samples from a local neighborhood defined by the instrument's spatial resolution, predicting the probability of atom types at a given voxel.
* **Addressing Poisson Noise:** Standard PCA is unreliable for APT because it overweights high-abundance isotopes (e.g., $^{58}\text{Ni}$) due to their large absolute variance. "Poisson-scaled PCA" is required to prevent the algorithm from identifying "structure in the noise."
* **Resolution Limits:** The Poisson distribution assumption holds at atomic scales but deviates as binning increases ($\ge 2\text{ nm}$), at which point variance becomes a quadratic function of the mean.
* **Spatial Scaling Avoidance:** Unlike EDXS or TOF-SIMS, the authors explicitly avoid applying spatial scaling in the analysis to prevent degrading the signal-to-noise ratio in binned data.

## Open Questions
* **Physical Interpretability:** PCA lacks a basis in physical principles and can produce "unphysical" outputs, such as negative spectral features in loading vectors; using Multivariate Curve Resolution (MCR) or abstract factor rotations may be necessary to achieve non-negative, physically realistic components.

## Citation Trail

- pages 1-2: **Summary: Multivariate Statistical Analysis of APT Data (Keenan et al., 2011)**

* **Objective & Method:** The study demonstrates the application of Multivariate Statistical Analysis (MVSA), specifically Principal Component Analysis (PCA), to estimate chemical phase composition in Atom Probe Tomography (APT) data at the instrument's full spatial resolution ($\sim$0.2 nm).
* **Resolution Improvement:** Unlike traditional methods that aggregate ions into $1\text{ nm}^3$ voxels—which results in a $\sim$125-fold loss of volumetric resolution—this approach seeks to extract chemical information directly from atomic-scale spectral-image datasets.
* **Data Challenges & Caveats:** The primary analytical challenge is the extreme sparsity of APT data; due to imperfect detection efficiency, the average spectrum contains $<1$ total count, meaning the data variance is almost entirely dominated by counting noise (Poisson noise).
* **Computational Efficiency:** The authors present efficient numerical approaches for performing PCA on massive datasets (comprising hundreds of millions of individual spectra) that can be executed in seconds on a standard laptop.
- pages 2-3: **Lab Notebook Summary: Multivariate Statistical Analysis (MVSA) of APT Data**

* **Methodology & Concept:** The study demonstrates that MVSA (specifically PCA) can resolve atomic-scale phase compositions by treating detected ions as random samples from a local neighborhood defined by the instrument's spatial resolution. Rather than predicting specific atom locations, the model predicts the probability of various atom types at a given voxel, effectively resolving chemical phases at the atomic scale.
* **Instrumentation & Sample Preparation:** Data were acquired using a **Cameca LEAP 3000X HR** (voltage-pulsed mode) on a Ni-base superalloy prepared via the matchstick method and electropolishing (10% $\text{HClO}_4$ in acetic acid). The instrument provides high precision ($<1\text{ nm}$ lateral; up to $0.06\text{ nm}$ longitudinal/Z-axis) with a detection efficiency of 37% for all ion types.
* **Computational Challenges & Optimization:** Due to the low detection efficiency, APT datasets are extremely sparse, often averaging $<1$ ion per voxel. To maintain computational tractability on standard hardware (e.g., MATLAB), the analysis was restricted to mass spectra containing $\ge 2$ total counts, as single-ion voxels provide no information regarding interatom correlations.
* **Data Processing & Simulation:** Mass spectra were constructed by binning ions into $0.5\text{ Da}$ width bins centered on unit and half-unit $m/z$ ratios. For statistical validation, simulations were performed using a multinomial distribution model based on the natural isotopes of Ni and its FCC crystal structure ($a = 0.352\text{ nm}$).
- pages 3-4: **Lab Notebook Summary: Multivariate Statistical Analysis of APT Data**

* **Methodology:** The study employs Principal Component Analysis (PCA) to decompose raw Atom Probe Tomography (APT) spectral datasets into scores ($T$, representing spatial abundances/distributions) and loadings ($P$, representing characteristic chemical spectra), based on a linear additive model of pure chemical components.
* **APT-Specific Challenge:** In APT data binned at the atomic scale, experimental noise is identified as the dominant source of variation. The analysis must account for this contamination, where the observed data ($D$) is the sum of the true chemical signal ($D_0$) and random experimental error ($E$).
* **Statistical Validity & Caveats:** While noise is significant, the authors demonstrate that if the error is uncorrelated and follows an identity covariance matrix (white noise), the principal components of the noisy data will still accurately recover the underlying chemical loading vectors ($P_0$). 
* **Implementation Strategy:** To extract phase-specific information, one should sort the eigenvectors of the raw data cross-product matrix ($D^T D$) by descending eigenvalue magnitude; the $p$ most significant eigenvectors represent the true chemical loadings, and scores can be estimated via $T = DP_0$.
- pages 4-5: **Summary of Multivariate Statistical Analysis for APT Data**

* **Statistical Modeling of APT Noise:** Because APT relies on particle counting, the data violates standard identity-matrix noise assumptions. However, when binned at the atomic scale, APT data is approximately Poisson-distributed; therefore, the error covariance matrix can be estimated *a priori* as a diagonal matrix using the elements of the mean spectrum.
* **Methodology (MVSA/PCA):** The approach utilizes Singular Value Decomposition (SVD) and a kernel-based approach to perform Principal Component Analysis (PCA) on weighted data. By transforming the weighted cross-product matrix, the algorithm identifies significant eigenvectors and eigenvalues that represent physical phase components through an efficient rotation process.
* **Computational Scalability:** The implementation supports "out-of-core" algorithms, which are essential for processing massive APT spectral images. This allows the calculation of principal component scores for datasets that are too large to be contained entirely within core memory by deferring spatial calculations until required.
* **Key Caveat regarding Spatial Scaling:** Unlike EDXS or TOF-SIMS, the authors explicitly avoid applying scaling in the spatial domain. Since APT detection efficiency is independent of atom type and atomic densities are relatively uniform, adding spatial parameters to model noise is avoided to prevent the degradation of the signal-to-noise ratio in binned data.
- pages 5-6: **Summary: Noise Characteristics and Pre-processing in APT Multivariate Analysis**

* **Computational Methods:** The study utilizes MATLAB with sparse-matrix operations to manage large atom probe tomography (APT) datasets efficiently. To prevent memory exhaustion during cross-product calculations of large matrices, custom C/MEX-files were implemented to avoid unnecessary data duplication.
* **Noise Dominance in High-Resolution Data:** In highly binned APT volumes (e.g., 0.2 nm cubes of a Ni-base superalloy), noise constitutes the vast majority of the signal; analysis revealed that ~93.7% of the total variance is attributable to noise, with only ~6.3% representing the underlying chemical composition.
* **Statistical Modeling & Poisson Distribution:** At high spatial resolutions, the number of counts per voxel is extremely low (averaging ~0.29 counts/spectrum), following a predictable Poisson distribution. Because Multivariate Statistical Analysis (MVSA) techniques like PCA tend to maximize variance, they are prone to identifying "structure in the noise" rather than actual chemical phases if not properly pre-processed.
* **Critical Pre-processing Step:** To prevent PCA from capturing noise artifacts, the data should be scaled by the inverse square root of the mean spectrum. This technique aims to transform the noise covariance matrix toward an identity matrix, though its effectiveness is strictly dependent on the assumption that the underlying atom counts follow a true Poisson distribution.
- pages 6-7: **Lab Notebook Summary: Multivariate Statistical Analysis (MVSA) of APT Data**

* **Methodology & Noise Reduction:** Principal Component Analysis (PCA) can be applied to raw ROI spectral data to separate signal from noise. By scaling eigenvalues to account for Poisson noise, the method effectively eliminates structural artifacts, leaving a single significant component representing the primary phase.
* **Instrumentation & Simulation Parameters:** Simulations utilized parameters representative of a LEAP 3000X HR, specifically assuming a detection efficiency of 37%. The study modeled nickel isotopes using a multinomial distribution, which approximates a Poisson distribution in the limit of low-probability atom detection events.
* **Statistical Caveats (Poisson Deviation):** APT data only follows a Poisson distribution when atom detection within a voxel is a "rare event." As spatial binning increases (coarser voxels), the data deviates significantly from Poisson behavior; specifically, once bins exceed ~2 nm per side, the variance becomes a quadratic function of the mean.
* **Impact of Sampling Density on PCA:** The ability to resolve correlations depends on atom density per sample site. Single-atom sampling results in uncorrelated data (diagonal covariance matrix) where only the most prevalent isotope is identified; however, multi-atom sampling allows PCA loadings to quantitatively describe known isotopic abundance relationships.
- pages 7-8: **Lab Notebook Summary: Multivariate Statistical Analysis (MVSA) of APT Data**

* **Methodological Innovation:** The study proposes using "Poisson-scaled PCA" as a multivariate statistical analysis (MVSA) tool to accurately determine isotope abundances in Atom Probe Tomography (APT) data. Standard Principal Component Analysis (PCA) is identified as unreliable for this purpose because it overweights high-abundance isotopes (e.g., $^{58}\text{Ni}$) due to their large absolute variance, which can mask chemically significant trace features.
* **Instrumentation & Simulation Parameters:** To test the method, a Ni lattice simulation was performed using reconstruction precision values of $0.2\text{ nm}$ in lateral dimensions and $0.1\text{ nm}$ in depth. Data were binned into $0.2\text{ nm}$ cubes; despite an average atom occupancy probability of only $\sim 27\%$ per voxel, the combination of lattice geometry (e.g., atoms near tetrahedral holes) and reconstruction error resulted in some voxels containing up to six atoms.
* **Key Findings & Scalability:** The simulation demonstrates that Poisson-scaled PCA successfully recovers quantitatively correct isotope distributions even when data are binned at the single-atom or sub-atomic scale. The results show high agreement with expected Poisson-distributed counts, proving that MVSA can effectively handle the statistical noise inherent in high-resolution APT reconstructions.
- pages 8-9: **Summary: Multivariate Statistical Analysis (MVSA) of Ni-Base Superalloy APT Data**

* **Methodology & Scaling:** The study utilizes Poisson-scaled Principal Component Analysis (PCA) on atom probe tomography (APT) data spatially binned into $0.2\text{ nm}$ cubes. This approach is specifically designed to identify multiple chemical components within sparse APT datasets by accounting for Poisson statistics during eigenanalysis.
* **Model Interpretation & Caveat:** A key distinction is made between the native atom probe model and the MVSA model: while the native model predicts specific atoms (including isotopes) at precise locations, the MVSA model predicts only the presence of phase-characteristic atoms based on their relative natural abundances.
* **Component Identification:** Eigenanalysis of the two-phase nickel-base superalloy revealed three significant principal components (PCs): PC1 and PC2 describe the compositional similarities and differences between the primary bulk phases, while PC3 identifies a distinct third component located at the interface.
* **Interface Characterization:** The third component (PC3) reveals unexpected interfacial chemistry, characterized by an increased abundance of singly charged metal ions (relative to the doubly charged ions dominant in the bulk) and the presence of metal oxides not found in the primary phases.
* **Statistical Validation:** To distinguish signal from noise, the researchers used eigenvalue plots where the "noise floor" is estimated by the number of voxels in the dataset; a slight slope in sorted eigenvalues is expected due to weighting by the degrees of freedom in the noise covariance estimate.
- pages 9-10: **Lab Notebook Summary: Multivariate Statistical Analysis (MVSA) in APT**

* **Methodology:** The study utilizes Multivariate Statistical Analysis (MVSA), specifically Principal Component Analysis (PCA), to analyze APT datasets of Ni-base superalloys. PCA was selected for its computational efficiency and its mathematical guarantee of providing the best least-squares fit for a $p$-component factor model.
* **Advantages over Manual Segmentation:** Unlike traditional image processing/segmentation, which requires "foreknowledge" of specific masses and is prone to analyst bias, PCA allows for the automated discovery of chemical phases, spectral characteristics, and spatial distributions without preconceived notions about the sample composition.
* **Sensitivity to Trace Species:** The MVSA approach excels at identifying subtle chemical variations and low-concentration species (e.g., oxides at interfaces) that are too tedious or difficult to characterize using univariate/manual data analysis methods. 
* **Key Findings & Application:** The method successfully identified phase-specific partitioning of trace elements, revealing that Nb and Ta are more prevalent in the Ni-rich phase than in the Cr/Co-rich phase, with PCA scores correlating closely with observed total ion intensity.
- pages 10-11: **Lab Notebook Summary: Multivariate Statistical Analysis of APT Data**

* **Limitations of PCA:** While Principal Component Analysis (PCA) is effective for variance maximization, it lacks a basis in physical principles. This often results in "unphysical" or abstract outputs, such as negative spectral features in loading vectors.
* **Alternative Methods for Physical Interpretability:** To achieve more physically realistic (e.g., non-negative) components, Multivariate Curve Resolution (MCR) or abstract factor rotations can be employed. The text notes a specific mathematical error in the previously published "spatial simplicity PCA" (SS-PCA) regarding the rotation of orthonormal loadings versus orthogonal scores.
* **Computational Scale & Data Volume:** APT datasets are extremely large; for example, a nickel-base superalloy sample containing ~56 million ions and ~190 million voxels would require approximately 280 GB of storage if represented as a dense, double-precision matrix.
* **Efficient Data Processing via Sparsity:** To make Multivariate Statistical Analysis (MVSA) computationally feasible, it is essential to exploit the inherent sparsity of APT data. Utilizing sparse matrix formats (such as triplet or compressed-column formats in Matlab) significantly reduces storage requirements and enables efficient linear algebra operations.
- pages 11-12: **Summary of APT Data Processing and Multivariate Statistical Analysis (MVSA)**

* **Data Compression & Efficiency:** Utilizing sparse matrix representation and binning spectra to the atomic scale significantly reduces storage requirements (by up to a factor of 160). For MVSA, spectra containing only a single count can be safely ignored because they provide no information regarding interchannel correlations, which are essential for PCA.
* **Computational Scaling & Methods:** While PCA computation is nearly "no-cost" at the atomic scale, the time required for eigenanalysis scales by $n^3$ relative to spectral resolution ($n$ = number of mass bins). To mitigate this, software like AXSIA can be used to compute only the most significant eigenvalues (e.g., the top 64) to maintain efficiency during high-resolution analysis.
* **Workflow & Instrumentation Details:** Converting raw `.pos` files to Matlab format incurs a large memory overhead due to Matlab limitations; therefore, this conversion should ideally be performed at the instrument workstation rather than on a mobile computer. Once converted, PCA can be executed on standard hardware (e.g., a laptop with 2 GB RAM).
* **Spectral Resolution Trade-offs:** Increasing spectral resolution (e.g., from $1/2$ Da to $1/12$ Da) for improved mass assignment does not significantly impact memory requirements when using sparse storage, but it does increase the time required for eigenanalysis of the data cross-product matrix.
- pages 12-13: **Lab Notebook Summary: Multivariate Statistical Analysis (MVSA) in APT**

* **Methodological Advantage:** MVSA provides an unbiased approach to chemical extraction by eliminating the need for manual Region of Interest (ROI) selection or specific mass channel selection; analysis performed on subsets/ROIs yields results consistent with the complete dataset.
* **Computational Optimization & Visualization:** To prevent storage requirements from exceeding the raw data size—a common issue when supplying full score matrices to 3D visualization tools—it is efficient to separate loading computation from score computation and store only the indices of non-zero scores.
* **Multi-resolution Scalability:** Scores at a desired spatial resolution can be estimated using loadings derived from a different resolution (provided they span the same spectral space), allowing for flexible analysis without the need to recompute the full PCA factorization.
* **Instrumental Physics & Resolution Caveat:** While atoms cannot physically occupy the same location, the inherent precision limits of the APT instrument cause single-atom detections to act as random samples from a local neighborhood; this allows MVSA to successfully exploit interelement correlations even at the atomic scale.
- page 13: **Summary of MVSA Application to Atom Probe Tomography (APT)**

* **Application & Capability:** Multivariate Statistical Analysis (MVSA) enables the unbiased identification of atomic-scale chemical neighborhoods and interfaces (e.g., discovering unexpected oxygen-enriched interfaces in Ni-base superalloys) without requiring *a priori* knowledge of species or locations.
* **Statistical Nature of High-Resolution Data:** At the atomic scale (e.g., 0.2 nm voxels), APT data is approximately Poisson-distributed with an extremely low signal-to-noise ratio (SNR < 1). For instance, $^{58}\text{Ni}$ may appear in only ~5% of voxels at this resolution.
* **Critical Methodological Caveat:** Standard variance-based methods like PCA may fail by treating random fluctuations as signals; it is essential to use MVSA procedures specifically designed to account for Poisson noise. Note that data binned more coarsely ($\ge 1\text{ nm}$) deviates from a Poisson distribution and requires different statistical treatment.
* **Computational Implementation:** To handle massive datasets (e.g., $>50$ million 200-channel mass spectra) without exceeding memory limits—which would exceed 75 GB if stored as a dense matrix—a sparse format approach is required. This allows for efficient, rapid MVSA processing on standard computational hardware.
