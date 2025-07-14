# 🕰️ EurekaSim Pendulum Plugin


---

## 📸 Demo

[![Pendulum Simulation on YouTube](https://img.shields.io/badge/YouTube-Watch%20Demo-red?logo=youtube)](https://www.youtube.com/watch?v=UVqJYrmjYRg&ab_channel=JudeTheDude)

---

## 🌟 Overview

The **Pendulum Plugin** is a sample C++ plugin for [EurekaSim](https://github.com/Judethedude007/eurekasim), demonstrating the simulation of a simple pendulum. This serves as a foundational example for developing scientific and engineering simulation modules with EurekaSim’s extensible SDK.

---

## ⚙️ How It Works

The plugin simulates the dynamics of a classical pendulum using the following equation:
- **θ (Theta):** Angular displacement (in radians)
- **g:** Acceleration due to gravity
- **L:** Length of the pendulum

It numerically solves the equation to animate the pendulum’s swing, visually displaying its motion, speed, and energy in real time.

---

## 📝 Key Attributes

- **Length:** Adjustable length of the pendulum arm
- **Mass:** Mass of the pendulum bob
- **Initial Angle:** Set the starting angular displacement
- **Damping:** Optional air resistance/friction
- **Gravity:** Customizable gravitational acceleration
- **Real-Time Controls:** Pause, resume, and reset the simulation
- **Live Visualization:** Animated motion and energy plots

---

## 🚀 Getting Started

1. **Build the Plugin**
    - Open the `Pendulum.vcxproj` file in Visual Studio.
    - Build the project (ensure all dependencies for EurekaSim SDK are set up).

2. **Run in EurekaSim**
    - Place the compiled DLL in EurekaSim's plugins directory.
    - Load the Pendulum plugin inside EurekaSim.
    - Adjust parameters and observe the simulation.

---

## 📂 Source Files Explained

- **Pendulum.vcxproj / .filters**: Visual Studio project and file organization.
- **Pendulum.idl / Pendulum.h**: COM interface/type library definitions.
- **Pendulum.cpp**: Main implementation and DLL exports.
- **Pendulum.def**: Specifies exported functions for the DLL.
- **Pendulum.rc / Resource.h**: Resource definitions (icons, dialogs, etc.).
- **StdAfx.h / StdAfx.cpp**: Precompiled header for faster compilation.

> These files are standard for Visual C++ plugin projects and ensure smooth integration and building.

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

---

**Enjoy simulating physics with EurekaSim Pendulum!**
