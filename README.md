# SCDV490 Final Project: Nationwide Electric Car Charging Network
### Authors: Michael Cammarere \& Noah Franz

Throughout the past decade, electric cars have gained popularity throughout
the US. But, a common complaint of those who have not hopped on the electric
car train is that the charging infrastructure is much farther behind that of
combustion vehicles. So, the goal of this project is to create a comprehensive
electric car charging network for the US. This includes the ideal locations
of electric car chargers throughout the US road network.

## The Data
For this project we used the open source map data available on the website
OpenStreetMap. The link to the OpenStreetMap website is
[https://www.openstreetmap.org/#map=8/39.330/-93.439](https://www.openstreetmap.org/#map=8/39.330/-93.439).
We can download OSM files (which are very similar to XML files) for each state.

## Environment Setup
1. Make sure Anaconda3 is installed by using the following the
instructions located [here](https://docs.anaconda.com/anaconda/install/index.html).

2. Once Anaconda3 is installed, create the conda environment in the primary directory
of this repo (the same directory that this README is in).
    * On the command line run `conda env create -f environment.yml` and it will
    create an environment named `ChargingNetwork`. To use this environment
    run `conda activate ChargingNetwork` before running the code.
    * For PyCharm reference [this link](https://www.jetbrains.com/help/pycharm/conda-support-creating-conda-virtual-environment.html)
    * For VSCode reference [this link](https://code.visualstudio.com/docs/python/environments)

## Running the Project Code
On the other hand, you can run the analysis for a certain state by doing
`./run-state.sh state-name` where `state-name` should be replaced by a state name
that is all lower case and spaces are separated by a -. We recommend only running on small states.
For example, Rhode Island would be `./run-state.sh rhode-island`. This is a memory and storage smart script (for small states!).
Other small states include the following: `district-of-columbia`, `deleware`, `vermont`, `south-dakota`, `new-hampshire`. This
pipeline will run on Linux (tested with Ubuntu 20.04) and MacOS as is. **This is the recommended approach!!**
* NOTE: To run on Windows, you will need to comment out the first line of the `./run-state.sh` pipeline script
and unzip the bzip2 files by hand.

To run the entire project code (the whole United States) simply execute the following command from your
favorite terminal: `./run.sh`.
* NOTE: this will take a very long time (even though it
is very optimized).
* NOTE: This project data takes approximately 350.76 GB of storage if
running on the entire United States. We do not recommend this approach!
* NOTE: Do not run on linux unless you have over 150 GBs of ram. Mac OS does run this due
to it's memory management. To run on Windows, you will need to comment out the
first line of the `./run.sh` pipeline script and unzip the bzip2 files by hand. 

To reproduce the plots from the presentation of this work, see the `analysis.ipynb` notebook.