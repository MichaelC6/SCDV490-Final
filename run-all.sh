#!/bin/bash

states=(alabama arizona arkansas california colorado connecticut delaware district-of-columbia florida georgia idaho illinois indiana iowa kansas kentucky louisiana maine maryland massachusetts michigan minnesota mississippi missouri montana nebraska nevada new-hampshire new-jersey new-mexico new-york north-carolina north-dakota ohio oklahoma oregon pennsylvania rhode-island south-carolina south-dakota tennessee texas utah vermont virginia washington west-virginia wisconsin wyoming)

for state in states
do
    echo Running on $state
    ./run-state.sh $state
done