from sim import Simulation


def main():
    sim = Simulation()

    for c in 'ABCDE':
        sim.spawn_new_life(representing_char=c)

    sim.run()

if __name__ == '__main__':
    main()