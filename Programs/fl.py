import argparse
import inspect
from itertools import chain
import json

from config import DATASETS, ML, COMM, FL, MODELS

new_args = set(
    chain.from_iterable(
        inspect.signature(fn).parameters.keys() 
        for fn in chain(
            DATASETS.values(), 
            ML.values(), 
            COMM.values(), 
            FL.values(),
        )
    )
)
new_args -= {'args', 'kwargs', 'file', 'dataset', 'ml', 'comm', 'fl', 'model', 'verbose', 'all_args'}

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, required=False, help="Config file")
parser.add_argument("-d", "--dataset", type=str, required=False, help="Dataset name", choices=DATASETS.keys(), default='IOT_DNL')
parser.add_argument("-m", "--model", type=str, required=False, help="Model name", choices=MODELS.keys())
parser.add_argument("--ml", type=str, required=False, help="ML framework", choices=ML.keys(), default='tf')
parser.add_argument("-c", "--comm", type=str, required=False, help="Communication framework", choices=COMM.keys(), default='mpi')
parser.add_argument("--fl", type=str, required=False, help="FL framework", choices=FL.keys(), default='ds')
parser.add_argument("-v", "--verbose", required=False, action='store_true', default=False, help="Verbose")
for arg in new_args:
    parser.add_argument(f"--{arg}", type=str, required=False, help=f"{arg}")
parser_args = parser.parse_args()

parser_args = vars(parser_args)
parser_args = {k: v for k, v in parser_args.items() if v is not None}
if 'file' in parser_args:
    with open(parser_args['file'], 'r') as f:
        args = json.load(f)
        args.update(parser_args)
else:
    args = parser_args
if 'model' not in args:
    args['model'] = args['dataset']

all_args = {**args}

dataset = DATASETS[args.pop('dataset')]()
model = MODELS[args.pop('model')]()
ml = ML[args.pop('ml')](model = model, dataset = dataset, **args)
comm = COMM[args.pop('comm')]()
fl = FL[args.pop('fl')](ml = ml, comm = comm, all_args = all_args, **args)

if args['verbose'] and comm.is_master():
    print(f"\nDataset {dataset.__class__.__name__}:\n{dataset}")
    print(f"\nModel {model.__class__.__name__}")
    print(f"\nML {ml.__class__.__name__}:\n{ml}")
    print(f"\nComm: {comm.__class__.__name__}")
    print(f"\nFL {fl.__class__.__name__}:\n{fl}")

fl.run()