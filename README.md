[![SWH](https://archive.softwareheritage.org/badge/origin/https://github.com/seclab-fudan/SCTrans/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/seclab-fudan/SCTrans)
[![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:8d41cfb4593d6d9ed32598c7f4b005d9a2023776/)](https://archive.softwareheritage.org/swh:1:dir:8d41cfb4593d6d9ed32598c7f4b005d9a2023776;origin=https://github.com/seclab-fudan/SCTrans;visit=swh:1:snp:fa8dc0740415fb547c5cb2fa33d79d999b6306ea;anchor=swh:1:rev:1bea2942f11ec72872d736f1de630d6d347b3233)

# SCTrans
Welcome to the SCTrans repository, which provides tools and scripts supporting our paper **"SCTrans: Constructing a Large Public Scenario Dataset for Simulation Testing of Autonomous Driving Systems"** accepted at ICSE24. Visit our [website](https://seclab-fudan.github.io/SCTrans/) for more information and **dataset access**(See Section Open Source Protocol).

### Quickstart
- **Source Code:**
  - Explore the `scenario-runner/` directory for modified versions of Lgsvl & Carla scenario runners.
  - The `transformation/` directory contains all code necessary for scenario transformations.
- **Docker Container:**
  - **Download:** Access the Docker container [here](https://drive.google.com/file/d/1NReqsgsbG_gj-j89GF_2wx6hB4u_NRSJ/view?usp=share_link) to streamline setup and usage.
  - **Instructions:** Detailed guidelines on using the Docker container are available in the artifact readme, accessible [here](https://github.com/seclab-fudan/SCTrans/blob/main/ICSE_Artifact_Readme.pdf).
- [**Note**] We’ve transitioned away from the VM as the Docker setup is designed to be sufficient.

### How to Contribute
We value your contributions to improve SCTrans. Here’s how you can help:
- **Code Contributions:** Feel free to fork the repository, make your changes, and submit a pull request.
- **Issue Reporting:** If you encounter issues or have suggestions, please submit them as issues on GitHub.


### File Contents
- `scenario-runner/` directory contains modified version of Lgsvl & Carla scenario runner
- `transformation/` directory contains all code for scenario transformation

### Supplemental Source

To complement the SCTrans tools and facilitate integration with popular simulation platforms, the following resources are available:

- **LGSVL Simulator Build Local Version:** 

  A local version of the LGSVL simulator can be accessed [here](https://github.com/emocat/simulator/tree/release-2021.2).

- **Carla and Autoware Bridge:**
  
  A simulation bridge between Carla and Autoware can be accessed [here](https://github.com/tumftm/carla-autoware-bridge).

- **Carla and Apollo Bridge Reference**
  
  A simulation bridge between Carla and Apollo can be accessed [here](https://github.com/guardstrikelab/carla_apollo_bridge).

- **LGSVL and Autoware Bridge Reference**

  A simulation bridge between LGSVL simulator and Autoware can be accessed [here](https://github.com/blabla-my/autoware-LGSVL-bridge).

- **LGSVL and Apollo Bridge**

  Please refer to the [LGSVL PythonAPI](https://github.com/lgsvl/PythonAPI) repository for more information.

### Publication
If you find this repository useful, please consider citing our paper and give this repository a Star🌟.

Paper Link: [ICSE24-SCTrans](https://dl.acm.org/doi/10.1145/3597503.3623350)

Paper Citation:
```
@inproceedings{SCTrans-ICSE-2024,
    author={Jiarun Dai and Bufan Gao and Mingyuan Luo and Zongan Huang and Zhongrui Li and Yuan Zhang and Min Yang},
    booktitle={Proceedings of the 2024 International Conference on Software Engineering},
    title={Constructing a Large Public Scenario Dataset for Simulation Testing of Autonomous Driving Systems},
    year={2024},
}
```



