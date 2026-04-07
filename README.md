---
title: Finance RL Environment
emoji: 💰
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# 💰 Finance RL Environment

## Overview
This environment simulates real-world financial decision-making.

## Actions
- invest
- save
- spend

## Tasks
- easy (high balance)
- medium (moderate balance)
- hard (low balance)

## Reward System
- Positive reward for saving/investing
- Negative reward for overspending

## Score
Final score between 0.0 and 1.0 using a grader.

## API
- POST /reset
- POST /step
- GET /state

“This environment focuses on personal financial behavior rather than market trading, making it useful for evaluating decision-making in everyday financial scenarios.”