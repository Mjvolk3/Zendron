# Parameter_Estimation
Estimating parameters for ODES using a CVAE

## Single Run
- Change parameters in `config.yaml`, if they are not set parameters from `default.yaml` will be used.
- `cd estimator`
- `python main.py`

## Wandb Sweep
- `cd estimator`
- `wandb sweep conf/wandb_sweep.yaml`
- Copy and paste the wandb agent and run from command line. The agent will be different every time. It looks something like this:
    -`wandb agent mjvolk3/parameter_estimation/qljj97pg`

## Wandb
### Setup
- Follow instructions here [wandb quickstart](https://docs.wandb.ai/quickstart)
- create account and initialize

### Toggle Tracking
- `wandb.mode: disabled` - Skip wandb. All run output can be found in the `output` folder produced by hydra.
- `wandb.mode: offline`- Use wandb, but don't log to account. Model output can be found locally in `wandb` folder.
- `wandb.mode: online` - Use wandb locally and online. Model output can be found locally in `wandb` folder and will be logged online

## Exporting Environment
- `conda env export --no-builds | grep -v "prefix" > env/env-param.yml`

### Conda Create from YAML
- `conda env create -f env/env-param.yml`

### Building Environment from Scratch
- Install python packages in the following order:
    - `conda create -n env-param python=3.8`
    - `conda activate env-parm`
    - `pip install torch` Do not conda install
    - `pip install hydra-core --upgrade`
    - `pip install hydra-optuna-sweeper --upgrade`
    - `pip install wandb`
    - `pip install pandas` - Do not conda install
    - `pip install -U scikit-learn`

## Developing Estimator module
- `conda install conda-build`
- `cd Parameter_Estimation`
- `conda develop .`

## Installing AMICI integrator, PEtab, and pyPESTO optimizer
- Instructions to install amici, petab, pypesto libraries in same conda environment:
    - `conda activate env-parm`
    - `conda install -c conda-forge gxx` (conda channel didn't work on M1 Pro)
    - `conda install -c conda-forge swig`
    - `conda install -c conda-forge openblas`
    - `conda install -c conda-forge hdf5`
    - `export BLAS_LIBS=-lopenblas`
    - `swig -version`   # Checking that SWIG is in PATH - returns SWIG 4.0.2 (conda version)
    - `pip3 install --no-cache --verbose amici`
    - `pip3 install petab pypesto openpyxl`
Note: This is necessary on Nano. Probably any linux machine.

## MV-M1
- Works on M1 with the following
    - `conda activate env-parm`
    - `conda install -c conda-forge swig`
    - `pip install amici`
    - `pip install petab`
    - `pip install pypesto`

## Vault Graph

![alt](notes/assets/diagram-Parameter_Estimation.svg)

## Publishing

- Refer to publishing note for reproducing preprints of the paper.
    - TLDR; run `cd notes && bash compile_paper.sh`


- Here is a change.
