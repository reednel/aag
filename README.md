# Anshel-Anshel-Goldfeld

[![GitHub Releases](https://img.shields.io/github/v/release/reednel/aag?display_name=tag)](https://github.com/reednel/aag/releases) [![GitHub license](https://img.shields.io/github/license/reednel/aag)](https://github.com/reednel/aag/blob/main/LICENCE) [![GitHub Issues](https://img.shields.io/github/issues/reednel/aag)](https://github.com/reednel/aag/issues) ![ ](https://img.shields.io/github/languages/code-size/reednel/aag)

## Description

A generic implementation of the AAG key exchange using the [SageMath](https://www.sagemath.org/) computer algebra system.

## Requirements

This program requires **Python** and **SAGE**. Sage may be installed in a Docker container as described in the next section.

## Docker Deployment

The `.devcontainer` folder contains the config to open this repository into a Docker container with VS code and the [VS code Dev Containers extension](https://code.visualstudio.com/docs/devcontainers/containers)

The Docker container comes with [SAGE](https://www.sagemath.org/) installed.

See [this documentation](https://doc.sagemath.org/html/en/tutorial/programming.html) for more details on the importance of creating compiled code for execution speed.

## Usage

When the environment is configured inside a Docker container, a python file `file.py` can be run from its directory with `sage --python file.py`.

## Simulations in the Manuscript

All scripts and instructions to reproduce the analyses in the manuscript can be found in the `simulations` folder.

## Contributions, Questions, Issues, and Feedback

Users interested in expanding functionalities in MiNAA are welcome to do so. Issues reports are encouraged through Github's [issue tracker](https://github.com/reednel/aag/issues). See details on how to contribute and report issues in [CONTRIBUTING.md](https://github.com/reednel/aag/blob/master/CONTRIBUTING.md).

## License

MiNAA is licensed under the [MIT](https://opensource.org/licenses/MIT) licence.
