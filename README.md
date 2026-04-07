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

## 🌍 Real-World Features

- Random life events (bonus, emergency)
- Goal-based savings objective
- Dynamic reward shaping
- Penalty for overspending

This environment simulates realistic financial decision-making.

## 🎯 Reward Design

The reward function combines:
- Immediate action impact
- Net financial health (balance + savings - expenses)
- Goal progress towards savings target
- Penalties for overspending
- Stochastic external events

This ensures a dense and meaningful learning signal for agent evaluation.