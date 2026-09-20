---
license: mit
tags:
- reinforcement learning
- world model
- continuous control
- robotics
pipeline_tag: reinforcement-learning
---

# Dreamer 4 Dataset for Continuous Control

Dataset released as part of an effort to open-source world model research. See [https://github.com/nicklashansen/dreamer4](https://github.com/nicklashansen/dreamer4) for detailed instructions on how to use the released dataset!

Our dataset contains 7,200 mixed-quality trajectories (3.6M frames) spanning **30 continuous control tasks** from [DMControl](https://arxiv.org/abs/1801.00690) and [MMBench](https://arxiv.org/abs/2511.19584). To construct the dataset, we collect 240 trajectories per task using expert [TD-MPC2](https://www.tdmpc2.com) agents that were released as part of our [Newt/MMBench](https://www.nicklashansen.com/NewtWM) project. We use a default resolution of 128×128 for training but the dataset supports up to 224×224.


# Citations

If you find our work useful, please consider citing us as:

```
@misc{Hansen2026Dreamer4PyTorch,
    title={Dreamer 4 in PyTorch},
    author={Nicklas Hansen},
    year={2026},
    publisher={GitHub},
    journal={GitHub repository},
    howpublished={\url{https://github.com/nicklashansen/dreamer4}},
}
```

as well as the original Dreamer 4 paper:

```
@misc{Hafner2025TrainingAgents,
    title={Training Agents Inside of Scalable World Models}, 
    author={Danijar Hafner and Wilson Yan and Timothy Lillicrap},
    year={2025},
    eprint={2509.24527},
    archivePrefix={arXiv},
    primaryClass={cs.AI},
    url={https://arxiv.org/abs/2509.24527}, 
}
```

## Contact

Correspondence to: [Nicklas Hansen](https://nicklashansen.github.io)