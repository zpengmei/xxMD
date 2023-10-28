# xxMD Dataset

## Description
The xxMD (Extended Excited-state Molecular Dynamics) dataset is a comprehensive collection of non-adiabatic trajectories encompassing several photo-sensitive molecules. This dataset challenges existing Neural Force Field (NFF) models with broader nuclear configuration spaces that span reactant, transition state, product, and conical intersection regions, making it more chemically representative than its contemporaries.

## Key Features

- Based on non-adiabatic dynamics, involving larger nuclear configuration space compared to previous datasets.
- Contains trajectories from four photo-sensitive molecules, each starting from an electronic excited state.
- Energies and forces computed using both multireference wave function theory and density functional theory.
- Samples reactant, transition state, product, and conical intersection regions of potential energy surfaces.

## Dataset Contents

1. **xxMD-CASSCF**: This subset contains potential energies and forces for the first three electronic states of four molecules: azobenzene, dithiopehene, malonaldehyde, and stilbene.
2. **xxMD-DFT**: Ground-state energies and forces re-computed using the M06 exchange-correlation functional for the trajectories in the xxMD-CASSCF subset.

## Usage

The datasets are stored in extented xyz format, which can be directly imported and used in various computational chemistry software and machine learning frameworks.

## Citation
If you use the xxMD dataset in your research, please cite the original publication:

```
@inproceedings{
pengmei2023beyond,
title={Beyond {MD}17: The xx{MD} Dataset as a Chemically Meaningful Benchmark for Neural Force Fields Development},
author={Zihan Pengmei and Junyu Liu and Yinan Shu},
booktitle={NeurIPS 2023 AI for Science Workshop},
year={2023},
url={https://openreview.net/forum?id=h9HuWcDJ6C}
}
```

## Feedback and Contributions
We welcome feedback, issue reports, and contributions. If you have any suggestions or find any inconsistencies in the dataset, please raise an issue or submit a pull request.

---

Designed and curated by Zihan Pengmei and Yinan Shu. For further inquiries, please contact shuxx055@umn.edu or zpengmei@uchicago.edu.
