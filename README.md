# Variant Annotation Technical Challenge

## Introduction

The goal for this technical interview is to understand how a candidate
approaches a software development task.  We will discuss a project to
annotate biological sequence variants using a remote REST service. No
prior knowledge of sequence variation is necessary.  This challenge
provides an opportunity to discuss the candidate's experience with
variant annotation (not required), code architecture, coding skills
and style.

There is no right answer to this challenge. Given the breadth of
relevant topics and skills, it is unlikely that candidates will be
able to address all discussion areas and implementation
considerations.  That's okay!


## In-Person Interview Discussion

### Sequence variation

* How are variants represented?
* What kinds of variant annotation and sources is the candidate aware
  of? How are they distributed?
* How can we search for annotations at these? What constitutes a
  matching variant? What challenges exist with matching variants?

### Code planning and architecture
* We want to write a program to annotate lists of variants on a
  command line.  How would you structure this code?  What questions
  occur to you when thinking about code structure?
* The proposed annotation system uses data from a remote REST
  service. What factors occur to you as you think about this approach
  in a clinical setting?
* Suppose we now want to write an internal microservice for variant
  annotation. How does this change your code structure?  What
  standards and tools might we use to implement it?


## Take-home challenge

* Go to https://github.com/reece/tc-variant-annotation and click "Use
  this template".  Please make the repo private (for your benefit).

* Write a module that annotates variants using Ensembl (see below).
  We want to report these values: input variant, `assembly name`,
  `seq_region_name`, `start`, `end`, `most_severe_consequnece`,
  `strand`, and genes. Genes should be a list of the unique
  `gene_symbol` field from `transcript_consequences`.
  
* Write a command line interface that accepts a file with a list of
  variants and outputs a TSV file with annotations.
  
* Demonstrate your interface using the variants.txt file included in
  this repo.  Please include the full output, errors, warnings and
  all.  The variants.txt is exactly as intended.

* Create a PR for your branch. Invite me to review it. Thanks!


## Questions

* Suppose we now want a web service interface that accepts a GET or
  POST request and returns the annotation as JSON.  What tools or
  standards would you implement this?  How does your code structure
  change?

* Start-ups and start-up employees must balance quick and satisfactory
  (i.e., good enough) results with more deliberate and reliable
  results. The same is true for code.  You do not have enough time to
  write the ultimate answer to variant annotation. What is important
  to get "right" now and what can be deferred.

* Oops. It turns out that the input files occasionally contain
  multiple requests for the same variant.  What's the simplest
  solution you can imagine to prevent multiple external requests?
  What other (more complicated) solutions might you consider?


## Ensembl Annotation Sources

An example Ensembl query and edited response is below.  **N.B. Ensembl
has two certs, one of which is old and leads to random failures. Use
http (not https) for now.** The response is also in
`ensembl-sample-response.json`.
  
  ```
  $ curl -H "Content-type:application/json" 'http://rest.ensembl.org/vep/human/hgvs/NC_000006.12:g.152387156G>A'
  [
     {
        "allele_string": "G/A",
        "assembly_name": "GRCh38",
        "end": 152387156,
        "most_severe_consequence": "synonymous_variant",
        "seq_region_name": "6",
        "start": 152387156,
        "strand": 1,
        "transcript_consequences": [
           {
              "amino_acids": "Y",
              "biotype": "protein_coding",
              "cdna_end": 8900,
              "cdna_start": 8900,
              "cds_end": 8424,
              "cds_start": 8424,
              "codons": "taC/taT",
              "consequence_terms": [
                 "synonymous_variant"
              ],
              "gene_id": "ENSG00000131018",
              "gene_symbol": "SYNE1",
              "gene_symbol_source": "HGNC",
              "hgnc_id": "HGNC:17089",
              "impact": "LOW",
              "protein_end": 2808,
              "protein_start": 2808,
              "strand": -1,
              "transcript_id": "ENST00000423061",
              "variant_allele": "A"
           },
           {
              "biotype": "retained_intron",
              "cdna_end": 8621,
              "cdna_start": 8621,
              "consequence_terms": [
                 "non_coding_transcript_exon_variant"
              ],
              "gene_id": "ENSG00000131018",
              "gene_symbol": "SYNE1",
              "gene_symbol_source": "HGNC",
              "hgnc_id": "HGNC:17089",
              "impact": "MODIFIER",
              "strand": -1,
              "transcript_id": "ENST00000461872",
              "variant_allele": "A"
           }
        ]
     }
  ]
  ```


- Reece Hart, 2021
