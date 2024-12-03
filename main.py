from simanalysis.core import H5FileGroup


def run():

    file = H5FileGroup("data/discrete/output")
    file.plot_charge("test.png")


if __name__ == '__main__':
    run()

