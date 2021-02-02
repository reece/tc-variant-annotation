# Variant Annotation Technical Challenge

## Introduction

The goal for this technical interview is to build a Python module to
annotate biological sequence variants and return selected
information. This challenge provides an opportunity to discuss the
candidate's experience with annotation, and to discuss code
architecture, and to demonstrate coding skills.

There is no right answer to this challenge. Given the breadth of
relevant topics and skills, it is unlikely that candidates will be
able to address all discussion areas and implementation
considerations.

## Interview Discussion

* How are variants represented?
* What kinds of variant annotation and sources is the candidate aware
  of? How are they distributed?
* How can we search for annotations? What constitutes a matching
  variant? What challenges exist with matching variants?
* Data sources might be files, local web service, or remote web
  service. What are the considerations between these for an analysis
  pipeline in a clinical setting?  What are downsides for each and how
  might we mitigate them?
* Suppose we build a Python module for annotation.  How would you
  write it?  Would you use a function or a class, and why?
* We now see that our module ends up looking up annotations for the
  same variant often.  Some element of our backend lookups are
  expensive in time or money.  How would you optimize it?
* How would we build an internal microservice for variant annotation?
  What standards and tools might we use to implement it?


## Take-home challenge

* Write a module that provides a service to annotate variants.  The
  data source may be local or remote.  The choice of which data types
  to return is up to you and need not be exhaustive (i.e., <10 columns
  is fine!). Some ideas: Gene id, gene name, HGVS expressions,
  population frequencies, and/or Sequence Ontology terms.

* Write an interface to that module.  You have two options:

  1. A command line interface that accepts a file with a list of
	 variants and outputs a TSV file with annotations.
  
  2. A web service interface that accepts a GET or POST request and
     returns the annotation as JSON.

* Demonstrate your interface using the variants.txt file included in
  this repo.  Please include the full output, errors, warnings and
  all.  The variants.txt is exactly as intended.

* Discuss your code. Start-ups and start-up employees must balance
  quick and satisfactory (i.e., good enough) results with more
  deliberate and reliable results. The same is true for code.  You do
  not have enough time to write the ultimate answer to variant
  annotation. So, as you write your code, please consider what is
  important to get "right" now and what can be deferred.  Discuss what
  your code achieves as well as what might be considered for future
  work.


## Hints

* The source of information is up to you.  If you're looking for sources, consider queries like:

  ```
  $ curl -H "Content-type:application/json" 'http://rest.ensembl.org/vep/human/hgvs/NC_000006.12:g.152387156G>A'
  ```

- Reece Hart, 2021
