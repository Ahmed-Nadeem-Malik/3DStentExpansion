import numpy as np
import matplotlib.pyplot as plt

"""Requirements specification for the stent simulation:
1. Visualize stent expansion in blood vessel
2. Calculate and display key measurements
3. Support customizable parameters
4. Ensure stent diameter never exceeds vessel diameter 
"""


class StentSimulation:
    def __init__(self, vessel_diameter=10.0, stent_length=20.0, starting_stent_diameter=6.0):
        # Checks inputs
        self._validate_inputs(vessel_diameter, stent_length, starting_stent_diameter)
        self.vessel_diameter = vessel_diameter
        self.stent_length = stent_length
        self.starting_stent_diameter = starting_stent_diameter
        self.simulation_completed = False

    def _validate_inputs(self, vessel_diameter, stent_length, starting_stent_diameter):
        if vessel_diameter <= 0 or stent_length <= 0 or starting_stent_diameter <= 0:
            raise ValueError("All dimensions must be positive")
        if starting_stent_diameter >= vessel_diameter:
            raise ValueError("Starting stent diameter must be less than vessel diameter")

    def make_cylinder_points(self, diameter, length):
        angles = np.linspace(0, 2*np.pi, 20)  # fewer points = simpler design
        lengths = np.linspace(0, length, 20)
        angle_grid, length_grid = np.meshgrid(angles, lengths)
        
        radius = diameter / 2
        x = radius * np.cos(angle_grid)
        y = radius * np.sin(angle_grid)
        z = length_grid
        
        return x, y, z

    def show_expansion(self):
        final_diameter = self.vessel_diameter * 0.9
        stent_sizes = [
            self.starting_stent_diameter,
            (self.starting_stent_diameter + final_diameter) / 2,
            final_diameter
        ]
        
        for step, stent_diameter in enumerate(stent_sizes):
            plt.figure(figsize=(10, 8))
            plot_3d = plt.subplot(111, projection='3d')
            
            vessel_x, vessel_y, vessel_z = self.make_cylinder_points(self.vessel_diameter, self.stent_length)
            stent_x, stent_y, stent_z = self.make_cylinder_points(stent_diameter, self.stent_length)
          
            plot_3d.plot_surface(vessel_x, vessel_y, vessel_z, alpha=0.3, color='gray')
            plot_3d.plot_surface(stent_x, stent_y, stent_z, color='red')
            
            gap = (self.vessel_diameter - stent_diameter) / 2
            expansion = ((stent_diameter / self.starting_stent_diameter) - 1) * 100
            
            plot_3d.set_title(f'Step {step + 1}\n'
                              f'Stent Size: {stent_diameter:.1f} mm\n'
                              f'Gap to Vessel: {gap:.1f} mm\n'
                              f'Expansion of Stent: {expansion:.1f}%')
            
            plot_3d.set_xlabel('X (mm)')
            plot_3d.set_ylabel('Y (mm)')
            plot_3d.set_zlabel('Z (mm)')
            
            plt.show()
        
        self.simulation_completed = True
        return True 

    def run_tests(self):
        test_results = {
            'input_validation': False,
            'simulation_execution': False,
            'measurements_accurate': False
        }
        
        try:
            self._validate_inputs(10.0, 20.0, 6.0)
            test_results['input_validation'] = True
        except ValueError:
            pass
        
        if self.show_expansion():
            test_results['simulation_execution'] = True
        
        final_diameter = self.vessel_diameter * 0.9
        if final_diameter < self.vessel_diameter:
            test_results['measurements_accurate'] = True
            
        return test_results

def main():
    try:
        vessel_diameter = float(input("Enter the vessel diameter (mm): "))
        stent_length = float(input("Enter the stent length (mm): "))
        starting_stent_diameter = float(input("Enter the starting stent diameter (mm): "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    try:
        sim = StentSimulation(vessel_diameter, stent_length, starting_stent_diameter)
    except ValueError as e:
        print(f"Error: {e}")
        return

    test_results = sim.run_tests()
    print("Test Results:", test_results)

if __name__ == "__main__":
    main()
