import argparse
import configparser
import biotools_API_querying as bAq
import sys


# Command-line argument
parser = argparse.ArgumentParser()
parser.add_argument("config_file", 
                    help="path of configuration file")
parser.add_argument("-v", "--verbose", 
                    help="prints detail information about the program progress to prompt", 
                    action="store_true")

# Configuration file
config = configparser.ConfigParser()


if __name__=='__main__':

    # get arguments
    if len(sys.argv)==1:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()

    # get configuration file parameters
    try:
        with open(args.config_file) as f:
            config.read_file(f)
    except IOError:
        error = f"Something went wrong while opening configuration file '{args.config}'. Please, make sure it exists."
        print(f"{bAq.bcolors.FAIL}{error}{bAq.bcolors.ENDC}")
        raise

    # Init tools discoverer
    tools_discov = bAq.tools_discoverer(config.get('optional','name'), 
                                        config.get('required','terms_file'), 
                                        config.get('optional','ranked_terms_file'), 
                                        config.get('optional','output_directory'),
                                        config.getfloat('optional','default_unspecified_keyword_weight'),
                                        args.verbose)

    # Run pipeline
    tools_discov.run_pipeline()

    # Save results
    tools_discov.save_outputs()

