---
date created: 2026-04-10
author: "StarDustX"
note type: pdf-summary
resource type: apt-fim-literature
source pdf: "[[Resources/APT-FIM/PDFs/2021_Miaja-Avila_EUV_Radiation_Pulsed_APT_of_III-Nitride_Semiconductors.pdf]]"
provider: "lmstudio"
model: "gemma-4-26B-A4B-it-Q4_K_M"
tags:
  - "#resource/pdf-summary"
  - "#apt"
  - "#fim"
---

# 2021_Miaja-Avila_EUV_Radiation_Pulsed_APT_of_III-Nitride_Semiconductors

## Source PDF

[[Resources/APT-FIM/PDFs/2021_Miaja-Avila_EUV_Radiation_Pulsed_APT_of_III-Nitride_Semiconductors.pdf]]

## Overview
This study demonstrates a novel approach to Atom Probe Tomography (APT) using Extreme Ultraviolet (EUV) radiation pulses ($\lambda = 29.6$ nm; $E_{photon} \approx 41.85$ eV) to trigger controlled field ion evaporation in III-nitride semiconductors (GaN, AlGaN, InGaN, and Mg-doped GaN). The method aims to mitigate significant compositional biases inherent in conventional Near-UV (NUV) or visible laser-assisted APT (LAPT), such as nitrogen loss ($\text{N}_2$ neutrals) and fluctuations in the Gallium charge-state ratio (CSR).

## Key Findings
* **Compositional Accuracy:** EUV-triggered APT produced consistent Ga/N composition data across all experimentally attainable CSR values. Mg doping concentrations ($\sim 3.6 \times 10^{19} \text{ cm}^{-3}$) were found to be consistent with SIMS measurements.
* **Validation of Alloys:** For $\text{In}_x\text{Ga}_{1-x}\text{N}$ quantum wells, EUV APT results were consistent with NUV LAPT ($7.7 \pm 0.5$ at.% vs $7.3 \pm 0.4$ at.% Indium).
* **Systematic Errors in AlGaN:** In $\text{Al}_x\text{Ga}_{1-x}\text{N}$ alloys, a systematic error was observed where Nitrogen was underestimated and Gallium overestimated. Analysis suggests this is driven by **detector dead time** (multiple detection events) rather than DC evaporation or neutral formation.
* **Non-Thermal Mechanism:** Calculations showed an extremely negligible instantaneous temperature rise ($\Delta T \approx 2\text{ mK}$), suggesting that field evaporation in EUV-APT does not follow the standard "bulk thermal model" used in LAPT, but likely follows a distinct ionization/desorption pathway.
* **Mass Spectrometry:** The $GaN_3^{++}$ peak common in NUV-LAPT was absent in EUV spectra. However, an ambiguity exists at the $14\text{ m/z}$ peak (identifiable as either $\text{N}^+$ or $\text{N}_2^{++}$), introducing a $\pm 1$ atom % uncertainty in Nitrogen concentration.

## Methods And Instrumentation Notes
* **Instrumentation:** A LEAP 3000X-Si (CAMECA) coupled via vacuum beamline to an XUUS EUV light source (KMLabs). The EUV is generated through high-harmonic generation (HHV) in an Argon-filled hollow-core waveguide driven by a 10 kHz, 800 nm ultrafast laser.
* **Beam Parameters:** Focused to a $\sim 50\ \mu\text{m}$ spot diameter with a pulse energy of $\sim 0.5\text{ pJ}$ and duration of $\sim 10\text{ fs}$. The photon fluence is $\sim 5 \times 10^{-4}\text{ J/m}^2$ (approximately one photon per pulse at the apex).
* **Specimen Preparation:** Standard FIB wedge liftout and annular milling; tip radii of $10\text{--}50\text{ nm}$.
* **Experimental Conditions:** Cryogenic temperatures ($20\text{--}100\text{ K}$) under ultrahigh vacuum ($3\text{--}7 \times 10^{-9}\text{ Pa}$) with high DC standing voltages ($\sim$tens of V/nm).
* **Operational Challenges:** The setup lacks automatic evaporation rate control; users must manually increase the DC bias voltage as the tip evaporates. Additionally, pulse energy can fluctuate by $\sim 20\%$ during runs.

## Relevance To APT/FIM
* **Mitigation of Bias:** Provides a way to avoid the nitrogen underestimation and Ga CSR fluctuations that plague LAPT in III-nitrides.
* **Material Versatility:** Demonstrates that identical EUV pulse energies can be applied to both insulating ($\text{SiO}_2$) and semiconducting samples, unlike NUV LAPT which requires different energies for different materials.
* **Nanoscale Capability:** Proves effective for analyzing features too small for SIMS or EDX, such as 4 nm $\text{In}_x\text{Ga}_{1-x}\text{N}$ quantum wells.

## Open Questions
* **Evaporation Physics:** The specific non-thermal ionization/desorption mechanism remains poorly understood due to current instrumental limitations.
* **Material Complexity:** It is unclear if EUV pulses can reliably trigger controlled evaporation in crystalline semiconductors given their higher thermal conductivity, lower electrical resistivity, and different optical absorption profiles compared to amorphous $\text{SiO}_2$.
* **Instrumental Upgrades:** Future work is required to increase the laser repetition rate, improve vacuum beamline efficiency, and implement tighter focusing to enhance photon fluence and acquisition speed.

## Citation Trail

- pages 1-2: **Summary: EUV Radiation-Triggered Atom Probe Tomography of III-Nitride Semiconductors**

* **Methodology & Instrumentation:** The study demonstrates a novel approach to Atom Probe Tomography (APT) using Extreme Ultraviolet (EUV) radiation pulses instead of conventional visible (355/532 nm) or near-UV lasers. The setup utilizes sharp specimen tips (10–50 nm radius) held at cryogenic temperatures (20–100 K) under ultrahigh vacuum and high DC standing voltages ($\sim$tens of V/nm) to trigger controlled field ion evaporation.
* **Scope of Application:** EUV-triggered APT was successfully applied to a variety of III-nitride semiconductors, including undoped and Mg-doped p-GaN, as well as $\text{Al}_x\text{Ga}_{1-x}\text{N}$ and $\text{In}_x\text{Ga}_{1-x}\text{N}$ alloys, using extremely low EUV photon fluence.
* **Key Advantages:** Unlike conventional Laser-pulsed APT (LAPT), where GaN chemical composition measurements are highly sensitive to experimental parameters and gallium charge-state ratios, the EUV method produces consistent composition data across all experimentally attainable ratios. Additionally, Mg doping concentrations measured via EUV APT were found to be consistent with other characterization techniques.
* **Mechanistic Caveat:** The researchers noted that because the EUV photon fluence used is so low, the evaporation does not appear to follow the standard "bulk thermal model" (laser-induced heating) typically associated with LAPT, suggesting a different, non-thermal evaporation mechanism is at play.
- pages 2-3: **Summary: EUV-Triggered APT of III-Nitride Semiconductors**

* **Objective & Relevance:** The study investigates the use of Extreme Ultraviolet (EUV) radiation-triggered Atom Probe Tomography (APT) on III-nitride semiconductors (GaN, AlGaN, InGaN, and Mg-doped GaN). This approach aims to mitigate the significant compositional biases—such as nitrogen loss ($\text{N}_2$ neutrals) and fluctuations in the Ga charge-state ratio (CSR)—inherent in conventional visible or NUV laser-assisted APT (LAPT).
* **Evaporation Mechanism:** Unlike the standard bulk thermal model used in LAPT, EUV radiation ($\sim 42\text{ eV}$ photon energy) at very low fluences ($\sim 5 \times 10^{-4}\text{ J/m}^2$) has demonstrated the ability to trigger field ion emission in $\text{SiO}_2$. The authors explore whether a similar, non-thermal mechanism can be applied to crystalline semiconductors.
* **Instrumentation & Sample Preparation:** Specimens were prepared using standard FIB wedge liftout and annular milling, resulting in tip diameters of $10\text{--}30\text{ nm}$. The measurements were performed using an EUV-specific atom probe instrument (Wyvern-based) capable of applying high DC voltage bias to the needle-shaped semiconductor samples.
* **Experimental Caveats:** Transitioning from amorphous $\text{SiO}_2$ to III-nitride semiconductors introduces significant physical complexities, including much higher thermal conductivity, lower electrical resistivity, and different optical absorption profiles. These differences raise questions regarding whether EUV pulses can reliably trigger controlled field ion evaporation in these crystalline, semiconducting materials.
- pages 3-4: **Summary: EUV-Pulse Atom Probe Tomography (APT) Setup and Parameters**

* **Instrumentation & Method:** The system utilizes a LEAP 3000X-Si atom probe chamber (CAMECA) coupled via a custom vacuum beamline to an XUUS EUV light source (KMLabs). EUV light ($\lambda = 29.6$ nm; $E_{photon} \approx 41.85$ eV) is generated through high-harmonic generation (HHG) in an Argon-filled hollow-core waveguide driven by a 10 kHz, 800 nm ultrafast laser.
* **Beam Characteristics at Specimen:** The EUV beam is focused to a $\sim 50\ \mu\text{m}$ spot diameter with a pulse energy of $\sim 0.5$ pJ and a duration of $\sim 10$ fs. Notably, the photon fluence is $2–5$ orders of magnitude lower than commercial Near-UV (NUV) LAPT systems due to the significantly larger focus spot size ($50\ \mu\text{m}$ vs. typical $2\ \mu\text{m}$).
* **Experimental Caveats & Operational Challenges:** 
    * **Manual Rate Control:** Unlike commercial systems, this setup lacks automatic evaporation rate control; users must manually increase the DC bias voltage as the specimen tip evaporates to prevent the rate from dropping into the background.
    * **Stability Issues:** The repetition rate is lower (10 kHz) than standard LAPT (hundreds of kHz), and pulse energy can fluctuate by $\sim 20\%$ during runs, requiring periodic monitoring via a Si photodiode.
* **Data Acquisition & Analysis:** Measurements were performed at a base temperature of 50 K under high vacuum ($3–7 \times 10^{-9}$ Pa), yielding datasets of approximately $10^6$ ions. Data processing involved CAMECA IVAS 3.8.0 and in-house software for automated mass calibration, peak ranging, and global background subtraction.
- pages 4-5: **Summary: EUV-Assisted Pulsed APT of GaN**

* **Instrumentation & Method:** This study reports the first use of EUV-assisted field ion evaporation on a semiconductor specimen at a base temperature of 50 K. The experimental parameters included an EUV energy per pulse of $\sim$0.5 pJ and a repetition rate of 10 kHz.
* **Mass Spectrometry & Compositional Uncertainty:** The mass spectra identified characteristic Ga ($Ga^+$, $Ga^{++}$, $Ga^{+++}$) and N ($N^+$, $N^{++}$) ions, as well as molecular ions like $N_2^+$ and $GaN^{++}$; notably, the $GaN_3^{++}$ peak common in NUV-LAPT studies was absent. A specific ambiguity exists regarding the 14 m/z peak (identifiable as either $N^+$ or $N_2^{++}$), introducing a $\pm$1 atom % uncertainty in Nitrogen concentration.
* **Experimental Control & Data Segmentation:** To maintain a constant evaporation rate over a 46-hour period, the DC bias was manually increased in discrete steps, causing the Ga Charge State Ratio (CSR) to fluctuate between 0.5 and 2.0. To manage spatial heterogeneity, the researchers segmented data by both ion sequence and detector hit position (distance from pole center), allowing for a broader exploration of Ga CSR values ranging from 0.03 to 6.
* **Critical Caveats & Accuracy:** At high Ga CSR ($>0.5$), the apparent Ga concentration tends to be underestimated (ranging from 45.7 to 52.5 atom %). This deviation is attributed to detector multiplicity effects, where focusing on multiple detection events rather than single detection events significantly lowers the measured Ga concentration at high CSR.
- pages 5-6: **Summary: EUV APT Analysis of Mg-doped GaN and $Al_xGa_{1-x}N$ Alloys**

* **Detection of Minority Species:** EUV APT was successfully used to detect Mg dopants in p-type GaN, yielding a concentration of $\sim3.6 \times 10^{19} \text{ cm}^{-3}$. This result was validated against SIMS measurements (which showed a range of $2.5–3.6 \times 10^{19} \text{ cm}^{-3}$ with $\sim$20% uncertainty), confirming that the presence of the dopant does not significantly perturb Ga/N concentration measurements.
* **Analysis of Ternary Alloys:** The study applied EUV APT to $Al_{0.5}Ga_{0.5}N$ to address known inconsistencies in Laser-APT (LAPT) regarding Al atomic fraction fluctuations. Mass spectra for the alloy clearly resolved $Al^+$ ($27\text{ m/z}$), $Al^{++}$ ($13.5\text{ m/z}$), $Al^{+++}$ ($9\text{ m/z}$), and the molecular ion $AlN^{++}$ ($20.5\text{ m/z}$), with concentrations verified via EDX spectroscopy.
* **Evaporation Physics & Caveats:** The text highlights critical challenges in LAPT for III-nitrides, specifically nitrogen underestimation caused by two mechanisms: (1) formation of $N_2$ neutrals during low-field/high-pulse energy evaporation, and (2) "DC evaporation" (evaporation between pulses) during high-field/low-pulse energy evaporation.
* **Data Processing Methodology:** Elemental composition was determined by segmenting datasets based on detector hit position and ion sequence. While the method is robust for Ga/N ratios, the low count rate of the Mg peak in p-type samples limited the ability to study dopant concentration as a function of the Correlated Sampling Ratio (CSR).
- pages 6-7: **Summary: EUV Pulsed APT Analysis of III-Nitride Semiconductors**

* **Systematic Compositional Errors in $Al_xGa_{1-x}N$:** In EUV APT measurements of $Al_xGa_{1-x}N$, a consistent systematic error was observed across the Ga CSR (Current Signal Ratio) range of 0.6 to 4: Nitrogen is consistently underestimated, and Gallium is overestimated, while Aluminum concentrations remain relatively accurate (within EDX error margins).
* **Mechanisms for N-Underestimation:** The study ruled out DC evaporation of N (due to lack of background signal increase) and $N_2$ neutral formation via dissociation (based on correlation histogram analysis); instead, the data suggests that **detector dead time** is a primary driver, as filtering for "multiple detection events" yields stoichiometric values much closer to the true composition than "single detection events."
* **Validation of EUV APT for Nanoscale Features:** For $In_xGa_{1-x}N$ quantum wells (4 nm thick), where SIMS and EDX are unsuitable due to scale, EUV APT was successfully validated by comparing results against NUV (Near-Ultraviolet) LAPT; both methods yielded consistent Indium concentrations ($7.7 \pm 0.5$ at.% vs $7.3 \pm 0.4$ at.%).
- pages 7-8: **Summary: EUV-Pulsed APT of III-Nitride Semiconductors**

* **Relevance & Capability:** EUV radiation-pulsed atom probe tomography (APT) is demonstrated to be an effective method for triggering controlled field ion emission in III-nitride semiconductor alloys (e.g., $In_xGa_{1-x}N$ and $Al_xGa_{1-x}N$).
* **Instrumentation Parameters:** The EUV pulse parameters used include an energy of $\sim0.5\text{ pJ}$ per pulse, a photon energy of $\sim41.85\text{ eV}$, and a beam diameter ($1/e^2$) of $\sim50\ \mu\text{m}$, resulting in an EUV fluence of $\sim5 \times 10^{-4}\text{ J/m}^2$ (averaging approximately one photon per pulse at the specimen apex).
* **Thermal Analysis:** Calculations for the specimen apex ($100\text{ nm} \times 100\text{ nm}$ cross-section) indicate an extremely negligible instantaneous temperature rise ($\Delta T \approx 2\text{ mK}$), a value that remains consistent across various III-nitride alloy compositions due to similar densities and heat capacities.
* **Mechanism Caveat:** Because the $\Delta T$ is significantly lower than that observed in Near-UV (NUV) LAPT ($10\text{ mK}$ to $2\text{ K}$), the results suggest that field evaporation in EUV-APT is not driven by traditional bulk heating and thermal cooling, but likely follows a distinct ionization/desorption pathway.
- pages 8-9: **Summary: EUV-Pulsed APT of III-Nitride Semiconductors**

* **Methodology & Scope:** Demonstrated a proof-of-principle for using coherent, pulsed EUV light in Atom Probe Tomography (APT) to analyze III-nitride semiconductors ($\text{GaN}$, $\text{In}_x\text{Ga}_{1-x}\text{N}$, and $\text{Al}_x\text{Ga}_{1-x}\text{N}$). The study successfully applied identical EUV pulse energies and repetition rates to both insulating ($\text{SiO}_2$) and semiconducting samples, unlike conventional NUV LAPT which requires significantly different energies for different materials.
* **Evaporation Mechanism:** The low photon fluence observed suggests that the field evaporation mechanism in EUV APT deviates from the traditional thermal bulk heating model; however, the specific ionization mechanisms remain poorly understood due to current instrumental limitations.
* **Instrumentation & Future Upgrades:** Current capabilities are limited by low photon fluence and a restricted experimental parameter space. Planned upgrades to the EUV APT instrument include increasing the laser repetition rate, improving vacuum beamline efficiency, and implementing tighter focusing conditions to enhance photon fluence and data acquisition speed.
* **Analytical Accuracy & Caveats:** While $\text{GaN}$ concentrations were stoichiometric and Mg-doped $\text{GaN}$ results aligned with SIMS measurements, $\text{Al}_x\text{Ga}_{1-x}\text{N}$ analysis showed systematic errors (underestimating N and overestimating Ga) as a function of the Ga charge-state ratio (CSR). Additionally, concentration variations were observed when comparing single vs. multiple detection events in $\text{Al}_x\text{Ga}_{1-x}\text{N}$.
- pages 9-10: Based on the provided excerpt from the references and introductory notes, here is a summary for your lab notebook:

* **Instrumentation & Method:** The study utilizes an Atom Probe Tomography (APT) setup featuring a wavelength-tunable, femtosecond-pulsed coherent Extreme Ultraviolet (EUV) light source to trigger field evaporation and field ion emission.
* **Application Focus:** The technique is specifically applied to the analysis of III-Nitride semiconductor materials (e.g., GaN, AlGaN).
* **Data Processing Caveat:** When reviewing mass spectrometry results, note that there is an implicit conversion from SI units (kg/C) to the conventional mass-to-charge ratio ($m/z$).
- page 10: Based on the references provided in the excerpt from Miaja-Avila et al. (2021), the following summary outlines the technical landscape of Atom Probe Tomography (APT) and Field Ion Microscopy (FIM) discussed in the paper:

*   **Specimen Preparation Methods:** The literature emphasizes the use of Focused Ion Beam (FIB) for site-specific specimen preparation, which is a standard requirement for creating the needle-shaped geometries necessary for APT (Refs 42–44).
*   **Instrumentation and Laser-Assisted APT (LAAPT):** There is a significant focus on Laser-Assisted Atom Probe Tomography, particularly regarding its application to oxides and thin films. Key research areas include managing laser-induced temperature rises and understanding field evaporation effects in materials like GaN and CdTe (Refs 48, 49, 63, 64).
*   **Data Interpretation Caveats:** The text highlights several critical physical phenomena that complicate quantitative analysis, including ion dissociation/correlative evaporation (Ref 40), post-ionization leading to multiple charge states (Ref 38), and the complexities of interpreting mass spectra due to correlated ion analysis (Ref 56).
*   **Quantitative Accuracy and Detection Limits:** Important technical constraints for high-precision metrology are noted, specifically the impact of detector dead-time on multi-hit detection events (e.g., Boron analysis) and the challenges of maintaining accuracy in isotopic and compositional analyses of III-Nitride semiconductor alloys (Refs 55, 57, 58).
