# Car Insurance Claims Optimization with Process Mining 

This project simulates a consulting engagement to analyze and optimize the car insurance claims process using real-world event log data from Kaggle..

---

## Project Objectives

- Understand and visualize the full insurance claim process
- Identify bottlenecks and rework loops
- Segment delays by resource, policy type, and accident type
- Provide strategic recommendations backed by data
- Prepare the foundation for a KPI dashboard in Power BI

---

## Tools Used

- Python: `pandas`, `seaborn`, `matplotlib`
- Power BI: for KPI dashboard and business storytelling
- Data source: [Kaggle - Insurance Claims Event Log](https://www.kaggle.com/datasets/carlosalvite/car-insurance-claims-event-log-for-process-mining)

---

## Key Analyses

### Data Wrangling
- Parsed timestamps from MM:SS.s format into durations
- Sorted events by `case_id` and time
- Calculated `activity_duration` and total `case_duration`

### Exploratory Data Analysis
- Activity-level delay analysis (boxplots)
- Case duration distribution (histogram)
- Process complexity via activity count
- Most common event sequences ("happy paths")
- Rare and broken paths (for root cause discovery)
- Delay by agent
- Segment delays by:
  - `type_of_policy`
  - `type_of_accident`
  - `car_year`

---

## Power BI Dashboard (Phase 3)
Exported clean datasets for use in Power BI:
- `cleaned_event_log.csv`: activity-level data
- `case_summary.csv`: case-level metrics

> Visualizations include:
> - KPI cards (avg duration, max delay)
> - Donut charts (claim types)
> - Bar plots (delay by agent/type)
> - Sankey or Gantt views of process flows

---

## File Structure


## Sample Insights

- Claims with rollover accidents take ~40% longer on average
- Some agents consistently contribute to delays above the mean
- Claims on older vehicles show higher variability in resolution time
- "Fast lane" patterns suggest room for triage-based routing

---

## Business Value

> A 25% reduction in average case duration could lead to significant time savings and increased customer satisfaction — insights like these drive real impact in enterprise process mining.
