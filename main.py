import numpy as np
import matplotlib.pyplot as plt


class StentSimulation:
    def __init__(self, tube_diameter=10.0, stent_length=20.0, initial_stent_diameter=6.0):
        # Set up the starting values
        self.tube_diameter = tube_diameter
        self.stent_length = stent_length
        self.initial_stent_diameter = initial_stent_diameter
        self.current_stent_diameter = initial_stent_diameter
        
    def expand_stent(self, expansion_steps=5):
        # Make the stent get bigger step by step
        target_diameter = self.tube_diameter * 0.9  # Don't expand all the way to the tube size
        diameter_increment = (target_diameter - self.initial_stent_diameter) / expansion_steps
        expansion_states = []
        
        for step in range(expansion_steps + 1):
            current_diameter = self.initial_stent_diameter + (step * diameter_increment)
            expansion_states.append(current_diameter)
            
        return expansion_states
    
    def generate_stent_mesh(self, diameter):
        # Make the points needed to draw the stent
        theta = np.linspace(0, 2*np.pi, 30)
        z = np.linspace(0, self.stent_length, 30)
        theta, z = np.meshgrid(theta, z)
        
        r = diameter/2
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        return x, y, z
    
    def generate_tube_mesh(self):
        # Make the points needed to draw the tube
        theta = np.linspace(0, 2*np.pi, 30)
        z = np.linspace(-5, self.stent_length + 5, 30)  # Make tube longer than stent
        theta, z = np.meshgrid(theta, z)
        
        r = self.tube_diameter/2
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        return x, y, z
    
    def visualize_expansion(self):
        # Show how the stent expands in 3D
        expansion_states = self.expand_stent()
        
        for step, diameter in enumerate(expansion_states):
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            # Draw the tube in gray
            x_tube, y_tube, z_tube = self.generate_tube_mesh()
            ax.plot_surface(x_tube, y_tube, z_tube, alpha=0.3, color='gray')
            
            # Draw the stent in red
            x_stent, y_stent, z_stent = self.generate_stent_mesh(diameter)
            ax.plot_surface(x_stent, y_stent, z_stent, color='red')
            
            # Calculate important measurements
            gap_to_vessel = (self.tube_diameter - diameter) / 2
            expansion_percentage = (diameter / self.initial_stent_diameter - 1) * 100
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            title = f'Stent Expansion - Step {step}\n' \
                   f'Stent Diameter: {diameter:.2f} mm\n' \
                   f'Gap to Vessel Wall: {gap_to_vessel:.2f} mm\n' \
                   f'Expansion: {expansion_percentage:.1f}%'
            ax.set_title(title)
            
            # Make sure the view stays the same size
            ax.set_xlim(-self.tube_diameter/2, self.tube_diameter/2)
            ax.set_ylim(-self.tube_diameter/2, self.tube_diameter/2)
            
            plt.show()

def main():
    # Create and run simulation
    sim = StentSimulation(tube_diameter=10.0, stent_length=20.0, initial_stent_diameter=6.0)
    sim.visualize_expansion()

if __name__ == "__main__":
    main()
