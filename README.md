# Project Name: Real Stock Market Analysis

## Table of Contents
- `Overview`
- `Challenges`
- `Screenshot`
- `My process`
- `Built with`
- `What I learned`
- `Author`
- `Acknowledgements`

### Overview

The Project implements a real-time data pipeline that extracts stock data from vantage API, stream it through Apache Kafka, processes it with Apache Spark, and loads it into a postgres database.

All components are containerized with Docker for easy deployment.

### Screen-shot Data Pipeline Architecture
![Data Pipeline Architecture](./img/real-time-pipeline.png)

### Built with (project Tech Stack and Flow)
- `Kafka UI - inspect topics/messages`.
- `API - produces JSON events into kafka`
- `Spark - consumes from kafka, writes to postgres`
- `Postgres - store result for analytics`
- `PgAdmin - manage postgres visually`
- `Power BI - external (connects to Postgres database)`

### Challenges
- `Unable to retrieve data successfully from the API due to typing error`
- `Docker hub used previously is no longer available`