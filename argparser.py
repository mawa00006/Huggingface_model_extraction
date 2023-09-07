import argparse

def get_args(argv=None):
    parser = argparse.ArgumentParser(description="TODO")

    parser.add_argument('-v', '--version', type=str, default='v4.19.4',
                        help= 'Specify the version of the Huggingface transformer doc. Default: v4.19.4')
    parser.add_argument('-a', '--architecture', type=str, default='transformers',
                        help='Specify the model architecture. Default: transformers')
    parser.add_argument('-c', '--classes', type=str, nargs='*', default=['Tokenizer'],
                        help='Specify the classes that the wanted model should implement as a list of strings'
                             ' (e.g.: [FeatureExtractor, ForImageClassification])')

    return parser.parse_args(argv)