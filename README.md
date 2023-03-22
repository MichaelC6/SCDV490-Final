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
OpenStreetPath. The link to the OpenStreetPath website is
[https://www.openstreetmap.org/#map=8/39.330/-93.439](https://www.openstreetmap.org/#map=8/39.330/-93.439).
You will need to make an account on OpenStreetPath by navigating to
the above link and clicking `Sign Up` in the top right corner. Then, edit
the file setup.sh so that it is exporting your username and password
rather than the sample username and password we give in there.

## Environment Setup

1. Make sure Anaconda3 is installed by using the following the
instructions located [here](https://docs.anaconda.com/anaconda/install/index.html).

2. Once Anaconda3 is installed, create the conda environment in the location
you will be running this code.
    * On the command line run `conda env create -f environment.yml` and it will
    create an environment named `ChargingNetwork`. To use this environment
    run `conda activate ChargingNetwork` before running the code.
    * For PyCharm reference [this link](https://www.jetbrains.com/help/pycharm/conda-support-creating-conda-virtual-environment.html)
    * For VSCode reference [this link](https://code.visualstudio.com/docs/python/environments)

## Running the Project Code
To run the project code simply execute the following command from your
favorite terminal: `./run.sh`
