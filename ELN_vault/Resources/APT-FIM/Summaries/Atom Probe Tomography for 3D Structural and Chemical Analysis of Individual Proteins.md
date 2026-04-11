---
date created: 2026-04-10
author: "StarDustX"
note type: pdf-summary
resource type: apt-fim-literature
source pdf: "[[Resources/APT-FIM/PDFs/Atom Probe Tomography for 3D Structural and Chemical Analysis of Individual Proteins.pdf]]"
provider: "lmstudio"
model: "gemma-4-26B-A4B-it-Q4_K_M"
tags:
  - "#resource/pdf-summary"
  - "#apt"
  - "#fim"
---

# Atom Probe Tomography for 3D Structural and Chemical Analysis of Individual Proteins

## Source PDF

[[Resources/APT-FIM/PDFs/Atom Probe Tomography for 3D Structural and Chemical Analysis of Individual Proteins.pdf]]

## Overview
The study explores the use of Atom Probe Tomography (APT) for the 3D structural and chemical analysis of individual proteins, such as IgG. To overcome the mechanical instability of soft biological molecules under high electric fields (Maxwell stresses), proteins are encapsulated within an amorphous solid silica matrix using a room-temperature sol-gel process (utilizing TEOS or sodium silicate/water glass). This method enables the 3D reconstruction of protein tertiary structures by comparing atomic number density maps against established Protein Data Bank (PDB) reference structures.

## Key Findings
* **Structural Validation:** Reconstructed IgG structures show strong agreement with established crystal structures (e.g., PDB 1HZH, 4GDQ), with TEM confirming the preservation of the "Y-shaped" morphology.
* **Resolution & Sensitivity:** The technique achieved visibility of the Fab loop at $\sim$15 Å resolution; however, detectors with $>80\%$ efficiency could potentially enable near-atomic ($\sim$1 Å) reconstruction. Mass spectrometry successfully identified organic tracers such as $CNH^{2+}$ and $CO^{2+}$.
* **Quantification:** Using a 37% detection efficiency, the reconstructed carbon atom count ($\sim$6405 atoms) demonstrated high agreement with literature values for rabbit IgG.
* **Chemical Mapping:** The presence of carbon-containing ions allows for unambiguous 3D mapping of molecules against the silica background, with potential for atomic-scale mapping via isotopic labeling.

## Methods And Instrumentation Notes
* **Specimen Preparation:** 
    * **Sol-Gel Embedding:** Proteins are embedded in a silica matrix. A critical trade-off exists: acidic synthesis produces a dense, stable matrix but can induce protein aggregation (particularly in the Fc region), while neutral pH prevents aggregation but results in a porous, unstable matrix. Neutralization via an acidic ion exchange column is used to reach physiological pH.
    * **FIB-SEM:** *In situ* lift-out on an FEI Versa 3D FIB-SEM using Pt deposition and trench milling. Final tip sharpening is achieved via annular ion milling (decreasing from $0.5\text{ nA}/30\text{ kV}$ to $7.7\text{ pA}/5\text{ kV}$) to produce radii $<50\text{ nm}$.
* **APT Operating Conditions:** 
    * **Instrument:** Imago LEAP 3000 X HR in laser-pulsed mode ($\lambda = 532\text{ nm}$; frequency: $100\text{--}200\text{ kHz}$; energy: $0.25\text{--}0.5\text{ nJ}$).
    * **Environment:** Base temperatures of $30$ or $50\text{ K}$ under ultra-high vacuum ($<10^{-8}\text{ Pa}$) with a controlled evaporation rate of $0.0025\text{--}0.005$ ions per pulse.
* **Data Processing:** 
    * **Software:** Reconstruction via Cameca IVAS (v3.4.3/3.6.6) using voltage evolution, with structural analysis in UCSF Chimera.
    * **Parameters:** Field factor $k_f = 5$, atom volume of $0.02\text{ nm}^3$, and delocalization parameters ($1.0\text{ nm}$ in $x/y$; $0.5\text{ nm}$ in $z$).

## Relevance To APT/FIM
* **Complementary Technique:** This method serves as a critical complement to X-ray crystallography, NMR, and cryo-EM, particularly for proteins with low crystallization propensity.
* **Unique Capabilities:** Provides a unique combination of sub-nanometer 3D structural resolution and high chemical sensitivity through mass spectrometry.

## Open Questions
* **Structural Integrity:** Whether the sol-gel process or the exchange of water for silica induces conformational changes in hydrophilic side chains, secondary structures, or side-chain rearrangements remains unruled out.
* **Mass Spectrometry Overlaps:** Significant peak overlaps (e.g., $N^+$ vs. $Si^{2+}$ and $S$ vs. $O^{2+}$) currently hinder full chemical identification without isotopic labeling.
* **Reconstruction Artifacts:** The potential for 3D reconstruction distortions due to differences in evaporation fields between the protein and the silica matrix.
* **Hydration & Stability:** The presence of residual hydration cannot be definitively ruled out, and the risk of premature specimen failure remains due to the porous nature of the silica matrix.

## Citation Trail

- pages 1-2: **Summary: 3D Structural and Chemical Analysis of Proteins via APT**

* **Methodology & Sample Preparation:** To overcome the lack of structural support in biological molecules, the study utilizes a sol-gel process to encapsulate model proteins (e.g., IgG) within an amorphous solid silica matrix. This matrix provides the necessary mechanical stability for the specimen to be shaped into the required needle geometry.
* **Instrumentation & Physics:** The technique employs Atom Probe Tomography (APT) principles, using high electric fields ($>1\text{ V \AA}^{-1}$) and short laser pulses to induce field evaporation of ions/molecules from a tip with a radius $<100\text{ nm}$. 3D reconstruction is achieved by recording the lateral position ($X$–$Y$) on a detector, the ion arrival sequence ($Z$), and the mass-to-charge ratio ($m/z$) via flight-time analysis.
* **Analytical Capabilities:** APT provides a unique combination of sub-nanometer 3D structural resolution and high chemical sensitivity (mass spectrometry). The method holds potential for atomic-scale chemical mapping through the use of isotopic labeling.
* **Relevance & Validation:** The approach was validated by demonstrating that reconstructed IgG structures show strong agreement with established crystal structures from the Protein Data Bank (PDB). This method serves as a critical complement to X-ray crystallography, NMR, and cryo-EM, particularly for analyzing proteins with low crystallization propensity.
- pages 2-3: **Summary: Protein Analysis via Atom Probe Tomography (APT)**

* **Challenge in Soft Matter APT:** The high electric fields required for field evaporation induce significant "Maxwell stresses," leading to mechanical fracture and deformation of soft biological specimens, which has historically prevented routine analysis of proteins.
* **Methodology (Sol-Gel Embedding):** To overcome mechanical instability, proteins (e.g., rabbit IgG) are embedded in a solid silica matrix using a room-temperature sol-gel process (utilizing TEOS or sodium silicate precursors). This provides the necessary mechanical integrity to withstand APT stresses while preserving the protein's native functional state.
* **Instrumentation and Specimen Preparation:** Specimens are prepared via *in situ* FIB-SEM lift-out followed by standard tip-sharpening to an ultra-fine radius (<100 nm). Analysis is performed using pulsed laser-induced field evaporation and a position-sensitive time-of-flight (ToF) mass spectrometry detector for 3D reconstruction.
* **Critical Experimental Trade-off:** Successful analysis requires balancing matrix density with protein stability; acidic synthesis conditions produce a high-density silica matrix capable of withstanding APT stresses but can induce protein aggregation (particularly in the IgG Fc region), whereas neutral pH prevents aggregation but results in a porous, mechanically unstable matrix.
- pages 3-4: **Lab Notebook Summary: APT Analysis of IgG in Silica Matrix**

* **Sample Preparation & Method:** IgG proteins were encapsulated in an amorphous silica matrix using a water glass (sodium silicate) sol-gel process. To prevent protein aggregation, the inherently basic sodium silicate was neutralized to physiological pH via an acidic ion exchange column. Specimens were prepared into electron-transparent foils using FIB-SEM; while TEM confirmed the preservation of the "Y-shaped" IgG structure, the resolution was insufficient to rule out sol-gel-induced changes to secondary structures or side-chain rearrangements.
* **APT Reconstruction & Traceability:** Using a standard voltage evolution-based reconstruction protocol, the inorganic silica matrix provided a stable medium that prevented premature specimen fracture during analysis. The presence of carbon-containing ions within the protein allowed for unambiguous 3D mapping of the IgG molecules against the background silica matrix.
* **Mass Spectrometry & Quantification:** Mass spectra identified key organic tracers, specifically $CNH^{2+}$ (amine group) and $CO^{2+}$ (carboxyl group). Based on a manufacturer-stated detection efficiency of 37%, the reconstructed carbon atom count (~6405 atoms) showed high agreement with established literature values for rabbit IgG.
* **Analytical Caveats & Limitations:** Significant peak overlaps hinder full chemical identification: $N^+$ (14 Da) is indistinguishable from $Si^{2+}$, and sulfur ($S$) overlaps with the abundant $O^{2+}$ signal, currently requiring isotopic labeling for differentiation. Furthermore, while characteristic water peaks (17–19 Da) were absent, the presence of residual hydration could not be definitively ruled out.
- pages 4-5: **Summary: Atom Probe Tomography of Individual Proteins**

* **Methodology & Context:** The study utilizes APT to analyze individual proteins (e.g., human IgG) by embedding them in a silica matrix via a sol–gel process (water glass-derived). This allows for the 3D reconstruction of protein tertiary structures by comparing APT atomic number density maps against known X-ray diffraction reference structures (e.g., PDB 1HZH).
* **Instrumentation & Mass Spectrometry:** The analysis was performed with a detector efficiency of 37%, identifying organic ions via characteristic mass spectra peaks such as $\text{CNH}_2^+$ and $\text{CO}_2^+$. While the study achieved visibility of the Fab loop ($\sim$15 Å resolution), the authors note that modern detectors exceeding 80% efficiency could potentially enable near-atomic (1 Å) reconstruction.
* **Spatial Resolution:** APT spatial resolution is anisotropic, performing better along the direction of analysis than laterally. While ideal cases approach 1 Å, biomolecule reconstruction is likely limited to the level of protein tertiary structure due to inherent complexity.
* **Experimental Caveats:** 
    * **Structural Integrity:** The sol–gel process (exchanging water for silica) may induce conformational changes, particularly in hydrophilic side chains.
    * **Reconstruction Artifacts:** Differences in evaporation fields between the protein and the silica matrix can cause 3D reconstruction distortions, though significant voltage drops were not observed in this specific study.
    * **Specimen Stability:** The porous nature of the silica matrix introduces risks of premature specimen failure during the reconstruction protocol.
- pages 5-6: **Lab Notebook Summary: APT Analysis of Encapsulated Proteins**

* **Sample Preparation (FIB-SEM):** Specimens were prepared using a standard *in situ* liftout procedure on an FEI Versa 3D FIB-SEM. Following Pt deposition and trench milling to create a wedge, segments were transferred to Si microtip posts. Final specimen sharpening was achieved via annular ion milling (decreasing from 0.5 nA/30 kV to 7.7 pA/5 kV) to produce sharp tips with radii $<50$ nm.
* **APT Instrumentation & Operating Conditions:** Analysis was conducted on an Imago LEAP 3000 X HR atom probe in laser-pulsed mode ($\lambda = 532$ nm; pulse frequency: 100–200 kHz; energy: 0.25–0.5 nJ). To maintain specimen stability, the base temperature was held at 30 or 50 K under ultra-high vacuum ($<10^{-8}$ Pa), with a controlled evaporation rate of $0.0025\text{--}0.005$ ions per pulse.
* **Reconstruction & Data Processing:** 3D reconstructions were performed using Cameca IVAS software (v3.4.3/3.6.6) based on voltage evolution. Key reconstruction parameters included a field factor $k_f = 5$, an assigned atom volume of $0.02 \text{ nm}^3$, and an estimated silica evaporation field of $\approx 2$ V/Å.
* **Analysis Parameters & Resolution:** Atomic number density heat maps were generated using a $0.2 \times 0.2 \times 0.2 \text{ nm}^3$ voxel grid. To account for reconstruction artifacts, delocalization parameters were applied ($1.0$ nm in $x$ and $y$; $0.5$ nm in $z$). Structural validation was performed by comparing reconstructed data against the IgG protein structure (PDB ID 4GDQ).
- page 6: **Lab Notebook Summary: Protein Analysis via APT/FIM**

* **Data Modeling & Reconstruction:** Structural reference data for rabbit IgG (PDB ID 4GDQ) was prepared by converting `.PDB` atomic coordinates into `.POS` files to allow for integration and analysis within IVAS software.
* **Sample Preparation Method:** The study utilizes a sol-gel based silica embedding procedure to encapsulate the protein molecules, facilitating their preparation for atom probe analysis.
* **Analytical Instrumentation:** A multi-modal characterization approach was employed, combining Atom Probe Tomography (mass spectrometry-based) and TEM imaging with SEM, BET measurements, and fluorescence (FL) imaging.
* **Software Tools:** Molecular structural analysis of the IgG molecule was conducted using UCSF Chimera (version 1.11.2).
