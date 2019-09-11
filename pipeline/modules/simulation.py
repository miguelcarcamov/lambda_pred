import sys, os, time, shutil, uuid, csv, json
from subprocess import Popen, PIPE, CalledProcessError

def create_dir(dir=""):
    if dir == "":
        sys.exit("Path directory for Simulation is empty.")

    if not os.path.exists(dir):
        os.mkdir(dir)
    else:
        if len(os.listdir(dir)) > 1:
            sys.exit('Simulation path has files in it.')

def start():
    while True:
        os.system('clear')

        print("Options for Simulation: ")
        print("    (1) Simulate co65")
        print("    (2) Simulate HLTau")
        print("    (3) Create JSON with data")
        print("    (4) Exit")

        r = input("option: ")

        if r == '1':
            test()
        elif r == '2':
            simulate_hltau()
        elif r == '3':
            normalized_visibilities()
        elif r == '4':
            break;
        else:
            print("Not a valid option, choose another one.")

    sys.exit("Exit...")


def test():
    print("testing")

def simulate_hltau():
    #TODO recordar directorio /home/hperez/uv_values_noise.csv

    os.system('clear')
    print("Simulate with Gridding ?")

    while True:
        gridding = input("Yes (1) or No (2): ")

        if gridding == '1' or gridding == '2':
            break

        print("Not a valid option.")

    #TODO Crear ciclo, verificar si es entero
    iterations = input("Number of iterations: ")
    directory = '../test/simulation-' + str(uuid.uuid4())

    outputs  = directory + '/simulation'
    uv_files = directory + '/uv_files'

    create_dir(directory)
    create_dir(outputs)
    create_dir(uv_files)

    command = {
        'gpuvsim': '/home/hperez/gpuvsim/bin/gpuvsim',
        'x': '16',
        'y': '16',
        'v': '256',
        'I': '../data/input.dat',
        'i': '../data/hltau_reducido.ms',
        'a': '../data/alpha_zeros.fits',
        'm': '../data/model_images/hltau5_whead.fits'
    }

    src = '/home/hperez/uv_values_noise.csv'

    #TODO Buscar opcion de gridding en GPUVSIM
    start = time.time()
    if gridding == '1':
        for count in range(int(iterations)):
            o = outputs + '/sim_out_' + str(count) + '.ms'

            with Popen([
                command['gpuvsim'],
                '-X', command['x'],
                '-Y', command['y'],
                '-V', command['v'],
                '-i', command['i'],
                '-I', command['I'],
                '-o', o,
                '-m', command['m'],
                '-a', command['a'],
                '--apply-noise',
                '--verbose'
            ], stdout=PIPE, universal_newlines=True) as p:
                for line in p.stdout:
                    print(line, end='')

            if p.returncode != 0:
                raise CalledProcessError(p.returncode, p.args)

    else:
        for count in range(int(iterations)):
            o = outputs + '/sim_out_' + str(count) + '.ms'

            with Popen([
                command['gpuvsim'],
                '-X', command['x'],
                '-Y', command['y'],
                '-V', command['v'],
                '-i', command['i'],
                '-I', command['I'],
                '-o', o,
                '-m', command['m'],
                '-a', command['a'],
                '--apply-noise',
                '--verbose'
            ], stdout=PIPE, universal_newlines=True) as p:
                for line in p.stdout:
                    print(line, end='')

            if p.returncode != 0:
                raise CalledProcessError(p.returncode, p.args)

    end = time.time()

# TODO falta agregarlo al pipeline
def normalized_visibilities():
    path = '/home/hperez/Desktop/uv_values_0.csv'
    total = 0


    with open(path) as f:
        reader = csv.reader(f)
        next(reader)
        data = [r for r in reader]

    for i in range(len(data)):
        row_data = data[i]
        if(len(row_data) == 10):
            if row_data[0] == '9':
                total += (float(row_data[7]) ** 2) + (float(row_data[8]) ** 2)

    print(total) #6609480360.685198
