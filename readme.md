# AWS Cost Report
I ran into a small issue of wanting to generate cost explorer reports in a format
that I desired. This was a simple and flexible way of doing that. 


## Usage

```
Usage: report [OPTIONS]

Options:
  --days INTEGER       Number of days to report
  --start TEXT         Start date to report, in YYYY-MM-DD format
  --end TEXT           End date to report, in YYYY-MM-DD format
  --grainularity TEXT  One of HOURLY, DAILY, MONTHLY
  --help               Show this message and exit.

```

The command will use whichever profile is currently activated. So for example, if you 
want to use `aws-vault` you would use something like the following:

```
aws-vault exec billing-profile -- poetry run report --start 2022-01-01 --end 2022-02-01

```

## Packaging and Releasing 
TRD

## Installation
TBD

## Development
Requires [poetry](https://python-poetry.org/) to be installed.
