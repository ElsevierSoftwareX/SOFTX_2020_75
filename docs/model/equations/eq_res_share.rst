.. _eq_res_share:

************************
Renewable Energy Share
************************

In this section, we present the formulation *con5a_minRes_0a* of our renewable energy share constraint. Descriptions of other available RES share constraints, as described in :ref:`this section <constraints>`, will be added soon.

----------------------------
con5a_minRes_0a
----------------------------

*Detailed explanations on every section of the equations will be added soon.*

Energy generation
^^^^^^^^^^^^^^^^^^

Base
*****

.. code::

    con5a_minRes_0a(n)..
    * demand (load + ev) and losses (storage + ev battery) are fulfilled with the minRES share
        
        sum( h ,
        + sum( map_n_tech(n,res), sum( dis$(sameas(res,dis)), G_L(n,dis,h)))
        + sum( map_n_tech(n,nondis), G_RES(n,nondis,h))
        + sum( map_n_rsvr(n,rsvr), RSVR_OUT(n,rsvr,h))

Reserves
********
    
.. code::
        
    %reserves%$ontext
         - sum( reserves_do , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_do,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_do,rsvr,h))) * phi_reserves_cal(n,    reserves_do,h))
         + sum( reserves_up , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_up,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_up,rsvr,h))) * phi_reserves_cal(n,    reserves_up,h))
    $ontext
    $offtext

Prosumage
*********
.. code::

    %prosumage%$ontext
        + sum( map_n_sto_pro(n,sto) , STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h)) + sum( map_n_res_pro(n,res) , G_MARKET_PRO2M(n,res,h) + G_RES_PRO(n,res,h))
    $ontext
    $offtext
    )

Reference
^^^^^^^^^^

RES share
*********

.. code::        

    =G= phi_min_res * phi_min_res_exog(n) 
 
Demand
******

Load and storage losses
++++++++++++++++++++++++

.. code::        
    
                                         * sum( h ,
    + d(n,h)
    + sum( map_n_sto(n,sto) , STO_IN(n,sto,h) - STO_OUT(n,sto,h))

Charging losses of endogenous electric vehicles
++++++++++++++++++++++++++++++++++++++++++++++++

.. code::        

    %EV_endogenous%$ontext
            + sum( map_n_ev(n,ev), EV_CHARGE(n,ev,h) - EV_DISCHARGE(n,ev,h))
    $ontext
    $offtext
            )
    ;