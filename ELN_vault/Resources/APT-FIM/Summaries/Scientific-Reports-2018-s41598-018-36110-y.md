---
date created: 2026-04-10
author: "StarDustX"
note type: pdf-summary
resource type: apt-fim-literature
source pdf: "[[Resources/APT-FIM/PDFs/Scientific-Reports-2018-s41598-018-36110-y.pdf]]"
provider: "lmstudio"
model: "gemma-4-26B-A4B-it-Q4_K_M"
tags:
  - "#resource/pdf-summary"
  - "#apt"
  - "#fim"
---

# Scientific-Reports-2018-s41598-018-36110-y

## Source PDF

[[Resources/APT-FIM/PDFs/Scientific-Reports-2018-s41598-018-36110-y.pdf]]

## Overview
The study focuses on the characterization of Amyloid-beta (Aβ) fibrils, specifically Aβ 1–42, using laser-pulsed Atom Probe Tomography (APT). The primary objective is to investigate elemental distribution and identify potential metal ions within protein assemblies by utilizing $^{13}\text{C}$ and $^{15}\text{N}$ isotopic markers for enhanced tracking. The technique aims to provide a near atomic-scale chemical complement to structural methods like Cryo-EM, NMR, and X-ray crystallography.

## Key Findings
* **Chemical Mapping:** The method successfully differentiated organic protein fragments from the aluminum (Al) substrate, identifying longitudinal structures composed of C, H, O, and N. 
* **Mass Spectrometry Ranges:** Organic phase peaks were primarily concentrated in the $29\text{--}31\text{ Da}$ ($\text{C}_2\text{H}_n$) and $41\text{--}45\text{ Da}$ ($\text{C}_3\text{H}_n$) ranges, while solvent-derived peaks (e.g., $\text{CH}_2$, $\text{CH}_3$, $\text{H}_2\text{O}$) were also detected.
* **Isotopic Identification:** Aluminum signals appeared at $9$, $13.5$, and $27\text{ Da}$ across three distinct charge states.
* **Detection Limitations:** Sulfur detection was unsuccessful due to isobaric overlaps and insufficient knowledge of bond-breaking mechanisms during evaporation.

## Methods And Instrumentation Notes
* **Specimen Preparation:** 
    * Aluminum wires were electropolished (using $\text{HNO}_3$ in methanol and $\text{HClO}_4$ in 2-butoxyethanol) and sharpened via Xe-PFIB (16 kV, 90 pA) to apex diameters of 40–100 nm.
    * Aβ fibrils were deposited via solution dipping and air-dried/desiccated ($\ge 36$ hours) to prevent UHV outgassing; chemical fixatives were avoided to prevent brittleness.
* **APT Parameters (LEAP 5000 XS):**
    * **Temperature/Pulse:** Experiments were conducted at 50 K using UV laser pulsing.
    * **Optimization:** Pulse energy was optimized between $10\text{--}15\text{ pJ}$ to minimize "heat tails" (mass-to-charge smears caused by prolonged heating). Higher energies ($20\text{--}40\text{ pJ}$) caused small peaks to disappear or undergo "DC" evaporation (driven by voltage rather than the laser).
    * **Frequency:** Pulse frequency was maintained between $125\text{--}500\text{ kHz}$. Frequencies $>500\text{ kHz}$ led to ion loss, while $<100\text{ kHz}$ degraded the signal-to-background ratio.
* **Reconstruction Strategy:** Due to differing evaporation fields between organic and metallic materials, a standard 3D reconstruction was replaced by an "image stack" approach, treating the Z-axis as a sequence of events without depth scaling.

## Relevance To APT/FIM
* **Interface Analysis:** The technique is highly effective for analyzing buried organic-inorganic interfaces at the nanometer scale and mapping elemental distributions (e.g., phosphorus in ferritin).
* **Structural Biology:** FIM can be utilized for point-projection imaging of macromolecular contours and direct visualization of unstained nucleic acids on metal substrates.
* **Broad Utility:** APT/FIM applications extend from semiconductor physics to the chemical tomography of mineralized tissues and complex biological systems (e.g., mammalian cells, bone).

## Open Questions
* **Isobaric Ambiguity:** Significant peak overlaps (particularly in the $26\text{--}32\text{ Da}$ and $40\text{--}46\text{ Da}$ ranges) make definitive chemical identification of specific ion species difficult, as many peaks represent complex combinations of C, H, O, and N.
* **Fragmentation Mechanisms:** The lack of certainty regarding molecular dissociation/fragmentation during ion flight and the unknown bond-breaking mechanisms during evaporation limit precise mass spectrometry assignments.

## Citation Trail

- pages 1-2: **Lab Notebook Summary: APT Characterization of Amyloid-beta (Aβ) Fibrils**

* **Methodology & Sample Prep:** Developed an approach to characterize Aβ fibrils using $^{13}\text{C}$ and $^{15}\text{N}$ isotopic markers. The modified protein fibrils were deposited onto pre-sharpened aluminum needles with apex diameters $<100\text{ nm}$.
* **APT Instrumentation & Mechanism:** Utilized laser-assisted field evaporation (high standing voltage combined with laser pulsing) to trigger the controlled evaporation of surface atoms and molecules. 3D chemically resolved information was reconstructed using position-sensitive mass-to-charge spectrometry of the resulting ion fragments.
* **Experimental Parameters & Caveats:** The size of the evaporated protein fragments is highly sensitive to experimental parameters, specifically the **laser pulse energy** and **pulse frequency**. Precise control of these settings is required to achieve the capability of localizing metal atoms (e.g., Cu, Fe, Zn) within the plaques.
* **Scientific Relevance:** Provides a near atomic-scale chemical complement to structural techniques such as Cryo-EM, NMR, and X-ray crystallography by enabling the 3D mapping of elemental/molecular compositions within protein assemblies.
- pages 2-3: **Lab Notebook Summary: APT Analysis of Aβ Fibrils**

* **Objective & Relevance:** The study utilizes laser-pulsed Atom Probe Tomography (APT) to investigate the elemental distribution and identify potential metal ions within amyloid-beta (Aβ) fibrils ($\sim$7 nm diameter), utilizing $^{13}\text{C}$ and $^{15}\text{N}$ isotopes for enhanced tracking.
* **Specimen Preparation & Instrumentation:** Proteins are deposited via incubation onto pre-sharpened Al specimens and air-dried to avoid brittleness caused by chemical fixatives. To prevent Xe implantation contamination, plasma FIB milling should be avoided (specifically at energies $>16\text{ kV}$, $90\text{ pA}$).
* **Optimization Parameters:** Key experimental variables include laser pulse energy ($10\text{--}40\text{ pJ}$) and pulse frequency ($125\text{--}500\text{ kHz}$). Frequencies exceeding $500\text{ kHz}$ result in ion loss because pulses occur too rapidly for detection, while frequencies below $100\text{ kHz}$ significantly degrade the signal-to-background ratio.
* **Experimental Caveats:** Thicker protein layers increase the risk of specimen fracture and require higher applied voltages ($2\text{--}3\text{ kV}$), which may lead to layer delamination. Additionally, high laser energy must be carefully controlled to prevent thermal decomposition of the biological structure or the formation of "heat tails" (mass-to-charge smears) caused by prolonged tip heating.
- pages 3-4: **Lab Notebook Summary: Mass-to-Charge Artifacts and Pulse Energy Effects**

* **Heat Tail Artifacts:** Prolonged heating of the APT tip induces "heat tails," which manifest as a smear of points toward higher masses in 2D correlation histograms and appear as trailing features in 1D $m/z$ spectra.
* **Laser Pulse Energy Optimization:** Laser pulse energy is a critical control parameter for mass accuracy; lower energies (10–15 pJ) minimize heat tails and allow for precise peak ranging, whereas higher energies (20–40 pJ) cause small peaks to disappear into the tails of larger peaks or become subject to signal spreading.
* **Uncorrelated Evaporation:** A second type of artifact involves field evaporation events that are correlated with each other but not time-correlated with the laser pulse; this contributes a uniform increase to the background noise in the 1D $m/z$ spectrum.
* **Specimen Preparation (PFIB):** For Al-specimens, tip sharpening was achieved using Plasma Focused Ion Beam (PFIB) with parameters exceeding 16 kV and 90 pA, utilizing Xe implementation.
- pages 4-5: **Lab Notebook Summary: Pulse Energy and Rate Effects in Protein APT**

* **Pulse Energy & Evaporation Mode:** At pulse energies below 20 pJ, "DC" evaporation occurs—driven by high specimen voltage rather than the laser pulse itself. In 2D $m/z$ correlation plots ($m_2 \ge m_1$), this manifests as curved lines crossing the $m_2$-axis, which can overlap with and obscure data via "heat tails."
* **Field-Induced Mass Shifts:** Lowering pulse energy (e.g., 10–15 pJ) increases specimen voltage and surface field strength, resulting in higher detected charge states (notably $C^{2+}$ at 6/6.5 Da and $N_2^+$ at 7/7.5 Da) but smaller peak intensities. Conversely, higher pulse energies (e.g., 20 pJ) shift prominent peaks toward higher mass-to-charge ratios (e.g., 44–45 Da).
* **Pulse Rate & Structural Stability:** Variations in pulse rate (100 kHz to 500 kHz) at a constant 10 pJ energy show only minimal impact on peak resolution. The longitudinal spatial structure of the protein remains detectable even at higher energies, though higher energies increase "smearing" from heat tails, causing smaller peaks to vanish.
* **Experimental Parameters & Mass Analysis:** Experiments were conducted at 50 K with pulse energies ranging from 10–40 pJ. For Amyloid-beta 1–42 ($C_{203}H_{311}N_{55}O_{60}S$), the analysis targeted specific fragments such as $^{13}C^+$ (13 Da), $^{15}N^+$ (15 Da), and $O^+$ (16 Da).
- pages 5-6: **Summary: Pulse Rate and Mass-to-Charge Correlation in Organic/Inorganic Interface Analysis**

* **Experimental Parameters:** Laser-pulsed APT was performed using a fixed pulse energy of 10 pJ, with testing conducted across four different pulse rates (100 kHz, 200 kHz, 333 kHz, and 500 kHz).
* **Pulse Rate Sensitivity:** Variations in the pulse rate were found to have only a slight influence on the appearance of individual mass peaks.
* **Coincidence Analysis:** Correlation histograms of mass-to-charge ($m/z$) ratios were utilized to analyze double ion detections and quantify simultaneous ion arrivals at the detector.
* **Spatial/Chemical Mapping:** The method effectively differentiated organic protein fragments (e.g., identifying species at 29 Da such as $\text{C}_2\text{H}_3$, $\text{CNH}$, and $\text{CO}$) from the inorganic aluminum substrate using detector maps and iso-surface concentration reconstructions.
- pages 6-7: **Summary: Mass Spectrometric Analysis of Protein/Al Interface (APT)**

*   **Mass-to-Charge ($m/z$) Overlap & Identification Challenges:** Significant peak overlaps exist in the mass spectra, particularly between $26\text{--}32\text{ Da}$ and $40\text{--}46\text{ Da}$. This makes definitive chemical identification of specific ion species difficult, as peaks often represent complex combinations of $\text{C}$, $\text{N}$, $\text{H}$, and $\text{O}$ (e.g., $\text{C}_2\text{H}_n$, $\text{C}_3\text{H}_n$, and various $\text{CN/CO}$ fragments).
*   **Elemental/Isotopic Context:** For mass spectrometry calculations, $\text{C}$ and $\text{N}$ are assumed to be the $^{13}\text{C}$ and $^{15}\text{N}$ isotopes unless otherwise noted. Aluminum ($\text{Al}$) signals appear at $9$, $13.5$, and $27\text{ Da}$, corresponding to three distinct charge states.
*   **Solvent vs. Protein Composition:** The mass spectra differentiate between the protein material and the surrounding solvent/buffer. Solvent-derived peaks (e.g., $\text{CH}_2$, $\text{CH}_3$, $\text{H}_2\text{O}$, $\text{H}_3\text{O}^+$) are found across all measurements, while organic phase peaks for the protein are primarily concentrated in the $29\text{--}31\text{ Da}$ ($\text{C}_2\text{H}_n$) and $41\text{--}45\text{ Da}$ ($\text{C}_3\text{H}_n$) ranges.
*   **Experimental Caveat:** Due to the high density of overlapping mass-to-charge peaks, it is impossible to provide a certain chemical identity for many detected ions; most peaks likely contain multiple elemental combinations from both the protein backbone and the buffer solution.
- pages 7-8: **Lab Notebook Summary: Analysis of Aβ Fibrils via Laser-Pulsed APT**

* **Methodology & Reconstruction:** The study utilized laser-pulsed Atom Probe Tomography (APT) to analyze Aβ fibrils deposited as a thin layer on an Al substrate. Rather than using standard 3D reconstruction protocols, the researchers reconstructed image stacks directly from detector information to analyze the field evaporation sequence and specimen morphology.
* **Instrumentation & Optimization:** To preserve low-intensity mass signals, laser energies were optimized at 10–15 pJ; higher energies induced "heat tails" that obscured significant mass-to-charge ($m/z$) peaks. The analysis identified organic compounds (C, H, O, N) as longitudinal structures situated atop the Al substrate, with Al evaporation occurring later in the sequence.
* **Analytical Challenges (Isobaric Overlap):** Precise peak assignment was significantly hindered by isobaric overlaps common in organic mass spectrometry, where different combinations of C, H, O, and N result in identical $m/z$ values (e.g., 29 Da could represent $\text{CNH}$, $\text{CO}$, or $\text{C}_2\text{H}_3$).
* **Experimental Caveats:** Spatial and compositional accuracy were limited by low count statistics, trajectory aberrations caused by complex specimen shapes during evaporation, and molecular dissociation/fragmentation during ion flight. Notably, sulfur detection was unsuccessful due to these overlaps and insufficient knowledge of bond-breaking mechanisms during evaporation.
- pages 8-9: **Lab Notebook Summary: Protein Deposition and APT Analysis (Aβ 1–42)**

* **Specimen Preparation & Sharpening:** Aluminum wire specimens were electropolished (20% $\text{HNO}_3$ in methanol at 6 VDC, followed by 2% $\text{HClO}_4$ in 2-butoxyethanol at 1–5 VDC) and sharpened using a Xe-PFIB (FEI Helios) with an annular milling pattern (16 kV, 90 pA). Final specimen diameters ranged from 40–100 nm.
* **APT Instrumentation & Parameters:** Measurements were performed on a LEAP 5000 XS using UV laser pulsing (125 kHz, 15 pJ) at a specimen temperature of 50 K. A detection rate of 0.2% ions/pulse was maintained with 81% detector efficiency. An initial "cleaning" run of 1–2 million ions was performed to remove Xe-contamination and smooth the surface prior to protein deposition.
* **Protein Deposition & Handling:** $^{13}\text{C}$ and $^{15}\text{N}$ labeled Aβ 1–42 was deposited via solution dipping (no specimen bias required). To prevent outgassing in the APT ultrahigh vacuum (UHV) chamber, specimens were dried in a desiccator for $\ge$ 36 hours.
* **Reconstruction Caveats & Methods:** Because differences in evaporation fields between organic and metallic materials make standard 3D reconstruction challenging, an "image stack" approach was used. In this method, the Z-axis was treated as a sequence of events with no depth scaling applied, utilizing only singly-detected ions from the EPOS file to ensure reliable spatial ranging.
- pages 9-10: Based on the provided reference list from *Scientific Reports* (2018), the following summary highlights the state of Atom Probe Tomography (APT) and Field Ion Microscopy (FIM) literature:

* **Broad Application Scope:** The literature demonstrates that APT/FIM techniques are applied across diverse fields, ranging from semiconductor physics (photovoltaics and LEDs) and polymer science (poly(3-alkylthiophene)s) to complex biological systems, including mammalian cells, bone, dental enamel, and specific proteins like ferritin.
* **Instrumentation & Methodologies:** Key methodologies identified include Atom Probe Tomography (APT), the Local Electrode Atom Probe (LEAP), and scanning atom probe techniques. FIM is specifically utilized for point-projection imaging of macromolecular contours and the direct visualization of unstained nucleic acids on metal substrates.
* **Analytical Capabilities:** These techniques enable 3D nanoscale chemical mapping and atomic-scale characterization, particularly effective for identifying elemental distributions (e.g., phosphorus in ferritin) and analyzing buried organic-inorganic interfaces at the nanometer scale.
* **Experimental Context & Preparation:** Significant research focuses on the chemical tomography of mineralized tissues and "superbugs," often requiring specific sample preparation contexts such as resin-embedded specimens or the use of field-emitter tips for macromolecular deposition.
- page 10: Note: The provided excerpt contains the **References** and **Back Matter** sections of the paper, rather than the experimental results. The following summary captures the technical themes and literature context presented in these references:

* **Instrumentation & Methods:** The literature cited covers diverse APT modes and optimizations, including Pulsed Laser Atom Probe (PLAP) for nanocomposite films (Ref 61), Scanning Atom Probe for biomolecule mass analysis (Ref 60), and advanced protocols for 3D reconstruction and multilayer analysis (Refs 67, 69).
* **Data Interpretation & Caveats:** Key technical challenges addressed in the references include modeling image distortions in 3DAP (Ref 68), interpreting mass spectra through correlated ion analysis (Ref 62), and understanding field-induced molecular dissociation and neutral emission channels (Refs 64, 65).
* **Sample Preparation & Correlation:** The references highlight specialized workflows for nanoparticle sample fabrication (Ref 66) and the use of correlative microscopy techniques, specifically combining APT with Transmission Electron Microscopy (TEM) for alloy characterization (Ref 70).
