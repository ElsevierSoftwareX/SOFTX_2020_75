********************************************************************************
$ontext
The Dispatch and Investment Evaluation Tool with Endogenous Renewables (DIETER).
Version 1.3.0, November 2018.
Written by Alexander Zerrahn and Wolf-Peter Schill.
This work is licensed under the MIT License (MIT).
For more information on this license, visit http://opensource.org/licenses/mit-license.php.
Whenever you use this code, please refer to http://www.diw.de/dieter.
We are happy to receive feedback under azerrahn@diw.de and wschill@diw.de.
$offtext
********************************************************************************

**************************
***** GLOBAL OPTIONS *****
**************************

* Set in control_variables.csv
$setglobal base_year "%py_base_year%"

* Set in ontrol_variables.csv to set end hour -> work in progress to be implemented
$setglobal end_hour %py_end_hour%
$setglobal h_set %py_h_set%


* Set in feature_configuration.csv to choose model modules
$setglobal DSM %py_dsm%
$setglobal reserves %py_reserves%
$setglobal prosumage %py_prosumage%
$setglobal heat %py_heat%

* Set in feature_configuration.csv to choose whether electric vehicle module is activated or not
* if EV_endogenous is activated than EV module is switch on and solved endogenously
* if additionally EV_exogenous is activated than EV module is solved exogeneously
$setglobal EV_exogenous %py_ev_exogenous%
$setglobal EV_endogenous %py_ev_endogenous%
* deprecated: Set star to indicate renewables constraint on electric vehicles - DEFAULT is same quota as for the rest of the electricity system
*$setglobal EV_DEFAULT ""
*$setglobal EV_100RES ""
*$setglobal EV_FREE ""

* Set in control_variables.csv whether the model optimizes only dispatch or also investments
$setglobal dispatch_only %py_dispatch_only%
$setglobal investment %py_investment%

* Set in control_variables.csv
$setglobal net_transfer %py_network_transfer%

* Set star for no crossover to speed up calculation time by skipping crossover in LP solver
$setglobal no_crossover %py_no_crossover%

* automatically imported
$setglobal feature_set %py_feature_set%


* --------------------------- GDX INPUT FILES ----------------------------------
$setglobal data_input_gdx %py_data_input_gdx%
$setglobal time_series_gdx %py_time_series_gdx%
$setglobal feat_node_gdx %py_feat_node_gdx%
$setglobal data_it_gdx %py_data_it_gdx%

* ------------- RES SHARE CONSTRAINT FORMULATION -------------------------------
* Select a RES share constraint implementation by setting the switch to yes in iteration_constraints.csv:

*RES share constraint (0a): G_RES- demand, storage losses and ev demand in proportion to RES share
$setglobal rescon_0a %py_rescon_0a%

* RES share constraint (1b): G_RES-and demand-based, storage losses completely covered by RES
$setglobal rescon_1b %py_rescon_1b%

* RES share constraint (2c): G_RES- and total-generation-based, storage losses covered by RES proportional to (1-phi_min_res/100)
$setglobal rescon_2c %py_rescon_2c%

* RES share constraint (3b): G_CON- and demand-based, storage losses completely covered by RES
$setglobal rescon_3b %py_rescon_3b%

* RES share constraint (4e): G_CON- demand, storage losses and ev demand in proportion to RES share
$setglobal rescon_4e %py_rescon_4e%

* --------------- MAX CARBON CONSTRAINT --------------------------------------
* Select either overall CO2 or node CO2

$setglobal max_overall_CO2 %py_max_overall_CO2%
$setglobal max_node_CO2 %py_max_node_CO2%


* ------------- COUNTRY SET ITERATION -----------------------------------------

*switches
$setglobal iter_countries_switch_on   %py_iter_countries_switch_on%
$setglobal iter_countries_switch_off  %py_iter_countries_switch_off%

* set countries
$setglobal iter_countries_set         %py_iter_countries_set%

* set lines
$setglobal iter_lines_set             %py_iter_lines_set%


* ------------- TIME SERIES ITERATION -----------------------------------------

* switch
$setglobal iter_data_switch           %py_iter_data_switch%

* ------------- DISPLAY GLOBAL OPTIONS -----------------------------------------
display
"base_year: %base_year%",
"end_hour %end_hour%",
"h_set: %h_set%",
"feature_set: %feature_set%",

"DSM: %DSM%",
"reserves: %reserves%",
"prosumage: %prosumage%",
"heat: %heat%",
"EV_endogenous: %EV_endogenous%",
"EV_exogenous: %EV_exogenous%",
"no_crossover: %no_crossover%",
"dispatch_only: %dispatch_only%",
"investment: %investment%",
"net_transfer: %net_transfer%",

"rescon_0a: %rescon_0a%",
"rescon_1b: %rescon_1b%",
"rescon_2c: %rescon_2c%",
"rescon_3b: %rescon_3b%",
"rescon_4e: %rescon_4e%",
"max_overall_CO2: %max_overall_CO2%",
"max_node_CO2: %max_node_CO2%",

"iter_countries_switch_on: %iter_countries_switch_on%",
"iter_countries_switch_off: %iter_countries_switch_off%",
"iter_countries_set: %iter_countries_set%",
"iter_lines_set: %iter_lines_set%",
"iter_data_switch: %iter_data_switch%"
;


********************************************************************************

* Sanity checks
$if "%dispatch_only%" == "*" $if "%investment%" == "*" $abort Choose an appropriate option! ;
$if "%dispatch_only%" == "" $if "%investment%" == "" $abort Choose one option, either dispatch or investment! ;
$if "%EV_endogenous%" == "" $if "%EV_exogenous%" == "*" $abort Switch on ev_exogenous in feature_configuration.csv! ;
$if "%rescon_0a%%rescon_1b%%rescon_2c%%rescon_3b%%rescon_4e%" == "**" or "***" $abort Please select (only) one RES constraint formulation! ;
$if "%rescon_0a%%rescon_1b%%rescon_2c%%rescon_3b%%rescon_4e%" == "" $abort Please select (only) one RES constraint formulation! ;

$if "%max_overall_CO2%%max_node_CO2%" == "**" or "***" $abort Please select (only) one carbon constraint formulation! ;
$if "%max_overall_CO2%%max_node_CO2%" == "" $abort Please select (only) one carbon constraint formulation! ;

********************************************************************************

**************************
***** SOLVER OPTIONS *****
**************************

options

* The reslim specifies the maximum time in seconds that a solver may run before it terminates.
reslim = 250000
*  dispwidth may be used to display longer names in full, such as, label names that are headers of columns in tables. cut off after X characters
dispwidth = 20
* solprint remove solution listings following solves.
solprint = off
* sysout Suppress additional solver generated output.
sysout = off
limrow = 1
limcol = 1
*lp = cplex
* The optcr setting is a tolerance for the relative optimality gap in a MIP or other discrete model.
optcr = 0.00
;

**************************
***** Declarations *******
**************************

***** Sets used in the model *****

Sets
tech                             Generation technologies
 dis(tech)                       Dispatchable generation technologies
 nondis(tech)                    Nondispatchable generation technologies
 con(tech)                       Conventional generation technologies
 res(tech)                       Renewable generation technologies
sto                              Storage technologies
rsvr                             Reservoir technologies
dsm                              DSM technologies
 dsm_shift(dsm)                  DSM load shifting technologies
 dsm_curt(dsm)                   DSM load curtailment technologies
year                             Base year for temporal data
h                                Hours
n                                Nodes
l                                Lines
ev                               EV types
reserves                         Reserve qualities
 reserves_up(reserves)           Positive reserves
 reserves_do(reserves)           Negative reserves
 reserves_spin(reserves)         Spinning reserves
 reserves_nonspin(reserves)      Nonspinning reserves
 reserves_prim(reserves)         Primary reserves
 reserves_nonprim(reserves)      Nonprimary reserves
 reserves_prim_up(reserves)      Primary positive reserves
 reserves_nonprim_up(reserves)   Nonprimary positive reserves
 reserves_prim_do(reserves)      Primary negative reserves
 reserves_nonprim_do(reserves)   Nonprimary negative reserves
bu                               Building archtypes
ch                               Heating combination type
 hst(ch)                         Heating technology that feeds to storage
 hp(ch)                          Heat pump technologies
 hel(ch)                         Hybrid electric heating technologies - electric part
 hfo(ch)                         Hybrid electric heating technologies - fossil part
features                         Model modules


***** Sets used for data upload *****

headers_tech                     Generation technologies - upload headers
 tech_dispatch                   Generation technologies - dispatchable or nondispatchable
 tech_res_con                    Generation technologies - renewable or "conventional"
headers_sto                      Storage technologies - upload headers
headers_reservoir                Reservoir technologies - upload headers
headers_dsm                      DSM technologies - upload headers
 dsm_type                        DSM technologies - shifting or curtailment
headers_time                     Temporal data - upload headers
headers_topology                 Spatial data - upload headers
headers_ev                       EV data - upload headers
headers_time_ev                  EV temporal data - upload headers
headers_prosumage_generation     Prosumage generation data - upload headers
headers_prosumage_storage        Prosumage storage data - upload headers
headers_reserves                 Reserve data - upload headers
 reserves_up_down                Reserve data - positive and neagtive reserves
 reserves_spin_nonspin           Reserve data - spinning and nonspinning reserves
 reserves_prim_nonprim           Reserve data - primary and nonprimary reserves
headers_heat                     Heat data - upload headers
 heat_storage                    Heat data - storage technologies
 heat_hp                         Heat data - heat pump technologies
 heat_elec                       Heat data - hybrid heating technologies - electric part
 heat_fossil                     Heat data - hybrid heating technologies - fossil part
headers_time_heat                Heat data - upload headers time data
headers_time_dhw                 Heat data - upload headers time data on DHW
headers_2dim
headers_1dim
;

***************  PARAMETERS  ***************************************************

Parameters

***** Generation technologies *****

*--- Variable and fixed costs ---*

eta(n,tech)                Efficiency of conventional technologies [0 1]
carbon_content(n,tech)     CO2 emissions per fuel unit used [tons per MWh thermal]
c_up(n,tech)               Load change costs UP [EUR per MWh]
c_do(n,tech)               Load change costs DOWN [EUR per MWh]
c_fix(n,tech)              Annual fixed costs [EUR per MW per year]
c_vom(n,tech)              Variable O&M costs [EUR per MWh]
co2price(n,tech)           CO2 price in [EUR per ton]

*--- Investment ---*
c_inv_overnight(n,tech)    Investment costs: Overnight [EUR per MW]
lifetime_tech(n,tech)      Investment costs: technical lifetime [a]
recovery(n,tech)           Investment costs: Recovery period according to depreciation tables [a]
interest_rate_tech(n,tech) Investment costs: Interest rate [%]
m_p(n,tech)                Investment: maximum installable capacity per technology [MW]
m_e(n,tech)                Investment: maximum installable energy [TWh per a]

*--- Flexibility ---*
grad_per_min(n,tech)       Maximum load change relative to installed capacity [% of installed capacity per minute]


***** Fuel and CO2 costs *****
fuelprice(n,tech)          Fuel price conventionals [EUR per MWh thermal]

***** Renewables *****
c_cu(n,tech)               Hourly Curtailment costs for renewables [Euro per MW]
phi_min_res                Minimum renewables share [0 1]
phi_min_res_exog(n)        Minimum renewables share per node [0 1]


***** CO2 *****
co2_cap          	   Yearly CO2 cap
co2_cap_exog(n)            Yearly CO2 cap per node

***** Storage *****
*--- Variable and fixed costs ---*
c_m_sto(n,sto)             Marginal costs of storing in or out [EUR per MWh]
eta_sto(n,sto)             Storage efficiency [0 1]
phi_sto_ini(n,sto)         Initial storage level [0 1]
etop_max(n,sto)            Maximum E to P ratio of storage types [#]
c_fix_sto(n,sto)           Annual fixed costs [EUR per MW]

*--- Investment ---*
c_inv_overnight_sto_e(n,sto)     Investment costs for storage energy: Overnight [EUR per MWh]
c_inv_overnight_sto_p(n,sto)     Investment costs for storage capacity: Overnight [EUR per MW]
lifetime_sto(n,sto)              Investment costs: for storage technical lifetime [a]
interest_rate_sto(n,sto)         Investment costs: for storage Interest rate [%]
m_sto_e(n,sto)                   Investment into storage: maximum installable energy [MWh]
m_sto_p(n,sto)                   Investment into storage: maximum installable power [MW]

***** Reservoir*****
*--- Variable and fixed costs ---*
c_m_rsvr(n,rsvr)           Marginal costs of generating energy from reservoir [EUR per MWh]
eta_rsvr(n,rsvr)           Generation efficiency [0 1]
phi_rsvr_ini(n,rsvr)       Initial reservoir level [0 1]
c_fix_rsvr(n,rsvr)         Annual fixed costs [EUR per MW per a]
phi_rsvr_min(n)            Minimum hourly reservoir outflow as fraction of annual energy [0 1]
phi_rsvr_lev_min(n,rsvr)   Minimum filling level [0 1]
min_flh(n,rsvr)            Min flh per node and reservoir
phi_rsvr_maxout(n,rsvr)    per node and reservoir
phi_rsvr_minout(n,rsvr)    per node and reservoir

*--- Investment ---*
c_inv_overnight_rsvr_e(n,rsvr)   Investment costs for reservoir energy: Overnight [EUR per MWh]
c_inv_overnight_rsvr_p(n,rsvr)   Investment costs for reservoir capacity: Overnight [EUR per MW]
inv_lifetime_rsvr(n,rsvr)        Investment costs for reservoir: technical lifetime [a]
inv_interest_rsvr(n,rsvr)        Investment costs for reservoir: Interest rate [%]
m_rsvr_e(n,rsvr)                 Investment into reservoir: maximum installable energy [MWh]
m_rsvr_p(n,rsvr)                 Investment into reservoir: maximum installable capacity [MW]

***** DSM *****
*--- Variable and fixed costs ---*
c_m_dsm_cu(n,dsm)          DSM: hourly costs of load curtailment [EUR per MWh]
c_m_dsm_shift(n,dsm)       DSM: costs for load shifting [EUR per MWh]
c_fix_dsm_cu(n,dsm)        Annual fixed costs load curtailment capacity [EUR per MW per a]
c_fix_dsm_shift(n,dsm)     Annual fixed costs load shifting capacity [EUR per MW per a]

*--- Flexibility, efficiency, recovery ---*
t_dur_dsm_cu(n,dsm)        DSM: Maximum duration load curtailment [h]
t_off_dsm_cu(n,dsm)        DSM: Minimum recovery time between two load curtailment instances [h]

t_dur_dsm_shift(n,dsm)     DSM: Maximum duration load shifting [h]
t_off_dsm_shift(n,dsm)     DSM: Minimum recovery time between two granular load upshift instances [h]
eta_dsm_shift(n,dsm)       DSM: Efficiency of load shifting technologies [0 1]

*--- Investment ---*
c_inv_overnight_dsm_cu(n,dsm)    Investment costs for DSM load curtailment: Overnight [EUR per MW]
c_inv_overnight_dsm_shift(n,dsm) Investment costs for DSM load shifting: Overnight [EUR per MW]
inv_recovery_dsm_cu(n,dsm)       Investment costs for DSM load curtailment: Recovery period [a]
inv_recovery_dsm_shift(n,dsm)    Investment costs for DSM load shifting: Recovery period [a]
inv_interest_dsm_cu(n,dsm)       Investment costs for DSM load curtailment: Interest rate [%]
inv_interest_dsm_shift(n,dsm)    Investment costs for DSM load shifting: Interest rate [%]
m_dsm_cu(n,dsm)                  DSM: Maximum installable capacity load curtailment [MW]
m_dsm_shift(n,dsm)               DSM: Maximum installable capacity load shifting [MW]

***** Time Data *****
d_y(n,year,h)                    Demand hour h for different years [MWh]
d(n,h)                           Demand hour h [MWh]
phi_res_y(n,year,tech,h)         Renewables availability technology res in hour h for different years [0 1]
phi_res(n,tech,h)                Renewables availability technology res in hour h [0 1]
rsvr_in_y(n,year,rsvr,h)         	  Reservoir inflow in hour h for different years [0 1]
rsvr_in(n,rsvr,h)                	  Reservoir inflow in hour h [0 1]
phi_reserves_call_y(n,year,reserves,h)    Hourly share of reserve provision that is actually activated for different years [0 1]
phi_reserves_call(n,reserves,h)  	  Hourly share of reserve provision that is actually activated [0 1]
reserves_exogenous_y(n,year,reserves,h)   Hourly reserve provision for different years [MW]
reserves_exogenous(n,reserves,h) 	  Hourly reserve provision [MW]

***** Transmission *****
*--- Investment ---*
c_inv_overnight_ntc(l)     Investment costs in: overnight [EUR per MW]
c_fix_ntc(l)               Fixed costs [EUR per MW per a]
inv_lifetime_ntc(l)        Investment costs: technical lifetime [a]
inv_recovery_ntc(l)        Investment costs: Recovery period in [a]
inv_interest_ntc(l)        Investment costs: Interest rate [%]
m_ntc(l)                   Investment into NTC: maximum installable capacity [MW]

*--- Topology and distance ---*
inc(l,n)              	   Incidence index of link l on node n
dist(l)             	   Distance covered by link l [km]

***** Electric vehicles *****
*--- Costs and attributes ---*
c_m_ev(n,ev)               Marginal costs of discharging V2G [EUR per MWh]
pen_phevfuel(n,ev)         Penalty for non-electric PHEV operation mode [EUR per MWh]
eta_ev_in(n,ev)            Electric vehicle efficiency of charging (G2V) [0 1]
eta_ev_out(n,ev)           Electric vehicle efficiency of discharging (V2G) [0 1]
phi_ev_ini(n,ev)           Electric vehicle charging level in initial period [0 1]

n_ev_e(n,ev)               Electric vehicle battery capacity [MWh]
ev_quant(n)        	       Overall number of electirc vehicles [#]
phi_ev(n,ev)           	   Share of electric vehicles per load profile in actual scenario [0 1]
ev_phev(n,ev)          	   Defines whether an electric vehicle is a PHEV REEV [1 if yes 0 otherwise]

*--- Temporal data ---*
n_ev_p(n,ev,h)             Power rating of the charging connection in hour h [MW - 0 when car is in use or parked without grid connection]
ev_ed(n,ev,h)              Electricity demand for mobility vehicle profile ev in hour h [MW]
ev_ged_exog(n,ev,h)        Electricity demand for mobility in case of uncontrolled (exogenous) charging vehicle profile ev in hour h [MW]

***** Prosumage *****
phi_pro_load(n)            Share of prosumagers among total load [0 1]
phi_pro_self               Minimum self-generation shares for prosumagers [0 1]
m_res_pro(n,tech)          Maximum installable: renewables capacity [MW]
m_sto_pro_e(n,sto)         Maximum installable: storage energy [MWh]
m_sto_pro_p(n,sto)         Maximum installable: storage capacity [MW]
phi_sto_pro_ini(n,sto)     Prosumagers initial storage loading [0 1]

***** Reserves *****
reserves_reaction(n,reserves)               Activation reaction time for reserves qualities [min]

***** Heat *****
*--- Time data ---*
dh_upload                                   Hourly heat demand per year for upload [MWh per m2]
dh_y(n,year,bu,ch,h)                        Hourly heat demand per year [MWh per m2]
dh(n,bu,ch,h)                               Hourly heat demand [MWh per m2]
temp_source(n,bu,ch,h)                      Heat pumps - source temperature [degree Celsius]
d_dhw_upload(h,n,year,headers_time_heat,bu) Hourly DHW demand per year for upload [MWh per m2] - dependencies
d_dhw_y(n,year,bu,ch,h)                     Hourly DHW demand per year [MWh per m2]
d_dhw(n,bu,ch,h)                            Hourly DHW demand [MWh per m2]
*nets_profile                                Hourly exogenous heat demand by nonsmart night-time storage heaters [MWh per m2]

*--- Technololgy attributes ---*
phi_heat_type(n,bu,ch)     Share of heating type ch per building archetype bu [0 1]
eta_heat_stat(n,bu,ch)     Static efficiency for heating technologies [0 1]
eta_heat_dyn(n,bu,ch)      Static efficiency for heating technologies [0 1]
eta_dhw_aux_stat(n,bu,ch)  Static efficiency for auxiliary DHW technologies [0 1]
n_heat_p_in(n,bu,ch)       Maximum power inflow into heating technologies [MW]
n_heat_p_out(n,bu,ch)      Maximum power outflow from heating technologies [MW]
n_heat_e(n,bu,ch)          Maximum energy level of heating storage technologies [MWh]
n_sets_p_in(n,bu,ch)       SETS - Power rating - electricity intake [MW]
n_sets_p_out(n,bu,ch)      SETS - Power rating - heat output [MW]
n_sets_e(n,bu,ch)          SETS - Energy storage capacity [MWh]
n_sets_dhw_p_in(n,bu,ch)   SETS auxiliary DHW module - power rating - electricity intake [MW]
n_sets_dhw_p_out(n,bu,ch)  SETS auxiliary DHW module - power rating - DHW output [MW]
n_sets_dhw_e(n,bu,ch)      SETS auxiliary DHW module - energy storage capacity [MWh]
phi_heat_ini(n,bu,ch)      Inititial storage level of heating technologies [0 1]
temp_sink(n,bu,ch)         Heat pumps - sink temperature [�Celsius]
pen_heat_fuel(n,bu,ch)     Penalty term for non-electric fuel usage for hybrid heating technologies [EUR per MWh]
area_floor(n,bu,ch)        Floor area subject to specific heating technology in specific building type [m2]
*theta_night               Indicator for night hours {0 1}

***************  DERIVED PARAMETERS  *******************************************

c_m(n,tech)                Marginal production costs for conventional plants including variable O and M costs [EUR per MWh]
c_i(n,tech)                Annualized investment costs by conventioanl plant [EUR per MW]

c_i_res(n,tech)            Annualized investment costs by renewable plant [EUR per MW]
c_fix_res(n,tech)          Annualized fixed costs by renewable plant [EUR per MW per a]

c_i_sto_e(n,sto)           Annualized investment costs storage energy [EUR per MWh]
c_i_sto_p(n,sto)           Annualized investment costs storage capacity [EUR per MW]

c_i_rsvr_e(n,rsvr)         Annualized investment costs storage energy [EUR per MWh]
c_i_rsvr_p(n,rsvr)         Annualized investment costs storage capacity [EUR per MW]

c_i_dsm_cu(n,dsm)          DSM: Annualized investment costs load curtailment [EUR per MW]
c_i_dsm_shift(n,dsm)       DSM: Annualized investment costs load shifting [EUR per MW]

c_i_ntc(l)                 Investment for net transfer capacity [EUR per MW and km]

phi_mean_reserves_call_y(n,year,reserves) Hourly mean of share reserves called per year [0 1]
phi_mean_reserves_call(n,reserves)        Hourly mean of share reserves called [0 1]

theta_dir(n,bu,ch)         Dummy equal to 1 if building type bu has direct heating type ch [0 1]
theta_sets(n,bu,ch)        Dummy equal to 1 if building type bu has SETS heating type ch [0 1]
theta_hp(n,bu,ch)          Dummy equal to 1 if building type bu has heat pump heating type ch [0 1]
theta_elec(n,bu,ch)        Dummy equal to 1 if building type bu has hybrif electric heating - electric part [0 1]
theta_fossil(n,bu,ch)      Dummy equal to 1 if building type bu has hybrif electric heating - fossil part [0 1]
theta_storage(n,bu,ch)     Dummy equal to 1 if building type ch has storage heating type ch [0 1]

******************* features table *************************

feat_node(features,n)      Features of each node

***************  PARAMETERS FOR DATA UPLOAD  ***********************************

technology_data_upload(n,tech,tech_res_con,tech_dispatch,headers_tech)
technology_data(n,tech,headers_tech)
storage_data(n,sto,headers_sto)
reservoir_data(n,rsvr,headers_reservoir)
time_data_upload(h,n,year,headers_time)
dsm_data_upload(n,dsm,dsm_type,headers_dsm)
dsm_data(n,dsm,headers_dsm)
topology_data(l,headers_topology)
* CG modify original: ev_data(n,ev,headers_ev) n was removed
ev_data(ev,headers_ev)
ev_time_data_upload(h,headers_time_ev,ev)
prosumage_data_generation(n,tech,headers_prosumage_generation)
prosumage_data_storage(n,sto,headers_prosumage_storage)
reserves_time_data_activation(h,year,reserves)
reserves_time_data_provision(h,year,reserves)
reserves_data_upload(n,reserves,reserves_up_down,reserves_spin_nonspin,reserves_prim_nonprim,headers_reserves)
reserves_data(n,reserves,headers_reserves)
heat_data_upload(n,bu,ch,heat_storage,heat_hp,heat_elec,heat_fossil,headers_heat)
heat_data(n,bu,ch,headers_heat)
dh_upload(h,n,year,headers_time_heat,bu)
d_dhw_upload(h,n,year,headers_time_heat,bu)
temp_source_upload
data_2dim(n,headers_2dim)
data_1dim(headers_1dim)
;

Scalar ms 'model status', ss 'solve status';

***********************************
***** Definition via Upload *******
***********************************

***** Define country set **********

* with iteration
%iter_countries_switch_on%$ontext
Set n "Nodes" / %iter_countries_set% / ;
Set l "Lines" / %iter_lines_set% / ;
$ontext
$offtext


* without iteration
%iter_countries_switch_off%$ontext
$GDXin "%data_input_gdx%"
$load n l
;
$ontext
$offtext

************************************

$GDXin "%data_input_gdx%"
$load tech headers_tech tech_dispatch tech_res_con
$load sto headers_sto rsvr headers_reservoir reservoir_data dsm headers_dsm dsm_type
$load technology_data_upload storage_data dsm_data_upload
$load headers_topology topology_data
$load inc
$load ev headers_ev ev_data
$load headers_prosumage_generation headers_prosumage_storage prosumage_data_generation prosumage_data_storage
$load reserves reserves_up_down reserves_spin_nonspin reserves_prim_nonprim headers_reserves reserves_data_upload
$load bu ch heat_storage heat_hp heat_elec heat_fossil headers_heat heat_data_upload
$load headers_2dim data_2dim headers_1dim data_1dim
;

***********************************
******* Definition end_hour *******
***********************************

******* Define custom h set *******
%end_hour%$ontext

Set h "Hours" / %h_set% / ;

$ontext
$offtext
***********************************

$GDXin "%time_series_gdx%"
%end_hour%$load h
$load headers_time year time_data_upload
$load headers_time_ev ev_time_data_upload
$load reserves_time_data_activation
$load reserves_time_data_provision
$load headers_time_heat dh_upload
$load temp_source_upload
$load headers_time_dhw d_dhw_upload
*$load nets_profile
*$load theta_night
;

* we need all global features as set-coordinates
set
features /%feature_set%/
;

$GDXin "%feat_node_gdx%"
$load feat_node
;


***************  ASSIGNMENTS  **************************************************
***** Aliases *****
alias (h,hh) ;
alias (res,resres) ;
alias (reserves,reservesreserves) ;
alias (nondis,nondisnondis) ;

***** Derived sets *****
dis(tech)$sum( (n,tech_res_con,headers_tech), technology_data_upload(n,tech,tech_res_con,'dis',headers_tech)) = yes;
nondis(tech)$sum( (n,tech_res_con,headers_tech), technology_data_upload(n,tech,tech_res_con,'nondis',headers_tech)) = yes;

con(tech)$sum( (n,tech_dispatch,headers_tech), technology_data_upload(n,tech,'con',tech_dispatch,headers_tech)) = yes;
res(tech)$sum( (n,tech_dispatch,headers_tech), technology_data_upload(n,tech,'res',tech_dispatch,headers_tech)) = yes;

reserves_up(reserves)$sum( (n,reserves_spin_nonspin,reserves_prim_nonprim,headers_reserves), reserves_data_upload(n,reserves,'up',reserves_spin_nonspin,reserves_prim_nonprim,headers_reserves)) = yes;
reserves_do(reserves)$sum( (n,reserves_spin_nonspin,reserves_prim_nonprim,headers_reserves), reserves_data_upload(n,reserves,'do',reserves_spin_nonspin,reserves_prim_nonprim,headers_reserves)) = yes;

reserves_spin(reserves)$sum( (n,reserves_up_down,reserves_prim_nonprim,headers_reserves), reserves_data_upload(n,reserves,reserves_up_down,'spin',reserves_prim_nonprim,headers_reserves)) = yes;
reserves_nonspin(reserves)$sum( (n,reserves_up_down,reserves_prim_nonprim,headers_reserves), reserves_data_upload(n,reserves,reserves_up_down,'nonspin',reserves_prim_nonprim,headers_reserves)) = yes;

reserves_prim(reserves)$sum( (n,reserves_up_down,reserves_spin_nonspin,headers_reserves), reserves_data_upload(n,reserves,reserves_up_down,reserves_spin_nonspin,'prim',headers_reserves)) = yes;
reserves_nonprim(reserves)$sum( (n,reserves_up_down,reserves_spin_nonspin,headers_reserves), reserves_data_upload(n,reserves,reserves_up_down,reserves_spin_nonspin,'nonprim',headers_reserves)) = yes;

reserves_prim_up(reserves)$sum( (n,reserves_spin_nonspin,headers_reserves), reserves_data_upload(n,reserves,'up',reserves_spin_nonspin,'prim',headers_reserves)) = yes;
reserves_prim_do(reserves)$sum( (n,reserves_spin_nonspin,headers_reserves), reserves_data_upload(n,reserves,'do',reserves_spin_nonspin,'prim',headers_reserves)) = yes;
reserves_nonprim_up(reserves)$sum( (n,reserves_spin_nonspin,headers_reserves), reserves_data_upload(n,reserves,'up',reserves_spin_nonspin,'nonprim',headers_reserves)) = yes;
reserves_nonprim_do(reserves)$sum( (n,reserves_spin_nonspin,headers_reserves), reserves_data_upload(n,reserves,'do',reserves_spin_nonspin,'nonprim',headers_reserves)) = yes;

hst(ch)$sum( (n,bu,heat_hp,heat_elec,heat_fossil,headers_heat), heat_data_upload(n,bu,ch,'yes',heat_hp,heat_elec,heat_fossil,headers_heat)) = yes;
hp(ch)$sum( (n,bu,heat_storage,heat_elec,heat_fossil,headers_heat), heat_data_upload(n,bu,ch,heat_storage,'yes',heat_elec,heat_fossil,headers_heat)) = yes;

hel(ch)$sum( (n,bu,heat_storage,heat_hp,heat_fossil,headers_heat), heat_data_upload(n,bu,ch,heat_storage,heat_hp,'yes',heat_fossil,headers_heat)) = yes;
hfo(ch)$sum( (n,bu,heat_storage,heat_hp,heat_elec,headers_heat), heat_data_upload(n,bu,ch,heat_storage,heat_hp,heat_elec,'yes',headers_heat)) = yes;

***** Parameters *****

*--- Generation technologies ---*
technology_data(n,tech,headers_tech) = sum((tech_res_con,tech_dispatch), technology_data_upload(n,tech,tech_res_con,tech_dispatch,headers_tech)) ;
eta(n,tech) = technology_data(n,tech,'eta_con') ;
carbon_content(n,tech) = technology_data(n,tech,'carbon_content') ;
c_up(n,dis) =technology_data(n,dis,'load change costs up') ;
c_do(n,dis) = technology_data(n,dis,'load change costs down') ;
c_fix(n,tech) = technology_data(n,tech,'fixed_costs') ;
c_vom(n,tech) = technology_data(n,tech,'variable_om') ;
co2price(n,tech) = technology_data(n,tech,'CO2_price') ;

c_inv_overnight(n,tech) = technology_data(n,tech,'oc') ;
lifetime_tech(n,tech) = technology_data(n,tech,'lifetime') ;
recovery(n,tech) = technology_data(n,tech,'recovery_period') ;
interest_rate_tech(n,tech) = technology_data(n,tech,'interest_rate') ;
m_p(n,tech) = technology_data(n,tech,'max_installable') ;
m_e(n,tech) = technology_data(n,tech,'max_energy') ;
grad_per_min(n,dis) = technology_data(n,dis,'load change flexibility') ;
fuelprice(n,tech) = technology_data(n,tech,'fuel costs') ;

c_cu(n,res) = technology_data(n,res,'curtailment_costs') ;

*--- Storage technologies ---*
c_m_sto(n,sto) = storage_data(n,sto,'mc');
eta_sto(n,sto) = sqrt(storage_data(n,sto,'efficiency'));
c_fix_sto(n,sto) = storage_data(n,sto,'fixed_costs');
phi_sto_ini(n,sto) = storage_data(n,sto,'level_start');
etop_max(n,sto) = storage_data(n,sto,'etop_max') ;

c_inv_overnight_sto_e(n,sto) = storage_data(n,sto,'oc_energy');
c_inv_overnight_sto_p(n,sto) = storage_data(n,sto,'oc_capacity');
lifetime_sto(n,sto) = storage_data(n,sto,'lifetime');
interest_rate_sto(n,sto) = storage_data(n,sto,'interest_rate');
m_sto_e(n,sto) = storage_data(n,sto,'max_energy');
m_sto_p(n,sto) = storage_data(n,sto,'max_power');

*--- Reservoir technologies ---*
c_m_rsvr(n,rsvr) = reservoir_data(n,rsvr,'mc');
eta_rsvr(n,rsvr) = reservoir_data(n,rsvr,'efficiency');
c_fix_rsvr(n,rsvr) = reservoir_data(n,rsvr,'fixed_costs');
phi_rsvr_ini(n,rsvr) = reservoir_data(n,rsvr,'level_start');
phi_rsvr_lev_min(n,rsvr) = reservoir_data(n,rsvr,'level_min');

c_inv_overnight_rsvr_e(n,rsvr) = reservoir_data(n,rsvr,'oc_energy');
c_inv_overnight_rsvr_p(n,rsvr) = reservoir_data(n,rsvr,'oc_capacity');
inv_lifetime_rsvr(n,rsvr) = reservoir_data(n,rsvr,'lifetime');
inv_interest_rsvr(n,rsvr) = reservoir_data(n,rsvr,'interest_rate');
m_rsvr_e(n,rsvr) = reservoir_data(n,rsvr,'max_energy');
m_rsvr_p(n,rsvr) = reservoir_data(n,rsvr,'max_power');

*--- DSM technologies ---*
dsm_curt(dsm)$sum( (n,dsm_type,headers_dsm), dsm_data_upload(n,dsm,'curt',headers_dsm)) = yes;
dsm_shift(dsm)$sum( (n,dsm_type,headers_dsm), dsm_data_upload(n,dsm,'shift',headers_dsm)) = yes;
dsm_data(n,dsm,headers_dsm) = sum(dsm_type, dsm_data_upload(n,dsm,dsm_type,headers_dsm) ) ;

c_m_dsm_cu(n,dsm_curt) = dsm_data(n,dsm_curt,'mc')     ;
c_m_dsm_shift(n,dsm_shift) = dsm_data(n,dsm_shift,'mc')  ;
c_fix_dsm_cu(n,dsm_curt) = dsm_data(n,dsm_curt,'fc')  ;
c_fix_dsm_shift(n,dsm_shift) = dsm_data(n,dsm_shift,'fc') ;

t_dur_dsm_cu(n,dsm_curt) = dsm_data(n,dsm_curt,'max_duration')   ;
t_off_dsm_cu(n,dsm_curt) = dsm_data(n,dsm_curt,'recovery_time')   ;
t_dur_dsm_shift(n,dsm_shift) = dsm_data(n,dsm_shift,'max_duration')   ;
t_off_dsm_shift(n,dsm_shift) = dsm_data(n,dsm_shift,'recovery_time')   ;
eta_dsm_shift(n,dsm_shift)  = dsm_data(n,dsm_shift,'efficiency')   ;

c_inv_overnight_dsm_cu(n,dsm_curt) =  dsm_data(n,dsm_curt,'oc')   ;
c_inv_overnight_dsm_shift(n,dsm_shift)  =  dsm_data(n,dsm_shift,'oc')   ;
inv_recovery_dsm_cu(n,dsm_curt)  =  dsm_data(n,dsm_curt,'lifetime')   ;
inv_recovery_dsm_shift(n,dsm_shift)   =  dsm_data(n,dsm_shift,'lifetime')   ;
inv_interest_dsm_cu(n,dsm_curt)   =  dsm_data(n,dsm_curt,'interest_rate')   ;
inv_interest_dsm_shift(n,dsm_shift)  =  dsm_data(n,dsm_shift,'interest_rate')   ;
m_dsm_cu(n,dsm_curt) =  dsm_data(n,dsm_curt,'max_installable')   ;
m_dsm_shift(n,dsm_shift) =  dsm_data(n,dsm_shift,'max_installable')   ;

*--- Temporal data ---*
d_y(n,year,h) = time_data_upload(h,n,year,'demand')  ;
phi_res_y(n,year,res,h) = sum(headers_time$(sameas(res,headers_time)), time_data_upload(h,n,year,headers_time));
rsvr_in_y(n,year,rsvr,h) = sum(headers_time$(sameas(rsvr,headers_time)), time_data_upload(h,n,year,headers_time));
phi_reserves_call_y(n,year,reserves,h) = reserves_time_data_activation(h,year,reserves) ;
reserves_exogenous_y(n,year,reserves,h) = reserves_time_data_provision(h,year,reserves) ;

*--- Spatial data ---*
inv_lifetime_ntc(l) = topology_data(l,'lifetime') ;
inv_recovery_ntc(l) = topology_data(l,'recovery_period') ;
inv_interest_ntc(l) = topology_data(l,'interest_rate') ;
c_inv_overnight_ntc(l) = topology_data(l,'overnight_costs') ;
c_fix_ntc(l) = topology_data(l,'fixed_costs') ;
m_ntc(l) = topology_data(l,'max_installable') ;
dist(l) = topology_data(l,'distance') ;

*--- Electric vehicles ---*
* CG modify original ev_data(n,ev,headers_ev) contained n as first set
c_m_ev(n,ev) = ev_data(ev,'mc') ;
pen_phevfuel(n,ev) = ev_data(ev,'penalty_fuel') ;
eta_ev_in(n,ev) = ev_data(ev,'efficiency_charge') ;
eta_ev_out(n,ev) = ev_data(ev,'efficiency_discharge') ;
phi_ev_ini(n,ev) = ev_data(ev,'ev_start') ;

n_ev_e(n,ev) = ev_data(ev,'ev_capacity') ;
phi_ev(n,ev) = ev_data(ev,'share_ev') ;
ev_phev(n,ev) = ev_data(ev,'ev_type') ;

n_ev_p(n,ev,h) = ev_time_data_upload(h,'n_ev_p',ev) ;
ev_ed(n,ev,h) = ev_time_data_upload(h,'ev_ed',ev) ;
ev_ged_exog(n,ev,h) = ev_time_data_upload(h,'ev_ged_exog',ev) ;

*--- Prosumage ---*
m_res_pro(n,res) = prosumage_data_generation(n,res,'max_power') ;
m_sto_pro_e(n,sto) = prosumage_data_storage(n,sto,'max_energy') ;
m_sto_pro_p(n,sto) = prosumage_data_storage(n,sto,'max_power') ;
phi_sto_pro_ini(n,sto) = prosumage_data_storage(n,sto,'level_start') ;

*--- Reserves ---*
reserves_data(n,reserves,headers_reserves) = sum((reserves_up_down,reserves_spin_nonspin,reserves_prim_nonprim), reserves_data_upload(n,reserves,reserves_up_down,reserves_spin_nonspin,reserves_prim_nonprim,headers_reserves)) ;
reserves_reaction(n,reserves) = reserves_data(n,reserves,'reaction_time') ;

*--- Heat ---*
heat_data(n,bu,ch,headers_heat) = sum((heat_storage,heat_hp,heat_elec,heat_fossil), heat_data_upload(n,bu,ch,heat_storage,heat_hp,heat_elec,heat_fossil,headers_heat)) ;
phi_heat_type(n,bu,ch) = heat_data(n,bu,ch,'share') ;
dh_y(n,year,bu,ch,h) = phi_heat_type(n,bu,ch) * dh_upload(h,n,year,'demand',bu) ;
d_dhw_y(n,year,bu,ch,h) = phi_heat_type(n,bu,ch) * d_dhw_upload(h,n,year,'demand',bu) ;

eta_heat_stat(n,bu,ch) = heat_data(n,bu,ch,'static_efficiency') ;
eta_heat_dyn(n,bu,ch) = heat_data(n,bu,ch,'dynamic_efficiency') ;
eta_dhw_aux_stat(n,bu,ch) = heat_data(n,bu,ch,'static_efficiency_sets_aux_dhw') ;
* currently not used
n_heat_p_in(n,bu,ch) = heat_data(n,bu,ch,'max_power') ;
n_heat_p_out(n,bu,ch) = heat_data(n,bu,ch,'max_outflow') ;
n_heat_e(n,bu,ch) = heat_data(n,bu,ch,'max_level') ;
n_sets_p_in(n,bu,ch) = heat_data(n,bu,ch,'max_power') ;
n_sets_p_out(n,bu,ch) = heat_data(n,bu,ch,'max_outflow') ;
n_sets_e(n,bu,ch) = heat_data(n,bu,ch,'max_level') ;
n_sets_dhw_p_in(n,bu,ch) = heat_data(n,bu,ch,'max_power_in_sets_aux_dhw') ;
n_sets_dhw_p_out(n,bu,ch) = heat_data(n,bu,ch,'max_power_out_sets_aux_dhw') ;
n_sets_dhw_e(n,bu,ch) = heat_data(n,bu,ch,'max_energy_sets_aux_dhw') ;
phi_heat_ini(n,bu,ch) = heat_data(n,bu,ch,'level_ini') ;
temp_sink(n,bu,ch) = heat_data(n,bu,ch,'temperature_sink') ;
temp_source(n,bu,'hp_as',h) = temp_source_upload(h,n,'hp_as') ;
temp_source(n,bu,'hp_gs',h) = heat_data(n,bu,'hp_gs','temperature_source') ;
temp_source(n,bu,'gas_hp_gs',h) = heat_data(n,bu,'gas_hp_gs','temperature_source') ;
temp_source(n,bu,'hp_gs_elec',h) = heat_data(n,bu,'hp_gs_elec','temperature_source') ;
pen_heat_fuel(n,bu,ch) = heat_data(n,bu,ch,'penalty_non-electric_heat_supply') ;
area_floor(n,bu,ch) = heat_data(n,bu,ch,'area_floor') ;

***************  CALCULATE DERIVED PARAMETERS  *********************************

c_m(n,tech) = fuelprice(n,tech)/eta(n,tech) + carbon_content(n,tech)/eta(n,tech)*co2price(n,tech) + c_vom(n,tech)   ;

c_i(n,tech) = c_inv_overnight(n,tech)*( interest_rate_tech(n,tech) * (1+interest_rate_tech(n,tech))**(lifetime_tech(n,tech)) )
                  / ( (1+interest_rate_tech(n,tech))**(lifetime_tech(n,tech))-1 )       ;

c_i_res(n,res) = c_i(n,res) ;
c_fix_res(n,res) = c_fix(n,res) ;

c_i_sto_e(n,sto) = c_inv_overnight_sto_e(n,sto)*( interest_rate_sto(n,sto) * (1+interest_rate_sto(n,sto))**(lifetime_sto(n,sto)) )
                 / ( (1+interest_rate_sto(n,sto))**(lifetime_sto(n,sto))-1 )       ;

c_i_sto_p(n,sto) = c_inv_overnight_sto_p(n,sto)*( interest_rate_sto(n,sto) * (1+interest_rate_sto(n,sto))**(lifetime_sto(n,sto)) )
                 / ( (1+interest_rate_sto(n,sto))**(lifetime_sto(n,sto))-1 )       ;

c_i_rsvr_e(n,rsvr) = c_inv_overnight_rsvr_e(n,rsvr)*( inv_interest_rsvr(n,rsvr) * (1+inv_interest_rsvr(n,rsvr))**(inv_lifetime_rsvr(n,rsvr)) )
                 / ( (1+inv_interest_rsvr(n,rsvr))**(inv_lifetime_rsvr(n,rsvr))-1 )       ;

c_i_rsvr_p(n,rsvr) = c_inv_overnight_rsvr_p(n,rsvr)*( inv_interest_rsvr(n,rsvr) * (1+inv_interest_rsvr(n,rsvr))**(inv_lifetime_rsvr(n,rsvr)) )
                 / ( (1+inv_interest_rsvr(n,rsvr))**(inv_lifetime_rsvr(n,rsvr))-1 )       ;

c_i_dsm_cu(n,dsm_curt) =c_inv_overnight_dsm_cu(n,dsm_curt)*( inv_interest_dsm_cu(n,dsm_curt) * (1+inv_interest_dsm_cu(n,dsm_curt))**(inv_recovery_dsm_cu(n,dsm_curt)) )
                 / ( (1+inv_interest_dsm_cu(n,dsm_curt))**(inv_recovery_dsm_cu(n,dsm_curt))-1 )       ;

c_i_dsm_shift(n,dsm_shift) = c_inv_overnight_dsm_shift(n,dsm_shift)*( inv_interest_dsm_shift(n,dsm_shift) * (1+inv_interest_dsm_shift(n,dsm_shift))**(inv_recovery_dsm_shift(n,dsm_shift)) )
                 / ( (1+inv_interest_dsm_shift(n,dsm_shift))**(inv_recovery_dsm_shift(n,dsm_shift))-1 )       ;

c_i_ntc(l) = c_inv_overnight_ntc(l) * (inv_interest_ntc(l) * (1 + inv_interest_ntc(l))**(inv_lifetime_ntc(l)) )
                 / ((1 + inv_interest_ntc(l)) ** (inv_lifetime_ntc(l))-1 ) ;

phi_mean_reserves_call_y(n,year,reserves) = sum(h, phi_reserves_call_y(n,year,reserves,h) ) / card(h) + eps ;


theta_sets(n,bu,'setsh')$(smax( (heat_storage,heat_hp,heat_elec,heat_fossil,headers_heat) , heat_data_upload(n,bu,'setsh',heat_storage,heat_hp,heat_elec,heat_fossil,headers_heat)) > 0 AND phi_heat_type(n,bu,'setsh')) = 1;
theta_dir(n,bu,'dir')$(smax((heat_storage,heat_hp,heat_elec,heat_fossil,headers_heat) , heat_data_upload(n,bu,'dir',heat_storage,heat_hp,heat_elec,heat_fossil,headers_heat)) > 0 AND phi_heat_type(n,bu,'dir')) = 1;

theta_storage(n,bu,ch)$(sum((heat_hp,heat_elec,heat_fossil,headers_heat), heat_data_upload(n,bu,ch,'yes',heat_hp,heat_elec,heat_fossil,headers_heat)) AND phi_heat_type(n,bu,ch)) = 1;
theta_hp(n,bu,ch)$sum( (heat_storage,heat_elec,heat_fossil,headers_heat), heat_data_upload(n,bu,ch,heat_storage,'yes',heat_elec,heat_fossil,headers_heat) AND phi_heat_type(n,bu,ch)) = 1;

theta_elec(n,bu,ch)$sum( (heat_storage,heat_hp,heat_fossil,headers_heat), heat_data_upload(n,bu,ch,heat_storage,heat_hp,'yes',heat_fossil,headers_heat) AND phi_heat_type(n,bu,ch)) = 1;
theta_fossil(n,bu,ch)$sum( (heat_storage,heat_hp,heat_elec,headers_heat), heat_data_upload(n,bu,ch,heat_storage,heat_hp,heat_elec,'yes',headers_heat) AND phi_heat_type(n,bu,ch)) = 1;

***************  Adjust costs to model's hourly basis **************************

c_i(n,tech) = c_i(n,tech)*card(h)/8760 ;
c_i_res(n,tech) = c_i_res(n,tech)*card(h)/8760 ;
c_i_sto_p(n,sto) = c_i_sto_p(n,sto)*card(h)/8760 ;
c_i_sto_e(n,sto) = c_i_sto_e(n,sto)*card(h)/8760 ;
c_i_rsvr_e(n,rsvr) = c_i_rsvr_e(n,rsvr)*card(h)/8760 ;
c_i_rsvr_p(n,rsvr) = c_i_rsvr_p(n,rsvr)*card(h)/8760 ;
c_i_dsm_cu(n,dsm_curt) = c_i_dsm_cu(n,dsm_curt)*card(h)/8760 ;
c_i_dsm_shift(n,dsm_shift) = c_i_dsm_shift(n,dsm_shift)*card(h)/8760 ;
c_i_ntc(l) = c_i_ntc(l)*card(h)/8760 ;

c_fix(n,tech) = c_fix(n,tech)*card(h)/8760 ;
c_fix_sto(n,sto) = c_fix_sto(n,sto)*card(h)/8760 ;
c_fix_dsm_cu(n,dsm_curt) = c_fix_dsm_cu(n,dsm_curt)*card(h)/8760 ;
c_fix_dsm_shift(n,dsm_shift) = c_fix_dsm_shift(n,dsm_shift)*card(h)/8760 ;
c_fix_rsvr(n,rsvr) = c_fix_rsvr(n,rsvr)*card(h)/8760 ;

m_e(n,'bio') = m_e(n,'bio')*card(h)/8760 ;

*t_dur_dsm_cu(n,dsm_curt) = t_dur_dsm_cu(n,dsm_curt) ;
*t_off_dsm_cu(n,dsm_curt) = t_off_dsm_cu(n,dsm_curt) ;
*t_dur_dsm_shift(n,dsm_shift)$(ord(dsm_shift)=2 or ord(dsm_shift)=4 or ord(dsm_shift)=5) = t_dur_dsm_shift(n,dsm_shift) / 2 ;
*t_dur_dsm_shift(n,dsm_shift)$(ord(dsm_shift)=1 or ord(dsm_shift)=3) = 2 ;

******  Check for parameter sanity ***********

Parameter
check_heat(n,bu)
check_heat_agg ;
check_heat(n,bu) = sum( ch , phi_heat_type(n,bu,ch)) ;
check_heat_agg = smax( (n,bu) , check_heat(n,bu) ) ;
*abort$(check_heat_agg > 1) "DATA: heating technologies for a building type do not add up to 100 percent" ;

**********  Infeasibility **************

Positive variable
G_INFES(n,h)
;

Parameter
c_infes
;

*************************************
***** Features for nodes ************
*************************************

%DSM%$ontext
m_dsm_cu(n,dsm_curt)$(feat_node('dsm',n) = 0) = 0 ;
m_dsm_shift(n,dsm_shift)$(feat_node('dsm',n) = 0) = 0 ;
$ontext
$offtext

%prosumage%$ontext
m_res_pro(n,res)$(feat_node('prosumage',n) = 0) = 0 ;
m_sto_pro_e(n,sto)$(feat_node('prosumage',n) = 0) = 0 ;
m_sto_pro_p(n,sto)$(feat_node('prosumage',n) = 0) = 0 ;
$ontext
$offtext

phi_rsvr_min(n) = 0 ;

%heat%$ontext
dh(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
d_dhw(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
$ontext
$offtext

**********  Mapping sets **************

Set
map_n_tech(n,tech)
map_n_sto(n,sto)
map_n_rsvr(n,rsvr)
map_n_dsm(n,dsm)
map_n_ev(n,ev)
map_l(l)
map_n_sto_pro(n,sto)
map_n_res_pro(n,tech)
;

map_n_tech(n,tech) = yes$m_p(n,tech) ;
map_n_sto(n,sto) = yes$m_sto_p(n,sto) ;
map_n_rsvr(n,rsvr) = yes$m_rsvr_p(n,rsvr) ;
map_n_dsm(n,dsm_curt) = yes$m_dsm_cu(n,dsm_curt) ;
map_n_dsm(n,dsm_shift) = yes$m_dsm_shift(n,dsm_shift) ;
map_n_ev(n,ev) = yes$phi_ev(n,ev) ;
map_l(l) = yes$m_ntc(l) ;
map_n_sto_pro(n,sto) = yes$(yes$m_sto_pro_p(n,sto)) ;
map_n_res_pro(n,res) = yes$(yes$m_res_pro(n,res)) ;

********************************************************************************

***************************
***** Initialize data *****
***************************

* Parameters for default base year
d(n,h) = d_y(n,%base_year%,h) ;
phi_res(n,res,h) = phi_res_y(n,%base_year%,res,h) ;
rsvr_in(n,rsvr,h) = rsvr_in_y(n,%base_year%,rsvr,h) ;
phi_reserves_call(n,reserves,h) = phi_reserves_call_y(n,%base_year%,reserves,h) ;
phi_mean_reserves_call(n,reserves) = phi_mean_reserves_call_y(n,%base_year%,reserves) ;
reserves_exogenous(n,reserves,h) = reserves_exogenous_y(n,%base_year%,reserves,h) ;
dh(n,bu,ch,h) = dh_y(n,%base_year%,bu,ch,h) ;
d_dhw(n,bu,ch,h) = d_dhw_y(n,%base_year%,bu,ch,h) ;

dh(n,bu,ch,h) = area_floor(n,bu,ch) * dh(n,bu,ch,h) ;
d_dhw(n,bu,ch,h) = area_floor(n,bu,ch) * d_dhw(n,bu,ch,h) ;

* No interconnections between non-adjacent or nonuploaded nodes
m_ntc(l)$( smax(n,inc(l,n)) = 0 OR smin(n,inc(l,n)) = 0 ) = 0 ;


********************************************************************************
********************* Model ****************************************************
********************************************************************************

Variables
Z                Value objective function [Euro]
F(l,h)           Energy flow over link l in hour h [MWh]
;

Positive Variables
G_L(n,tech,h)            Generation level in hour h [MWh]
G_UP(n,tech,h)           Generation upshift in hour h [MWh]
G_DO(n,tech,h)           Generation downshift in hour h [MWh]

G_RES(n,tech,h)          Generation renewables type res in hour h [MWh]
CU(n,tech,h)             Renewables curtailment technology res in hour h [MWh]

STO_IN(n,sto,h)          Storage inflow technology sto hour h [MWh]
STO_OUT(n,sto,h)         Storage outflow technology sto hour h [MWh]
STO_L(n,sto,h)           Storage level technology sto hour h [MWh]

EV_CHARGE(n,ev,h)        Electric vehicle charging vehicle profile ev hour h [MWh]
EV_DISCHARGE(n,ev,h)     Electric vehicle discharging vehicle profile ev hour h [MWh]
EV_L(n,ev,h)             Electric vehicle charging level vehicle profile ev hour h [MWh]
EV_PHEVFUEL(n,ev,h)      Plug in hybrid electric vehicle conventional fuel use vehicle profile ev hour h [MWh]
EV_GED(n,ev,h)           Grid electricity demand for mobility vehicle profile ev hour h [MWh]

N_TECH(n,tech)           Technology tech built [MW]
N_STO_E(n,sto)           Storage technology built - Energy [MWh]
N_STO_P(n,sto)           Storage loading and discharging capacity built - Capacity [MW]

DSM_CU(n,dsm,h)          DSM: Load curtailment hour h [MWh]
DSM_UP(n,dsm,h)          DSM: Load shifting up hour h technology dsm [MWh]
DSM_DO(n,dsm,h,hh)       DSM: Load shifting down in hour hh to account for upshifts in hour h technology dsm [MWh]

DSM_UP_DEMAND(n,dsm,h)   DSM: Load shifting up active for wholesale demand in hour h of technology dsm [MWh]
DSM_DO_DEMAND(n,dsm,h)   DSM: Load shifting down active for wholesale demand in hour h of technology dsm [MWh]

N_DSM_CU(n,dsm)          DSM: Load curtailment capacity [MW]
N_DSM_SHIFT(n,dsm)       DSM: Load shifting capacity [MWh]

RP_DIS(n,reserves,tech,h)        Reserve provision by conventionals in hour h [MW]
RP_NONDIS(n,reserves,tech,h)     Reserve provision by renewables in hour h [MW]
RP_STO_IN(n,reserves,sto,h)      Reserve provision by storage in in hour h [MW]
RP_STO_OUT(n,reserves,sto,h)     Reserve provision by storage out in hour h [MW]
RP_EV_V2G(n,reserves,ev,h)       Reserve provision by electric vehicles V2G hour h [MW]
RP_EV_G2V(n,reserves,ev,h)       Reserve provision by electric vehicles G2V hour h [MW]
RP_DSM_CU(n,reserves,dsm,h)      Reserve provision by DSM load curtailment in hour h [MW]
RP_DSM_SHIFT(n,reserves,dsm,h)   Reserve provision by DSM load shifting in hour h [MW]
RP_RSVR(n,reserves,rsvr,h)       Reserve provision by reservoirs h [MW]
RP_SETS(n,reserves,bu,ch,h)      Reserve provision by SETS [MW]
RP_SETS_AUX(n,reserves,bu,ch,h)  Reserve provision by SETS auxiliary DHW modules [MW]
RP_HP(n,reserves,bu,ch,h)        Reserve provision by heat pumps [MW]
RP_H_ELEC(n,reserves,bu,ch,h)    Reserve provision by hybrid electric heaters [MW]

CU_PRO(n,tech,h)                 Prosumage: curtailment of renewable generation in hour h [MWh]
G_MARKET_PRO2M(n,tech,h)         Prosumage. energy sent to market in hour h [MWh]
G_MARKET_M2PRO(n,h)              Prosumage: withdrawal of energy from market in hour h [MWh]
G_RES_PRO(n,tech,h)              Prosumage: hourly renewables generation in hour h [MWh]
STO_IN_PRO2PRO(n,tech,sto,h)     Prosumage: storage loading from generation for discharging to consumption in hour h [MWh]
STO_IN_PRO2M(n,tech,sto,h)       Prosumage: storage loading from generation for discharging to market in hour h [MWh]
STO_IN_M2PRO(n,sto,h)            Prosumage: storage loading from market for discharging to consumption in hour h [MWh]
STO_IN_M2M(n,sto,h)              Prosumage: storage loading from market for discharging to market in hour h [MWh]
STO_OUT_PRO2PRO(n,sto,h)         Prosumage: storage discharging to consumption from generation in hour h [MWh]
STO_OUT_PRO2M(n,sto,h)           Prosumage: storage discharging to market from generation in hour h [MWh]
STO_OUT_M2PRO(n,sto,h)           Prosumage: storage discharging to consumption from market in hour h [MWh]
STO_OUT_M2M(n,sto,h)             Prosumage: storage discharging to market from market in hour h [MWh]
STO_L_PRO2PRO(n,sto,h)           Prosumage: storage level generation to consumption in hour h [MWh]
STO_L_PRO2M(n,sto,h)             Prosumage: storage level generation to market in hour h [MWh]
STO_L_M2PRO(n,sto,h)             Prosumage: storage level market to consumotion in hour h [MWh]
STO_L_M2M(n,sto,h)               Prosumage: storage level market to market in hour h [MWh]
N_STO_E_PRO(n,sto)               Prosumage: installed storage energy [MWh]
N_STO_P_PRO(n,sto)               Prosumage: installed storage power [MW]
STO_L_PRO(n,sto,h)               Prosumage: overall storage level in hour h [MWh]
N_RES_PRO(n,tech)                Prosumage: installed renewables capacities [MW]

NTC(l)                           Trade: installed NTC on line l [MW]

RSVR_OUT(n,rsvr,h)               Reservoirs: outflow in hour h [MWh]
RSVR_L(n,rsvr,h)                 Reservoirs: level in hour h [MWh]
N_RSVR_E(n,rsvr)                 Reservoirs: installed energy capacity [MWh]
N_RSVR_P(n,rsvr)                 Reservoirs: installed power capacity [MW]

H_DIR(n,bu,ch,h)                 Heating: direct heating in hour h for building type bu with haeting technology ch [MWh]
H_SETS_LEV(n,bu,ch,h)            Heating: storage level SETS technologies [MWh]
H_SETS_IN(n,bu,ch,h)             Heating: storage inflow SETS technologies [MWh]
H_SETS_OUT(n,bu,ch,h)            Heating: storage outflow SETS technologies [MWh]
H_HP_IN(n,bu,ch,hh)              Heating: electricity demand heat pump technologies [MWh]
H_STO_LEV(n,bu,ch,h)             Heating: storage level storage technologies [MWh]
H_STO_IN_HP(n,bu,ch,h)           Heating: storage inflow from heat pumps to storage technologies [MWh]
H_STO_IN_ELECTRIC(n,bu,ch,h)     Heating: storage inflow from electric heating to storage technologies [MWh]
H_ELECTRIC_IN(n,bu,ch,h)         Heating: hybrid electric heaters electricity demand [MWh]
H_STO_IN_FOSSIL(n,bu,ch,h)       Heating: storage inflow from nonelectric heating to storage technologies [MWh]
H_STO_OUT(n,bu,ch,h)             Heating: storage outflow from storage technologies [MWh]

H_DHW_DIR(n,bu,ch,h)             Heating - domestic hot water: provision in case of direct electric heating [MWh]
H_DHW_STO_OUT(n,bu,ch,h)         Heating - domestic hot water: DHW storage outflow [MWh]

H_DHW_AUX_ELEC_IN(n,bu,ch,h)     Heating - domestic hot water: electrical energy input of auxiliary hot water tank for SETS [MWh]
H_DHW_AUX_LEV(n,bu,ch,h)         Heating - domestic hot water: level of auxiliary hot water tank for SETS [MWh]
H_DHW_AUX_OUT(n,bu,ch,h)         Heating - domestic hot water: auxiliary DHW provision for SETS [MWh]

;

********************************************************************************

Equations
* Objective
obj                      Objective cost minimization

* Energy balance
con1a_bal(n,h)                   Energy Balance

* Load change costs
con2a_loadlevel(n,tech,h)        Load change costs: Level
con2b_loadlevelstart(n,tech,h)   Load change costs: Level for first period

* Capacity contraints and flexibility constraints
con3a_maxprod_dispatchable(n,tech,h)            Capacity Constraint conventionals
con3b_minprod_dispatchable(n,tech,h)            Minimum production conventionals if reserves contracted
con3c_flex_reserves_spin(n,tech,reserves,h)     Flexibility of conventionals for reserves provision
con3d_flex_reserves_nonspin(n,tech,reserves,h)  Flexibility of conventionals for reserves provision
con3e_maxprod_res(n,tech,h)                     Capacity constraints renewables
con3f_minprod_res(n,tech,h)                     Minimum production RES if reserves contracted

* Storage constraints
con4a_stolev_start(n,sto,h)      Storage Level Dynamics Initial Condition
con4b_stolev(n,sto,h)            Storage Level Dynamics
con4c_stolev_max(n,sto,h)        Storage Power Capacity
con4d_maxin_sto(n,sto,h)         Storage maximum inflow
con4e_maxout_sto(n,sto,h)        Storage maximum outflow
con4f_resrv_sto(n,sto,h)         Constraint on reserves (up)
con4g_resrv_sto(n,sto,h)         Constraint on reserves (down)
con4h_maxout_lev(n,sto,h)        Maximum storage outflow - no more than level of last period
con4i_maxin_lev(n,sto,h)         Maximum storage inflow - no more than ebergy capacity minus level of last period
con4j_ending(n,sto,h)            End level equal to initial level
con4k_PHS_EtoP(n,sto)            Maximum E to P ratio for PHS

* Minimum restrictions for renewables and biomass and CO2 cap
con5a_minRes_0a(n)               Minimum yearly renewables requirement: G_RES- demand, storage losses and ev demand in proportion to RES share
con5a_minRES_1b(n)          	 Minimum yearly renewables requirement: G_RES- and demand-based, storage losses completely covered by RES
con5a_minRES_2c(n)          	 Minimum yearly renewables requirement: G_RES- and G_TOTAL-based, storage losses covered by RES proportional to (1-phi_min_res)
con5a_minRES_3b(n)          	 Minimum yearly renewables requirement: G_CON- and demand-based, storage losses completely covered by RES
con5a_minRes_4e(n)               Minimum yearly renewables requirement: G_CON- demand, storage losses and ev demand in proportion to RES share
con5b_max_energy(n,tech)     	 Maximum yearly biomass energy
con5c_max_node_CO2(n)            Maximum yearly CO2 cap per node
con5c_max_overall_CO2            Maximum yearly CO2 cap across all nodes


* DSM conditions: Load curtailment
con6a_DSMcurt_duration_max(n,dsm,h)   Maximum curtailment energy budget per time
con6b_DSMcurt_max(n,dsm,h)            Maximum curtailment per period

* DSM conditions: Load shifting
con7a_DSMshift_upanddown(n,dsm,h)     Equalization of upshifts and downshifts in due time
con7b_DSMshift_granular_max(n,dsm,h)  Maximum shifting in either direction per period
con7c_DSM_distrib_up(n,dsm,h)         Distribution of upshifts between wholesale and reserves
con7d_DSM_distrib_do(n,dsm,h)         Distribution of downshifts between wholesale and reserves
con7e_DSMshift_recovery(n,dsm,h)      Recovery times

* Maximum installation conditions
con8a_max_I_power(n,tech)             Maximum installable capacity: Conventionals
con8b_max_I_sto_e(n,sto)              Maximum installable energy: Storage in MWh
con8c_max_I_sto_p(n,sto)              Maximum installable capacity: Storage inflow-outflow in MW
con8d_max_I_dsm_cu(n,dsm)             Maximum installable capacity: DSM load curtailment
con8e_max_I_dsm_shift_pos(n,dsm)      Maximum installable capacity: DSM load shifting
con8f_max_pro_res(n,tech)             Maximum installable capacity: prosumage renewables
con8g_max_pro_sto_e(n,sto)            Maximum installable capacity: prosumage storage energy
con8h_max_sto_pro_p(n,sto)            Maximum installable capacity: prosumage storage power
con8i_max_I_ntc(l)                    Maximum installable NTC
con8j_max_I_rsvr_e(n,rsvr)            Maximum installable energy reservoirs
con8k_max_I_rsvr_p(n,rsvr)            Maximum installable power reservoirs

* Reserves
con9a_reserve_prov_exogenous(n,reserves,h)      Reserve provision SR and MR (exogenous reserve provision)
con9b_reserve_prov_PR_exogenous(n,reserves,h)   Reserve provision PR (exogenous reserve provision)

* Electric vehicles
con10a_ev_ed(n,ev,h)                  Energy balance of electric vehicles
con10b_ev_chargelev_start(n,ev,h)     Cumulative charging level in the first hour
con10c_ev_chargelev(n,ev,h)           Cumulative charging level in hour h
con10d_ev_chargelev_max(n,ev,h)       Cumulative maximal charging level
con10e_ev_maxin(n,ev,h)               Cumulative maximal charging power
con10f_ev_maxout(n,ev,h)              Cumulative maximal discharging power
con10g_ev_chargelev_ending(n,ev,h)    Cumulative charging level in the last hour
con10h_ev_minin(n,ev,h)               Cumulative minimal charging power
con10i_ev_maxin_lev(n,ev,h)           Cumulative maximal charging limit
con10j_ev_minout(n,ev,h)              Cumulative minimal discharging power
con10k_ev_maxout_lev(n,ev,h)          Cumulative maximal discharging limit
con10l_ev_exog(n,ev,h)                Exogenous EV charging

* Prosumage
con11a_pro_distrib(n,tech,h)                    Prosumage: distribution of generated energy
con11b_pro_balance(n,h)                         Prosumage: energy balance
con11c_pro_selfcon(n)                           Prosumage: minimum self-generation requirement
con11d_pro_stolev_PRO2PRO(n,sto,h)              Prosumage: storage level prosumager-to-prosumagers
con11e_pro_stolev_PRO2M(n,sto,h)                Prosumage: storage level prosumagers-to-market
con11f_pro_stolev_M2PRO(n,sto,h)                Prosumage: storage level market-to-prosumagers
con11g_pro_stolev_M2M(n,sto,h)                  Prosumage: storage level market-to-market
con11h_1_pro_stolev_start_PRO2PRO(n,sto,h)      Prosumage: storage level initial conditions
con11h_2_pro_stolev_start_PRO2M(n,sto,h)        Prosumage: storage level initial conditions
con11h_3_pro_stolev_start_M2PRO(n,sto,h)        Prosumage: storage level initial conditions
con11h_4_pro_stolev_start_M2M(n,sto,h)          Prosumage: storage level initial conditions
con11i_pro_stolev(n,sto,h)                      Prosumage: storage level total
con11j_pro_stolev_max(n,sto,h)                  Prosumage: maximum overall storage level
con11k_pro_maxin_sto(n,sto,h)                   Prosumage: maximum storage inflow
con11l_pro_maxout_sto(n,sto,h)                  Prosumage: maximum storage outflow
con11m_pro_maxout_lev(n,sto,h)                  Prosumage: maximum storage outflow linked to level
con11n_pro_maxin_lev(n,sto,h)                   Prosumage: maximum storage inflow linked to level
con11o_pro_ending(n,sto,h)                      Prosumage: storage ending condition

* Cross-nodal trade
con12a_max_f(l,h)                Maximum energy flow limited to positive NTC
con12b_min_f(l,h)                Minimum energy flow limited to negative NTC

* Resevoirs
con13a_rsvrlev_start(n,rsvr,h)   Reservoir level law of motion initial condition
con13b_rsvrlev(n,rsvr,h)         Reservoir level law of motion
con13c_rsvrlev_max(n,rsvr,h)     Maximum reservoir energy level
con13d_maxout_rsvr(n,rsvr,h)     Maximum hourly reservoir outflow in relation to installed power capacity
con13d2_minout_rsvr(n,rsvr,h)
con13e_resrv_rsvr(n,rsvr,h)      Minimum hourly reservoir outflow in relation to provided negativr reserves
con13f_maxout_lev(n,rsvr,h)      Maximum hourly reservoir outflow in relation tom installed energy capacity
con13g_ending(n,rsvr,h)          Reservoir level law of motion ending condition
con13h_smooth(n,rsvr,h)          Smooth reservoir outflow
con13i_min_level(n,rsvr,h)       Reservoir minimum level
con13j_min_FLH(n,rsvr)

* Residential heat
con14a_heat_balance(n,bu,ch,h)                  Space heating energy balance
con14b_dhw_balance(n,bu,ch,h)                   Domestic hot water energy balance
con14c_sets_level(n,bu,ch,h)                    SETS - level law of motion
con14d_sets_level_start(n,bu,ch,h)              SETS - storage level initial condition
con14e_sets_maxin(n,bu,ch,h)                    SETS - maximum energy inflow
con14f_sets_maxout(n,bu,ch,h)                   SETS - maximum energy outflow
con14g_sets_minin(n,bu,ch,h)                    SETS - minimum energy inflow if reserves contracted
con14h_sets_maxlev(n,bu,ch,h)                   SETS - maximum storage level
con14i_sets_aux_dhw_level(n,bu,ch,h)            SETS auxiliary DHW module - storage level law of motion
con14j_sets_aux_dhw_level_start(n,bu,ch,h)      SETS auxiliary DHW module - storage level initial consition
con14k_sets_aux_dhw_maxin(n,bu,ch,h)            SETS auxiliary DHW module - maximum energy inflow
con14l_sets_aux_dhw_minin(n,bu,ch,h)            SETS auxiliary DHW module - minimum energy inflow if reserves contracted
con14m_sets_aux_dhw_maxlev(n,bu,ch,h)           SETS auxiliary DHW module - maximum storage level
con14n_hp_in(n,bu,ch,h)                         Heat pumps - electricity demand
con14o_hp_maxin(n,bu,ch,h)                      Heat pumps - maximum electricity demand
con14p_hp_minin(n,bu,ch,h)                      Heat pumps - minimum electricity demand if reserves contracted
con14q_storage_elec_in(n,bu,ch,h)               Hybrid electric heating - electricity demand
con14r_storage_elec_maxin(n,bu,ch,h)            Hybrid electric heating - maximum electricity demand
con14s_storage_elec_minin(n,bu,ch,h)            Hybrid electric heating - minimum electricity demand if reserves contracted
con14t_storage_level(n,bu,ch,h)                 Storage heating - level law of motion
con14u_storage_level_start(n,bu,ch,h)           Hybrid electric heating - storage level initial condition
con14v_storage_maxlev(n,bu,ch,h)                Hybrid electric heating - maximum storage level
;

********************************************************************************

* ---------------------------------------------------------------------------- *
***** Objective function *****
* ---------------------------------------------------------------------------- *

obj..
         Z =E=
                   sum( (h,map_n_tech(n,dis)) , c_m(n,dis)*G_L(n,dis,h) )
                 + sum( (h,map_n_tech(n,dis))$(ord(h)>1) , c_up(n,dis)*G_UP(n,dis,h) )
                 + sum( (h,map_n_tech(n,dis)) , c_do(n,dis)*G_DO(n,dis,h) )
                 + sum( (h,map_n_tech(n,nondis)) , c_cu(n,nondis)*CU(n,nondis,h) )
                 + sum( (h,map_n_sto(n,sto)) , c_m_sto(n,sto) * ( STO_OUT(n,sto,h) + STO_IN(n,sto,h) ) )
%DSM%$ontext
                 + sum( (h,map_n_dsm(n,dsm_curt)) , c_m_dsm_cu(n,dsm_curt)*DSM_CU(n,dsm_curt,h) )
                 + sum( (h,map_n_dsm(n,dsm_shift)) , c_m_dsm_shift(n,dsm_shift) * DSM_UP_DEMAND(n,dsm_shift,h) )
                 + sum( (h,map_n_dsm(n,dsm_shift)) , c_m_dsm_shift(n,dsm_shift) * DSM_DO_DEMAND(n,dsm_shift,h) )
$ontext
$offtext
%EV_endogenous%$ontext
                 + sum( (h,map_n_ev(n,ev)) , c_m_ev(n,ev) * EV_DISCHARGE(n,ev,h) )
                 + sum( (h,map_n_ev(n,ev)) , pen_phevfuel(n,ev) * EV_PHEVFUEL(n,ev,h) )
$ontext
$offtext
                 + sum( map_n_tech(n,tech) , c_i(n,tech)*N_TECH(n,tech) )
                 + sum( map_n_tech(n,tech) , c_fix(n,tech)*N_TECH(n,tech) )
                 + sum( map_n_sto(n,sto) , c_i_sto_e(n,sto)*N_STO_E(n,sto) )
                 + sum( map_n_sto(n,sto) , c_fix_sto(n,sto)/2*(N_STO_P(n,sto)+N_STO_E(n,sto)) )
                 + sum( map_n_sto(n,sto) , c_i_sto_p(n,sto)*N_STO_P(n,sto) )
%DSM%$ontext
                 + sum( map_n_dsm(n,dsm_curt) , c_i_dsm_cu(n,dsm_curt)*N_DSM_CU(n,dsm_curt) )
                 + sum( map_n_dsm(n,dsm_curt) , c_fix_dsm_cu(n,dsm_curt)*N_DSM_CU(n,dsm_curt) )
                 + sum( map_n_dsm(n,dsm_shift) , c_i_dsm_shift(n,dsm_shift)*N_DSM_SHIFT(n,dsm_shift) )
                 + sum( map_n_dsm(n,dsm_shift) , c_fix_dsm_shift(n,dsm_shift)*N_DSM_SHIFT(n,dsm_shift) )
$ontext
$offtext
%reserves%$ontext
                 + sum( (h,map_n_sto(n,sto),reserves_up) , phi_reserves_call(n,reserves_up,h) * c_m_sto(n,sto) * (RP_STO_OUT(n,reserves_up,sto,h) - RP_STO_IN(n,reserves_up,sto,h)) )
                 - sum( (h,map_n_sto(n,sto),reserves_do) , phi_reserves_call(n,reserves_do,h) * c_m_sto(n,sto) * (RP_STO_OUT(n,reserves_do,sto,h) - RP_STO_IN(n,reserves_do,sto,h)) )
                 + sum( (h,map_n_rsvr(n,rsvr),reserves_up) , RP_RSVR(n,reserves_up,rsvr,h) * phi_reserves_call(n,reserves_up,h) * c_m_rsvr(n,rsvr) )
                 - sum( (h,map_n_rsvr(n,rsvr),reserves_do) , RP_RSVR(n,reserves_do,rsvr,h) * phi_reserves_call(n,reserves_do,h) * c_m_rsvr(n,rsvr) )
$ontext
$offtext
%reserves%$ontext
%EV_endogenous%$ontext
%EV_exogenous%        + sum( (h,map_n_ev(n,ev),reserves_up) , RP_EV_V2G(n,reserves_up,ev,h) * phi_reserves_call(n,reserves_up,h) * c_m_ev(n,ev) )
%EV_exogenous%        - sum( (h,map_n_ev(n,ev),reserves_do) , RP_EV_V2G(n,reserves_do,ev,h) * phi_reserves_call(n,reserves_do,h) * c_m_ev(n,ev) )
$ontext
$offtext
%DSM%$ontext
%reserves%$ontext
                 + sum( (h,map_n_dsm(n,dsm_curt),reserves_up) , RP_DSM_CU(n,reserves_up,dsm_curt,h) * phi_reserves_call(n,reserves_up,h) * c_m_dsm_cu(n,dsm_curt) )
                 + sum( (h,map_n_dsm(n,dsm_shift),reserves) , RP_DSM_SHIFT(n,reserves,dsm_shift,h) * phi_reserves_call(n,reserves,h) * c_m_dsm_shift(n,dsm_shift) )
$ontext
$offtext
%prosumage%$ontext
                 + sum( map_n_res_pro(n,res) , c_i(n,res)*N_RES_PRO(n,res) )
                 + sum( map_n_res_pro(n,res) , c_fix(n,res)*N_RES_PRO(n,res) )

                 + sum( map_n_sto_pro(n,sto) , c_i_sto_e(n,sto)*N_STO_E_PRO(n,sto) )
                 + sum( map_n_sto_pro(n,sto) , c_fix_sto(n,sto)/2*(N_STO_P_PRO(n,sto) + N_STO_E_PRO(n,sto)) )
                 + sum( map_n_sto_pro(n,sto) , c_i_sto_p(n,sto)*N_STO_P_PRO(n,sto) )

                 + sum( (h,map_n_sto_pro(n,sto)) , c_m_sto(n,sto) * ( STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_M2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h) + STO_OUT_M2M(n,sto,h) + sum( res , STO_IN_PRO2PRO(n,res,sto,h) + STO_IN_PRO2M(n,res,sto,h)) + STO_OUT_PRO2M(n,sto,h) + STO_OUT_M2M(n,sto,h) ) )
$ontext
$offtext
                 + sum( map_l(l) , c_i_ntc(l) * NTC(l)*dist(l) )

                 + sum( (h,map_n_rsvr(n,rsvr)), c_m_rsvr(n,rsvr) * RSVR_OUT(n,rsvr,h) )
                 + sum( map_n_rsvr(n,rsvr) , c_i_rsvr_e(n,rsvr) * N_RSVR_E(n,rsvr) )
                 + sum( map_n_rsvr(n,rsvr) , c_i_rsvr_p(n,rsvr) * N_RSVR_P(n,rsvr) )
                 + sum( map_n_rsvr(n,rsvr) , c_fix_rsvr(n,rsvr) * N_RSVR_P(n,rsvr) )
%heat%$ontext
                 + sum( (h,n,bu,hfo) , pen_heat_fuel(n,bu,hfo) * H_STO_IN_FOSSIL(n,bu,hfo,h))
$ontext
$offtext
                 + sum( (h,n) , c_infes * G_INFES(n,h) )
;

* ---------------------------------------------------------------------------- *
***** Energy balance and load levels *****
* ---------------------------------------------------------------------------- *

* Energy balance
con1a_bal(n,hh)..
         ( 1 - phi_pro_load(n) ) * d(n,hh) + sum( map_n_sto(n,sto) , STO_IN(n,sto,hh) )
%DSM%$ontext
         + sum( map_n_dsm(n,dsm_shift) , DSM_UP_DEMAND(n,dsm_shift,hh) )
$ontext
$offtext
%EV_endogenous%$ontext
         + sum( map_n_ev(n,ev) , EV_CHARGE(n,ev,hh) )
$ontext
$offtext
%prosumage%$ontext
         + G_MARKET_M2PRO(n,hh)
         + sum( map_n_sto_pro(n,sto) , STO_IN_M2PRO(n,sto,hh))
         + sum( map_n_sto_pro(n,sto) , STO_IN_M2M(n,sto,hh))
$ontext
$offtext
%heat%$ontext
        + sum( (bu,ch) , theta_dir(n,bu,ch) * (H_DIR(n,bu,ch,hh) + H_DHW_DIR(n,bu,ch,hh)) )
        + sum( (bu,ch) , theta_sets(n,bu,ch) * (H_SETS_IN(n,bu,ch,hh) + H_DHW_AUX_ELEC_IN(n,bu,ch,hh)) )
        + sum( (bu,hp) , theta_hp(n,bu,hp) * H_HP_IN(n,bu,hp,hh) )
        + sum( (bu,hel) , theta_elec(n,bu,hel) * H_ELECTRIC_IN(n,bu,hel,hh) )
$ontext
$offtext
         =E=
         sum( map_n_tech(n,dis) , G_L(n,dis,hh)) + sum( map_n_tech(n,nondis) , G_RES(n,nondis,hh)) + sum( sto , STO_OUT(n,sto,hh) ) + sum( map_n_rsvr(n,rsvr) , RSVR_OUT(n,rsvr,hh))
         + sum( map_l(l) , inc(l,n) * F(l,hh))
%reserves%$ontext
*Balancing Correction Factor
        + sum( map_n_tech(n,dis) ,
          sum( reserves_do ,  RP_DIS(n,reserves_do,dis,hh) * phi_reserves_call(n,reserves_do,hh))
        - sum( reserves_up ,  RP_DIS(n,reserves_up,dis,hh) * phi_reserves_call(n,reserves_up,hh))
         )
$ontext
$offtext
%DSM%$ontext
         + sum( map_n_dsm(n,dsm_curt) , DSM_CU(n,dsm_curt,hh))
         + sum( map_n_dsm(n,dsm_shift) , DSM_DO_DEMAND(n,dsm_shift,hh))
$ontext
$offtext
%EV_endogenous%$ontext
        + sum( map_n_ev(n,ev) , EV_DISCHARGE(n,ev,hh) )
$ontext
$offtext
%prosumage%$ontext
         + sum( map_n_res_pro(n,res) , G_MARKET_PRO2M(n,res,hh) )
         + sum( map_n_sto_pro(n,sto) , STO_OUT_PRO2M(n,sto,hh))
         + sum( map_n_sto_pro(n,sto) , STO_OUT_M2M(n,sto,hh))
$ontext
$offtext
         + G_INFES(n,hh)
;

con2a_loadlevel(n,dis,h)$(ord(h) > 1 AND map_n_tech(n,dis))..
        G_L(n,dis,h) =E= G_L(n,dis,h-1) + G_UP(n,dis,h) - G_DO(n,dis,h)
;

con2b_loadlevelstart(n,dis,h)$(ord(h) = 1 AND map_n_tech(n,dis))..
         G_L(n,dis,h) =E= G_UP(n,dis,h)
;

* ---------------------------------------------------------------------------- *
***** Hourly maximum generation caps and constraints related to reserves   *****
* ---------------------------------------------------------------------------- *

con3a_maxprod_dispatchable(n,dis,h)$(map_n_tech(n,dis))..
        G_L(n,dis,h)
%reserves%$ontext
        + sum( reserves_up , RP_DIS(n,reserves_up,dis,h))
*Balancing Correction Factor
        + sum( reserves_do ,  RP_DIS(n,reserves_do,dis,h) * phi_reserves_call(n,reserves_do,h))
        - sum( reserves_up ,  RP_DIS(n,reserves_up,dis,h) * phi_reserves_call(n,reserves_up,h))
$ontext
$offtext
        =L= N_TECH(n,dis)
;

con3b_minprod_dispatchable(n,dis,h)$(map_n_tech(n,dis))..
        sum( reserves_do , RP_DIS(n,reserves_do,dis,h))
        =L= G_L(n,dis,h)
* Balancing Correction Factor
        + sum( reserves_do ,  RP_DIS(n,reserves_do,dis,h) * phi_reserves_call(n,reserves_do,h))
        - sum( reserves_up ,  RP_DIS(n,reserves_up,dis,h) * phi_reserves_call(n,reserves_up,h))
;

con3c_flex_reserves_spin(n,dis,reserves_spin,h)$(map_n_tech(n,dis))..
        RP_DIS(n,reserves_spin,dis,h)
        =L= grad_per_min(n,dis) * reserves_reaction(n,reserves_spin) * ( G_L(n,dis,h)
* Balancing Correction Factor
        + sum( reserves_do ,  RP_DIS(n,reserves_do,dis,h) * phi_reserves_call(n,reserves_do,h))
        - sum( reserves_up ,  RP_DIS(n,reserves_up,dis,h) * phi_reserves_call(n,reserves_up,h)) )
;

con3d_flex_reserves_nonspin(n,dis,reserves_nonspin,h)$(map_n_tech(n,dis))..
        RP_DIS(n,reserves_nonspin,dis,h)
        =L= grad_per_min(n,dis) * reserves_reaction(n,reserves_nonspin) * N_TECH(n,dis)
;

con3e_maxprod_res(n,nondis,h)$(map_n_tech(n,nondis))..
        G_RES(n,nondis,h) + CU(n,nondis,h)
%reserves%$ontext
        + sum( reserves_up , RP_NONDIS(n,reserves_up,nondis,h))
$ontext
$offtext
        =E= phi_res(n,nondis,h) * N_TECH(n,nondis)
;

con3f_minprod_res(n,nondis,h)$(map_n_tech(n,nondis))..
        sum( reserves_do , RP_NONDIS(n,reserves_do,nondis,h))
        =L= G_RES(n,nondis,h)
;

* ---------------------------------------------------------------------------- *
***** Storage constraints *****
* ---------------------------------------------------------------------------- *

con4a_stolev_start(n,sto,h)$(map_n_sto(n,sto) AND ord(h) = 1)..
        STO_L(n,sto,h) =E= phi_sto_ini(n,sto) * N_STO_E(n,sto) + STO_IN(n,sto,h)*eta_sto(n,sto) - STO_OUT(n,sto,h)/eta_sto(n,sto)
;

con4b_stolev(n,sto,h)$((ord(h)>1) AND map_n_sto(n,sto))..
         STO_L(n,sto,h) =E= STO_L(n,sto,h-1) + STO_IN(n,sto,h)*eta_sto(n,sto) - STO_OUT(n,sto,h)/eta_sto(n,sto)
%reserves%$ontext
         + sum( reserves_do , phi_reserves_call(n,reserves_do,h) * ( RP_STO_IN(n,reserves_do,sto,h)*eta_sto(n,sto) + RP_STO_OUT(n,reserves_do,sto,h)/eta_sto(n,sto) ))
         - sum( reserves_up , phi_reserves_call(n,reserves_up,h) * ( RP_STO_IN(n,reserves_up,sto,h)*eta_sto(n,sto) + RP_STO_OUT(n,reserves_up,sto,h)/eta_sto(n,sto) ))
$ontext
$offtext
;

con4c_stolev_max(n,sto,h)$(map_n_sto(n,sto))..
        STO_L(n,sto,h) =L= N_STO_E(n,sto)
;

con4d_maxin_sto(n,sto,h)$(map_n_sto(n,sto))..
        STO_IN(n,sto,h)
%reserves%$ontext
        + sum( reserves_do , RP_STO_IN(n,reserves_do,sto,h))
$ontext
$offtext
        =L= N_STO_P(n,sto)
;

con4e_maxout_sto(n,sto,h)$(map_n_sto(n,sto))..
        STO_OUT(n,sto,h)
%reserves%$ontext
        + sum( reserves_up , RP_STO_OUT(n,reserves_up,sto,h))
$ontext
$offtext
        =L= N_STO_P(n,sto)
;

con4f_resrv_sto(n,sto,h)$(map_n_sto(n,sto))..
        sum( reserves_up , RP_STO_IN(n,reserves_up,sto,h))
        =L= STO_IN(n,sto,h)
;

con4g_resrv_sto(n,sto,h)$(map_n_sto(n,sto))..
        sum( reserves_do , RP_STO_OUT(n,reserves_do,sto,h))
        =L= STO_OUT(n,sto,h)
;

con4h_maxout_lev(n,sto,h)$(map_n_sto(n,sto))..
        ( STO_OUT(n,sto,h)
%reserves%$ontext
        + sum( reserves_up , RP_STO_OUT(n,reserves_up,sto,h))
$ontext
$offtext
        ) /eta_sto(n,sto)
        =L= STO_L(n,sto,h-1)
;

con4i_maxin_lev(n,sto,h)$(map_n_sto(n,sto))..
        ( STO_IN(n,sto,h)
%reserves%$ontext
        + sum( reserves_do , RP_STO_IN(n,reserves_do,sto,h))
$ontext
$offtext
        ) * eta_sto(n,sto)
        =L= N_STO_E(n,sto) - STO_L(n,sto,h-1)
;

con4j_ending(n,sto,h)$(ord(h) = card(h) AND map_n_sto(n,sto))..
         STO_L(n,sto,h) =E= phi_sto_ini(n,sto) * N_STO_E(n,sto)
;

con4k_PHS_EtoP(n,sto)$(map_n_sto(n,sto))..
        N_STO_E(n,sto) =L= etop_max(n,sto) * N_STO_P(n,sto)
;

* ---------------------------------------------------------------------------- *
***** Quotas for renewables and biomass, CO2 cap *****
* ---------------------------------------------------------------------------- *

con5a_minRes_0a(n)..
* demand (load + ev) and losses (storage + ev battery) are fulfilled with the minRES share
        sum( h ,
        + sum( map_n_tech(n,res), sum( dis$(sameas(res,dis)), G_L(n,dis,h)))
        + sum( map_n_tech(n,nondis), G_RES(n,nondis,h))
        + sum( map_n_rsvr(n,rsvr), RSVR_OUT(n,rsvr,h))
%reserves%$ontext
         - sum( reserves_do , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_do,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_do,rsvr,h))) * phi_reserves_call(n,reserves_do,h))
         + sum( reserves_up , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_up,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_up,rsvr,h))) * phi_reserves_call(n,reserves_up,h))
$ontext
$offtext
%prosumage%$ontext
         + sum( map_n_sto_pro(n,sto) , STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h)) + sum( map_n_res_pro(n,res) , G_MARKET_PRO2M(n,res,h) + G_RES_PRO(n,res,h))
$ontext
$offtext

        )
        =G= phi_min_res * phi_min_res_exog(n) * sum( h ,
        + d(n,h)
        + sum( map_n_sto(n,sto) , STO_IN(n,sto,h) - STO_OUT(n,sto,h))
%EV_endogenous%$ontext
        + sum( map_n_ev(n,ev), EV_CHARGE(n,ev,h) - EV_DISCHARGE(n,ev,h))
$ontext
$offtext
        )
;

* RES share constraint (1b): G_RES-and demand-based, storage losses completely covered by RES (original implementation)
con5a_minRES_1b(n)..
         sum( h , G_L(n,'bio',h) + sum( map_n_tech(n,nondis) , G_RES(n,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RSVR_OUT(n,rsvr,h))
%reserves%$ontext
         - sum( reserves_do , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_do,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_do,rsvr,h))) * phi_reserves_call(n,reserves_do,h))
         + sum( reserves_up , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_up,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_up,rsvr,h))) * phi_reserves_call(n,reserves_up,h))
$ontext
$offtext
%prosumage%$ontext
         + sum( map_n_sto_pro(n,sto) , STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h)) + sum( map_n_res_pro(n,res) , G_MARKET_PRO2M(n,res,h) + G_RES_PRO(n,res,h))
$ontext
$offtext
)
        =G= phi_min_res * phi_min_res_exog(n) * sum( h , d(n,h) )
         + sum( h, sum( map_n_sto(n,sto) , STO_IN(n,sto,h) - STO_OUT(n,sto,h) ) )
;

* RES share constraint (2c): G_RES- and total-generation-based, storage losses covered by RES proportional to (1-phi_min_res)
con5a_minRES_2c(n)..
        sum( h , G_L(n,'bio',h) + sum( map_n_tech(n,nondis) , G_RES(n,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RSVR_OUT(n,rsvr,h))
%reserves%$ontext
        - sum( reserves_do , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_do,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_do,rsvr,h))) * phi_reserves_call(n,reserves_do,h))
        + sum( reserves_up , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_up,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_up,rsvr,h))) * phi_reserves_call(n,reserves_up,h))
$ontext
$offtext
%prosumage%$ontext
        + sum( map_n_sto_pro(n,sto) , STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h)) + sum( map_n_res_pro(n,res) , G_MARKET_PRO2M(n,res,h) + G_RES_PRO(n,res,h))
$ontext
$offtext
        )
        =G= phi_min_res * phi_min_res_exog(n) * sum( h ,
        sum( map_n_tech(n,dis) , G_L(n,dis,h)) + sum( map_n_tech(n,nondis) , G_RES(n,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RSVR_OUT(n,rsvr,h))
%reserves%$ontext
        - sum( reserves_do , ( sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_do,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_do,rsvr,h))) * phi_reserves_call(n,reserves_do,h))
        + sum( reserves_up , ( sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_up,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_up,rsvr,h))) * phi_reserves_call(n,reserves_up,h))
$ontext
$offtext
%prosumage%$ontext
        + sum( map_n_res_pro(n,res) , phi_res(n,res,h) * N_RES_PRO(n,res) - CU_PRO(n,res,h))
$ontext
$offtext
         )
         + (1 - phi_min_res * phi_min_res_exog(n)) * sum( (sto,h), STO_IN(n,sto,h) - STO_OUT(n,sto,h) )
;


* RES share constraint (3b): G_CON- and demand-based, storage losses completely covered by RES
con5a_minRES_3b(n)..
        sum(h, sum( map_n_tech(n,con) , G_L(n,con,h))
%reserves%$ontext
        - sum( reserves_do , sum( map_n_tech(n,con) , RP_NONDIS(n,reserves_do,con,h)) * phi_reserves_call(n,reserves_do,h))
        + sum( reserves_up , sum( map_n_tech(n,con) , RP_NONDIS(n,reserves_up,con,h)) * phi_reserves_call(n,reserves_up,h))
$ontext
$offtext
*%prosumage%$ontext
*        conventional prosumage?
*$ontext
*$offtext
        )
        =L= (1-phi_min_res * phi_min_res_exog(n)) * sum( h, d(n,h) )
;

con5a_minRes_4e(n)..
* demand (load + ev) and losses (storage + ev battery) are fulfilled with the minRES share
        sum( h , sum(map_n_tech(n,con), sum( dis$(sameas(con,dis)) , G_L(n,dis,h)))
%reserves%$ontext
        - sum( reserves_do , sum( map_n_tech(n,con) , RP_NONDIS(n,reserves_do,con,h)) * phi_reserves_call(n,reserves_do,h))
        + sum( reserves_up , sum( map_n_tech(n,con) , RP_NONDIS(n,reserves_up,con,h)) * phi_reserves_call(n,reserves_up,h))
$ontext
$offtext
%prosumage%$ontext
         + sum( map_n_sto_pro(n,sto) , STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h)) + sum( map_n_res_pro(n,res) , G_MARKET_PRO2M(n,res,h) + G_RES_PRO(n,res,h))
$ontext
$offtext
        )
        =L= (1-phi_min_res * phi_min_res_exog(n)) * sum( h ,
        + d(n,h)
        + sum( map_n_sto(n,sto) , STO_IN(n,sto,h) - STO_OUT(n,sto,h))
%EV_endogenous%$ontext
        + sum( map_n_ev(n,ev), EV_CHARGE(n,ev,h) - EV_DISCHARGE(n,ev,h))
$ontext
$offtext
        )
;


con5b_max_energy(n,dis)$(map_n_tech(n,dis) AND m_e(n,dis))..
         sum( h , G_L(n,dis,h) ) =L= m_e(n,dis)
;

con5c_max_node_CO2(n)..
         sum( (dis,h) , carbon_content(n,dis)/eta(n,dis) * G_L(n,dis,h)$(map_n_tech(n,dis)) ) =L= co2_cap_exog(n) * 1000000
;

con5c_max_overall_CO2..
         sum( (dis,h,n) , carbon_content(n,dis)/eta(n,dis) * G_L(n,dis,h)$(map_n_tech(n,dis)) ) =L= co2_cap * 1000000
;
* ---------------------------------------------------------------------------- *
***** DSM constraints - curtailment *****
* ---------------------------------------------------------------------------- *

con6a_DSMcurt_duration_max(n,dsm_curt,h)$(map_n_dsm(n,dsm_curt))..
         sum( hh$( ord(hh) >= ord(h) AND ord(hh) < ord(h) + t_off_dsm_cu(n,dsm_curt) ) , DSM_CU(n,dsm_curt,hh)
%reserves%$ontext
        + sum( reserves_up , RP_DSM_CU(n,reserves_up,dsm_curt,hh) * phi_reserves_call(n,reserves_up,hh) )
$ontext
$offtext
         )
         =L= N_DSM_CU(n,dsm_curt) * t_dur_dsm_cu(n,dsm_curt)
;

con6b_DSMcurt_max(n,dsm_curt,h)$(map_n_dsm(n,dsm_curt))..
        DSM_CU(n,dsm_curt,h)
%reserves%$ontext
        + sum( reserves_up , RP_DSM_CU(n,reserves_up,dsm_curt,h) )
$ontext
$offtext
          =L= N_DSM_CU(n,dsm_curt)
;

* ---------------------------------------------------------------------------- *
***** DSM constraints - shifting *****
* ---------------------------------------------------------------------------- *

con7a_DSMshift_upanddown(n,dsm_shift,h)$(map_n_dsm(n,dsm_shift))..
         DSM_UP(n,dsm_shift,h) * (1 + eta_dsm_shift(n,dsm_shift))/2 =E= 2/(1+eta_dsm_shift(n,dsm_shift)) * sum( hh$( ord(hh) >= ord(h) - t_dur_dsm_shift(n,dsm_shift) AND ord(hh) <= ord(h) + t_dur_dsm_shift(n,dsm_shift) ) , DSM_DO(n,dsm_shift,h,hh))
;

con7b_DSMshift_granular_max(n,dsm_shift,h)$(map_n_dsm(n,dsm_shift))..
         DSM_UP_DEMAND(n,dsm_shift,h) + DSM_DO_DEMAND(n,dsm_shift,h)
%reserves%$ontext
         + sum( reserves , RP_DSM_SHIFT(n,reserves,dsm_shift,h) )
$ontext
$offtext
         =L= N_DSM_SHIFT(n,dsm_shift)
;

con7c_DSM_distrib_up(n,dsm_shift,h)$(map_n_dsm(n,dsm_shift))..
         DSM_UP(n,dsm_shift,h) =E= DSM_UP_DEMAND(n,dsm_shift,h)
%reserves%$ontext
         + sum( reserves_do , RP_DSM_SHIFT(n,reserves_do,dsm_shift,h) * phi_reserves_call(n,reserves_do,h))
$ontext
$offtext
;

con7d_DSM_distrib_do(n,dsm_shift,h)$(map_n_dsm(n,dsm_shift))..
         sum( hh$( ord(hh) >= ord(h) - t_dur_dsm_shift(n,dsm_shift) AND ord(hh) <= ord(h) + t_dur_dsm_shift(n,dsm_shift) ) , DSM_DO(n,dsm_shift,hh,h) )
                 =E=
         DSM_DO_DEMAND(n,dsm_shift,h)
%reserves%$ontext
         + sum( reserves_up , RP_DSM_SHIFT(n,reserves_up,dsm_shift,h) * phi_reserves_call(n,reserves_up,h))
$ontext
$offtext
;

con7e_DSMshift_recovery(n,dsm_shift,h)$(map_n_dsm(n,dsm_shift))..
         sum( hh$( ord(hh) >= ord(h) AND ord(hh) < ord(h) + t_off_dsm_shift(n,dsm_shift) ) , DSM_UP(n,dsm_shift,hh))
         =L= N_DSM_SHIFT(n,dsm_shift) * t_dur_dsm_shift(n,dsm_shift)
;

* ---------------------------------------------------------------------------- *
***** Maximum installation constraints *****
* ---------------------------------------------------------------------------- *

con8a_max_I_power(n,tech)$(map_n_tech(n,tech))..
         N_TECH(n,tech) =L= m_p(n,tech)
;

con8b_max_I_sto_e(n,sto)$(map_n_sto(n,sto))..
         N_STO_E(n,sto) =L= m_sto_e(n,sto)
;

con8c_max_I_sto_p(n,sto)$(map_n_sto(n,sto))..
         N_STO_P(n,sto) =L= m_sto_p(n,sto)
;

con8d_max_I_dsm_cu(n,dsm_curt)$(map_n_dsm(n,dsm_curt))..
         N_DSM_CU(n,dsm_curt) =L= m_dsm_cu(n,dsm_curt)
;

con8e_max_I_dsm_shift_pos(n,dsm_shift)$(map_n_dsm(n,dsm_shift))..
         N_DSM_SHIFT(n,dsm_shift) =L= m_dsm_shift(n,dsm_shift)
;

con8f_max_pro_res(n,res)$(map_n_res_pro(n,res))..
         N_RES_PRO(n,res) =L= m_res_pro(n,res)
;

con8g_max_pro_sto_e(n,sto)$(map_n_sto_pro(n,sto))..
         N_STO_E_PRO(n,sto) =L= m_sto_pro_e(n,sto)
;

con8h_max_sto_pro_p(n,sto)$(map_n_sto_pro(n,sto))..
         N_STO_P_PRO(n,sto) =L= m_sto_pro_p(n,sto)
;

con8i_max_I_ntc(l)$(map_l(l))..
         NTC(l) =L= m_ntc(l)
;

con8j_max_I_rsvr_e(n,rsvr)$(map_n_rsvr(n,rsvr))..
         N_RSVR_E(n,rsvr) =L= m_rsvr_e(n,rsvr)
;

con8k_max_I_rsvr_p(n,rsvr)$(map_n_rsvr(n,rsvr))..
         N_RSVR_P(n,rsvr) =L= m_rsvr_p(n,rsvr)
;

* ---------------------------------------------------------------------------- *
***** Reserve constraints *****
* ---------------------------------------------------------------------------- *

con9a_reserve_prov_exogenous(n,reserves_nonprim,h)..
          sum( map_n_tech(n,dis) , RP_DIS(n,reserves_nonprim,dis,h))
        + sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_nonprim,nondis,h))
        + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_nonprim,rsvr,h))
        + sum( map_n_sto(n,sto) , RP_STO_IN(n,reserves_nonprim,sto,h) + RP_STO_OUT(n,reserves_nonprim,sto,h))
%DSM%$ontext
        + sum( map_n_dsm(n,dsm_curt) , RP_DSM_CU(n,reserves_nonprim,dsm_curt,h))
        + sum( map_n_dsm(n,dsm_shift) , RP_DSM_SHIFT(n,reserves_nonprim,dsm_shift,h) )
$ontext
$offtext
%EV_endogenous%$ontext
%EV_exogenous%   + sum( map_n_ev(n,ev) , RP_EV_G2V(n,reserves_nonprim,ev,h) + RP_EV_V2G(n,reserves_nonprim,ev,h) )
$ontext
$offtext
%heat%$ontext
        + sum( (bu,ch) , theta_sets(n,bu,ch) * ( RP_SETS(n,reserves_nonprim,bu,ch,h) + RP_SETS_AUX(n,reserves_nonprim,bu,ch,h)) )
        + sum( (bu,ch) , theta_hp(n,bu,ch) * RP_HP(n,reserves_nonprim,bu,ch,h) )
        + sum( (bu,ch) , theta_elec(n,bu,ch) * RP_H_ELEC(n,reserves_nonprim,bu,ch,h) )
$ontext
$offtext
        =E= feat_node('reserves',n) * reserves_exogenous(n,reserves_nonprim,h)$(ord(h) > 1)
;

con9b_reserve_prov_PR_exogenous(n,reserves_prim,h)..
          sum( map_n_tech(n,dis) , RP_DIS(n,reserves_prim,dis,h))
        + sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_prim,nondis,h))
        + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_prim,rsvr,h))
        + sum( map_n_sto(n,sto) , RP_STO_IN(n,reserves_prim,sto,h) + RP_STO_OUT(n,reserves_prim,sto,h) )
%EV_endogenous%$ontext
%EV_exogenous%   + sum( map_n_ev(n,ev) , RP_EV_G2V(n,reserves_prim,ev,h) + RP_EV_V2G(n,reserves_prim,ev,h) )
$ontext
$offtext
         =E= feat_node('reserves',n) * reserves_exogenous(n,reserves_prim,h)$(ord(h) > 1)
;

* ---------------------------------------------------------------------------- *
***** Electric vehicle constraints *****
* ---------------------------------------------------------------------------- *

con10a_ev_ed(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev_endogenous',n))..
         ev_ed(n,ev,h) * phi_ev(n,ev) * ev_quant(n)
         =e= EV_GED(n,ev,h) + EV_PHEVFUEL(n,ev,h)$(ev_phev(n,ev)=1)
;

con10b_ev_chargelev_start(n,ev,h)$(map_n_ev(n,ev) AND ord(h) = 1 AND feat_node('ev_endogenous',n))..
         EV_L(n,ev,h) =E= phi_ev_ini(n,ev) * n_ev_e(n,ev) * phi_ev(n,ev) * ev_quant(n)
         + EV_CHARGE(n,ev,h) * eta_ev_in(n,ev)
         - EV_DISCHARGE(n,ev,h) / eta_ev_out(n,ev)
         - EV_GED(n,ev,h)
;

con10c_ev_chargelev(n,ev,h)$(map_n_ev(n,ev) AND ord(h) > 1 AND feat_node('ev_endogenous',n))..
         EV_L(n,ev,h) =E= EV_L(n,ev,h-1)
         + EV_CHARGE(n,ev,h) * eta_ev_in(n,ev)
         - EV_DISCHARGE(n,ev,h) / eta_ev_out(n,ev)
%reserves%$ontext
%EV_exogenous%   + sum( reserves_do , phi_reserves_call(n,reserves_do,h) * (RP_EV_G2V(n,reserves_do,ev,h)*eta_ev_in(n,ev) + RP_EV_V2G(n,reserves_do,ev,h)/eta_ev_out(n,ev)) )
%EV_exogenous%   - sum( reserves_up , phi_reserves_call(n,reserves_up,h) * (RP_EV_G2V(n,reserves_up,ev,h)*eta_ev_in(n,ev) + RP_EV_V2G(n,reserves_up,ev,h)/eta_ev_out(n,ev)) )
$ontext
$offtext
         - EV_GED(n,ev,h)
;

con10d_ev_chargelev_max(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev_endogenous',n))..
         EV_L(n,ev,h) =L= n_ev_e(n,ev) * phi_ev(n,ev) * ev_quant(n)
;

con10e_ev_maxin(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev_endogenous',n))..
        EV_CHARGE(n,ev,h)
%reserves%$ontext
        + sum( reserves_do , RP_EV_G2V(n,reserves_do,ev,h))
$ontext
$offtext
        =L= n_ev_p(n,ev,h) * phi_ev(n,ev) * ev_quant(n)
;

con10f_ev_maxout(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev_endogenous',n))..
        EV_DISCHARGE(n,ev,h)
%reserves%$ontext
        + sum( reserves_up , RP_EV_V2G(n,reserves_up,ev,h))
$ontext
$offtext
        =L= n_ev_p(n,ev,h) * phi_ev(n,ev) * ev_quant(n)
;

con10g_ev_chargelev_ending(n,ev,h)$(map_n_ev(n,ev) AND ord(h) = card(h) AND feat_node('ev_endogenous',n))..
         EV_L(n,ev,h) =E= phi_ev_ini(n,ev) * n_ev_e(n,ev) * phi_ev(n,ev) * ev_quant(n)
;

con10h_ev_minin(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev_endogenous',n))..
         0 =L= EV_CHARGE(n,ev,h)
        - sum( reserves_up , RP_EV_G2V(n,reserves_up,ev,h))
;

con10i_ev_maxin_lev(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev_endogenous',n))..
        ( EV_CHARGE(n,ev,h)
        + sum( reserves_do , RP_EV_G2V(n,reserves_do,ev,h))
        ) * eta_ev_in(n,ev)
        =L= n_ev_e(n,ev) * phi_ev(n,ev) * ev_quant(n) - EV_L(n,ev,h-1)
;

con10j_ev_minout(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev_endogenous',n))..
         0 =L= EV_DISCHARGE(n,ev,h)
        - sum( reserves_do , RP_EV_V2G(n,reserves_do,ev,h))
;

con10k_ev_maxout_lev(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev_endogenous',n))..
        ( EV_DISCHARGE(n,ev,h)
        + sum( reserves_up , RP_EV_V2G(n,reserves_up,ev,h))
) / eta_ev_out(n,ev)
        =L= EV_L(n,ev,h-1)
;

con10l_ev_exog(n,ev,h)$(map_n_ev(n,ev) AND feat_node('ev_exogenous',n))..
         EV_CHARGE(n,ev,h)
         =E=
         ev_ged_exog(n,ev,h) * phi_ev(n,ev) * ev_quant(n)
;

* ---------------------------------------------------------------------------- *
***** Prosumage constraints *****
* ---------------------------------------------------------------------------- *

con11a_pro_distrib(n,res,h)$(map_n_res_pro(n,res))..
         phi_res(n,res,h) * N_RES_PRO(n,res)
         =E=
         CU_PRO(n,res,h) + G_MARKET_PRO2M(n,res,h) + G_RES_PRO(n,res,h) + sum( map_n_sto_pro(n,sto) , STO_IN_PRO2PRO(n,res,sto,h) + STO_IN_PRO2M(n,res,sto,h) )
;

con11b_pro_balance(n,h)..
         phi_pro_load(n) * d(n,h)
         =E=
         sum( map_n_res_pro(n,res) , G_RES_PRO(n,res,h)) + sum( map_n_sto_pro(n,sto) , STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_M2PRO(n,sto,h) ) + G_MARKET_M2PRO(n,h)
;

con11c_pro_selfcon(n)..
         sum( (h,map_n_res_pro(n,res)) , G_RES_PRO(n,res,h) ) + sum( (h,sto) , STO_OUT_PRO2PRO(n,sto,h) )
         =G=
         phi_pro_self * sum( h , phi_pro_load(n) * d(n,h))
;

con11d_pro_stolev_PRO2PRO(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) > 1 )..
         STO_L_PRO2PRO(n,sto,h) =E= STO_L_PRO2PRO(n,sto,h-1) + sum( map_n_res_pro(n,res) , STO_IN_PRO2PRO(n,res,sto,h))*(1+eta_sto(n,sto))/2 - STO_OUT_PRO2PRO(n,sto,h)/(1+eta_sto(n,sto))*2
;

con11e_pro_stolev_PRO2M(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) > 1)..
         STO_L_PRO2M(n,sto,h) =E= STO_L_PRO2M(n,sto,h-1) + sum( map_n_res_pro(n,res) , STO_IN_PRO2M(n,res,sto,h))*(1+eta_sto(n,sto))/2 - STO_OUT_PRO2M(n,sto,h)/(1+eta_sto(n,sto))*2
;

con11f_pro_stolev_M2PRO(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) > 1)..
         STO_L_M2PRO(n,sto,h) =E= STO_L_M2PRO(n,sto,h-1) + STO_IN_M2PRO(n,sto,h)*(1+eta_sto(n,sto))/2 - STO_OUT_M2PRO(n,sto,h)/(1+eta_sto(n,sto))*2
;

con11g_pro_stolev_M2M(n,sto,h)$(ord(h) > 1)..
         STO_L_M2M(n,sto,h) =E= STO_L_M2M(n,sto,h-1) + STO_IN_M2M(n,sto,h)*(1+eta_sto(n,sto))/2 - STO_OUT_M2M(n,sto,h)/(1+eta_sto(n,sto))*2
;

con11h_1_pro_stolev_start_PRO2PRO(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) = 1)..
        STO_L_PRO2PRO(n,sto,h) =E= 0.25 * phi_sto_pro_ini(n,sto) * N_STO_E_PRO(n,sto) + sum( map_n_res_pro(n,res) , STO_IN_PRO2PRO(n,res,sto,h))*(1+eta_sto(n,sto))/2 - STO_OUT_PRO2PRO(n,sto,h)/(1+eta_sto(n,sto))*2
;

con11h_2_pro_stolev_start_PRO2M(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) = 1)..
        STO_L_PRO2M(n,sto,h) =E= 0.25 * phi_sto_pro_ini(n,sto) * N_STO_E_PRO(n,sto) + sum( map_n_res_pro(n,res) , STO_IN_PRO2M(n,res,sto,h))*(1+eta_sto(n,sto))/2 - STO_OUT_PRO2M(n,sto,h)/(1+eta_sto(n,sto))*2
;

con11h_3_pro_stolev_start_M2PRO(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) = 1)..
        STO_L_M2PRO(n,sto,h) =E= 0.25 * phi_sto_pro_ini(n,sto) * N_STO_E_PRO(n,sto) + STO_IN_M2PRO(n,sto,h)*(1+eta_sto(n,sto))/2 - STO_OUT_M2PRO(n,sto,h)/(1+eta_sto(n,sto))*2
;

con11h_4_pro_stolev_start_M2M(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) = 1)..
        STO_L_M2M(n,sto,h) =E= 0.25 * phi_sto_pro_ini(n,sto) * N_STO_E_PRO(n,sto) + STO_IN_M2M(n,sto,h)*(1+eta_sto(n,sto))/2 - STO_OUT_M2M(n,sto,h)/(1+eta_sto(n,sto))*2
;

con11i_pro_stolev(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h)>1)..
         STO_L_PRO(n,sto,h) =E=   STO_L_PRO2PRO(n,sto,h) +  STO_L_PRO2M(n,sto,h) + STO_L_M2PRO(n,sto,h) + STO_L_M2M(n,sto,h)
;

con11j_pro_stolev_max(n,sto,h)..
        STO_L_PRO(n,sto,h) =L= N_STO_E_PRO(n,sto)
;

con11k_pro_maxin_sto(n,sto,h)$(map_n_sto_pro(n,sto))..
        sum( map_n_res_pro(n,res) , STO_IN_PRO2PRO(n,res,sto,h) + STO_IN_PRO2M(n,res,sto,h) ) + STO_IN_M2PRO(n,sto,h) + STO_IN_M2M(n,sto,h)
        =L= N_STO_P_PRO(n,sto)
;

con11l_pro_maxout_sto(n,sto,h)$(map_n_sto_pro(n,sto))..
        STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h) + STO_OUT_M2PRO(n,sto,h) + STO_OUT_M2M(n,sto,h)
        =L= N_STO_P_PRO(n,sto)
;

con11m_pro_maxout_lev(n,sto,h)$(map_n_sto_pro(n,sto))..
        ( STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_M2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h) + STO_OUT_M2M(n,sto,h) ) / (1+eta_sto(n,sto))*2
        =L= STO_L_PRO(n,sto,h-1)
;

con11n_pro_maxin_lev(n,sto,h)$(map_n_sto_pro(n,sto))..
        ( sum( map_n_res_pro(n,res) , STO_IN_PRO2PRO(n,res,sto,h) + STO_IN_PRO2M(n,res,sto,h) ) + STO_IN_M2PRO(n,sto,h) + STO_IN_M2M(n,sto,h) ) * (1+eta_sto(n,sto))/2
        =L= N_STO_E_PRO(n,sto) - STO_L_PRO(n,sto,h-1)
;

con11o_pro_ending(n,sto,h)$(map_n_sto_pro(n,sto) AND ord(h) = card(h))..
         STO_L_PRO(n,sto,h) =E= phi_sto_pro_ini(n,sto) * N_STO_E_PRO(n,sto)
;

* ---------------------------------------------------------------------------- *
***** NTC constraints *****
* ---------------------------------------------------------------------------- *

***** Constraint on energy flow between nodes ******
con12a_max_f(l,h)$(map_l(l))..
         F(l,h) =L= NTC(l)
;

con12b_min_f(l,h)$(map_l(l))..
         F(l,h) =G= -NTC(l)
;

* ---------------------------------------------------------------------------- *
***** Reservoir constraints *****
* ---------------------------------------------------------------------------- *

con13a_rsvrlev_start(n,rsvr,h)$(map_n_rsvr(n,rsvr) AND ord(h) = 1)..
        RSVR_L(n,rsvr,h) =E= phi_rsvr_ini(n,rsvr) * N_RSVR_E(n,rsvr) + rsvr_in(n,rsvr,h)/1000 * N_RSVR_E(n,rsvr) - RSVR_OUT(n,rsvr,h)
;

con13b_rsvrlev(n,rsvr,h)$(ord(h) > 1 AND map_n_rsvr(n,rsvr))..
         RSVR_L(n,rsvr,h) =E= RSVR_L(n,rsvr,h-1) + rsvr_in(n,rsvr,h)/1000 * N_RSVR_E(n,rsvr) - RSVR_OUT(n,rsvr,h)
%reserves%$ontext
                - sum( reserves_up , RP_RSVR(n,reserves_up,rsvr,h) * phi_reserves_call(n,reserves_up,h) )
                + sum( reserves_do , RP_RSVR(n,reserves_do,rsvr,h) * phi_reserves_call(n,reserves_do,h) )
$ontext
$offtext
;

con13c_rsvrlev_max(n,rsvr,h)$(map_n_rsvr(n,rsvr))..
        RSVR_L(n,rsvr,h) =L= N_RSVR_E(n,rsvr)
;

con13d_maxout_rsvr(n,rsvr,h)$(map_n_rsvr(n,rsvr))..
        RSVR_OUT(n,rsvr,h)
%reserves%$ontext
        + sum( reserves_up , RP_RSVR(n,reserves_up,rsvr,h))
$ontext
$offtext
        =L= phi_rsvr_maxout(n,rsvr) * N_RSVR_P(n,rsvr)
;

con13d2_minout_rsvr(n,rsvr,h)$(map_n_rsvr(n,rsvr) AND (ord(h) > 1) AND (ord(h) < card(h)))..
        RSVR_OUT(n,rsvr,h)
        =G= phi_rsvr_minout(n,rsvr) * N_RSVR_P(n,rsvr)
;

con13e_resrv_rsvr(n,rsvr,h)$(map_n_rsvr(n,rsvr))..
        sum( reserves_do , RP_RSVR(n,reserves_do,rsvr,h))
        =L= RSVR_OUT(n,rsvr,h)
;

con13f_maxout_lev(n,rsvr,h)$(map_n_rsvr(n,rsvr))..
        RSVR_OUT(n,rsvr,h)
%reserves%$ontext
        + sum( reserves_up , RP_RSVR(n,reserves_up,rsvr,h))
$ontext
$offtext
        =L= RSVR_L(n,rsvr,h-1)
;

con13g_ending(n,rsvr,h)$(map_n_rsvr(n,rsvr) AND ord(h) = card(h))..
         RSVR_L(n,rsvr,h) =G= phi_rsvr_ini(n,rsvr) * N_RSVR_E(n,rsvr)
;

con13h_smooth(n,rsvr,h)$(map_n_rsvr(n,rsvr) AND feat_node('rsvr_outflow',n))..
         RSVR_OUT(n,rsvr,h) =G= phi_rsvr_min(n) * sum( hh , rsvr_in(n,rsvr,hh)/1000/card(hh)) * N_RSVR_E(n,rsvr)
;

con13i_min_level(n,rsvr,h)$(map_n_rsvr(n,rsvr))..
         RSVR_L(n,rsvr,h) =G= phi_rsvr_lev_min(n,rsvr) * N_RSVR_E(n,rsvr)
;

con13j_min_FLH(n,rsvr)$(map_n_rsvr(n,rsvr))..
         sum( h , RSVR_OUT(n,rsvr,h) ) =G= min_flh(n,rsvr) * N_RSVR_P(n,rsvr)
;


* ---------------------------------------------------------------------------- *
***** Heating constraints *****
* ---------------------------------------------------------------------------- *

* Energy balances
con14a_heat_balance(n,bu,ch,h)$feat_node('heat',n)..
         theta_dir(n,bu,ch) * H_DIR(n,bu,ch,h) + theta_sets(n,bu,ch) * H_SETS_OUT(n,bu,ch,h)+ theta_storage(n,bu,ch) * H_STO_OUT(n,bu,ch,h)
         + theta_sets(n,bu,ch) * (1-eta_heat_stat(n,bu,ch)) * H_SETS_LEV(n,bu,ch,h-1)$(theta_sets(n,bu,ch) AND ord(h) > 1)
         =G= dh(n,bu,ch,h)
;

con14b_dhw_balance(n,bu,ch,h)$feat_node('heat',n)..
         theta_storage(n,bu,ch) * H_DHW_STO_OUT(n,bu,ch,h) + theta_dir(n,bu,ch) * H_DHW_DIR(n,bu,ch,h) + theta_sets(n,bu,ch) * H_DHW_AUX_OUT(n,bu,ch,h)
         =E=
         d_dhw(n,bu,ch,h)
;

* SETS
con14c_sets_level(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch) AND ord(h) > 1)..
         H_SETS_LEV(n,bu,ch,h) =E= eta_heat_stat(n,bu,ch) * H_SETS_LEV(n,bu,ch,h-1) + eta_heat_dyn(n,bu,ch) * H_SETS_IN(n,bu,ch,h) - H_SETS_OUT(n,bu,ch,h)
%reserves%$ontext
         - theta_sets(n,bu,ch) * eta_heat_dyn(n,bu,ch) * (sum( reserves_up , RP_SETS(n,reserves_up,bu,ch,h) * phi_reserves_call(n,reserves_up,h) )
         - sum( reserves_do , RP_SETS(n,reserves_do,bu,ch,h) * phi_reserves_call(n,reserves_do,h) ))
$ontext
$offtext
;

con14d_sets_level_start(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch) AND (ord(h) = 1 OR ord(h) = card(h)))..
         H_SETS_LEV(n,bu,ch,h) =E= phi_heat_ini(n,bu,ch) * n_sets_e(n,bu,ch)
;

con14e_sets_maxin(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch))..
         H_SETS_IN(n,bu,ch,h)
%reserves%$ontext
         + theta_sets(n,bu,ch) * sum( reserves_do , RP_SETS(n,reserves_do,bu,ch,h) )
$ontext
$offtext
         =L= n_sets_p_in(n,bu,ch)
;

con14f_sets_maxout(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch))..
         H_SETS_OUT(n,bu,ch,h) =L= n_sets_p_out(n,bu,ch)
;

con14g_sets_minin(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch))..
        sum( reserves_up , RP_SETS(n,reserves_up,bu,ch,h))
        =L= H_SETS_IN(n,bu,ch,h)
;

con14h_sets_maxlev(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch))..
         H_SETS_LEV(n,bu,ch,h) =L= n_sets_e(n,bu,ch)
;

* SETS and DHW
con14i_sets_aux_dhw_level(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch) AND ord(h) > 1)..
         H_DHW_AUX_LEV(n,bu,ch,h) =E= eta_dhw_aux_stat(n,bu,ch) * H_DHW_AUX_LEV(n,bu,ch,h-1) + H_DHW_AUX_ELEC_IN(n,bu,ch,h) - H_DHW_AUX_OUT(n,bu,ch,h)
%reserves%$ontext
         - theta_sets(n,bu,ch) * (sum( reserves_up , RP_SETS_AUX(n,reserves_up,bu,ch,h) * phi_reserves_call(n,reserves_up,h) )
         - sum( reserves_do , RP_SETS_AUX(n,reserves_do,bu,ch,h) * phi_reserves_call(n,reserves_do,h) ))
$ontext
$offtext
;

con14j_sets_aux_dhw_level_start(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch) AND (ord(h) = 1 OR ord(h) = card(h)) )..
         H_DHW_AUX_LEV(n,bu,ch,h) =E= phi_heat_ini(n,bu,ch) * n_sets_dhw_e(n,bu,ch)
;

con14k_sets_aux_dhw_maxin(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch) )..
         H_DHW_AUX_ELEC_IN(n,bu,ch,h)
%reserves%$ontext
         + theta_sets(n,bu,ch) * sum( reserves_do , RP_SETS_AUX(n,reserves_do,bu,ch,h) )
$ontext
$offtext
         =L= n_sets_dhw_p_in(n,bu,ch)
;

con14l_sets_aux_dhw_minin(n,bu,ch,h)$(feat_node('heat',n) AND feat_node('reserves',n) AND theta_sets(n,bu,ch)  )..
        sum( reserves_up , RP_SETS_AUX(n,reserves_up,bu,ch,h))
        =L= H_DHW_AUX_ELEC_IN(n,bu,ch,h)
;

con14m_sets_aux_dhw_maxlev(n,bu,ch,h)$(feat_node('heat',n) AND theta_sets(n,bu,ch) )..
         H_DHW_AUX_LEV(n,bu,ch,h) =L= n_sets_dhw_e(n,bu,ch)
;

* HEAT PUMPS
con14n_hp_in(n,bu,hp,h)$(feat_node('heat',n) AND theta_hp(n,bu,hp))..
         H_STO_IN_HP(n,bu,hp,h) =E= (H_HP_IN(n,bu,hp,h)
%reserves%$ontext
         - theta_hp(n,bu,hp) * (sum( reserves_up , RP_HP(n,reserves_up,bu,hp,h) * phi_reserves_call(n,reserves_up,h) )
         - sum( reserves_do , RP_HP(n,reserves_do,bu,hp,h) * phi_reserves_call(n,reserves_do,h) ))
$ontext
$offtext
         ) * eta_heat_dyn(n,bu,hp) * ((temp_sink(n,bu,hp)+273.15)/(temp_sink(n,bu,hp) - temp_source(n,bu,hp,h)))
;

con14o_hp_maxin(n,bu,hp,h)$(feat_node('heat',n) AND theta_hp(n,bu,hp))..
         H_HP_IN(n,bu,hp,h)
%reserves%$ontext
         + sum( reserves_do , RP_HP(n,reserves_do,bu,hp,h) )
$ontext
$offtext
         =L= n_heat_p_in(n,bu,hp)
;

con14p_hp_minin(n,bu,hp,h)$(feat_node('heat',n) AND theta_hp(n,bu,hp))..
        sum( reserves_up , RP_HP(n,reserves_up,bu,hp,h))
        =L= H_HP_IN(n,bu,hp,h)
;

* (Hybrid) ELECTRIC HEATING
con14q_storage_elec_in(n,bu,hel,h)$(feat_node('heat',n) AND theta_storage(n,bu,hel) AND theta_elec(n,bu,hel) )..
         H_STO_IN_ELECTRIC(n,bu,hel,h) =E= H_ELECTRIC_IN(n,bu,hel,h)
%reserves%$ontext
         - theta_elec(n,bu,hel) * (sum( reserves_up , RP_H_ELEC(n,reserves_up,bu,hel,h) * phi_reserves_call(n,reserves_up,h) )
         - sum( reserves_do , RP_H_ELEC(n,reserves_do,bu,hel,h) * phi_reserves_call(n,reserves_do,h) ))
$ontext
$offtext
;

con14r_storage_elec_maxin(n,bu,hel,h)$(feat_node('heat',n) AND theta_storage(n,bu,hel) AND theta_elec(n,bu,hel ))..
         H_ELECTRIC_IN(n,bu,hel,h)
%reserves%$ontext
         + sum( reserves_do , RP_H_ELEC(n,reserves_do,bu,hel,h) )
$ontext
$offtext
         =L= n_heat_p_in(n,bu,hel)
;

con14s_storage_elec_minin(n,bu,hel,h)$(feat_node('heat',n) AND feat_node('reserves',n) AND theta_storage(n,bu,hel) AND theta_elec(n,bu,hel) )..
        sum( reserves_up , RP_H_ELEC(n,reserves_up,bu,hel,h))
        =L= H_ELECTRIC_IN(n,bu,hel,h)
;

* HEAT STORAGE
con14t_storage_level(n,bu,hst,h)$(feat_node('heat',n) AND theta_storage(n,bu,hst) AND ord(h) > 1)..
         H_STO_LEV(n,bu,hst,h)
         =E=
         eta_heat_stat(n,bu,hst) * H_STO_LEV(n,bu,hst,h-1) + theta_hp(n,bu,hst)*H_STO_IN_HP(n,bu,hst,h) + theta_elec(n,bu,hst)*H_STO_IN_ELECTRIC(n,bu,hst,h) + theta_fossil(n,bu,hst) * H_STO_IN_FOSSIL(n,bu,hst,h)
         - H_STO_OUT(n,bu,hst,h) - H_DHW_STO_OUT(n,bu,hst,h)
;

con14u_storage_level_start(n,bu,hst,h)$(feat_node('heat',n) AND theta_storage(n,bu,hst) AND (ord(h) = 1 OR ord(h) = card(h)))..
         H_STO_LEV(n,bu,hst,h) =E= phi_heat_ini(n,bu,hst) * theta_storage(n,bu,hst)*n_heat_e(n,bu,hst)
;

con14v_storage_maxlev(n,bu,hst,h)$(feat_node('heat',n) AND theta_storage(n,bu,hst))..
         H_STO_LEV(n,bu,hst,h) =L= n_heat_e(n,bu,hst)
;

********************************************************************************
***** MODEL *****
********************************************************************************

model DIETER /
obj

con1a_bal

con2a_loadlevel
con2b_loadlevelstart

con3a_maxprod_dispatchable
%reserves%$ontext
  con3b_minprod_dispatchable
  con3c_flex_reserves_spin
  con3d_flex_reserves_nonspin
$ontext
$offtext
con3e_maxprod_res
%reserves%$ontext
  con3f_minprod_res
$ontext
$offtext

con4a_stolev_start
con4b_stolev
con4c_stolev_max
con4d_maxin_sto
con4e_maxout_sto
%reserves%$ontext
  con4f_resrv_sto
  con4g_resrv_sto
$ontext
$offtext
con4h_maxout_lev
con4i_maxin_lev
con4j_ending
con4k_PHS_EtoP

%rescon_0a%$ontext
con5a_minRES_0a
$ontext
$offtext
%rescon_1b%$ontext
con5a_minRES_1b
$ontext
$offtext
%rescon_2c%$ontext
con5a_minRES_2c
$ontext
$offtext
%rescon_3b%$ontext
con5a_minRES_3b
$ontext
$offtext
%rescon_4e%$ontext
con5a_minRES_4e
$ontext
$offtext

con5b_max_energy

%max_overall_CO2%$ontext
con5c_max_overall_CO2
$ontext
$offtext
%max_node_CO2%$ontext
con5c_max_node_CO2
$ontext
$offtext

%DSM%$ontext
con6a_DSMcurt_duration_max
con6b_DSMcurt_max

con7a_DSMshift_upanddown
con7b_DSMshift_granular_max
con7c_DSM_distrib_up
con7d_DSM_distrib_do
*con_7e_DSMshift_recovery
$ontext
$offtext

con8a_max_I_power
con8b_max_I_sto_e
con8c_max_I_sto_p
%DSM%$ontext
  con8d_max_I_dsm_cu
  con8e_max_I_dsm_shift_pos
$ontext
$offtext
con8i_max_I_ntc
con8j_max_I_rsvr_e
con8k_max_I_rsvr_p

%reserves%$ontext
 con9a_reserve_prov_exogenous
 con9b_reserve_prov_PR_exogenous
$ontext
$offtext

%EV_endogenous%$ontext
 con10a_ev_ed
%EV_exogenous% con10b_ev_chargelev_start
 con10c_ev_chargelev
 con10d_ev_chargelev_max
%EV_exogenous% con10e_ev_maxin
%EV_exogenous% con10f_ev_maxout
%EV_exogenous% con10g_ev_chargelev_ending
$ontext
$offtext
%EV_endogenous%$ontext
%reserves%$ontext
%EV_exogenous% con10h_ev_minin
%EV_exogenous% con10i_ev_maxin_lev
%EV_exogenous% con10j_ev_minout
%EV_exogenous% con10k_ev_maxout_lev
$ontext
$offtext
%EV_endogenous%$ontext
%EV_exogenous%$ontext
 con10l_ev_exog
$ontext
$offtext

%prosumage%$ontext
con8f_max_pro_res
con8g_max_pro_sto_e
con8h_max_sto_pro_p
con11a_pro_distrib
con11b_pro_balance
con11c_pro_selfcon
con11d_pro_stolev_PRO2PRO
con11e_pro_stolev_PRO2M
con11f_pro_stolev_M2PRO
con11g_pro_stolev_M2M
con11h_1_pro_stolev_start_PRO2PRO
con11h_2_pro_stolev_start_PRO2M
con11h_3_pro_stolev_start_M2PRO
con11h_4_pro_stolev_start_M2M
con11i_pro_stolev
con11j_pro_stolev_max
con11k_pro_maxin_sto
con11l_pro_maxout_sto
con11m_pro_maxout_lev
con11n_pro_maxin_lev
con11o_pro_ending
$ontext
$offtext

con12a_max_f
con12b_min_f

con13a_rsvrlev_start
con13b_rsvrlev
con13c_rsvrlev_max
con13d_maxout_rsvr
con13d2_minout_rsvr
*con13e_resrv_rsvr
*con13f_maxout_lev
con13g_ending
*con13h_smooth
con13i_min_level
*con13j_min_FLH

%heat%$ontext
con14a_heat_balance
con14b_dhw_balance
con14c_sets_level
con14d_sets_level_start
con14e_sets_maxin
con14f_sets_maxout
con14h_sets_maxlev

con14i_sets_aux_dhw_level
con14j_sets_aux_dhw_level_start
con14k_sets_aux_dhw_maxin
con14l_sets_aux_dhw_minin
con14m_sets_aux_dhw_maxlev

con14n_hp_in
con14o_hp_maxin
con14q_storage_elec_in
con14r_storage_elec_maxin
con14t_storage_level
con14u_storage_level_start
con14v_storage_maxlev
$ontext
$offtext

%heat%$ontext
%reserves%$ontext
con14g_sets_minin
con14p_hp_minin
con14s_storage_elec_minin
$ontext
$offtext
/;

********************************************************************************
************** Options, fixings, report preparation ****************************
********************************************************************************

* lpmethod: parameter for choosing an optimizer
*      0 "Automatic selection of an optimizer", 1 "Primal Simplex", 2 " Dual Simplex", 3 "Network Simplex", 4 " Barrier", 5 "Sifting", 6 "Concurrent optimizer"
*      Barrier optimizer offers an approach particularly efficient on large and sparse problems.
* threads: multithreaded parallel barrier, parallel MIP, and concurrent optimizers.
*      These parallel optimizers are implemented to run on hardware platforms with multiple cores.
*      default setting 0 (zero), the number of threads that CPLEX actually uses during a parallel optimization ->
*      is no more than 32 or the number of CPU cores available on the computer where CPLEX is running (whichever is smaller)
* epgap: Sets a relative tolerance on the gap between the best integer objective and the objective of the best node remaining.
*      MIP?
*  barcrossalg: if any, crossover is performed at the end of a barrier optimization.
*      -1 No crossover, 0 Automatic: let CPLEX choose; default. 1 Primal crossover, 2  Dual crossover
* barepcomp: Barrier Convergence Tolerance 1e-10 to INF default 1e-8. The Convergence Tolerance sets the tolerance on complementarity for convergence.
*       The barrier algorithm will terminate with an optimal solution if the relative complementarity is smaller than this value.
* barcrossalg -1
* Depreciated value -1 for BarCrossAlg. Using SolutionType=2

* Solver options
$onecho > cplex.opt

lpmethod 4
threads 0
epgap 1e-3
$offecho

%no_crossover%$ontext
$onecho > cplex.opt
lpmethod 4
threads 0
epgap 1e-3
SolutionType 2
barepcomp 1e-8
$offecho
$ontext
$offtext

* in case of guss tool
$onecho > cplexd.opt

lpmethod 4
threads 1
epgap 1e-3
$offecho

%no_crossover%$ontext
$onecho > cplexd.opt
lpmethod 4
threads 1
epgap 1e-3
SolutionType 2
barepcomp 1e-8
$offecho
$ontext
$offtext




* .OptFile: Do not forget to “tell” the solver to read the options file by adding a line
dieter.OptFile = 1;
* .holdFixed: 1 Fixed variables are treated as constants, 0 Fixed variables are not treated as constants.
dieter.holdFixed = 1 ;


********************************************************************************
****************** Exogenous EV  ***********************************************
********************************************************************************

%EV_endogenous%$ontext
%EV_exogenous%$ontext
EV_DISCHARGE.fx(n,ev,h) = 0 ;
RP_EV_G2V.fx(n,reserves,ev,h) = 0 ;
RP_EV_V2G.fx(n,reserves,ev,h) = 0 ;
$ontext
$offtext



********************************************************************************
**** No storage and DSM in first period  ***************************************
********************************************************************************

** No storage inflow in first period **
* CG Why? i remove it with a star
*STO_IN.fx(n,sto,h)$(ord(h) = 1) = 0;

%DSM%$ontext
** No DSM load shifting in the first period **
DSM_UP.fx(n,dsm_shift,h)$(ord(h) = 1) = 0;
DSM_DO.fx(n,dsm_shift,h,hh)$(ord(h) = 1) = 0 ;
DSM_DO.fx(n,dsm_shift,h,h)$(ord(h) = 1) = 0 ;
DSM_UP_DEMAND.fx(n,dsm_shift,h)$(ord(h) = 1) = 0 ;
DSM_DO_DEMAND.fx(n,dsm_shift,h)$(ord(h) = 1) = 0 ;

** No reserves provision by DSM in first period **
RP_DSM_SHIFT.fx(n,reserves,dsm_shift,h)$(ord(h) = 1) = 0;
RP_DSM_CU.fx(n,reserves,dsm_curt,h)$(ord(h) = 1) = 0 ;
RP_DSM_CU.fx(n,reserves,dsm_curt,h)$(ord(h) = 1) = 0 ;

** No provision of PR and negative reserves by DSM load curtailment **
RP_DSM_CU.fx(n,reserves_prim,dsm_curt,h) = 0 ;
RP_DSM_CU.fx(n,reserves_do,dsm_curt,h) = 0 ;

** No provision of PR by DSM load shifting **
RP_DSM_SHIFT.fx(n,reserves_prim,dsm_shift,h) = 0 ;
$ontext
$offtext



********************************************************************************
**** No primary reserves by heating devices  ***********************************
********************************************************************************

%heat%$ontext
%reserves%$ontext
RP_HP.fx(n,reserves_prim,bu,hp,h) = 0 ;
RP_SETS.fx(n,reserves_prim,bu,ch,h) = 0 ;
RP_SETS_AUX.fx(n,reserves_prim,bu,ch,h) = 0 ;
RP_H_ELEC.fx(n,reserves_prim,bu,ch,h) = 0 ;
$ontext
$offtext



********************************************************************************
**** Fixing to reduce model size  **********************************************
********************************************************************************

F.fx(l,h)$(m_ntc(l) = 0) = 0 ;
NTC.fx(l)$(m_ntc(l) = 0) = 0 ;

G_L.fx(n,tech,h)$(m_p(n,tech) = 0) = 0 ;
G_UP.fx(n,tech,h)$(m_p(n,tech) = 0) = 0 ;
G_DO.fx(n,tech,h)$(m_p(n,tech) = 0) = 0 ;
N_TECH.fx(n,tech)$(m_p(n,tech) = 0) = 0 ;
G_RES.fx(n,tech,h)$(m_p(n,tech) = 0) = 0 ;
CU.fx(n,tech,h)$(m_p(n,tech) = 0) = 0 ;

N_STO_P.fx(n,sto)$(m_sto_p(n,sto) = 0) = 0 ;
N_STO_E.fx(n,sto)$(m_sto_e(n,sto) = 0) = 0 ;
STO_IN.fx(n,sto,h)$(m_sto_p(n,sto) = 0) = 0 ;
STO_OUT.fx(n,sto,h)$(m_sto_p(n,sto) = 0) = 0 ;
STO_L.fx(n,sto,h)$(m_sto_p(n,sto) = 0) = 0 ;
RP_STO_IN.fx(n,reserves,sto,h)$(m_sto_p(n,sto) = 0) = 0 ;
RP_STO_OUT.fx(n,reserves,sto,h)$(m_sto_p(n,sto) = 0) = 0 ;

RSVR_OUT.fx(n,rsvr,h)$(m_rsvr_p(n,rsvr) = 0) = 0 ;
RSVR_L.fx(n,rsvr,h)$(m_rsvr_p(n,rsvr) = 0) = 0 ;
N_RSVR_E.fx(n,rsvr)$(m_rsvr_p(n,rsvr) = 0) = 0 ;
N_RSVR_P.fx(n,rsvr)$(m_rsvr_p(n,rsvr) = 0) = 0 ;

%reserves%$ontext
RP_DIS.fx(n,reserves,tech,h)$(feat_node('reserves',n) = 0 OR m_p(n,tech) = 0) = 0 ;
RP_NONDIS.fx(n,reserves,tech,h)$(feat_node('reserves',n) = 0 OR m_p(n,tech) = 0) = 0 ;
RP_STO_IN.fx(n,reserves,sto,h)$(feat_node('reserves',n) = 0 OR m_sto_p(n,sto) = 0) = 0 ;
RP_STO_OUT.fx(n,reserves,sto,h)$(feat_node('reserves',n) = 0 OR m_sto_p(n,sto) = 0) = 0 ;
RP_EV_V2G.fx(n,reserves,ev,h)$(feat_node('reserves',n) = 0) = 0 ;
RP_EV_G2V.fx(n,reserves,ev,h)$(feat_node('reserves',n) = 0) = 0 ;
RP_DSM_CU.fx(n,reserves,dsm_curt,h)$(feat_node('reserves',n) = 0 OR m_dsm_cu(n,dsm_curt) = 0) = 0 ;
RP_DSM_SHIFT.fx(n,reserves,dsm_shift,h)$(feat_node('reserves',n) = 0 OR m_dsm_shift(n,dsm_shift) = 0) = 0 ;
RP_RSVR.fx(n,reserves,rsvr,h)$(feat_node('reserves',n) = 0  OR m_rsvr_p(n,rsvr) = 0) = 0 ;
$ontext
$offtext

%prosumage%$ontext
CU_PRO.fx(n,res,h)$(feat_node('prosumage',n) = 0 OR m_res_pro(n,res) = 0) = 0 ;
G_MARKET_PRO2M.fx(n,res,h)$(feat_node('prosumage',n) = 0 OR m_res_pro(n,res) = 0) = 0 ;
G_MARKET_M2PRO.fx(n,h)$(feat_node('prosumage',n) = 0) = 0 ;
G_RES_PRO.fx(n,res,h)$(feat_node('prosumage',n) = 0 OR m_res_pro(n,res) = 0) = 0 ;
STO_IN_PRO2PRO.fx(n,res,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_IN_PRO2M.fx(n,res,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_IN_M2PRO.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_IN_M2M.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_OUT_PRO2PRO.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_OUT_PRO2M.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_OUT_M2PRO.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_OUT_M2M.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_L_PRO2PRO.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_L_PRO2M.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_L_M2PRO.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_L_M2M.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
N_STO_E_PRO.fx(n,sto)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
N_STO_P_PRO.fx(n,sto)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
STO_L_PRO.fx(n,sto,h)$(feat_node('prosumage',n) = 0 OR m_sto_pro_p(n,sto) = 0) = 0 ;
N_RES_PRO.fx(n,res)$(feat_node('prosumage',n) = 0 OR m_res_pro(n,res) = 0) = 0 ;
$ontext
$offtext

%EV_endogenous%$ontext
EV_CHARGE.fx(n,ev,h)$(feat_node('ev_endogenous',n) = 0) = 0 ;
EV_DISCHARGE.fx(n,ev,h)$(feat_node('ev_endogenous',n) = 0) = 0 ;
EV_L.fx(n,ev,h)$(feat_node('ev_endogenous',n) = 0) = 0 ;
EV_PHEVFUEL.fx(n,ev,h)$(feat_node('ev_endogenous',n) = 0) = 0 ;
EV_GED.fx(n,ev,h)$(feat_node('ev_endogenous',n) = 0) = 0 ;
RP_EV_V2G.fx(n,reserves,ev,h)$(feat_node('ev_endogenous',n) = 0) = 0 ;
RP_EV_G2V.fx(n,reserves,ev,h)$(feat_node('ev_endogenous',n) = 0) = 0 ;
$ontext
$offtext

%heat%$ontext
H_DIR.up(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_SETS_LEV.up(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_SETS_IN.up(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_SETS_OUT.up(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_HP_IN.up(n,bu,ch,hh)$(feat_node('heat',n) = 0) = 0 ;
H_STO_LEV.up(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_STO_IN_HP.up(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_STO_IN_ELECTRIC.up(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_STO_IN_NONELECTRIC.up(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
H_STO_OUT.up(n,bu,ch,h)$(feat_node('heat',n) = 0) = 0 ;
$ontext
$offtext

*****************************************
**** Scenario file **********************
*****************************************

Parameter
m_exog_p(n,tech)
m_exog_sto_e(n,sto)
m_exog_sto_p(n,sto)
m_exog_rsvr_p(n,rsvr)
m_exog_rsvr_e(n,rsvr)
m_exog_ntc(l)
;

m_exog_p(n,tech) = technology_data(n,tech,'fixed_capacities') ;
m_exog_sto_e(n,sto) = storage_data(n,sto,'fixed_capacities_energy');
m_exog_sto_p(n,sto) = storage_data(n,sto,'fixed_capacities_power');
m_exog_rsvr_p(n,rsvr) = reservoir_data(n,rsvr,'fixed_capacities_power');
m_exog_rsvr_e(n,rsvr) = reservoir_data(n,rsvr,'fixed_capacities_energy');
m_exog_ntc(l) = topology_data(l,'fixed_capacities_ntc');


*** Dispatch model
%dispatch_only%$ontext
N_TECH.fx(n,tech) = m_exog_p(n,tech) ;
N_STO_P.fx(n,sto) = m_exog_sto_p(n,sto) ;
N_STO_E.fx(n,sto) = m_exog_sto_e(n,sto) ;
*** here N_RSVR_E is missing??
N_RSVR_P.fx(n,rsvr) =  m_exog_rsvr_p(n,rsvr) ;
NTC.fx(l) = m_exog_ntc(l) ;
$ontext
$offtext

*** Investment model
%investment%$ontext
N_TECH.lo(n,tech) = technology_data(n,tech,'min_installable') ;
N_TECH.up(n,tech) = technology_data(n,tech,'max_installable') ;

N_STO_P.lo(n,sto) = storage_data(n,sto,'min_power') ;
N_STO_E.lo(n,sto) = storage_data(n,sto,'min_energy') ;
N_STO_P.up(n,sto) = storage_data(n,sto,'max_power') ;
N_STO_E.up(n,sto) = storage_data(n,sto,'max_energy') ;

N_RSVR_P.lo(n,rsvr) =  reservoir_data(n,rsvr,'min_power') ;
N_RSVR_E.lo(n,rsvr) =  reservoir_data(n,rsvr,'min_energy') ;

N_RSVR_P.up(n,rsvr) =  reservoir_data(n,rsvr,'max_power') ;
N_RSVR_E.up(n,rsvr) =  reservoir_data(n,rsvr,'max_energy') ;

NTC.lo(l) = topology_data(l,'min_installable') ;
NTC.up(l) = topology_data(l,'max_installable') ;
$ontext
$offtext

*** No network transfer
%net_transfer%NTC.fx(l) = 0 ;
%net_transfer%F.fx(l,h) = 0 ;

phi_rsvr_maxout(n,rsvr) = reservoir_data(n,rsvr,'maxout') ;
phi_rsvr_minout(n,rsvr) = reservoir_data(n,rsvr,'minout') ;
min_flh(n,rsvr) = reservoir_data(n,rsvr,'min_flh') ;

*** Heating
*Parameter
*security_margin_n_heat_out /1.0/
*;
*
* Parameterization of water-based heat storage
*n_heat_p_out(n,bu,ch) = security_margin_n_heat_out * smax( h , dh(n,bu,ch,h) + d_dhw(n,bu,ch,h) ) ;
*n_heat_e(n,bu,ch) = 3 * n_heat_p_out(n,bu,ch) ;
*n_heat_p_in(n,bu,ch) = n_heat_p_out(n,bu,ch) ;
*n_heat_p_in(n,bu,'hp_gs') = n_heat_p_out(n,bu,'hp_gs') / ( eta_heat_dyn(n,bu,'hp_gs') * (temp_sink(n,bu,'hp_gs')+273.15) / (temp_sink(n,bu,'hp_gs') - 10) ) ;
* at least -5�C; applied to 98% of hoursn; minimum: -13.4
*n_heat_p_in(n,bu,'hp_as') = n_heat_p_out(n,bu,'hp_as') / ( eta_heat_dyn(n,bu,'hp_as') * (temp_sink(n,bu,'hp_as')+273.15) / (temp_sink(n,bu,'hp_as') + 5) ) ;
*
* Parameterization of SETS
*n_sets_p_out(n,bu,ch) = security_margin_n_heat_out * smax( h , dh(n,bu,ch,h) ) ;
*n_sets_p_in(n,bu,ch) = 2 * n_sets_p_out(n,bu,ch) ;
*n_sets_e(n,bu,ch) = 16 * n_sets_p_out(n,bu,ch) ;
*
* Parameterization of DHW SETS
*n_sets_dhw_p_out(n,bu,ch) = security_margin_n_heat_out * smax( h , d_dhw(n,bu,ch,h) ) ;
*n_sets_dhw_p_in(n,bu,ch) = n_sets_dhw_p_out(n,bu,ch) ;
*n_sets_dhw_e(n,bu,ch) = 2.2 * n_sets_dhw_p_out(n,bu,ch) ;

phi_min_res = data_1dim('phi_min_res') ;
co2_cap = data_1dim('co2_cap') ;
phi_pro_self = data_1dim('phi_pro_self') ;
*ev_quant = data_1dim('ev_quant') ;
c_infes = data_1dim('c_infes') ;

phi_min_res_exog(n) = data_2dim(n,'phi_min_res_exog') ;
co2_cap_exog(n) = data_2dim(n,'co2_cap_exog') ;
phi_pro_load(n) = data_2dim(n,'phi_pro_load') ;
ev_quant(n) = data_2dim(n,'ev_quant') ;

*set used for report
Set feat_included(features);
feat_included(features) = yes$(sum(n, feat_node(features,n))) ;

***** Data iteration **********************************************************

%iter_data_switch%$ontext

Sets
scenario
identifer
;

Parameters
iter_data(h,identifer,scenario)
;

$GDXin "%data_it_gdx%"

$load scenario
$load identifer
$load iter_data
;

$ontext
$offtext

*******************************************************************************
