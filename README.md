# Drone Research

Simulation and flight-control research using PX4, Gazebo, and MAVSDK-Python.
This page walks through prerequisites, downloads, and running your first flight with `fly.py`.

## Contents

1. [Prerequisites](#prerequisites)
2. [Workspace setup](#workspace-setup)
3. [Python environment](#python-environment)
4. [Verify GPU rendering](#verify-gpu-rendering)
5. [Install MAVSDK](#install-mavsdk)
6. [Get the flight files](#get-the-flight-files)
7. [Run a flight](#run-a-flight)
8. [Following the drone in Gazebo](#following-the-drone-in-gazebo)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Ubuntu (native or WSL2)
- PX4 + Gazebo simulation already installed (models such as `x500` should spawn)
- `sudo` access
- A GPU with working drivers (software rendering via `llvmpipe` works but is very slow)

## Workspace setup

All commands start from your home directory:

```bash
cd ~
mkdir dronestuff && cd dronestuff
```

## Python environment

```bash
sudo apt install python3-full python3-venv
```

Create and activate a virtual environment (recommended, and required on newer Ubuntu releases where system-wide `pip` is blocked):

```bash
python3 -m venv venv
source venv/bin/activate
```

## Verify GPU rendering

Install the Mesa utilities:

```bash
sudo apt install mesa-utils
```

Check which renderer is in use:

```bash
glxinfo -B | grep -i "renderer"
```

If the output shows `llvmpipe` or anything other than your graphics card, Gazebo is rendering on the CPU. Fix it by pointing Mesa at your GPU adapter (this applies mainly to **WSL2**):

```bash
echo 'export MESA_D3D12_DEFAULT_ADAPTER_NAME=____' >> ~/.bashrc
source ~/.bashrc
```

Replace `____` with your graphics card name (e.g. `NVIDIA`). Re-run `glxinfo -B | grep -i "renderer"` to confirm your GPU now appears.

## Install MAVSDK

```bash
pip install "mavsdk<4"
```

> The quotes are required. Without them the shell treats `<4` as input redirection and the install fails.

## Get the flight files

Download everything needed to run `fly.py` into `~/dronestuff`:

```bash
# TODO: replace with your repo URL
git clone https://github.com/<your-username>/<your-repo>.git .
```

Expected contents:

```
dronestuff/
├── fly.py
└── ...            # list any supporting modules/files here
```

## Run a flight

1. Start the PX4 + Gazebo simulation in one terminal.
2. In a second terminal, activate the environment and run the script:

```bash
cd ~/dronestuff
source venv/bin/activate
python fly.py
```

## Following the drone in Gazebo

To have the Gazebo camera follow a vehicle:

```bash
gz service -s /gui/follow \
  --reqtype gz.msgs.StringMsg \
  --reptype gz.msgs.Boolean \
  --timeout 2000 \
  --req 'data: "x500_0"'
```

Run this in a **separate terminal** from the simulation and from `fly.py`.

### Multiple drones

Each spawned model gets an incrementing suffix: `x500_0`, `x500_1`, `x500_2`, and so on. To see the exact model names currently in the world:

```bash
gz model --list
```

Then change the `data: "..."` value in the follow command to the model you want, for example `data: "x500_1"`.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Gazebo is very slow / low FPS | Software rendering (`llvmpipe`) | Set `MESA_D3D12_DEFAULT_ADAPTER_NAME` as shown above |
| `pip install mavsdk<4` creates a file named `4` | Unquoted `<` | Use `pip install "mavsdk<4"` |
| `externally-managed-environment` error | System Python is protected | Activate the venv first |
| Follow command times out | Wrong model name | Run `gz model --list` and use the exact name |
