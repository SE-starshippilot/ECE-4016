# ECE 4016 Assignment 2 Report

**Tianhao SHI (120090472)**

Nov, 2023

****

## Algorithm Analysis

The Buffer Occupancy-based Lyapunov Algorithm (BOLA) is a near-optimal bitrate adaptation algorithm for online videos. It is designed to maximize each encoded chunk’s video quality while minimizing rebuffering time. The algorithm effectively transforms the adaptive bitrate algorithm into solving a well-defined optimization problem. 

### Problem Formulation

In the original paper, the authors proposed to model the downloading process into multiple submodels.

The video model consists of a series of **N** segments, each of which spans **p** seconds in duration. These segments are encoded at **M** different bitrates, with higher bitrate indices corresponding to larger segments. The size of the segment encoded at bitrate **m** is denoted as $\textbf{S}_m$. 

In this video streaming setup, the buffer has a finite capacity, and it can store a maximum of $\textbf{Q}_{max}$ segments. If the buffer reaches its capacity, a pause of $\textbf{${\Delta}$}$ seconds will be triggered. During this pause period, the video player will temporarily halt downloading of new video segments to fill the buffer. 

The proposed network model considers the available network bandwidth between the client and server as a stochastic variable denoted by $\omega(t)$. This bandwidth fluctuates over time, and the cumulative data downloaded, denoted as $S_M$, is determined by integrating the bandwidth function from time $t$ to $t'$. The choice of video bitrate has a direct impact on the download time, as the client strives to maximize the utilization of the available bandwidth for segment retrieval. 

Finally, the authors divided the timeline into multiple *non-overlapping, consecutive* segments. Each segment starts at time $t_k$, and at this time point, the client player makes a decision whether or not to download a video segment. If so, the timeslot lasts for $T_k$ seconds long; if not, there will be a fixed pause of $\Delta$ seconds. The decision is formulated as an indicator function $a_m(t_k)$.
$$
a_m(t_k)=\begin{cases*}1\quad &\text{if download a  segment with bitrate index \textit{m} at slot \textit{k}} \\ 0&\text{else}\end{cases*}
$$
It is then derived that $\sum\limits_{m=1}^Ma_m(t_k)\leq1$, because there could be at most 1 segment to be chosen. An illustration is shown below:

![Slot.drawio](/Users/shitianhao/Documents/Year 4 Term 1/ECE 4016/A2_ABR/Slot.drawio.png)

### Objective Function

The overall goal of BOLA is to strike a balance between reducing the probability that the video freezes (rebuffers) and enhancing the quality of the video. The enhancement of video quality is described by the time-average expected *playback utility*:
$$
\bar{v}_N=\frac{\mathbb{E}\{\sum_{k=1}^{K_N}\sum_{m=1}^{M}a_m(t_k)v_m\}}{\mathbb{E}\{T_{end}\}}
$$
On the other hand, to minimize rebuffering, the authors introduced another term, *playback smoothness*:
$$
\bar{s}_N=\frac{Np}{E(T_{end})}=\frac{\mathbb{E}\{\sum_{k=1}^{K_N}\sum_{m=1}^{M}a_m(t_k)p\}}{\mathbb{E}\{T_{end}\}}
$$


Therefore, the overall utility function is derived as $\bar{v}_N+\gamma\bar{s}_N$

## Implementation

At the beginning of a time slot, given the buffer level $Q(t_k)$, segment sizes $S_m$ and corresponding watching utilities $v_m$,
$$
\text{Define:} \quad \rho(t_kma(t_k))=\begin{cases}0\qquad&\text{if} \sum_{m=1}^Ma_m(t_k)=0\\ \frac{\sum_{m=1}^Ma_m(t_k)(V{v_m}+V\gamma p-Q(t_k))}{\sum_{m=1}^Ma_m(t_k)S_m}&\text{otherwise}\end{cases}
$$
Where $V, \gamma$ are hyperparameters, and $p$ is a known value, our goal is to solve the problem is defined as follows:
$$
\begin{align}&\text{Maximize:} \quad \rho(t_kma(t_k))\\
&\text{Subject to:} \sum_{m=1}^Ma_m(t_k)\leq1, a_m(t_k)\in\{0,1\}\end{align}
$$
The optimal is derived at
$$
\DeclareMathOperator*{\argmax}{argmax} % no space, limits underneath in display
\argmax_{m}\quad(Vv_m+V\gamma p-Q(t_k))/S_m
$$


Moreover, to prevent the buffer from running dry during a segment download, we have to dynamically adjust $V$. We follow the psuedo code provided in the paper:

![image-20231105151805019](/Users/shitianhao/Library/Application Support/typora-user-images/image-20231105151805019.png)

However, it should be noted that we cannot adopt the download abandoning policy in this figure, because we don't have access to downloading control.  Moreover, since our code does not directly measure buffer in terms of seconds, we have to do a conversion from bits to seconds: $Q_{max, sec}=Q_{max, bits}/S_{-1}$

In our implementation, we set $\gamma p=10$, as it provides optimal performance.

## Evaluation

**Table 1: Comparison of Score**

|             | testALThard   | testHD       | testPQ   | badtest    | testALTsoft | testHDmanPQtrace |
| ----------------- | :-----------: | :---------:  | -------  | -----------| ----------- | ---------------- |
| Baseline   | 8535.21       | 3825384.87   | 0.16     | 7518.93    | 407852.94  | 0.20           |
| BOLA (ours) | **567115.37** | **1689312.29** | 0.16     | **566795.45** | **1245902.72** | 0.20           |

As the figure shows, our implementation of BOLA algorithm significantly outperformed Baseline algorithm in most cases. However, it achieved same performance on **testPQ ** and **testHDmanPQtrace**. The reason is that in these two cases, the network bandwidth stayed at a consistent low level. To prevent rebuffering, BOLA chooses to use a lower bitrate.
