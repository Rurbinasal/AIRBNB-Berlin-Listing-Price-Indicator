![title](data/title.png)

# Description
Predictive modeling applying the entire data science lifecycle and building a Plotly Dash web application for user interaction with the model (retrieve listing pricing indication).

**Core idea**: Taking data from a given specific listing time stamp of Berlin, can we accurately predict its price in order to provide future hosts with a solid pricing estimate without requiring an Airbnb account beforehand? (aim: offer a tool for new users to get a first pricing and potential earnings indication without requiring an account)

# Findings:
- While it is not a trivial task to predict based only on features potentially available before listing creation, the **predictive model yielded acceptable results** and can definitely serve as a first indicator when considering a new listing
- Of the eventually used features, **room type** appeared to be the most important one, followed by **guests included**, **bedrooms** and **host listings** (i.e. whether the host already has prior listings)

# Outcomes:
- **Predictive model** based on features that a user without a prior listing may be able to provide (e.g. guests, bedrooms, bathrooms, etc.)
- **Pricing indication** and range based on Median Average Percentage Error
- **Web application** providing the pricing indication and potential earnings estimate based on up to 24 listing features 
- **Interactive input fields** with sensible default values based on average listings
- **Dynamically changing listing recommendation** as soon as input values are adapted

# Files in repository:
- 1_Predictive_Modeling.ipynb (Jupyter Notebook for Predictive Modeling, including data cleaning and feature engineering)
- 2_EDA.ipynb (Jupyter Notebook for EDA, including one part after data cleaning and another after data engineering)
- 3_App_Preparation.ipynb (Jupyter Notebook for fast access to saved models as means to review and/or overwrite them)
- 4_predictor.py (Python code for web application)
- 2020-09_02_Final Presentation.pdf (presentation of findings)

# Structure of 1_Predictive_Modeling.ipynb file
- **1 Set-up**
  - 1.1 Libraries and Dashboard
- **2 Preprocessing (Train/Test Split and Pipeline)**
  - 2.1 Preprocessing pipeline
  - 2.2 Train/test split
  - 2.3 Global Functions and Variables
- **3 Modeling: Binary Classification ("price_binary")**
  - 3.1 Apply Classification Models
  - 3.2 Clf Model 1: Logistic Regression
  - 3.3 NN Model 1: TBD (Future Work)
  - 3.4 Best Model Evaluation with Testing Set and Export
- **4 Modeling: Multi-Class Classification ("price_class")**
  - 4.1 Apply Classification Models
  - 4.2 Clf Model 1: Logistic Regression
  - 4.3 Clf Model 2: Random Forest
  - 4.4 Clf Model 3: XGBoost
  - 4.5 NN Model 1: TBD (Future Work)
- **5 Modeling: Regression ("price_log")**
  - 5.1 Apply Regression Models
  - 5.2 Reg Model 1: XGBoost
  - 5.3 Reg Model 2: Support Vector Machines
  - 5.4 Reg Model 3: Random Forest
  - 5.5 Reg Model 4: CatBoost
  - 5.6 NN Model 1: Neural Networks
  - 5.7 Final Evaluation with Testing Set
- **6 Future Work**

# Python modules used
- Pandas
- NumPy
- Matplotlib
- SciPy
- Seaborn
- Math
- Datetime
- statsmodels
- Scikit Learn
- Keras
- Plotly
- Plotly Dash

# Future work
**Predictive modeling**
- Apply further models and adapt current ones (e.g. NN)
- Examine other prediction targets (e.g. occupancy rate)

**Feature engineering**
- Explore NLP for text fields (descriptions, reviews, ...)
- Scrape listing photos and analyze quality
- Enhance current feature set

**Lean structure**
- Remove remaining redundancies wherever possible (e.g. pack repeated steps into functions, apply more pipelines, ...)

**Cloud**
- Move both model creation and app into the cloud (GCP)

**Automatization and replicability**
- Build a workflow to automatically retrain model monthly with new datasets
- Use automated outlier detection
- Use automated feature engineering

**Replicability**
- Reduce redundancies wherever possible (e.g. pack repeated steps into functions, apply more pipelines, ...)
- Apply analysis to other cities and compare results
