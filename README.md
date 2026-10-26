# Drone Research

Simulation and flight-control research using PX4, Gazebo, and MAVSDK-Python.
This page walks through the full setup: Ubuntu, PX4 Autopilot, GPU rendering, MAVSDK, and running your first flight with `fly.py`.

## Contents

1. [Ubuntu](#1-ubuntu)
2. [Update packages](#2-update-packages)
3. [Workspace setup](#3-workspace-setup)
4. [Download and build PX4 Autopilot](#4-download-and-build-px4-autopilot)
5. [Python environment](#5-python-environment)
6. [Verify GPU rendering](#6-verify-gpu-rendering)
7. [Install MAVSDK](#7-install-mavsdk)
8. [Get the flight files](#8-get-the-flight-files)
9. [Run a flight](#9-run-a-flight)
10. [Following the drone in Gazebo](#10-following-the-drone-in-gazebo)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Ubuntu

Make sure Ubuntu **24.04 LTS** (or the latest Ubuntu version PX4 supports) is installed, either natively or under WSL2.

> PX4's `ubuntu.sh` targets Ubuntu LTS releases. If you are on a newer non-LTS release, check the [PX4 dev environment docs](https://docs.px4.io/main/en/dev_setup/dev_env_linux_ubuntu.html) before building.

Check your version:

```bash
lsb_release -a
```

## 2. Update packages

```bash
sudo apt update -y
```

You will also need `git`:

```bash
sudo apt install -y git
```

## 3. Workspace setup

```bash
cd ~
mkdir dronestuff
```

## 4. Download and build PX4 Autopilot

Download PX4 (with submodules) into your home directory:

```bash
cd ~
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
```

Move it into the workspace:

```bash
mv ~/PX4-Autopilot ~/dronestuff/
```

Run the Ubuntu setup script from the PX4 folder. This installs the toolchain and Gazebo:

```bash
cd ~/dronestuff/PX4-Autopilot
bash ./Tools/setup/ubuntu.sh
```

Restart your computer (or WSL instance, via `wsl --shutdown` from Windows) when the script finishes, then build and test the simulator:

```bash
cd ~/dronestuff/PX4-Autopilot
make px4_sitl gz_x500
```

The first build takes a while. When Gazebo opens with an x500 quadcopter, PX4 is working. Close it with `Ctrl+C` and continue.

## 5. Python environment

```bash
cd ~/dronestuff
sudo apt install python3-full python3-venv
```

Create and activate a virtual environment (required on newer Ubuntu releases where system-wide `pip` is blocked):

```bash
python3 -m venv venv
source venv/bin/activate
```

## 6. Verify GPU rendering

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

## 7. Install MAVSDK

With the virtual environment active:

```bash
pip install "mavsdk<4"
```

> The quotes are required. Without them the shell treats `<4` as input redirection and the install fails.

## 8. Get the flight files

Download everything needed to run `fly.py` into the workspace:

```bash
cd ~/dronestuff
# TODO: replace with your repo URL
git clone https://github.com/<your-username>/<your-repo>.git drone-research
```

Expected layout:

```
dronestuff/
├── PX4-Autopilot/
├── venv/
└── drone-research/
    ├── fly.py
    └── ...            # list any supporting modules/files here
```

## 9. Run a flight

1. Start the PX4 + Gazebo simulation in one terminal:

```bash
cd ~/dronestuff/PX4-Autopilot
make px4_sitl gz_x500
```

2. In a second terminal, activate the environment and run the script:

```bash
cd ~/dronestuff
source venv/bin/activate
cd drone-research
python fly.py
```

## 10. Following the drone in Gazebo

To have the Gazebo camera follow a vehicle, run this in a **separate terminal** from the simulation and from `fly.py`:

```bash
gz service -s /gui/follow \
  --reqtype gz.msgs.StringMsg \
  --reptype gz.msgs.Boolean \
  --timeout 2000 \
  --req 'data: "x500_0"'
```

### Multiple drones

Each spawned model gets an incrementing suffix: `x500_0`, `x500_1`, `x500_2`, and so on. To see the exact model names currently in the world:

```bash
gz model --list
```

Then change the `data: "..."` value in the follow command to the model you want, for example `data: "x500_1"`.

## 11. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Gazebo is very slow / low FPS | Software rendering (`llvmpipe`) | Set `MESA_D3D12_DEFAULT_ADAPTER_NAME` as shown in step 6 |
| `pip install mavsdk<4` creates a file named `4` | Unquoted `<` | Use `pip install "mavsdk<4"` |
| `externally-managed-environment` error | System Python is protected | Activate the venv first |
| `make px4_sitl` fails after `ubuntu.sh` | Environment not reloaded | Restart your machine / WSL, then rebuild |
| Follow command times out | Wrong model name | Run `gz model --list` and use the exact name |
