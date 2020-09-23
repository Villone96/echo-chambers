# Master Degree Thesis
## Echo Chamber Analysis
### Villa Giacomo

The project concerns the development of a pipeline for controversy reduction on Social Media. Part of the datasets used can be found at [Garimella Dataset](https://github.com/gvrkiran/controversy-detection/tree/master/networks/retweet_networks), Vaccination dataset can be found at [Kaggle Dataset](https://www.kaggle.com/keplaxo/twitter-vaccination-dataset), only Covid-19 dataset isn't freely accessible; in case of necessity, it will be share under request.

#### Folder
In the src folder you can find:

* **main.py**: launcher of entire pipeline.
preprocessing: it contains all functions for graph building activities
* **community**: it contains all functions about community detection activities and community tracking metrics assessments. After this step a summary log_community file is created. 
* **controversy_detection**: it contains all functions about controversy detection metrics used, a log file that contains a info about metrics values it is created after each run.
* **link_prediction**: it contains all function about links prediction strategy (state of arts strategy and homemade strategy as well), a plot result will be provided after running.
* **community Analysis & Code Snippets**: a jupyter notebooks that contain community metadata analysis and access graph activities. The second one is not necessary in this study.
* **analysis_images**: it contains, for each dataset, a set of images about analysis (metadata, controversy reduction, ecc.).

In the discussion folder you can find (not yet here):
```
TODO
```
#### How to run
In order to run the pipeline is necessary creates the following folders:
```
src/data: it will contain the following folders
src/data/corona_virus/raw_data: it will contain all raw data (csv file) of all months of observation.
src/data/vaccination/raw_data: it will contain all raw data (csv file) (look at the top for it).
src/data/garimella_data/retweet_networks: it will contain all raw data (txt file) about #beefban, 
                                          #nationalkissingday and #ukrain (look at the top for them).
```
and launch the following command:
```
python main
```

