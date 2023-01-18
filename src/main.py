import pyglet
import time
from aiDrive.src.utils.game import app_window
from aiDrive.src.utils.genetic_algo import GeneticAlgorithm

NUM_NETWORKS = 50
NUM_GENERATIONS = 100

def train_ai(window, num_generations):
    print('yes')

    genetic_algo = GeneticAlgorithm(NUM_NETWORKS)
    # for generation in range(num_generations):
    window.create_new_generation(genetic_algo.networks)
    #time.sleep(1)
    genetic_algo.update_networks()



if __name__ == '__main__':
    width, height = 800, 500
    window = app_window(width=width, height=height)
    train_ai(window, NUM_GENERATIONS)

    pyglet.clock.schedule_interval(window.update, 1/60.0)  # update at 60Hz
    pyglet.app.run()
