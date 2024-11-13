# Acts Common Tracking Software
## Step by step instruction:

#### Clone repo
```
git clone https://github.com/OlivierSalin/Faser2_acts.git acts_faser2
cd acts_faser2
git clone  https://gitlab.cern.ch/acts/OpenDataDetector.git thirdparty/OpenDataDetector
```
#### Install all dependencies if access to cvmfs
```
source CI/setup_cvmfs_lcg.sh
```
##### If this does not work directly use those command line 
EL9: /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc13-opt/setup.sh \
Centos7: /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-centos7-gcc12-dbg/setup.sh
#### Build
```
cd ..
cmake -B acts-build -S acts_faser2 \
  -GNinja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX="acts-install" \
  -DACTS_BUILD_ODD=ON \
  -DACTS_BUILD_FATRAS=ON \
  -DACTS_BUILD_FATRAS_GEANT4=ON \
  -DACTS_BUILD_EXAMPLES_DD4HEP=ON \
  -DACTS_BUILD_EXAMPLES_GEANT4=ON \
  -DACTS_BUILD_EXAMPLES_PYTHIA8=ON \
  -DACTS_BUILD_EXAMPLES_PYTHON_BINDINGS=ON \
  -DACTS_BUILD_PLUGIN_DD4HEP=ON \
  -DACTS_BUILD_PLUGIN_EDM4HEP=OFF \
  -DACTS_BUILD_PLUGIN_GEANT4=ON \
  -DACTS_BUILD_PLUGIN_FPEMON=ON \
  -DACTS_BUILD_PLUGIN_JSON=ON \
  -DACTS_BUILD_PLUGIN_TGEO=ON \
  -DACTS_FORCE_ASSERTIONS=ON \
  -DACTS_ENABLE_LOG_FAILURE_THRESHOLD=ON

cmake --build acts-build --target install -j4
```

ACTS needs to be source before each use:
```
cd acts_faser2
source CI/setup_cvmfs_lcg.sh
source acts-install/bin/this_acts.sh
source acts-install/python/setup.sh
```
Or you can directly use the bash script
cd acts_faser2
source Setup_acts.sh

Setup can be testied using this tutorial examples if bug contact me: olivier.salin@cern.ch
```
cd ..
python acts_faser2/Examples/Scripts/Python/truth_tracking_kalman.py
python acts_faser2/Examples/Scripts/Python/truth_tracking_telescope.py
python acts_faser2/Examples/Scripts/Python/truth_tracking_Faser2.py
```

More information can be found in the [Acts documentation](https://acts.readthedocs.io/).

## Repository organization

The repository contains all code of the Acts projects, not just the core library
that a physics experiment is expected to use as part of its reconstruction code.
All optional components are disabled by default. Please see the
[getting started guide](docs/getting_started.md) on how-to enable them.

-   `Core/` contains the core library that provides functionality in the `Acts`
    namespace.
-   `Plugins/` contains plugins for core functionality that requires
    additional external packages. The functionality also resides in the `Acts`
    namespace.
-   `Fatras/` provides fast track simulation tools based on the core
    library. This is not part of the core functionality and thus resides in the
    separate `ActsFatras` namespace.
-   `Examples/` contains simulation and reconstruction examples. These are
    internal tools for manual full-chain development and tests and reside in
    the `ActsExamples` namespace.
