# Code for Tau3Mu-related analyses
Use this code to produce nanoAOD ntuples from miniAOD [<v4] for $W\to\tau(3\mu)\nu$ Run3 analysis.\
DATA : process eras C, D and E of 2022 with this code\
MC   : miniAODv4 available for whole 2022 and 2023 -> use branch `CMSSW_13_0_13`\
> [!NOTE]
> CRAB runs only on `lxplus8` having operating system el8.\
> Make sure to compile CMSSW release and code with el8 architecture.

## Getting started

```shell
cmsrel CMSSW_12_4_11
cd CMSSW_12_4_11/src
cmsenv
git cms-init
```

## checkout 
```
git clone -b CMSSW_12_4_11 git@github.com:BasChiara/Tau3muNANO.git ./PhysicsTools/Tau3muNANO
cd PhysicsTools/Tau3muNANO
```

## make sure we use a consistent tag
```
git fetch origin
git checkout -b myBranch origin/myBranch
```

## add your own fork as a remote. Skip if you dont have one
```
git remote add crovelli git@github.com:crovelli/Tau3muNANO.git
git fetch crovelli
#git checkout -b devChiara crovelli/master
```

## compile
```
cd ../../
scramv1 b
```
