# RAMP starting kit on Restaurant scores lives standard

_Authors: Emma Demarecaux, Charles Desaleux, Romain Fabre, Julien Lenhardt, Luz Pascal, Benjamin Wallyn_

The Health Department has developed an inspection report and scoring system. After conducting an inspection of the facility, the Health Inspector calculates a score based on the violations observed. Violations can fall into:
* **high risk category**: records specific violations that directly relate to the transmission of food borne illnesses, the adulteration of food products and the contamination of food-contact surfaces;
* **moderate risk category**: records specific violations that are of a moderate risk to the public health and safety;
* **low risk category**: records violations that are low risk or have no immediate risk to the public health and safety.

Our goal is to estimate the restaurant score in order to help health inspectors select places that may not respect the health quality needed for a restaurant.

## Set up

Open a terminal and

1. install the `ramp-workflow` library (if not already done)
  ```
  $ pip install git+https://github.com/paris-saclay-cds/ramp-workflow.git
  ```

2. Follow the ramp-kits instructions from the [wiki](https://github.com/paris-saclay-cds/ramp-workflow/wiki/Getting-started-with-a-ramp-kit)

## Project structure

The project structure has been made using the project structure [Cookiecutter for Data Science](https://drivendata.github.io/cookiecutter-data-science/)

## Local notebook

Get started on this RAMP with the [notebook](restaurant_scores_starting_kit.ipynb).

To test the starting-kit, run

```
ramp_test_submission --submission starting_kit
```
or for a test mode :

```
ramp_test_submission --submission starting_kit --quick-test
```

## Help
Go to the `ramp-workflow` [wiki](https://github.com/paris-saclay-cds/ramp-workflow/wiki) for more help on the [RAMP](http:www.ramp.studio) ecosystem.
