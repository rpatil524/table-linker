import sys
import argparse
import traceback
import tl.exceptions


def parser():
    return {
        'help': 'computes feature smallest-qnode-number'
    }


def add_arguments(parser):
    """
    Parse Arguments
    Args:
        parser: (argparse.ArgumentParser)

    """
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)


def run(**kwargs):
    from tl.features.smallest_qnode_number import smallest_qnode_number
    import pandas as pd
    try:
        df = pd.read_csv(kwargs['input_file'], dtype=object)
        odf = smallest_qnode_number(df)
        odf.to_csv(sys.stdout, index=False)
    except:
        message = 'Command: smallest-qnode-number\n'
        message += 'Error Message:  {}\n'.format(traceback.format_exc())
        raise tl.exceptions.TLException(message)
