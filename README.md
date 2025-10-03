# SBD_OTS_RISK
The ORS risk prediction model estimates the likelihood of OTS misses for packages due out at each SBD-CPT within a fulfillment center (FC). Instead of assessing individual orders, the model evaluates groups of orders tied to a given CPT. It works in two steps: 
1. First step forecasts the expected number of units shipped per hour at an FC, providing an estimate of available ship capacity until the CPT;
2. Second step compares this forecasted capacity against the backlog due for the CPT, generating a high-fidelity risk score. This score is then used as an input to the SBD2 service, which applies precise padding to risky orders, ensuring customer promise times are protected.


Figure 1, provides an example of the risk prediction at HOU1 when evaluated at 6:00 on 15th of September. HOU1 is a day-shift FC with three distinct CPTs. 
1. Actual shipped units is the actual number of units shipped by FC between 6:00 and the CPT. For example, 37468 units were shipped between 6:00 and 14:30 on this day. Note: not all capacity is necessarily used for shipping out orders due for the CPT. FCs typically ship out a mix of currents and futures.
2. Forecasted shipped units is the forecast for the number of units the model estimates the FC to ship out between 6:00 and 14:30.
3. Backlog SBDT is the backlog due out on or before the SBDT as reported by WMS to ORS. For example, 11715 units are due for the 14:30 CPT. Similarly, 17928 units are due out leading up to the 16:00 CPT which includes the 11k units from the 14:30 CPT. And 40494 units are due out at the 17:00 CPT which includes all the units due out at the 14:30 CPT and 16:00 CPT.
4. Risk Score Actual is the ratio of the backlog to actual capacity. This value will not be known in production and is a model evaluation metric.
5. Risk Score Predicted is the ratio of the backlog to forecasted capacity. This predicted risk score will be the input to SBD2 service for making padding decisions.

| eval_dttm          | sbdt            | actual_shipped_units   | forecasted_shipped_units   | backlog_sbdt   | risk_score_actual   | risk_score_predicted   |
|:-------------------|:----------------|:-----------|:-----------|:-----------|:-----------|:-----------|
|2025-09-15 06\:00\:00|2025-09-15 14\:30\:00|37468.0|34644.85|11715|31.26|33.81|
|2025-09-15 06\:00\:00|2025-09-15 16\:00\:00|46886.0|44445.91|17928|38.23|40.33|
|2025-09-15 06\:00\:00|2025-09-15 17\:00\:00|52657.0|49304.88|40494|76.90|82.13|

Figure 1: Risk Score predictions at HOU1 at 6:00 on 15th of September.


## Ship Capacity Forecast Model
The following model was developed to forecast the ship capacity at an FC for each hour in the day.

$E[C_{fc,h}]=f(l_{shift,fc},tph_{shift,fc},l_{ot,shift,fc},l_{vot,shift,fc},fc,t_{fc},w,h,h_{start,fc},h_{start-1,fc},h_{start+1,fc},s)$

where:

$E[C_{fc,h}]$ forecasted mean ship capacity of fc at hr

$l_{shift,fc}$ labor hours/units planned for the shift at the fc

$tph_{shift,fc}$ tph planned for the shift

$l_{ot,shift,fc}$ overtime planned for the shift

$l_{vot,shift,fc}$ voluntary time share planned for the shift

$fc$ FC being forecasted

$t_{fc}$ FC type 1G/2G

$w$ day of the week

$h$ hour of the day being forecasted

$h_{start}$   indicator of shift start at FC

$h_{start-1}$ indicator of shift start -1 hour

$h_{start+1}$ indicator of shift start +1 hour

$s$ day or night shift flag

# How to run the model
1. Update the date ranges in configs.py
2. Run preprocessor.py
3. Run model_training.py
4. Run sbd_risk_estimate.py



#####Author: Gautham Sunder <gsunder@chewy.com>





