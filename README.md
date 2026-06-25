# CRML — Centralized Robotic Machine Learning

> The learning layer for your home robot fleet.

CRML is an extension of [CRCS](https://github.com/siddhesh1008/CRCS) that centralizes ML training across all robots in a home environment. Rather than training each robot separately, CRML trains a unified set of models — covering motion planning, perception, and task management — that the entire fleet shares.

It runs as a container alongside CRCS, Home Assistant, a local AI model, and Mosquitto, forming a single integrated stack for home robotics.
