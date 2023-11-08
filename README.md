# rd2md

A converter to transform R doc files (.Rd) into markdown files (.md).

## Installation

```shell
pip install rd2md
```

## Usage

In the following command-line examples you can use `rd2md` or `python -m rd2md`.

```shell
rd2md [RD-DIRECTORY] [MD-DIRECTORY] BASE-FILENAME-1 BASE-FILENAME-2 ...
```

where:

* [RD-DIRECTORY] is the directory of .Rd files (eg, `R/man`)
* [MD-DIRECTORY] is the output directory
* BASE-FILENAME is the name of an Rd file without the directory or extension

## Example

To use `R/man` as the directory of Rd files, and `documentation` as
the output directory, converting `R/man/create_experiment.Rd` and
`R/man/Experiment.Rd` do this:

```shell
rd2md R/man documentation create_experiment Experiment
```
