# HelloWorldAIFusion
Our submission for the event AI Fusion in IITRPR Advitiya 2024 

## Command and Control Sub Systems
### Path Planning 

### Monitoring and Control


## Guidance and Navigation Sub Systems

### Guidance System

### Navigation System

## Drone Sub Systems

### Drone Hardware

### Payload System
Maintaining specific temperatures for sensitive medications during drone delivery is crucial. Here are some methods and potential algorithms:

**Passive methods:**
- Insulation: High-quality insulation materials like vacuum panels or aerogels minimize heat transfer, maintaining temperature for short or controlled flights.
- Phase-change materials (PCMs): Materials like paraffin wax absorb and release heat at specific temperatures, providing a buffer without external power.

**Active methods:**

- **Peltier devices:** Thermoelectric coolers use electricity to create a temperature difference, ideal for precise control but require power management.

Algorithmic methods are can be used to optimize passive and active methods:

- **Predictive algorithms:** Based on weather data, flight duration, and container properties, predict internal temperature and adjust passive elements (e.g., PCM placement) or activate cooling units. 

- **Adaptive control algorithms:** Monitor internal temperature in real-time and adjust cooling/heating intensity of Peltier devices for precise temperature regulation. A basic implementation can be found at `/src/PayloadSystem/AdaptiveControl.rs`

Using a language like Rust is ideal for these algorithms due to its safety and performance, crucial for real-time control systems. Its low overhead and high-level abstractions make it suitable for embedded systems and high-level control algorithms.