.. _eq_objective:

Objective Function
==================

The objective function, which is minimized by the model, consists of several cost components which are explained subsequently.

Variable costs
------------------

Base
****

.. code::

    Z = E =
                sum( (h,map_n_tech(n,dis)) , c_m(n,dis)*G_L(n,dis,h) )
            + sum( (h,map_n_tech(n,dis))$(ord(h)>1) , c_up(n,dis)*G_UP(n,dis,h) )
            + sum( (h,map_n_tech(n,dis)) , c_do(n,dis)*G_DO(n,dis,h) )
            + sum( (h,map_n_tech(n,nondis)) , c_cu(n,nondis)*CU(n,nondis,h) )
            + sum( (h,map_n_sto(n,sto)) , c_m_sto(n,sto) * ( STO_OUT(n,sto,h) + STO_IN(n,sto,h) ) )
        
The function value ``Z``, which reflects overall system costs, is made up of various additive terms. 

For the following terms, sums are formed as products of a cost parameter and a variable and run over every hour `h` as well as all countries `n`. The objective function includes:

* the sum of variable costs of conventional power plants (``sum( (h,map_n_tech(n,dis)) , c_m(n,dis)*G_L(n,dis,h) )``), where ``c_m(n,dis)`` is the variable cost parameter of dispatchable technology ``dis`` in country ``n`` and ``G_L(n,dis,h)`` the generation of that technology in that country in hour ``h``. To reduce the model size, the function `map_n_tech(n, dis)` makes sure that only those generation technologies are considered that are actually available in the respective country. Similar mapping functions are used in the following in numerous instances.
* the costs related to changing the (aggregate) generation of dispatchable power plants (``G_UP`` and ``G_DO``)
* the costs attached to curtailment ``CU`` (variable) and ``c_cu`` (parameter) for non-dispatchable technologies ``nondis``.

*Further explanations will be added soon.*

DSM
****

.. code::   

    %DSM%$ontext

        + sum( (h,map_n_dsm(n,dsm_curt)) , c_m_dsm_cu(n,dsm_curt) * DSM_CU(n,dsm_curt,h) )
        + sum( (h,map_n_dsm(n,dsm_shift)) , c_m_dsm_shift(n,dsm_shift) * DSM_UP_DEMAND(n,dsm_shift,h) )
        + sum( (h,map_n_dsm(n,dsm_shift)) , c_m_dsm_shift(n,dsm_shift) * DSM_DO_DEMAND(n,dsm_shift,h) )

    $ontext
    $offtext
In case the demand-side management (DSM) module is switched on, the objective function also includes the variable costs of load curtailment as well as of upward and downward load shifting.

Endogenous electric vehicles
*****************************

.. code::   

    %EV_endogenous%$ontext

        + sum( (h,map_n_ev(n,ev)) , c_m_ev(n,ev) * EV_DISCHARGE(n,ev,h) )
        + sum( (h,map_n_ev(n,ev)) , pen_phevfuel(n,ev) * EV_PHEVFUEL(n,ev,h) )

    $ontext
    $offtext
If the electric vehicle module with endogenous vehicle charging and discharging decisions is switched on, variable costs of discharching electricity from vehicles to the grid are added to the objective function. A penalty for fuel use in plug-in hybrid electric vehicles may also be included, which can minimize the non-electric use of these vehicles.

Investment
-----------

Base
****

.. code::   

    + sum( map_n_tech(n,tech) , c_i(n,tech)*N_TECH(n,tech) )
    + sum( map_n_tech(n,tech) , c_fix(n,tech)*N_TECH(n,tech) )
    + sum( map_n_sto(n,sto) , c_i_sto_e(n,sto)*N_STO_E(n,sto) )
    + sum( map_n_sto(n,sto) , c_fix_sto(n,sto)/2*(N_STO_P(n,sto)+N_STO_E(n,sto)) )
    + sum( map_n_sto(n,sto) , c_i_sto_p(n,sto)*N_STO_P(n,sto) )

DSM
***

.. code::   

    %DSM%$ontext

        + sum( map_n_dsm(n,dsm_curt) , c_i_dsm_cu(n,dsm_curt)*N_DSM_CU(n,dsm_curt) )
        + sum( map_n_dsm(n,dsm_curt) , c_fix_dsm_cu(n,dsm_curt)*N_DSM_CU(n,dsm_curt) )
        + sum( map_n_dsm(n,dsm_shift) , c_i_dsm_shift(n,dsm_shift)*N_DSM_SHIFT(n,dsm_shift) )
        + sum( map_n_dsm(n,dsm_shift) , c_fix_dsm_shift(n,dsm_shift)*N_DSM_SHIFT(n,dsm_shift) )

    $ontext
    $offtext

Reserves
********
.. code::   

    %reserves%$ontext

        + sum( (h,map_n_sto(n,sto),reserves_up) , phi_reserves_call(n,reserves_up,h) * c_m_sto(n,sto) * (RP_STO_OUT(n,reserves_up,sto,h) - RP_STO_IN(n,reserves_up,sto,h)) )
        - sum( (h,map_n_sto(n,sto),reserves_do) , phi_reserves_call(n,reserves_do,h) * c_m_sto(n,sto) * (RP_STO_OUT(n,reserves_do,sto,h) - RP_STO_IN(n,reserves_do,sto,h)) )
        + sum( (h,map_n_rsvr(n,rsvr),reserves_up) , RP_RSVR(n,reserves_up,rsvr,h) * phi_reserves_call(n,reserves_up,h) * c_m_rsvr(n,rsvr) )
        - sum( (h,map_n_rsvr(n,rsvr),reserves_do) , RP_RSVR(n,reserves_do,rsvr,h) * phi_reserves_call(n,reserves_do,h) * c_m_rsvr(n,rsvr) )

    $ontext
    $offtext
    %reserves%$ontext

Endogenous electric vehicles
****************************

.. code::   

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

Prosumage
*********

.. code::   

    %prosumage%$ontext

        + sum( map_n_res_pro(n,res) , c_i(n,res)*N_RES_PRO(n,res) )
        + sum( map_n_res_pro(n,res) , c_fix(n,res)*N_RES_PRO(n,res) )

        + sum( map_n_sto_pro(n,sto) , c_i_sto_e(n,sto)*N_STO_E_PRO(n,sto) )
        + sum( map_n_sto_pro(n,sto) , c_fix_sto(n,sto)/2*(N_STO_P_PRO(n,sto) + N_STO_E_PRO(n,sto)) )
        + sum( map_n_sto_pro(n,sto) , c_i_sto_p(n,sto)*N_STO_P_PRO(n,sto) )

        + sum( (h,map_n_sto_pro(n,sto)) , c_m_sto(n,sto) * ( STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_M2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h) + STO_OUT_M2M(n,sto,h) 
        + sum( res , STO_IN_PRO2PRO(n,res,sto,h) + STO_IN_PRO2M(n,res,sto,h)) + STO_OUT_PRO2M(n,sto,h) + STO_OUT_M2M(n,sto,h) ) )

    $ontext
    $offtext

NTC
***

.. code::   

    + sum( map_l(l) , c_i_ntc(l) * NTC(l)*dist(l) )


Reservoirs
**********

.. code::   

    + sum( (h,map_n_rsvr(n,rsvr)), c_m_rsvr(n,rsvr) * RSVR_OUT(n,rsvr,h) )
    + sum( map_n_rsvr(n,rsvr) , c_i_rsvr_e(n,rsvr) * N_RSVR_E(n,rsvr) )
    + sum( map_n_rsvr(n,rsvr) , c_i_rsvr_p(n,rsvr) * N_RSVR_P(n,rsvr) )
    + sum( map_n_rsvr(n,rsvr) , c_fix_rsvr(n,rsvr) * N_RSVR_P(n,rsvr) )
  
Heat
****

.. code::   

    %heat%$ontext

        + sum( (h,n,bu,hfo) , pen_heat_fuel(n,bu,hfo) * H_STO_IN_FOSSIL(n,bu,hfo,h))

    $ontext
    $offtext

Infeasibility
-------------

.. code::   

    + sum( (h,n) , c_infes * G_INFES(n,h) )

    ;
