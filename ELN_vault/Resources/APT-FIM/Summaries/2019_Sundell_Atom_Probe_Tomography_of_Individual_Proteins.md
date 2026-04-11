---
date created: 2026-04-10
author: "StarDustX"
note type: pdf-summary
resource type: apt-fim-literature
source pdf: "[[Resources/APT-FIM/PDFs/2019_Sundell_Atom_Probe_Tomography_of_Individual_Proteins.pdf]]"
provider: "lmstudio"
model: "gemma-4-26B-A4B-it-Q4_K_M"
tags:
  - "#resource/pdf-summary"
  - "#apt"
  - "#fim"
---

# 2019_Sundell_Atom_Probe_Tomography_of_Individual_Proteins

## Source PDF

[[Resources/APT-FIM/PDFs/2019_Sundell_Atom_Probe_Tomography_of_Individual_Proteins.pdf]]

## Overview
The study presents a novel method for the 3D structural and chemical analysis of individual proteins (using rabbit IgG as a model) via Atom Probe Tomography (APT). To overcome the mechanical challenges of analyzing soft matter under high electric fields, proteins are encapsulated within an amorphous solid silica matrix using a room-temperature sol-gel process. This approach provides the necessary structural support to withstand field-induced "Maxwell stresses" that otherwise cause deformation or fracture in biological specimens.

## Key Findings
* **Structural Validation:** 3D reconstructions of embedded IgG showed high agreement with established Protein Data Bank (P2B) crystal structures (e.g., 1HZH, 4GDQ), achieving an estimated resolution of $\sim$15 Å for the Fab loop.
* **Chemical Identification:** APT mass spectra successfully identified organic traces, specifically $CNH_2^+$ and $CO_2^+$ (representing amine and carboxyl groups). Carbon quantification (~6405 atoms) aligned with literature values for rabbit IgG.
* **Matrix Optimization:** A sodium silicate-based sol-gel process at pH 7 was found to better preserve the protein's monomeric "Y-shaped" state compared to acidic TEOS-derived silica, which can trigger aggregation in the Fc region.
* **Hydration Removal:** The sol-gel process effectively replaced the protein's hydration shell, as evidenced by the absence of characteristic water peaks (17, 18, and 19 Da).

## Methods And Instrumentation Notes
* **Sample Preparation:** 
    * **Embedding:** Sol-gel encapsulation using TEOS or sodium silicate precursors.
    * **Tip Fabrication:** *In situ* lift-out and sharpening via FIB-SEM (FEI Versa 3D) to achieve tip radii $<100\text{ nm}$ (specifically reaching $<50\text{ nm}$ through annular ion milling). Specimens were attached to Si microtip posts using Pt deposition.
    * **Verification:** TEM was used to verify the preservation of the monomeric structure; SEM and BET surface area analysis were used for characterization.
* **APT Instrumentation:** 
    * **System:** Imago LEAP 3000 X HR operating in laser-pulsed mode.
    * **Parameters:** Green laser ($\lambda = 532\text{ nm}$); pulse frequencies of $100\text{--}200\text{ kHz}$; pulse energies of $0.25\text{--}0.5\text{ nJ}$.
    * **Conditions:** Base temperatures of $30$ or $50\text{ K}$ under ultra-high vacuum ($<10^{-8}\text{ Pa}$).
* **Data Processing:** 
    * **Software:** Reconstruction via Cameca IVAS (v3.4.3/3.6.6) using a voltage evolution protocol; structural analysis via UCSF Chimera.
    * **Parameters:** Field factor $k_f = 5$; atom volume of $0.02\text{ nm}^3$; voxel grid of $0.2\text{ nm}^3$ with delocalization parameters ($1.0\text{ nm}$ for $x,y$; $0.5\text{ nm}$ for $z$).

## Relevance To APT/FIM
* **Overcoming Soft Matter Limitations:** Provides a solution to the mechanical instability of biological molecules under high electric fields ($>1 \text{ V \AA}^{-1}$).
* **Complementary Technique:** Serves as a powerful complement to X-ray crystallography, NMR, and cryo-EM by providing simultaneous sub-nanometer 3D structural mapping and mass spectrometry-based chemical identification.
* **Versatility:** Promising for studying proteins with low crystallization propensity or those requiring atomic-scale analysis via isotopic labeling.

## Open Questions
* **Spectral Overlap & Quantification:** Identification of nitrogen ($N^+$ vs $Si^{2+}$) and sulfur (obscured by $O^{2+}$) is severely limited by peak overlaps, making reliable atomic quantification difficult for elements other than carbon.
* **Structural Integrity:** It remains unknown if the water-to-silica exchange in the sol-gel process induces conformational changes or if evaporation field mismatches between the protein and matrix cause reconstruction distortions.
* **Resolution Limits:** While the monomer shape is preserved, current methods cannot detect changes in secondary structure or amino acid side-chain rearrangements.

## Citation Trail

- pages 1-2: **Summary: 3D Structural and Chemical Analysis of Individual Proteins via APT**

* **Methodology & Sample Prep:** The study demonstrates a novel approach for analyzing individual proteins (using IgG as a model) by encapsulating them within an amorphous solid silica matrix via a sol-gel process. This synthesis is specifically tuned to mimic physiological conditions and provides the necessary structural support required for atom probe analysis.
* **APT Instrumentation & Physics:** The technique utilizes field evaporation of ions/molecules from a needle-shaped specimen (radius < 100 nm) driven by high electric fields ($> 1 \text{ V \AA}^{-1}$) and short laser pulses. 3D reconstruction is achieved by recording X-Y impact positions on a position-sensitive detector, determining the Z-coordinate through ion sequence, and calculating mass-to-charge ratios via time-of-flight.
* **Analytical Relevance:** APT serves as a powerful complement to X-ray crystallography, NMR, and cryo-EM by providing simultaneous sub-nanometer 3D structural mapping and mass spectrometry-based chemical identification. It is particularly promising for studying proteins with low crystallization propensity or those requiring atomic-scale chemical analysis via isotopic labeling.
* **Validation & Findings:** 3D reconstructions of the embedded IgG showed high agreement with established protein data bank (PDB) crystal structures, validating the silica-embedding strategy as a viable method for biological molecule analysis.
- pages 2-3: **Summary: Atom Probe Tomography of Individual Proteins (Sundell et al., 2019)**

* **Challenge in APT of Soft Matter:** High electric fields during APT induce significant "Maxwell stresses," leading to mechanical deformation or premature fracture of soft biological specimens. This has historically prevented routine analysis of proteins, with only rare exceptions (e.g., ferritin).
* **Methodology (Sol-Gel Embedding):** To provide necessary mechanical integrity, proteins (specifically rabbit IgG) are embedded in a solid silica matrix via a room-temperature sol-gel process using TEOS or sodium silicate precursors. This glassy matrix allows the specimen to withstand field-induced stresses during field evaporation without requiring modifications to standard APT reconstruction protocols.
* **Instrumentation & Workflow:** Specimens are prepared using FIB-SEM for *in situ* lift-out and tip-sharpening (achieving a radius <100 nm). Analysis is performed via pulsed laser-induced field evaporation, utilizing position-sensitive time-of-flight mass spectrometry to achieve 3D reconstruction with near-atomic resolution.
* **Critical Experimental Caveats:** Successful analysis requires balancing matrix density with protein stability. While acidic TEOS-derived silica produces a dense, mechanically stable matrix capable of withstanding APT stresses, the low pH can trigger IgG aggregation (particularly in the Fc region). Conversely, sodium silicate-based synthesis at pH 7 was found to better preserve the monomeric state of the protein.
- pages 3-4: **Summary: Atom Probe Tomography of IgG in Silica Matrix**

* **Methodology & Sample Preparation:** Individual IgG proteins were encapsulated in an amorphous silica matrix using a water glass (sodium silicate) sol-gel process. To prevent protein aggregation, the pH was adjusted to physiological levels via an acidic ion exchange column. Specimens were prepared as electron-transparent foils using FIB-SEM, with TEM used to verify the preservation of the characteristic "Y-shaped" monomer structure.
* **APT Instrumentation & Reconstruction:** Data reconstruction followed a standard voltage evolution protocol. The inorganic nature of the silica matrix enabled unambiguous mapping of carbon-containing organic species within the protein. While the manufacturer-stated detection efficiency was 37%, carbon quantification (detecting ~6405 atoms) showed strong agreement with literature values for rabbit IgG.
* **Mass Spectrometry & Chemical Identification:** APT mass spectra identified key organic traces, specifically $CNH^{2+}$ and $CO^{2+}$, representing amine and carboxyl functional groups. The sol-gel process appeared to effectively replace the protein's hydration shell, as characteristic water peaks (17, 18, and 19 Da) were absent in the analysis.
* **Technical Caveats & Limitations:** 
    * **Spectral Overlap:** Identification of nitrogen and sulfur is severely limited by peak overlaps; $N^+$ (14 Da) is indistinguishable from $Si^{2+}$, and $S$ atoms are obscured by abundant $O^{2+}$ ions, necessitating isotopic labeling for resolution.
    * **Structural Resolution:** While TEM confirmed monomer shape, it could not detect changes in secondary structure or amino acid side-chain rearrangements caused by the sol-gel process. 
    * **Quantification Limits:** Due to these overlaps, reliable atomic quantification was only possible for carbon.
- pages 4-5: **Summary: Atom Probe Tomography of Individual Proteins (Sundell, 2019)**

* **Methodology & Instrumentation:** The study utilizes a sol-gel process to embed proteins within a silica matrix for APT analysis. Mass spectra of organic components are identified via characteristic $CNH_2^+$ and $CO_2^+$ peaks. The experiment used an APT detector with 37% efficiency, though the authors note that modern commercial detectors can exceed 80%.
* **Resolution & Validation:** While APT spatial resolution is anisotropic (better along the direction of analysis than laterally), the reconstruction showed good agreement with X-ray diffraction reference structures (e.g., PDB 1HZH) in atomic number density maps, achieving an estimated resolution of $\sim$15 Å for the Fab loop.
* **Technical Caveats:** Potential sources of error include conformational changes during the water-to-silica exchange in the sol-gel process and reconstruction distortions caused by evaporation field mismatches between the protein and the silica matrix (though no major voltage drops were observed in this specific study).
* **Sample Requirements:** Successful analysis requires sufficient protein concentration to ensure at least one molecule per analysis volume ($<10^5 \text{ nm}^3$). Standard FIB-SEM preparation is highly efficient, requiring only $\sim$50 fL of material to produce multiple needle-shaped specimens.
- pages 5-6: **Summary of Atom Probe Tomography (APT) Methodology: Sundell et al. (2019)**

* **Sample Preparation & Tip Shaping:** Samples were prepared using a standard *in situ* liftout procedure via FIB-SEM (FEI Versa 3D). Wedge segments were attached to Si microtip posts (Cameca) using Pt deposition. Final tip radii ($<50\text{ nm}$) were achieved through annular ion milling patterns with decreasing currents and voltages (from $0.5\text{ nA}$, $30\text{ kV}$ down to $7.7\text{ pA}$, $5\text{ kV}$).
* **APT Instrumentation & Operating Conditions:** Analysis was performed on an Imago LEAP 3000 X HR in laser-pulsed mode using a green laser ($\lambda = 532\text{ nm}$) at frequencies of $100\text{--}200\text{ kHz}$ and pulse energies of $0.25\text{--}0.5\text{ nJ}$. The system was operated at base temperatures of $30$ or $50\text{ K}$ under ultra-high vacuum ($<10^{-8}\text{ Pa}$) with a controlled evaporation rate of $0.0025\text{--}0.005$ ions per pulse.
* **Reconstruction & Data Processing:** 3D reconstructions were performed using Cameca IVAS software (v3.4.3/3.6.6) based on voltage evolution. Key parameters included a field factor $k_f = 5$, an atom volume of $0.02\text{ nm}^3$, and atomic number density heat maps generated via a $0.2\text{ nm}^3$ voxel grid with delocalization parameters of $1.0\text{ nm}$ ($x,y$) and $0.5\text{ nm}$ ($z$).
* **Experimental Context & Caveats:** The method allows for the analysis of single proteins without the chemical ambiguity caused by spectral overlaps. For accuracy, the evaporation field of the silica matrix was verified via SEM ($\approx 27\text{ V \AA}^{-1}$), and protein structures were validated against PDB coordinates (e.g., ID 4GDQ).
- page 6: **Lab Notebook Summary: Sundell et al. (2019) – Atom Probe Tomography of Individual Proteins**

* **Data Reconstruction & Modeling:** For structural comparison, the authors utilized a reference rabbit IgG structure (PDB ID: 4GDQ). The workflow involved converting atomic coordinates from `.PDB` files into `.POS` files to allow for data import and reconstruction within the IVAS software environment.
* **Sample Preparation Method:** A critical component of the experimental setup was a specialized silica embedding procedure (sol–gel process) used to stabilize the protein molecules for analysis.
* **Instrumentation & Characterization:** The study employed Atom Probe Tomography (APT) and Transmission Electron Microscopy (TEM) for primary measurements, supplemented by SEM imaging and BET surface area analysis for sample characterization.
* **Software Tools:** Structural analysis of the IgG molecule was performed using UCSF Chimera (version 1.11.2).
