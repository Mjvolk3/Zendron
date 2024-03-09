---
id: 0qlynh7ogx26szg23o964gi
title: Annotations
desc: ''
updated: 1709419791273
created: 1709370914115
isDir: false
---
## Annotations

### Date Added: 2024-03-02 08:57:40+00:00

![](./assets/images/zendron-image-import-DBPIRL4I.png)

- Annotator: @mjvolk3
- Comment (🟡)
- Tags:

### Date Added: 2024-03-02 09:13:10+00:00

Here, $ \boldsymbol { \mu } = \mathrm { GCN } _ { \boldsymbol { \mu } } ( \mathbf { X } , \mathbf { A } ) $ is the matrix of mean vectors $ \boldsymbol { \mu } _ { i } ; $ similarly $ \log \boldsymbol { \sigma } = \mathrm { GCN } _ { \boldsymbol { \sigma } } ( \mathbf { X } , \mathbf { A } ) $.

The two-layer

The two-layer $\operatorname{GCN}$ is defined as

$$
\operatorname{GCN} (\mathbf{X} , \mathbf{A}) = \tilde {\mathbf{A}} \operatorname{ReLU} \left(\tilde{\mathbf{A}}\mathbf{X}\mathbf{W}_0\right)\mathbf{W}_1
$$

, with weight matrices

$ \mathbf { W } _ { i } \cdot \operatorname { GCN } _ { \boldsymbol { \mu } } ( \mathbf { X } , \mathbf { A } ) $ and $ \operatorname { GCN } _ { \boldsymbol { \sigma } } ( \mathbf { X } , \mathbf { A } ) $ share first-layer parameters $ \mathbf { W } _ { 0 } \cdot \operatorname { ReLU } ( \cdot ) = \max ( 0 , \cdot ) $ and
$ \tilde { \mathbf { A } } = \mathbf { D } ^ { - \frac { 1 } { 2 } } \mathbf { A } \mathbf { D } ^ { - \frac { 1 } { 2 } } $ is the symmetrically normalized adjacency matrix.

- Annotator: @mjvolk3
- Comment (🟡)
- Tags: #mpx

### Date Added: 2024-03-02 09:10:22+00:00

> where KL[q(·)||p(·)] is the Kullback-Leibler divergence between q(·) and p(·). We further take a Gaussian prior p(Z) = ∏ i p(zi) = ∏ i N (zi | 0, I). For very sparse A, it can be beneficial to re-weight terms with Aij = 1 in L or alternatively sub-sample terms with Aij = 0. We choose the former for the following experiments. We perform full-batch gradient descent and make use of the reparameterization trick [2] for training. For a featureless approach, we simply drop the dependence on X and replace X with the identity matrix in the GCN.

- Annotator: @mjvolk3
- Comment (🔵) : This highlight has a lot of math that might not be rendered very nicely.
- Tags:

## Local Comments

- [[Local Comments|dendron://Zendron/zendron.import.variational-graph-auto-encoders.comments]]
