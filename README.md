# Autonomous Mobile Robot 🤖

A hands-on robotics project developed alongside Stanford University's
AA274A - Principles of Robot Autonomy course.

## Project Goal

Build a simulated differential-drive mobile robot capable of autonomous
indoor navigation.

## Current Features

- ROS 2 velocity publisher using `/cmd_vel`
- Unicycle kinematic model
- Robot pose updates using numerical integration
- Flask-based web dashboard for robot visualization

## Tech Stack

- Python 3
- ROS 2 Jazzy
- Ubuntu 24.04
- Docker / OrbStack
- Flask

## Robot Kinematics

The robot state is `(x, y, theta)`.

- `dx/dt = v * cos(theta)`
- `dy/dt = v * sin(theta)`
- `dtheta/dt = omega`

## Development Roadmap

- [x] ROS 2 development environment
- [x] Velocity publisher and subscriber
- [x] Unicycle kinematics
- [x] Web dashboard
- [ ] Indoor environment and obstacles
- [ ] Collision detection
- [ ] A* path planning
- [ ] PRM and RRT planning
- [ ] Trajectory tracking and control
- [ ] Simulated sensors

## Learning Resources

[Stanford AA274A - Principles of Robot Autonomy](https://stanfordasl.github.io/PoRA-I/aa274a_aut2223/)

## Status

Work in progress.
