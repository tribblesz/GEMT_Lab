---
date created: 2026-04-10
author: "StarDustX"
note type: pdf-summary
resource type: apt-fim-literature
source pdf: "[[Resources/APT-FIM/PDFs/atomic-scale-phase-composition-through-multivariate-statistical-analysis-of-atom-probe-tomography-data.pdf]]"
provider: "lmstudio"
model: "gemma-4-26B-A4B-it-Q4_K_M"
tags:
  - "#resource/pdf-summary"
  - "#apt"
  - "#fim"
---

# atomic-scale-phase-composition-through-multivariate-statistical-analysis-of-atom-probe-tomography-data

## Source PDF

[[Resources/APT-FIM/PDFs/atomic-scale-phase-composition-through-multivariate-statistical-analysis-of-atom-probe-tomography-data.pdf]]

## Overview
Multivariate Statistical Analysis (MVSA), specifically Poisson-scaled Principal Component Analysis (PCA), is used to identify chemical phases in 3D atom probe tomography (APT) data at full spatial resolution ($\sim$0.2 nm). This approach enables the automated, unbiased discovery of chemical components and their spatial distributions without requiring prior knowledge of species or manual region-of-interest (ROI) selection. By predicting the probability of atom types at each voxel, the method maintains the instrument's native resolution and avoids the 125-fold loss of volumetric resolution associated with traditional $\sim$1 nm$^3$ binning.

## Key Findings
* **Phase Identification:** In Ni-base superalloys, MVSA identified three significant principal components: PC1 and PC2 described bulk phase compositional differences, while PC3 identified a distinct interfacial component characterized by increased metal oxides and a higher ratio of singly to doubly charged ions.
* **Trace Element Detection:** The method successfully identified subtle chemical variations and trace partitioning of Nb and Ta between Ni-rich and Cr/Co-rich phases.
* **Isotope Quantification:** Poisson-scaled PCA successfully recovered nickel isotope abundances consistent with natural abundance, whereas standard PCA was heavily biased by the primary isotope signal.
* **Signal vs. Noise:** In high-resolution Ni-base superalloy datasets, experimental noise was found to be the dominant source of variance, accounting for approximately 93.7% of total variance, with only 6.3% representing the underlying chemical model.

## Methods And Instrumentation Notes
* **Instrumentation:** Analysis was performed on a Cameca LEAP 3000X HR in voltage-pulsed mode (37% detection efficiency) using Ni-base superalloys prepared via the "matchstick method" and electropolishing ($10\% \text{HClO}_4$ in acetic acid).
* **Statistical Approach:** The method utilizes Eigenanalysis/SVD and a "Poisson-scaled PCA" approach. Data is preprocessed by scaling it with the inverse square root of the mean spectrum to drive the noise covariance matrix toward an identity matrix. 
* **Computational Strategy:** To manage massive datasets (e.g., $>50$ million ions), the implementation utilizes sparse matrix formats (triplet or compressed-column) and "out-of-core" algorithms in MATLAB. This prevents memory exhaustion and allows processing on standard hardware by focusing on mass spectra with $\ge 2$ total counts and ignoring zero-count voxels.
* **Modeling:** The approach assumes a linear additive model where measured spectra are the sum of pure-component spectra weighted by local abundances.

## Relevance To APT/FIM
* **Resolution Preservation:** Unlike traditional binning, MVSA works at the atomic scale ($\sim$0.2 nm), preserving the instrument's high longitudinal ($0.06\text{ nm}$) and lateral ($<1\text{ nm}$) precision.
* **Handling Sparsity:** The method is specifically designed for the extreme sparsity and high dimensionality of APT data, where many voxels contain $<1$ ion on average.
* **Overcoming Univariate Limits:** While APT is inherently "univariate" (detecting single atoms), MVSA exploits interelement correlations to resolve multi-channel chemical information.

## Open Questions
* **Physical Realism:** Because PCA is based on variance maximization rather than physical principles, it can produce "unphysical" results, such as negative spectral features in loading vectors; alternative methods like Multivariate Curve Resolution (MCR) may be required for non-negative components.
* **Statistical Limits of Binning:** While the method is robust at the atomic scale, the statistical nature of the data changes at coarser resolutions ($\ge 2\text{ nm}$), where it deviates from a Poisson distribution and variance becomes a quadratic function of the mean.
* **Noise Estimation:** Since the true noise covariance matrix is unknown, it must be estimated from the data, resulting in a characteristic slope in eigenvalue plots rather than a flat noise floor.
* **Score Contamination:** Estimated scores ($T$) remain subject to "collinear noise," representing the projection of experimental noise into the space spanned by spectral loadings.

## Citation Trail

- pages 1-2: **Lab Notebook Summary: Multivariate Statistical Analysis (MVSA) of APT Data**

* **Objective & Method:** The paper demonstrates using Multivariate Statistical Analysis (MVSA)—specifically Principal Component Analysis (PCA)—to identify chemical phases in 3D atom probe tomography (APT) data at full spatial resolution ($\sim$0.2 nm). This avoids the traditional method of binning atoms into $\sim$1 nm$^3$ volumes, which results in a 125-fold loss of volumetric resolution.
* **Data Characteristics & Instrumentation:** APT datasets are characterized by extreme sparsity and high dimensionality, often comprising hundreds of millions of individual spectra. Due to imperfect detection efficiency, the average spectrum is extremely sparse, frequently containing less than one total count per spectrum.
* **Key Challenges (Caveats):** Because the data is so sparse, the variance is almost entirely dominated by counting noise, testing the fundamental limits of statistical analysis. Furthermore, applying MVSA is non-trivial because APT data is inherently "univariate" (detecting single atoms one at a time) rather than providing simultaneous multi-channel observations.
* **Computational Implementation:** The authors present efficient numerical approaches for performing PCA on these massive datasets, showing that the dimensionality reduction and extraction of latent variables (representing chemical phases) can be completed in seconds on a standard laptop computer.
- pages 2-3: **Summary: Multivariate Statistical Analysis (MVSA) of APT Data**

* **Methodology & Objective:** The study demonstrates that MVSA (specifically PCA) can resolve atomic-scale chemical-phase composition by predicting the probability of atom types at each voxel rather than specific atom locations. This approach allows for the discovery of elemental relationships while maintaining the instrument's native spatial resolution.
* **Instrumentation & Sample Preparation:** Data was collected from a Ni-base superalloy prepared via the "matchstick method" and electropolishing (10% $\text{HClO}_4$ in acetic acid). Analysis was performed on a Cameca LEAP 3000X HR in voltage-pulsed mode, featuring a detection efficiency of 37% and high positioning precision ($<1\text{ nm}$ lateral; up to $0.06\text{ nm}$ longitudinal/Z-axis).
* **Computational Challenges & Strategy:** Due to low detection efficiency, APT datasets are extremely sparse, with many voxels containing $<1$ ion on average. To make MVSA computationally tractable on standard hardware, the analysis was restricted to mass spectra containing $\ge 2$ total counts, which provides sufficient information for interatom correlation without processing millions of empty voxels.
* **Statistical Modeling:** Simulations were used to validate the approach, utilizing a multinomial distribution model based on the five naturally occurring Ni isotopes and an FCC crystal structure ($a = 0.352\text{ nm}$). This accounts for the probabilistic nature of ion detection (where outcomes include either a specific isotope or no detection).
- pages 3-4: **Lab Notebook Summary: Multivariate Statistical Analysis (MVSA) for APT Data**

* **Methodology & Model Assumption:** The approach utilizes Principal Component Analysis (PCA) to decompose APT spectral datasets based on a linear additive model. It assumes that any measured spectrum is the sum of pure-component spectra ($S_0$) weighted by their local abundances ($A_0$), allowing the extraction of chemical information through the identification of orthogonal loading vectors ($P$).
* **APT/FIM Relevance:** The technique is specifically applied to resolve phase compositions in high-resolution datasets (e.g., nickel-base superalloys). It is particularly critical for APT data binned at the atomic scale, where experimental noise—rather than chemical variation—often becomes the dominant source of signal variance.
* **Computational Approach:** To recover the underlying chemical model from noisy raw data ($D$), the method involves calculating the eigenvectors of the raw data cross-product matrix ($D^T D$). By sorting these eigenvectors by descending eigenvalue magnitude, the $p$ most significant eigenvectors are identified as the true chemical loading vectors ($P_0$), with scores ($T$) estimated via $T = DP_0$.
* **Critical Caveats:** 
    * **Noise Dominance:** Because noise is the primary source of variation in atomic-scale APT, it cannot be ignored; however, the model remains valid if the error is assumed to be zero-mean and uncorrelated (identity covariance).
    * **Component Distortion:** The principal components of noisy raw data are not mathematically identical to the true underlying chemical components ($T_0$ and $P_0$), though they can be recovered through eigenvalue sorting. 
    * **Score Contamination:** Estimated scores ($T$) are subject to "collinear noise," meaning they represent the true model scores plus the projection of experimental noise into the space spanned by the spectral loadings.
- pages 4-5: **Summary: Multivariate Statistical Analysis (MVSA) of APT Data**

* **Noise Modeling & Statistical Assumptions:** Because binned APT data follows an approximate Poisson distribution, the error covariance matrix can be estimated *a priori* as a diagonal matrix using the mean spectrum. This approach bypasses the issue where particle-counting techniques violate standard assumptions of identity noise covariance matrices.
* **Methodology (Eigenanalysis/SVD):** The method utilizes Eigenanalysis and Singular Value Decomposition (SVD) to extract principal components. By applying a scaling transformation ($C^{-1/2}$), the data is transformed into a space where statistical assumptions are met, allowing for the calculation of physical-space loadings and scores through an "oblique" rotation.
* **Computational Efficiency & Large Datasets:** The implementation uses a rotation approach that facilitates "out-of-core" algorithms. This allows researchers to process massive APT datasets that exceed core memory capacity by deferring the calculation of spatial components until after the rotation matrix is determined.
* **Important Caveat (Spatial vs. Spectral Scaling):** While spectral scaling is necessary, scaling in the *spatial* domain should be avoided for APT. Unlike EDXS or TOF-SIMS, APT detection efficiency is independent of atom type and densities are relatively uniform; attempting to model noise per voxel can have deleterious effects on the derived components.
* **Data Format:** Raw mass spectral data is processed from `.pos` files (position-tagged masses), which utilize a sparse storage format to manage large-scale position-tagged datasets efficiently.
- pages 5-6: **Lab Notebook Summary: Multivariate Statistical Analysis (MVSA) of APT Data**

* **Computational Methods:** Large APT datasets are processed using MATLAB with sparse-matrix operations to maintain efficiency. To prevent memory exhaustion during large-scale cross-product calculations, custom C/MEX-files were implemented to avoid unnecessary data duplication in the MATLAB environment.
* **Noise Dominance in High-Resolution APT:** At high spatial resolutions (e.g., 0.2 nm voxels), noise significantly outweighs chemical signal. In a tested homogeneous Ni-base superalloy, approximately 93.7% of the total variance was attributed to noise, with only 6.3% representing the underlying chemical model.
* **Preprocessing via Poisson-Scaling:** To prevent Multivariate Statistical Analysis (such as PCA) from identifying "structure in the noise" rather than actual chemistry, the data must be preprocessed. The authors recommend scaling the data by the inverse square root of the mean spectrum to drive the noise covariance matrix toward an identity matrix.
* **Statistical Caveats:** The effectiveness of this scaling method is strictly dependent on the assumption that the atom detection process follows a Poisson distribution. In high-resolution binning where counts per voxel are extremely low ($\approx$ 0.29 counts/voxel), the validity of the MVSA results must be verified by comparing experimental count histograms against predicted Poisson models.
- pages 6-7: **Lab Notebook Summary: Multivariate Statistical Analysis (MVSA) in APT**

*   **Methodology (PCA & Noise Reduction):** The study utilizes Principal Component Analysis (PCA) on raw ROI spectral data to differentiate structural features from noise. By applying "Poisson-scaled PCA," the researchers can account for Poisson noise; a successful implementation is indicated when eigenvalues corresponding to noise match the summed spectrum, effectively isolating significant components from background fluctuations.
*   **Instrumentation & Simulation Parameters:** Simulations were modeled after the **LEAP 3000X HR**, specifically incorporating a detection efficiency of **37%**. The study tested the ability of MVSA to recover Ni isotope abundances by simulating atom-by-atom sampling, treating the multi-channel isotopic spectrum as a multivariate observation.
*   **Statistical Caveats (Poisson vs. Quadratic Variance):** A critical limitation is that APT data only follows a Poisson distribution when atom detection within a voxel is a "rare event." As spatial binning increases (coarser voxels), the data deviates significantly from Poisson behavior; specifically, once bins reach approximately **2 nm**, the variance becomes a quadratic function of the mean.
*   **Data Distribution Modeling:** While the underlying multinomial distribution (due to discrete isotope counts) governs the true nature of the measurement, the authors note that it can be accurately approximated by a Poisson distribution in the limit of large observations and low-probability events.
- pages 7-8: **Summary: Multivariate Statistical Analysis (MVSA) for APT Isotope Quantification**

* **Methodological Improvement:** Standard Principal Component Analysis (PCA) is ineffective for determining relative isotope abundances in APT because it overweights high-magnitude noise in major spectral features (e.g., $^{58}\text{Ni}$) due to the Poisson nature of the data (where variance equals the mean). The authors propose a "Poisson-scaled PCA" (MVSA) to accurately recover true isotopic distributions by accounting for this variance.
* **Instrumentation & Precision Modeling:** To test the limits of MVSA, simulations incorporated realistic APT reconstruction errors, applying Gaussian root-mean-square precision of $0.2\text{ nm}$ in lateral dimensions and $0.1\text{ nm}$ in depth. 
* **Spatial Binning & Statistical Validity:** The study demonstrates that MVSA is robust even when data is binned at the single-atom scale (e.g., $0.2\text{ nm}$ voxels). While instrumental precision and lattice geometry (such as atoms centered near tetrahedral holes) can cause multiple atoms to appear within a single voxel, the resulting atom counts follow a predictable Poisson distribution, allowing for accurate statistical estimation of composition.
* **Validation Results:** In large-scale simulations ($~10$ million atoms), Poisson-scaled PCA successfully recovered nickel isotope abundances that were quantitatively consistent with natural abundance, whereas standard PCA loadings were heavily biased by the primary isotope signal.
- pages 8-9: **Lab Notebook Summary: MVSA of Ni-Base Superalloys**

* **Methodology:** The study utilizes Multivariate Statistical Analysis (MVSA) via Poisson-scaled Principal Component Analysis (PCA) to identify chemical phases in Ni-base superalloy APT data. Data was processed using spatial binning into 0.2 nm cubes, with eigenvalues scaled to account for Poisson statistics.
* **Phase Identification:** Eigenanalysis revealed three significant principal components (PCs): PC1 and PC2 describe the compositional differences between the major bulk phases, while PC3 identifies a distinct interfacial component characterized by an increased abundance of metal oxides and a higher ratio of singly charged to doubly charged ions.
* **Model Interpretation:** A key distinction is noted between the "native" APT model (predicting specific atoms at specific sites) and the MVSA model; the latter predicts the presence of a phase based on isotopic relative abundance rather than discrete atomic placement.
* **Technical Caveats:** Because the true noise covariance matrix is unknown, it must be estimated from the data. This requires weighting successive eigenvalues by their degrees of freedom, which results in a characteristic slope in the eigenvalue plot rather than a perfectly flat "noise floor" at the number of voxels.
- pages 9-10: **Summary: Multivariate Statistical Analysis (MVSA) of APT Data**

* **Methodology:** The study utilizes Principal Component Analysis (PCA)—specifically a Poisson-scaled PCA method—to extract chemical information from large Atom Probe Tomography (APT) datasets of Ni-base superalloys. PCA was selected for its computational efficiency and its mathematical optimality in a least-squares fitting sense.
* **Automated Phase Identification:** Unlike standard image processing/segmentation, which requires "foreknowledge" of specific masses to define criteria, MVSA allows for the automated discovery of the number of components, their spectral characteristics, and spatial distributions without preconceived notions or analyst bias.
* **Sensitivity to Trace Elements:** The MVSA approach is highly effective at identifying subtle chemical variations and low-concentration species (e.g., oxide species at interfaces) that are difficult to characterize using manual univariate analysis. It successfully identified trace partitioning of Nb and Ta between the Ni-rich and Cr/Co-rich phases.
* **Key Caveat:** Traditional manual segmentation is prone to introducing bias and may fail to detect small but significant spectral features if the analyst does not pre-select the relevant mass ranges for analysis.
- pages 10-11: **Lab Notebook Summary: Multivariate Statistical Analysis of APT Data**

* **Limitations of PCA:** While widely used, Principal Component Analysis (PCA) is based on mathematical orthogonality and variance maximization rather than physical principles. This often results in "unphysical" or abstract interpretations, such as negative spectral features in loading vectors.
* **Alternative Analytical Methods:** To achieve physically realistic, non-negative components, Multivariate Curve Resolution (MCR) or factor rotations can be employed. Note that the "Spatial Simplicity PCA" (SS-PCA) method described by Parish and Miller (2010) contains mathematical inaccuracies regarding the rotation of orthonormal loading vectors.
* **Computational Scale & Data Management:** APT datasets are extremely large; a single nickel-base superalloy sample can contain >56 million ions and ~190 million voxels. Storing this as a dense 4D matrix (with 200-channel mass spectra) would require approximately 280 GB of storage, making standard dense-matrix processing unfeasible.
* **Efficient Processing via Sparsity:** Successful Multivariate Statistical Analysis (MVSA) on large datasets requires exploiting the inherent sparsity of APT data. Utilizing sparse matrix formats (e.g., triplet format or Matlab’s compressed-column format) is essential to reduce storage requirements and enable efficient linear algebra operations.
- pages 11-12: **Lab Notebook Summary: Multivariate Statistical Analysis (MVSA) of APT Data**

* **Data Optimization & Storage:** Utilizing sparse matrix representations for APT datasets significantly reduces storage requirements (up to 160x less than dense-matrix formats). Memory efficiency is further enhanced by binning spectra to the atomic scale and ignoring zero-count voxels, provided that spatial indices are retained to ensure accurate 3D reconstruction.
* **Methodological Filtering:** For PCA-based analysis, spectra containing only a single count can be safely excluded from the dataset without degrading the quality of principal component loadings. This is because single-count spectra provide no information regarding the interchannel correlations essential to MVSA.
* **Computational Scaling & Efficiency:** The computational cost of eigenanalysis scales at $O(n^3)$, where $n$ is the number of mass bins (spectral resolution). To mitigate the time required for high-resolution datasets (e.g., 1/12 Da), it is highly effective to compute only a truncated subset of significant eigenvalues/vectors (e.g., the top 64), as implemented in AXSIA software.
* **Workflow Caveats:** The conversion of raw `.pos` files to analysis-ready formats (e.g., Matlab) incurs heavy memory overhead due to software limitations; this process should ideally be performed at the instrument rather than on standard workstations. While PCA computation itself is extremely fast ("no-cost"), the initial data loading and file conversion are the primary bottlenecks.
- pages 12-13: **Summary: Multivariate Statistical Analysis (MVSA) in APT Data Processing**

* **Methodology & Bias Reduction:** MVSA allows for the extraction of chemical information without the analyst-induced bias typically associated with manual Region of Interest (ROI) selection or specific mass channel selection. The analysis is robust, as results derived from specific ROIs are consistent with those obtained from the complete dataset.
* **Computational Efficiency for 3D Visualization:** To prevent storage requirements from exceeding the original data matrix when using 3D visualization tools, it is recommended to decouple the computation of principal-component *loadings* from the *scores*. Scores can be estimated at an appropriate spatial resolution using loadings derived from a different resolution, provided the spectral basis vectors span the same space.
* **APT Spatial Resolution & Correlation:** While APT detects single ions, the inherent precision limits of the instrument mean that detected atoms are effectively random samples drawn from a local neighborhood. MVSA exploits these interelement correlations to automate and identify phase compositions at the full spatial resolution of the atom probe.
- page 13: **Summary: Multivariate Statistical Analysis (MVSA) of Atomic-Scale APT Data**

* **Objective & Application:** MVSA enables the unbiased identification of atomic-scale neighborhoods and chemical phases without prior knowledge of species or locations. The method was successfully demonstrated on a Ni-base superalloy, identifying both expected two-phase zones and an unexpected oxygen-enriched interface.
* **Statistical Caveats (Noise Handling):** At high resolutions (e.g., 0.2 nm voxels), APT data exhibits a very low signal-to-noise ratio (SNR < 1) and follows a Poisson distribution. Standard variance-based methods like PCA are prone to mistaking random noise for informative signals; therefore, specific procedures for handling Poisson-distributed data are required to accurately discriminate chemical information from noise.
* **Binning Effects:** The statistical nature of the data changes with spatial resolution; while 0.2 nm voxels are approximately Poisson-distributed, coarser binning ($\ge$ 1 nm) deviates significantly from Poisson statistics and requires different analytical considerations.
* **Computational Implementation:** To manage massive datasets (e.g., $>50$ million 200-channel mass spectra), which would exceed 75 GB in a dense matrix format, the authors utilize a sparse matrix approach. This allows for efficient processing of large-scale spectral images on modest hardware within seconds.
