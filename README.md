# SPP-project
As part of a course project with final presentation, I developed a Python code to study the behavior of Surface Plasmon Polaritons (SPP) and Surface Plasmon Resonance (SPR) using the Kretschmann-Raether configuration, as illustrated in configuration-figure (uploaded in the repository).

## Main output: 
### Figure 1:
Observing SPR behaviour and effect of varying metal thickness and refractive index of the dieletric material on SPR angles and reflectivity at specific angle (suitable for fixed angle sensor applicatios)
### Figure 2 and 3:
optimizing sensitvity of sensor by studying the behaviour of the system as refractive index of dielectric medium is varied: 

1) moving/ varying incident angle: sensitivity presented by d(SPR angle)/dn 
  
2) fixed incident angle: presented by dR/dn; change in reflectivity over varying refractive index at constant angle.

## Data Extraction:
The refractive index data of the metals was manually extracted from refractiveindex.info and saved in a text file ( can be found in the repository). data are then read and extrapolated by the code for further calculations.
## Reflection Coefficient Calculations:
Computes the reflectivity as the square modulus of total reflection coeffecient at different incident angles employing Snell’s Law and the TM-polarized light reflection coefficient equations.
## Figure of Merit (FOM) Calculation:
Calculates the Figure of Merit (FOM) to evaluate the efficiency of Surface Plasmon Polaritons (SPPs) in sensors. This helps assess the sensitivity and effectiveness of SPR-based sensors, which operate using a He-Ne laser. the assesment is perfomed through: 
       SPR Response Shift Analysis: Investigates the shift in the SPR response over variations in refractive index (RI), using different metals with varying thicknesses to assess sensor performance.

The code provides valuable insights into the efficiency of SPR sensors and helps optimize them for practical applications.
