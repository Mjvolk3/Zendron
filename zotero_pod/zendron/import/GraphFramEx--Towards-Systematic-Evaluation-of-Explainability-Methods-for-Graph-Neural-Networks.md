---
metadata_key: AZ78ZU3N
---

## Metadata

- Title: [[GraphFramEx: Towards Systematic Evaluation of Explainability Methods for Graph Neural Networks|dendron://Zendron/zendron.import.title.GraphFramEx--Towards-Systematic-Evaluation-of-Explainability-Methods-for-Graph-Neural-Networks]]
- Authors: [[Kenza Amara|dendron://Zendron/zendron.import.authors.Kenza-Amara]], [[Rex Ying|dendron://Zendron/zendron.import.authors.Rex-Ying]], [[Zitao Zhang|dendron://Zendron/zendron.import.authors.Zitao-Zhang]], [[Zhihao Han|dendron://Zendron/zendron.import.authors.Zhihao-Han]], [[Yinan Shan|dendron://Zendron/zendron.import.authors.Yinan-Shan]], [[Ulrik Brandes|dendron://Zendron/zendron.import.authors.Ulrik-Brandes]], [[Sebastian Schemm|dendron://Zendron/zendron.import.authors.Sebastian-Schemm]], [[Ce Zhang|dendron://Zendron/zendron.import.authors.Ce-Zhang]]
- Date: [[2022-10-11|dendron://Zendron/zendron.import.date.2022.10.11]]
- Date Accessed: [[2023-01-13|dendron://Zendron/zendron.import.date.2023.01.13]]
- Date Added: [[2023-02-03-17-17-09|dendron://Zendron/zendron.import.date.2023.02.03.17.17.09]]
- Date Modified: [[2023-04-20-19-13-21|dendron://Zendron/zendron.import.date.2023.04.20.19.13.21]]
- URL: [http://arxiv.org/abs/2206.09677](http://arxiv.org/abs/2206.09677)
- DOI: [10.48550/arXiv.2206.09677](http://doi.org/10.48550/arXiv.2206.09677)
- Citation Key: [[amaraGraphFramExSystematicEvaluation2022|user.amaraGraphFramExSystematicEvaluation2022]]
- Citations: No citations
- Publication Title: No publication title
- Journal Abbreviation: No publication title
- Item Type: [[preprint|dendron://Zendron/zendron.import.item-type.preprint]]
- PDF Attachments: [Online PDF attachment](https://www.zotero.org/groups/4932032/zendron/items/AZ78ZU3N/attachment/F4TCQH4B/reader)
- Tags: #Computer Science - Artificial Intelligence, #Computer Science - Machine Learning
- Local Library: [Local Library](zotero://select/items/4932032)
- Cloud Library: [Cloud Library](https://www.zotero.org/groups/4932032/Zendron/library)

## Abstract

As one of the most popular machine learning models today, graph neural networks (GNNs) have attracted intense interest recently, and so does their explainability. Users are increasingly interested in a better understanding of GNN models and their outcomes. Unfortunately, today's evaluation frameworks for GNN explainability often rely on few inadequate synthetic datasets, leading to conclusions of limited scope due to a lack of complexity in the problem instances. As GNN models are deployed to more mission-critical applications, we are in dire need for a common evaluation protocol of explainability methods of GNNs. In this paper, we propose, to our best knowledge, the first systematic evaluation framework for GNN explainability, considering explainability on three different "user needs". We propose a unique metric that combines the fidelity measures and classifies explanations based on their quality of being sufficient or necessary. We scope ourselves to node classification tasks and compare the most representative techniques in the field of input-level explainability for GNNs. For the inadequate but widely used synthetic benchmarks, surprisingly shallow techniques such as personalized PageRank have the best performance for a minimum computation time. But when the graph structure is more complex and nodes have meaningful features, gradient-based methods are the best according to our evaluation criteria. However, none dominates the others on all evaluation dimensions and there is always a trade-off. We further apply our evaluation protocol in a case study for frauds explanation on eBay transaction graphs to reflect the production environment.