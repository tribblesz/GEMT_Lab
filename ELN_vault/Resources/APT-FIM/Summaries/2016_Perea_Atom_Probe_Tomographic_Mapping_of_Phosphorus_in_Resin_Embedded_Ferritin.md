---
date created: 2026-04-10
author: "StarDustX"
note type: pdf-summary
resource type: apt-fim-literature
source pdf: "[[Resources/APT-FIM/PDFs/2016_Perea_Atom_Probe_Tomographic_Mapping_of_Phosphorus_in_Resin_Embedded_Ferritin.pdf]]"
provider: "lmstudio"
model: "gemma-4-26B-A4B-it-Q4_K_M"
tags:
  - "#resource/pdf-summary"
  - "#apt"
  - "#fim"
---

# 2016_Perea_Atom_Probe_Tomographic_Mapping_of_Phosphorus_in_Resin_Embedded_Ferritin

## Source PDF

[[Resources/APT-FIM/PDFs/2016_Perea_Atom_Probe_Tomographic_Mapping_of_Phosphorus_in_Resin_Embedded_Ferritin.pdf]]

## Overview
The study demonstrates a scalable Atom Probe Tomography (APT) approach to map elemental distributions at complex biological interfaces by embedding horse spleen ferritin in nitrogen-free Lowicryl K4M resin. The method leverages chemical contrast between the iron-rich ferrihydrite core, the protein shell, and the surrounding organic resin to achieve 3D compositional mapping of inorganic-organic and organic-organic interfaces with ppm sensitivity.

## Key Findings
* **Elemental Mapping:** Successfully identified phosphorus (P) enrichment at the surface of the ferrihydrite mineral core (likely as iron phosphate) and a specific spike of sodium (Na) at the mineral/protein interface.
* **Interface Differentiation:** Used nitrogen (N) presence/depletion to distinguish the protein shell from the nitrogen-free resin matrix, and used Fe isotopes to define the mineral core.
* **Structural Observations:** Proxygram analysis revealed an Fe-dominated core followed by a distinct radial composition through the protein shell.

## Methods And Instrumentation Notes
* **Specimen Preparation:** 
    * Ferritin was mixed with Lowicryl K4M resin, UV-cured at $-35\text{ °C}$ for 48 hours (via Leica EMAFS freeze substitution), and prepared using a dual-beam FIB/SEM.
    * A $\sim200\text{ nm}$ Pt/C capping layer was deposited via EBAD to protect the region of interest (identified via EDX mapping of the Fe-L edge).
    * **Gas-Assisted Etching:** $\text{XeF}_2$ was used during FIB milling to increase the milling rate by 3–5x and prevent specimen overheating, pits, or voids in the soft resin.
    * **Tip Engineering:** Specimens were produced via annular milling ($8\text{ kV } ^{69}\text{Ga}^+$) with end diameters $<100\text{ nm}$. A $10\text{--}20\text{ nm}$ conformal Cr coating was sputtered onto the tips to enhance mechanical stability and electrical conductivity.
* **APT Parameters & Optimization:**
    * **Instrument:** LEAP 4000X-HR using a $355\text{ nm}$ UV laser at $44.1\text{ K}$.
    * **Mass Spectral Optimization:** Laser energy was increased to $450\text{ pJ}$ to minimize the $CH_2^+$ signal from the resin, which otherwise overlaps with the $^{14}\text{N}^+$ peak ($14.00$ Da vs. $14.02$ Da).
    * **Data Processing:** 3D reconstruction used the tip profile method (IVAS software). 1D compositional profiles were generated via proxygram analysis, averaging 10 individual isoconcentration surfaces (specifically a $15\% \text{ }^{56}\text{Fe}^+$ surface), excluding any surfaces truncated by the reconstruction edge.

## Relevance To APT/FIM
* **Scalability:** This method provides a robust alternative to time-consuming serial manipulation of individual nanoparticles or metal-layer embedding techniques, which can introduce artifacts or low yields.
* **Chemical Contrast:** The use of nitrogen-free resin is critical for providing the chemical contrast necessary to distinguish biological protein components from the embedding matrix.

## Open Questions
* **Origin of Sodium:** It remains uncertain if the detected Na spike originates from buffer solution contaminants or is an artifact from the Lowicryl resin (though pure K4M resin showed no Na peaks).
* **Fe Intensity Interpretation:** The observed increase in Fe intensity beyond $1\text{ nm}$ may be a result of averaging multiple individual ferritin molecules with variable spacing rather than representing a single continuous structure.

## Citation Trail

- pages 1-2: **Summary: Perea et al. (2016) – APT Mapping of Phosphorus in Ferritin**

* **Technique & Instrumentation:** The study utilizes Atom Probe Tomography (APT) for 3D compositional mapping, employing thermally-assisted field evaporation from cryogenically-cooled, needle-shaped specimens. Chemical identification is achieved via time-of-flight mass spectrometry (TOF-MS), with spatial reconstruction derived from detector position and evaporation time sequences.
* **Specimen Preparation Method:** To overcome the traditional difficulty of applying APT to soft biological materials, a robust FIB-based preparation method was used. Ferritin was embedded in a specialized organic polymer resin that lacks nitrogen; this provides critical chemical contrast to distinguish the interfaces between the ferrihydrite mineral core, the protein shell, and the surrounding resin.
* **Analytical Relevance & Findings:** The iron-rich ferrihydrite core serves as an internal fiducial marker for atom-by-atom reconstruction. This approach allowed for the definitive mapping of phosphorus at the surface of the mineral core and the detection of sodium within the protein shell environment, particularly at the mineral/protein interface.
* **Key Context/Caveats:** The presence of an iron signature in the mass spectrum is used to confirm the successful field evaporation of the organic protein components. This nitrogen-free resin approach is presented as a scalable method for studying interfaces in other biological, organic, and inorganic nanomaterials.
- pages 2-3: **Summary: Atom Probe Tomography of Ferritin in Resin**

* **Objective & Chemical Contrast:** The study utilizes APT to map elemental distributions at complex biological interfaces by leveraging chemical contrast. By embedding ferritin in nitrogen-free Lowicryl K4M resin, the researchers could distinguish the ferrihydrite mineral core (via Fe), the protein shell (via N), and the organic-organic interface between the protein and the resin (by tracking N depletion/presence).
* **Specimen Preparation Method:** Ferritin was mixed with resin in a gelatin capsule and UV-cured at $-35\text{ °C}$ for 48 hours. The cured specimen was cleaved to expose the interior, followed by a FIB-based lift-out of a lamellar wedge. These wedges were attached to Si microposts and subjected to annular milling to produce needle-shaped specimens with an end diameter $<100\text{ nm}$ (radius of curvature $\sim 100\text{ nm}$).
* **Instrumentation & Process Optimization:** A dual-beam FIB/SEM was used for preparation, employing EDX to identify regions of interest with high Fe concentrations. Notably, the use of $\text{XeF}_2$ during large-area trenching in the FIB was found to significantly increase specimen preparation success rates.
* **Experimental Controls:** To validate the mapping of interfaces, the study included control specimens consisting of pure Lowicryl resin needles (lacking ferritin) and $\text{Fe}_3\text{O}_4$ nanoparticles embedded in resin.
- pages 3-4: **Summary: APT Analysis of Ferritin in Resin Matrix (Perea et al., 2016)**

* **Specimen Preparation & Stability:** To improve electrical conductivity and mechanical stability for APT, needle-shaped specimens containing ferritin embedded in resin were conformally coated with ~10–20 nm of sputtered Cr.
* **Mass Spectral Optimization:** A critical challenge in analyzing organic matrices is the overlap of $m/z$ peaks (e.g., $^{14}N^+$ at 14.00 Da vs. $CH_2^+$ at 14.02 Da). By increasing laser energy to 450 pJ (355 nm wavelength), the $CH_2^+$ signal from the resin was minimized, enabling definitive detection of nitrogen from the protein shell.
* **Elemental Identification & Mapping:** The presence of ferritin was confirmed via mass spectrometry by identifying Fe isotopes, N ions ($N^+$, $N^{++}$), and phosphorus species ($FePO_2^+$, $FePO_3^+$, etc.), which allowed for the spatial distinction between the bio-organic protein shell and the nitrogen-free resin matrix.
* **Data Reconstruction & Quantitation:** 3D reconstruction utilized a 15% $^{56}Fe^+$ isoconcentration surface to define the ferrihydrite mineral core; proximity histogram (proxygram) analysis was then applied along the morphological contours of these surfaces to generate 1D compositional profiles of the protein/resin interface.
* **Experimental Caveats:** While high laser energies can induce thermal artifacts (e.g., thermal tails or humps) and complicate reconstruction, the 450 pJ setting was found to be optimal here as it eliminated interfering mass peaks without introducing significant thermal instability.
- pages 4-5: * **Methodology:** Proxygram analysis was employed to map the compositional profile of ferritin embedded in resin by averaging profiles from 10 individual isoconcentration surfaces, specifically tracking Fe, $\text{FePO}_2$, P, Na, N, and C.
* **Data Processing Caveats:** To ensure accuracy, only fully enclosed isoconcentration surfaces were included in the proxygram analysis; any surfaces truncated by the reconstruction edge were excluded.
* **Instrumentation & Calibration:** Mass spectra of pure Lowicryl resin were collected at varying UV laser energies (30 pJ, 200 pJ, and 450 pJ) to establish a baseline for organic species peaks (e.g., $^{14}\text{N}$ and $^{56}\text{Fe}$) and to distinguish them from the ferritin signal.
* **Quantitative Limitations:** Reported values represent relative compositions rather than absolute concentrations; this approach was used because the analysis focused on identifying unambiguous compositional differences between the ferritin and the resin, despite a measurable mass offset in the $^{56}\text{Fe}^+$ peak (55.94 Da vs. 56.00 Da for $^{12}\text{C}^{4+++}$).
- pages 5-6: **Summary: Atom Probe Tomography of Resin-Embedded Ferritin**

* **Methodology & Instrumentation:** The study utilized UV laser-pulsed Atom Probe Tomography (APT) at 450 pJ to map the elemental distribution of ferritin embedded in Lowicryl K4M resin. Mass spectrometry was used to identify specific species, such as $\text{FePO}_2$ and P, to delineate the transition between the ferrihydrite mineral core and the protein shell.
* **Structural Findings:** APT proxygrams revealed a distinct radial composition: an Fe-dominated mineral core, an inorganic/organic interface (between -1 nm and 1 nm), and a phosphorus (P) enrichment specifically at the surface of the ferrihydrite core, likely existing as iron phosphate.
* **Experimental Caveats (Sodium):** A peak for Na was detected following the P enrichment; however, its origin is uncertain. While it could be an artifact from the Lowicryl resin, the authors note that pure K4M resin shows no Na mass peaks, suggesting the Na may instead originate from buffer solutions or other contaminants.
* **Data Interpretation Limits:** The researchers noted that the observed increase in Fe intensity beyond 1 nm is likely a result of averaging multiple individual ferritin molecules with variable spacing rather than a single continuous structure. Additionally, peaks at 14 Da and 56 Da in pure resin samples were attributed to organic species within the resin itself rather than the protein.
- pages 6-7: * **Methodology & Instrumentation:** APT was utilized to generate proxygram composition profiles and corresponding mass spectra for key elements ($\text{Fe}$, $\text{FePO}_4$, $\text{P}$, $\text{Na}$, $\text{N}$, and $\text{C}$) within ferritin embedded in lowicryl resin.
* **Key Findings:** The analysis revealed a specific spike in $\text{Na}$ at the surface of the ferrihydrite mineral core, rather than a continuous compositional gradient from the core to the external buffer; $\text{Fe}$ localization was found to be consistent with the known iron-rich core structure.
* **Experimental Controls:** To differentiate protein-specific signals from the resin matrix, composition profiles were benchmarked against pure lowicryl (control) and $\text{Fe}_3\text{O}_4$ specimens (reference dashed curves).
- pages 7-8: **Summary of Perea et al. (2016) – Pages 7-8**

* **Methodology & Instrumentation:** The study utilizes a local electrode atom probe for the tomographic reconstruction of horse spleen ferritin embedded in Lowicryl resin. Specimen preparation involves UV-polymerization at $-35^\circ\text{C}$ via a Leica EMAFS freeze substitution system, followed by site-specific liftout and APT specimen preparation using a dual-beam FIB/SEM.
* **Analytical Capabilities:** The technique enables the mapping of both inorganic-organic interfaces (ferrihydrite core/protein shell) and organic-organic interfaces (protein shell/embedding resin) with ppm sensitivity. Key findings include the identification of phosphorus at the ferrihydrite surface and sodium enrichment at the mineral/protein interface.
* **Technical Advantages:** This approach provides a scalable alternative to traditional APT methods, such as the time-consuming serial manipulation of individual nanoparticles or the use of metal-layer embedding, which can introduce potential artifacts or low analysis yields.
* **Experimental Caveats:** To mitigate electrical charging during FIB/SEM imaging, a $\sim$10 nm carbon sputter coating is required. Additionally, researchers must account for high background signals from the organic embedding resin, which can obscure subtle compositional trends in the carbon profile.
- pages 8-9: **Summary of Perea et al. (2016) – Pages 8-9**

* **FIB Preparation & Gas-Assisted Etching (GAE):** To mitigate the challenges of milling soft, electrically insulating lowicryl resin—specifically the formation of pits, voids, and specimen overheating—the authors utilized $XeF_2$ gas-assisted etching during FIB milling. This approach increased the milling rate by 3–5x and improved morphological uniformity, enabling the fabrication of needle-shaped specimens with tip diameters $<100\text{ nm}$.
* **Targeting & Protective Layering:** Using an FEI Quanta dual-beam FIB/SEM, regions of interest (ROI) were identified via EDX mapping of the Fe-L edge to target high Fe content. A protective Pt/C capping layer ($\sim 200\text{ nm}$ thick) was deposited over the ROI using electron-beam-assisted deposition (EBAD) prior to milling.
* **Tip Engineering for Stability:** Following annular milling with an $8\text{ kV } ^{69}Ga^+$ ion beam, a conformal $10\text{--}20\text{ nm}$ Cr coating was sputtered onto the sharpened tips. This step was critical to enhance both the mechanical stability and electrical conductivity of the specimens before APT loading.
* **APT Instrumentation & Parameters:** Analysis was performed on a LEAP 4000X-HR equipped with a $355\text{ nm}$ UV laser at a temperature of $44.1\text{ K}$. Experimental parameters included laser energies of $0.2\text{--}400\text{ pJ}$, a frequency of $160\text{ kHz}$, and detection rates of $320\text{--}480\text{ ions/sec}$; data reconstruction was performed using the tip profile method in IVAS software.
- page 9: Based on the references and metadata provided on page 9 of the excerpt, the following summary can be made regarding the experimental context:

* **Specimen Preparation Methods:** The study utilizes Focused Ion Beam (FIB) milling for the site-specific fabrication of nanoscale volumes from solidified, resin-embedded ferritin (Ref 19, 23).
* **Instrumentation Details:** Data collection was performed using Local Electrode Atom Probe Tomography (LEAP), with specific technical considerations given to laser-specimen interactions during the atom probe process (Ref 24, 33).
* **Experimental Caveats:** A significant challenge in this workflow is managing chemical degradation and morphological instabilities in the polymer/resin components caused by ion bombardment during the FIB prototyping stage (Ref 31, 32).
