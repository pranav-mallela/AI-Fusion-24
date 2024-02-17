// This example simulates temperature prediction in a simplified system

use rand::Rng;

// Define state variables
struct SystemState {
  initial_temp: f32,
  target_temp: f32,
  ambient_temp: f32, // Simulate weather data
  flight_duration: u32, // Simulate flight duration
  container_properties: f32, // Simulate insulation
  control_state: bool, // True for active cooling, False for passive
}

// Define a simple predictive algorithm based on linear approximation
fn predict_temp(state: &SystemState) {
  // Simulate temperature change (replace with actual physics models)
  let mut rng = rand::thread_rng();
  let temp_change = (state.ambient_temp - state.initial_temp) / state.flight_duration as f32;
  let predicted_temp = state.initial_temp + temp_change * state.flight_duration as f32;

  // Simple control decision based on prediction
  if predicted_temp > state.target_temp + 1.0 {
    state.control_state = true; // Activate cooling
  } else if predicted_temp < state.target_temp - 1.0 {
    state.control_state = false; // Rely on passive insulation
  }
}

fn main() {
  // Initialize state
  let mut state = SystemState {
    initial_temp: 20.0,
    target_temp: 25.0,
    ambient_temp: rng.gen_range(15.0, 30.0), // Random weather
    flight_duration: rng.gen_range(10, 30), // Random flight duration
    container_properties: 0.5, // Simulate insulation level
    control_state: false,
  };

  // Predict temperature
  predict_temp(&mut state);

  // Print results
  println!("Initial temp: {}", state.initial_temp);
  println!("Target temp: {}", state.target_temp);
  println!("Ambient temp: {}", state.ambient_temp);
  println!("Flight duration: {} minutes", state.flight_duration);
  println!("Control state: {}", if state.control_state { "Active cooling" } else { "Passive insulation" });
}
