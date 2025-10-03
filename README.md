# SBD_OTS_RISK
The ORS risk prediction model estimates the likelihood of OTS misses for packages due out at each SBD-CPT within a fulfillment center (FC). Instead of assessing individual orders, the model evaluates groups of orders tied to a given CPT. It works in two steps: first, it forecasts the expected number of units shipped per hour at an FC, providing an estimate of available ship capacity until the CPT; second, it compares this forecasted capacity against the backlog due for the CPT, generating a high-fidelity risk score. This score is then used as an input to the SBD2 service, which applies precise padding to risky orders, ensuring customer promise times are protected. 
Figure 1, provides an example of the risk prediction at HOU1 when evaluated at 6:00 on 15th of September. HOU1 is a day-shift FC with three distinct CPTs. 
a.	Actual shipped units is the actual number of units shipped by FC between 6:00 and the CPT. For example, 37468 units were shipped between 6:00 and 14:30 on this day. Note: not all capacity is necessarily used for shipping out orders due for the CPT. FCs typically ship out a mix of currents and futures.  
b.	Forecasted shipped units is the forecast for the number of units the model estimates the FC to ship out between 6:00 and 14:30. 
c.	Backlog SBDT is the backlog due out on or before the SBDT as reported by WMS to ORS. For example, 11715 units are due for the 14:30 CPT. Similarly, 17928 units are due out leading up to the 16:00 CPT which includes the 11k units from the 14:30 CPT. And 40494 units are due out at the 17:00 CPT which includes all the units due out at the 14:30 CPT and 16:00 CPT.
d.	Risk Score Actual is the ratio of the backlog to actual capacity. This value will not be known in production and is a model evaluation metric.
e.	Risk Score Predicted is the ratio of the backlog to forecasted capacity. This predicted risk score will be the input to SBD2 service for making padding decisions.
 
Figure 1: Risk Score predictions at HOU1 at 6:00 on 15th of September.
<img width="468" height="494" alt="image" src="https://github.com/user-attachments/assets/d1810c55-4c23-4dc1-86db-f301e5f493dd" />


## Ship Capacity Forecast Model
The following model was developed to forecast the ship capacity at an FC for each hour in the day.
E[C_(hr,fc) ]=f(l_(shift,fc),tph_(shift,fc),l_(ot,shift,fc),l_(vot,shift,fc),fc,t_fc,w,h,h_(start,fc),h_(start-1,fc),h_(start+1,fc),s)
where:
E[C_(fc,hr) ] forecasted mean ship capacity of fc at hr
l_(shift,fc) labor hours/units planned for the shift at the fc
tph_(shift,fc) tph planned for the shift
l_(ot,shift,fc) overtime planned for the shift
l_(vot,shift,fc) voluntary time share planned for the shift
fc FC being forecasted
t_fc FC type 1G/2G
w day of the week
h hour of the day being forecasted
h_start   indicator of shift start at FC
h_(start-1) indicator of shift start -1 hour
h_(start+1) indicator of shift start +1 hour
s day or night shift flag








