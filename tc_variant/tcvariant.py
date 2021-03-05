"""
TcVariantAnnotation version 0.0.1

TcVariantAnnotation is a class that provides variant annotation functionality. It include methods to annotate a
single variant or a file containing multiple variants to be annotated and writes data to a tsv file.

Future enhancement considerations:
- using async or distributed workers for performance on larger variant files
- better validation of entries in the variants list (variants.txt) to avoid API calls on invalid variants
- parameterize values used in annotation so user can define/select data included in output file
- using dataframes (pandas) for json->csv and gene symbol processing
- add additional output formats (csv, excel, etc.)
- read input file by bytes instead of lines
- allow alternative input methods (API, database, etc.)
"""
import logging
import requests
import csv
import re


class TcVariantAnnotation:
    """ """

    def __init__(self, output):
        """ class entry point """
        self.output = output

    def validate_variant(self, variant):
        """
        validate the provided variant is formatted correctly via regex pattern

        Args:
            variant: (str) variant to create annotation for; ex. NC_000006.12:g.152387156G>A

        Returns:
            0 if variant is formatted correctly
            1 if variant is NOT formatted correctly
        """
        logging.debug(f'checking variant formatting for variant {variant}')
        # not sure if this is a comprehensive variant pattern; this is based off sample data; adjust as applicable
        variant_regex_pattern = 'NC_\d{6}.(11|12):g.\d{8,9}(A|C|G|T)>(A|G|T)'
        if re.match(variant_regex_pattern, variant):
            logging.debug(f'variant format for {variant} is valid')
            return 0
        logging.debug(f'variant format for {variant} is invalid')
        return 1

    def get_variant_data(self, variant, root_url='http://rest.ensembl.org/vep/human/hgvs'):
        """ get variant data via Ensembl API; ex. http://rest.ensembl.org/vep/human/hgvs/NC_000006.12:g.152387156G>A

        Args:
            variant: (str) variant to get values for; ex. NC_000006.12:g.152387156G>A

        Returns:
            json response as returned from Ensembl api
        """
        logging.debug(f'getting ensembl data for variant {variant}')
        try:
            url = f'{root_url}/{variant}'
            headers = {'Content-type': 'application/json'}
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                logging.error(f'error retrieving data. URL: {url} {response.json()["error"]}')
            return response.json()[0]
        except Exception as err:
            logging.error(f'exception encountered while attempting to retrieve data from ensembl: {err}')

    def parse_variant_data(self, variant, json_data):
        """ parse json data retrieved from Ensmbl and construct a dict of specifically identified data;
            data we care about is:
                assembly_name, seq_region_name, start, end, most_severe_consequence, strand, gene_symbols
        Args:
            variant: (str) variant to annotate; ex. NC_000006.12:g.152387156G>A
            json_data: (dict) variant data as returned from the Ensembl API

        Returns:
            dict: dictionary containing specific variant values; empty dict on exception
        """
        logging.debug(f'parsing data for variant {variant}')
        try:
            # first get a list of unique gene symbols as available in the 'transcript_consequences' in the json data
            gene_symbol_list = list()
            for transcript_consequences in json_data['transcript_consequences']:
                if transcript_consequences['gene_symbol'] not in gene_symbol_list:
                    gene_symbol_list.append(transcript_consequences['gene_symbol'])
            return dict(variant=variant,
                        assembly_name=json_data['assembly_name'],
                        seq_region_name=json_data['seq_region_name'],
                        start=json_data['start'],
                        end=json_data['end'],
                        most_severe_consequence=json_data['most_severe_consequence'],
                        strand=json_data['strand'],
                        gene_symbols=','.join(gene_symbol_list),
                        )
        except Exception as err:
            logging.error(f'exception encountered when parsing variant data: {err}')
            return dict()

    def write_tsv(self, data, output_file):
        """ write data to a tsv file
        headers: variant, assembly_name, seq_region_name, start, end, most_severe_consequence, strand, gene_symbols

        Args:
            data: (list) list of dictionaries containing desired variant values
            output_file: (str) name of file created output (tsv) file containing annotations

        Returns:
            None
        """
        logging.debug('writing output file')
        try:
            keys = data[0].keys()
            with open(output_file, 'wt', newline='') as f:
                dict_writer = csv.DictWriter(f, delimiter='\t', fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
        except Exception as err:
            logging.error(f'exception encountered when attempting to write tsv file: {err}')

    def annotate_variants_from_file(self, input_file):
        """
        Reads variants from a file and autputs a tsv file of annotations

        Args:
            input_file: (str) full path and file name of file containing a list of variants (one per line)

        Returns:
            None
        """
        logging.debug(f'getting annotations for variants in: {input_file}')
        data = list()
        with open(input_file, 'r') as f:
            for variant in f.readlines():
                variant = variant.strip()
                if self.validate_variant(variant):
                    logging.error(f'{variant} does not appear to be a valid variant; skipping annotation')
                    continue
                api_data = self.get_variant_data(variant)
                if api_data:
                    data.append(self.parse_variant_data(variant, self.get_variant_data(variant)))
                else:
                    logging.error(f'error retrieving data from from ensembl; skipping annotation for variant {variant}')
        self.write_tsv(data, self.output)

    def annotate_single_variant(self, variant):
        """
        Annotates a single variant and writes to data to a tsv file

        Args:
            variant: (str) variant to create annotation for; ex. NC_000006.12:g.152387156G>A

        Returns:
            None
        """
        logging.debug(f'getting annotation for single variant: {variant}')
        variant = variant.strip()
        if self.validate_variant(variant):
            logging.error(f'{variant} does not appear to be a valid variant; skipping annotation')
            return
        parsed_data = self.parse_variant_data(variant, self.get_variant_data(variant))
        self.write_tsv([parsed_data], self.output)
