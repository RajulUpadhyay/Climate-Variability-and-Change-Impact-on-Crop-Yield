# Climate-Variability-and-Change-Impact-on-Crop-Yield

This repository contains the code and data used to assess the potential impact of climate change on wheat yield across 27 districts in Chhattisgarh, India.

**Objective:**

Investigate the long-term effects of climate change on wheat production in Chhattisgarh.
Analyze potential wheat yield changes under various climate scenarios from 2015 to 2100.
Methodology:

**Data Acquisition and Processing:**

Download a 210 GB dataset containing climate projections (precipitation, maximum & minimum temperature) from 2015 to 2100 for CMIP6 models.
Utilize Linux tools to downscale the coarse-resolution data to a finer spatial resolution suitable for the analysis.
Employ Python scripts to perform bias correction on the climate data, addressing potential systematic errors in Global Climate Model (GCM) outputs.

**Crop Simulation Model:**

Implement the DSSAT crop simulation model, a process-based model that requires soil and climate data as input to estimate crop yields.
Script the model for parallel execution using Windows shell scripting, enabling simulations at various locations within each district.
Conduct a total of 2352 simulations, covering all 27 districts at a high spatial resolution (every 0.25 degrees).

**Data Analysis and Visualization:**

Utilize Python for data summarization and analysis of the simulated wheat yield data.
Compare projected wheat yields with baseline values from 1985 to 2014 to assess potential changes.

**Impact Assessment:**

Analyze the potential impact of climate change on wheat yields across different climate scenarios.
Identify potential worst-case scenarios and estimate the magnitude of yield decrease (up to 51% in your findings).

**Result**
!![plot](https://github.com/RajulUpadhyay/Climate-Variability-and-Change-Impact-on-Crop-Yield/blob/main/Change_Impact.png)

