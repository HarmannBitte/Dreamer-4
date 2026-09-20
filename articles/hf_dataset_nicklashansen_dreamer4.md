<!-- source: https://huggingface.co/datasets/nicklashansen/dreamer4
     fetched: 2026-09-20T13:37:22Z -->

[Paper • 2511.19584 • Published](https://huggingface.co/papers/2511.19584)   

[Duplicate](https://huggingface.co/datasets/nicklashansen/dreamer4?duplicate=true)

## The dataset viewer is not available for this split.

Error code:   JobManagerCrashedError

Need help to make the dataset viewer work? Make sure to review [how to configure the dataset viewer](https://huggingface.co/docs/hub/datasets-data-files-configuration), and [open a discussion](https://huggingface.co/datasets/nicklashansen/dreamer4/discussions/new?title=Dataset+Viewer+issue%3A+JobManagerCrashedError&description=The+dataset+viewer+is+not+working.%0A%0AError+details%3A%0A%0A%60%60%60%0AError+code%3A+++JobManagerCrashedError%0A%0A%60%60%60%0A%0A%0Acc+%40lhoestq+%40cfahlgren1.) for direct support.

# 
	
		
	
	
		Dreamer 4 Dataset for Continuous Control
	

Dataset released as part of an effort to open-source world model research. See [https://github.com/nicklashansen/dreamer4](https://github.com/nicklashansen/dreamer4) for detailed instructions on how to use the released dataset!

Our dataset contains 7,200 mixed-quality trajectories (3.6M frames) spanning **30 continuous control tasks** from [DMControl](https://arxiv.org/abs/1801.00690) and [MMBench](https://arxiv.org/abs/2511.19584). To construct the dataset, we collect 240 trajectories per task using expert [TD-MPC2](https://www.tdmpc2.com) agents that were released as part of our [Newt/MMBench](https://www.nicklashansen.com/NewtWM) project. We use a default resolution of 128×128 for training but the dataset supports up to 224×224.

# 
	
		
	
	
		Citations
	

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
## 
	
		
	
	
		Contact
	

Correspondence to: [Nicklas Hansen](https://nicklashansen.github.io)

- Downloads last month
- 816