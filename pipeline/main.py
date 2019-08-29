import getopt, sys, os, shutil, uuid
from modules import routines, reconstruction, visualization

def params():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:", ["type="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit("Error en parámetro -t")

    # Tipo de pipeline a seguir
    # t = 0 (default, visualization only); t = 1 (simulation only); t = 2 (reconstruction only); t = 3 (full)
    t = '   0'
    for opt, value in opts:
        if opt in ("-t", "--type"):
            t = value
        else:
            assert False, "unhandled option"

    return t


def main():
    os.system('clear')
    t = params()

    if t == '0':
        routines.visualization()

    elif t == '1':
        visualization.plot_lcurve_iter('2d')
    elif t == '2':
        reconstruction.reconstruction()

    elif t == '3':
        print("Full!")
    else:
        sys.exit("Option in -t not valid.")


if __name__ == "__main__":
    main()
