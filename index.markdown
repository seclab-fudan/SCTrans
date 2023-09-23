---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
title: SCTrans

---

## Research Problem

Simulation testing has become a crucial tool for assessing the safety of autonomous driving systems (ADS), complementing physical road testing. Effective simulation testing relies on high-quality scenarios. These scenarios must also be properly formatted for ADS simulation platforms to use them as inputs. The absence of extensive public datasets of simulation scenarios hampers both industry and academic applications of ADS simulation testing.

Existing datasets offer vehicle-side raw sensor data or naturalistic trajectories of traffic participants for training and testing standalone algorithms within ADS (e.g., object detection, object tracking, and motion planning). However, these datasets often use non-standard formats that are incompatible with ADS simulation platforms. Some groups claim to have curated well-formatted simulation scenario files for ADS testing, but these datasets are not freely available due to commercial reasons. This lack of accessible simulation scenario datasets forces both ADS practitioners and academic researchers to manually curate scenarios, a time-consuming and expertise-dependent process.

In this work, we introduce a transformation-based approach which utilizes existing real-world traffic scenario datasets to create simulation scenario files. Formalizing it as a  Model Transformation Problem, we generate simulation-ready format scenario files that are compatible with advanced autonomous driving simulation platforms. We've implemented this concept in an automated tool called SCTrans, and we've assembled a dataset of over 1,900 diverse simulation scenarios.

We plan to release the [source code](#open-source-protocol) and [datasets](#open-source-protocol), see [our sharing policy](#open-source-protocol) for more details.

## Approach Overview

To address the aforementioned issue, we propose to achieve a format transformation, i.e., to transform traffic scenario recording files into simulation scenario files while preserving the scenario semantics. To ensure the correctness of this format conversion, we formalize this task as a Model Transformation Problem.

Specifically, we begin by creating <strong>Meta-Models</strong> for both traffic scenario recording files and simulation scenario files, referred to as the <strong>source Meta-Model</strong> and <strong>target Meta-Model</strong> respectively. These <strong>Meta-Models</strong> outline the abstract syntax of the respective languages, encompassing elements, structures, attributes, and their constraints.

Once we meticulously establish the precise mappings between the elements and attributes of the <strong>source Meta-Model</strong> and the <strong>target Meta-Model</strong>, we proceed to formulate concrete <strong>transformation rules</strong>. These rules enable the automated conversion of a traffic scenario recording file into a simulation scenario file.

Our approach is denoted as SCTrans

![SCTRans-running-example](./img/running-example.png)

## Paper Info

[ICSE 2024] <strong>Constructing a Large Public Scenario Dataset for Simulation Testing of Autonomous Driving Systems</strong>

*Jiarun Dai, Bufan Gao, Mingyuan Luo, Zongan Huang, Zhongrui Li, Yuan Zhang, Min Yang.*

To appear in the 46th International Conference on Software Engineering (ICSE), Lisbon, Portugal, April 14-20, 2024 (coming soon).

## Citation

```
@inproceedings{SCTrans-ICSE-2024,
    author={Jiarun Dai and Bufan Gao and Mingyuan Luo and Zongan Huang and Zhongrui Li and Yuan Zhang and Min Yang},
    booktitle={Proceedings of the 2024 International Conference on Software Engineering},
    title={Constructing a Large Public Scenario Dataset for Simulation Testing of Autonomous Driving Systems},
    year={2024},
}
```

## Open Source Protocol

### Introduction

For the safety assessment of autonomous driving systems (ADS), scenario-based simulation testing has become an important complementary technique to physical road testing, whose effectiveness is highly dependent on the quality of given simulation scenarios. However, the public availability of simulation scenario files is quite limited, largely hindering the applications of ADS simulation testing. In light of this, we are highly motivated to construct a large public dataset of ready-to-use simulation scenario files. However, to avoid misuse of our tool and dataset, we apply simple authentication to verify the identity of the user who wants to request access to our source code and dataset. 

### Usage Limitation

SCTrans tool and dataset provided within this initiative are exclusively intended for non-commercial academic research purposes. It is strictly prohibited to use the dataset for any commercial purposes, which includes but is not restricted to licensing, selling, or engaging in activities aimed at attaining commercial gains. Additionally, users are required to obtain our explicit permission before sharing the dataset or source code with any third parties.

### Accessing the Dataset

To apply for access to our source code and dataset, please read the following instructions and send your request email to Jiarun Dai (jrdai14@fudan.edu.cn) and Bufan Gao (bfgao22@m.fudan.edu.cn).

**=======  Instructions about Request Email =======**

**For Academic Researchers:**

If you are a student(or postdoc), please have your advisor (or host) send us an access email. If you are a faculty member, please send us an email from your university email account.

In your email, please include your name, affiliation, and home page (if we do not recognize each other). This information is required only for verification purposes. Please note that if we are unable to determine your identity or affiliation, your request may be ignored.

If your papers or articles use our dataset or our tool, please cite our ICSE 2024 paper.

**For Industry Researchers:**

If you are currently in industry (including research labs), please send us an email from your company's email account.

In the email, please briefly introduce yourself (e.g., name and title - in case we don't know each other) and your company.

**Mail Content:**

In your email, please kindly attach a justification letter (in PDF format) printed on official letterhead. This letter should recognize the "SCTrans" project from Fudan University and explicitly outline the purpose behind your dataset or source code request. Moreover, confirm your commitment to utilizing the dataset or source code solely for non-commercial purposes and assure that it will not be disseminated to others without our prior consent.


It is imperative to stress that we will disregard emails that do not adhere to the instructions provided above. Furthermore, please be aware that we reserve the right to publicly display on the SCTrans homepage the names of universities, research laboratories, and companies that have submitted dataset access requests. By sending an email to us requesting access to our source code or dataset, you acknowledge and agree to abide by the aforementioned policy.



## Dataset

To evaluate the prototype of SCTrans, we selected random traffic scenario recording files from representative traffic scenario datasets: CommonRoad<sup><a href="#reference">[1]</a></sup>, inD<sup><a href="#reference">[2]</a></sup>, and highD<sup><a href="#reference">[3]</a></sup>. This resulted in a collection of 1,994 simulation scenario files. The breakdown is as follows: 994 from CommonRoad, 500 from inD, and another 500 from highD. These scenarios were built on 406 different maps and are compatible with advanced simulation platforms like LGSVL<sup><a href="#reference">[4]</a></sup>+Apollo<sup><a href="#reference">[5]</a></sup> and Carla<sup><a href="#reference">[6]</a></sup>+Autoware<sup><a href="#reference">[7]</a></sup>.

Each output includes two description files (VSE Scenario and OpenScenario), four map description files (Apollo HD Map, Autoware Vector Map, OpenDrive, and Lanelet2), and a map assets file (LGSVL AssetBundle). Additionally, we provide scenario players for two simulators.

We intend to release this comprehensive dataset, containing all curated scenario files generated by SCTrans. To access this dataset, please follow our sharing protocol.

Please note that according to our policy, we cannot provide access to the source traffic scenarios directly. If you wish to access these source traffic scenarios, kindly refer to the provided reference<sup><a href="#reference">[8,9,10]</a></sup> and adhere to the specified requirements.


## Source Code

We are also in the process of releasing the complete source code for all SCTrans modules. This includes SCTrans itself, the scenario player for two simulators, and any other modified code. To access the source code, please follow our established sharing protocol.


## Team Members

- Jiarun Dai, Fudan University

- Bufan Gao, Fudan University

- Mingyuan Luo, Fudan University

- Zongan Huang, Fudan University

- Zhongrui Li, Fudan University

- [Yuan Zhang](https://yuanxzhang.github.io/), Fudan University

- Min Yang, Fudan University



## Reference
[1] M. Althoff, M. Koschi, and S. Manzinger. CommonRoad: Composable Benchmarks for Motion Planning on Roads. In Proceedings of the IEEE Intelligent Vehicles Symposium (IV), 2017.

[2] J. Bock, R. Krajewski, T. Moers, S. Runde, L. Vater, and L. Eckstein. The Ind Dataset: A Drone Dataset of Naturalistic Road User Trajectories at German Intersections. In Proceedings of the IEEE Intelligent Vehicles Symposium (IV), 2020.

[3] R. Krajewski, J. Bock, L. Kloeker, and L. Eckstein. The Highd Dataset: A Drone Dataset of Naturalistic Vehicle Trajectories on German Highways for Validation 1256 of Highly Automated Driving Systems. In Proceedings of the 21st International 1257 Conference on Intelligent Transportation Systems (ITSC), 2018.

[4] G. Rong, B. H. Shin, H. Tabatabaee, Q. Lu, S. Lemke, M. Možeiko, E. Boise, G. Uhm, M. Gerow, S. Mehta, et al. Lgsvl Simulator: A High Fidelity Simulator for Autonomous Driving. In Proceedings of the 23rd IEEE International Conference on Intelligent Transportation Systems (ITSC), 2020.

[5] Open-sourced Version of Baidu Apollo. https://github.com/ApolloAuto/apollo, 2023.

[6] A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, and V. Koltun. CARLA: An Open 1236 Urban Driving Simulator. In Conference on Robot Learning, 2017.

[7] Autoware-AI. https://github.com/autowarefoundation/autoware, 2023.

[8] CommonRoad. https://commonroad.in.tum.de, 2023.

[9] InD Dataset. https://www.ind-dataset.com, 2023.

[10] HighD Dataset. https://www.highd-dataset.com, 2023.
