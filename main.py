from sim import Simulation
import sys

def main():
    width = 14
    height = 30
    if len(sys.argv) > 2:
        height = int(sys.argv[1])
        width = int(sys.argv[2])
    elif len(sys.argv) == 2:
        width = height = int(sys.argv[1])
    sim = Simulation(width, height)

    for c in 'ABCDE':
        sim.spawn_new_life(representing_char=c)

    sim.run()

if __name__ == '__main__':
    main()