# HelloWorldAIFusion
Our submission for the event AI Fusion in IITRPR Advitiya 2024 

## Command and Control Sub Systems
### Path Planning 

### Monitoring and Control


## Guidance and Navigation Sub Systems

### Guidance System & Navigation System
The guidance system consists of four submodules:
1. Danger Detection
    - Intruder detection using YOLOv4
    - Weapon detection using YOLOv4
2. Flight Control:
    - LIDAR based obstacle avoidance
3. Command Center Path:
    - Path planning using RRT* algorithm and GPS
4. SOS:
    - This is used in case the drone is unable to handle the current situation and needs human intervention.

The basic implementation for this logic can be found at `./GuidanceNav`. It was done in python for simplicity.

## Drone Sub Systems

### Safety Subsystems
Since this system is to be used in war zones, it is crucial to have a robust safety system to prevent accidents and protect the drone from hostile attacks and protect any confidential information that the drone may have stored/transmit. Here are some safety subsystems that can be implemented:

**Security and Encryption:**

- **Communication security:** Use of strong encryption protocols like AES or ChaCha20 for all communication between the drone, ground control, and any intermediate relays is essential. This protects data like flight path, payload information, and user details from eavesdropping.
- **Data encryption at rest**: It is crucial to encrypt sensitive data stored on the drone itself, even if it's temporary, to prevent unauthorized access if the drone is intercepted.

**Physical Security:**

- **Tamper-evident seals and enclosures:** The drone can be designed with tamper-evident seals and enclosures that trigger alerts or self-destruct mechanisms if tampered with.
- **Geofencing and no-fly zones:** Set virtual boundaries to restrict drone operation in sensitive areas and prevent unauthorized access to specific locations. This can be implemented using GPS and geofencing algorithms in drone Guidanc subsytems.
- **Kill switch and remote disabling:** It will be prudent to implement a kill switch or remote disabling mechanism to deactivate the drone in case of security breaches or emergencies.

### Payload System
Maintaining specific temperatures for sensitive medications during drone delivery is crucial. Here are some methods and potential algorithms:

**Passive methods:**
- Insulation: High-quality insulation materials like vacuum panels or aerogels minimize heat transfer, maintaining temperature for short or controlled flights.
- Phase-change materials (PCMs): Materials like paraffin wax absorb and release heat at specific temperatures, providing a buffer without external power.

**Active methods:**

- **Peltier devices:** Thermoelectric coolers use electricity to create a temperature difference, ideal for precise control but require power management.

Algorithmic methods are can be used to optimize passive and active methods:

- **Predictive algorithms:** Based on weather data, flight duration, and container properties, predict internal temperature and adjust passive elements (e.g., PCM placement) or activate cooling units. A basic implementation can be found at `/src/PayloadSystem/predictiveControl.rs`

- **Adaptive control algorithms:** Monitor internal temperature in real-time and adjust cooling/heating intensity of Peltier devices for precise temperature regulation. A basic implementation can be found at `/src/PayloadSystem/adaptiveControl.rs`

Using a language like Rust is ideal for these algorithms due to its safety and performance, crucial for real-time control systems. Its low overhead and high-level abstractions make it suitable for embedded systems and high-level control algorithms.