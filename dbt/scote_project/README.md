## dbt Project

## Overview

This dbt project is responsible for transforming raw car listing data into clean, structured, and analytics-ready models.

It follows a layered approach:

- **Bronze** → raw source data
- **Silver** → cleaned and standardized data
- **Gold** → business-ready models for reporting and dashboarding

The transformed data is used in Power BI for analysis and visualization.

---

## Main Functions

This dbt project is used to:

- read raw data from the source table
- clean and standardize important fields
- apply filtering and business rules
- create analytical models for reporting
- support dashboard development in Power BI

---

## Project Layers

### Bronze
The Bronze layer contains the raw data loaded from the source table without major transformation.

### Silver
The Silver layer applies cleaning and standardization, such as:

- trimming text values
- standardizing fuel names
- standardizing transmission values
- filtering invalid prices
- filtering unrealistic years

### Gold
The Gold layer contains final reporting models such as:

- top car models
- fuel distribution
- average price, average kilometers, and average year
- transmission distribution and percentage share

---

## How to Run

Run the following commands inside the dbt project:

```
bash
dbt run
dbt test
```
```bash
dbt run
dbt test
