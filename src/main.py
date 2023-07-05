import pyglet
import time
from aiDrive.src.utils.game import app_window
from aiDrive.src.utils.genetic_algo import GeneticAlgorithm

NUM_NETWORKS = 100
NUM_GENERATIONS = 100

def initialize_new_generation(dt=None, first=False):
    if not first:
        for car in window.cars:
            car.calculate_fitness(window.map)
            print("car fitness", car.network.fitness)
        
        genetic_algo.update_networks()
    
    window.create_new_generation(genetic_algo.networks)


if __name__ == '__main__':
    width, height = 800, 500
    window = app_window(width=width, height=height)

    genetic_algo = GeneticAlgorithm(NUM_NETWORKS)

    initialize_new_generation(first=True)
    #pyglet.clock.schedule_interval(initialize_new_generation, 5)
    pyglet.clock.schedule_interval(window.update, 1/60.0)
    pyglet.app.run()  
