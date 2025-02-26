import sys
import argparse
import traceback
import tl.exceptions
from tl.utility.logging import Logger


def parser():
    return {
        'help': 'builds a json lines file to be loaded into elasticsearch from a kgtk edge file.'
    }


def add_arguments(parser):
    """
    Parse Arguments
    Args:
        parser: (argparse.ArgumentParser)

    """

    parser.add_argument('--label-properties', action='store', type=str, dest='label_properties', required=True,
                        help='the name of property which has labels for the node1')

    parser.add_argument('--alias-properties', action='store', type=str, dest='alias_properties', default=None,
                        help='the name of property which has aliases for the node1')

    parser.add_argument('--description-properties', action='store', type=str, dest='description_properties',
                        default=None,
                        help='the name of property which has descriptions for the node1')

    parser.add_argument('--pagerank-properties', action='store', type=str, dest='pagerank_properties', default=None,
                        help='the name of property which has pagerank for the node1')

    parser.add_argument('--mapping-file', action='store', dest='mapping_file_path', required=True,
                        help='path where a mapping file for the ES index will be output')

    parser.add_argument('--blacklist-file', action='store', dest='blacklist_file_path', default=None,
                        help='blacklist file path nodes from which will be ignored in the output')

    parser.add_argument('--extra-information', action='store_true', dest='extra_information', default=False,
                        help='store extra information about node1 or not')

    parser.add_argument('--add-text', action='store_true', dest='add_text', default=False,
                        help='add a text field in the json which contains all text in label, alias and description')

    parser.add_argument('--input-file', action='store', dest='input_file_path', required=True,
                        help='input kgtk edge file, sorted by node1')

    parser.add_argument('--output-file', action='store', dest='output_file_path', required=True,
                        help='output json lines file, to be loaded into ES')

    parser.add_argument('--copy-to-properties', action='store', type=str, dest='copy_to_properties', default=None,
                        help='''Name of the properties separated by comma which need to be added to all_labels in mapping file.
                        Property Names supported by are: labels, aliases, descriptions, pagerank''')

    parser.add_argument('--es-version', action='store', type=float, dest='es_version', default=7.9,
                        help='Version of the Elasticsearch you are using')

    parser.add_argument('--property-datatype-file', action='store', dest='property_datatype_file', default=None,
                        help='A file in KGTK edge file format with data types for properties')


def run(**kwargs):
    from tl.utility.utility import Utility
    import time
    try:
        start = time.time()
        Utility.build_elasticsearch_file(kwargs['input_file_path'], kwargs['label_properties'],
                                         kwargs['mapping_file_path'], kwargs['output_file_path'],
                                         alias_fields=kwargs['alias_properties'],
                                         pagerank_fields=kwargs['pagerank_properties'],
                                         black_list_file_path=kwargs['blacklist_file_path'],
                                         extra_info=kwargs['extra_information'],
                                         description_properties=kwargs['description_properties'],
                                         add_text=kwargs['add_text'],
                                         copy_to_properties=kwargs['copy_to_properties'],
                                         es_version=kwargs['es_version'],
                                         property_datatype_file=kwargs['property_datatype_file']
                                         )
        end = time.time()
        logger = Logger(kwargs["logfile"])
        logger.write_to_file(args={
            "command": "build-elasticsearch-input",
            "time": end-start
        })
    except:
        message = 'Command: build-elasticsearch-input\n'
        message += 'Error Message:  {}\n'.format(traceback.format_exc())
        raise tl.exceptions.TLException(message)
