.. _eq_res_share:

************************
Renewable Energy Share
************************

In this section, we present the formulation *con5a_minRes_0a* of our renewable energy share constraint. Descriptions of other available RES share constraints, the effect of which we explored in a separate analysis, and which are described in :ref:`this section <constraints>`, will be added soon.

----------------------------
con5a_minRes_0a
----------------------------


Left-hand side: renewable energy generation
^^^^^^^^^^^^^^^^^^

Base
*****

.. code::

    con5a_minRes_0a(n)..
        sum( h ,
        + sum( map_n_tech(n,res), sum( dis$(sameas(res,dis)), G_L(n,dis,h)))
        + sum( map_n_tech(n,nondis), G_RES(n,nondis,h))
        + sum( map_n_rsvr(n,rsvr), RSVR_OUT(n,rsvr,h))
This is yearly electricity generation of all variable and dispatchable renewable energy sources, excluding renewable curtailment and prosumage installations.

Reserves
********
    
.. code::
        
    %reserves%$ontext
         - sum( reserves_do , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_do,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_do,rsvr,h))) * phi_reserves_cal(n,    reserves_do,h))
         + sum( reserves_up , (sum( map_n_tech(n,nondis) , RP_NONDIS(n,reserves_up,nondis,h)) + sum( map_n_rsvr(n,rsvr) , RP_RSVR(n,reserves_up,rsvr,h))) * phi_reserves_cal(n,    reserves_up,h))
    $ontext
    $offtext
This is a correction for activated balancing reserves provided by hydro reservoirs.

Prosumage
*********
.. code::

    %prosumage%$ontext
        + sum( map_n_sto_pro(n,sto) , STO_OUT_PRO2PRO(n,sto,h) + STO_OUT_PRO2M(n,sto,h)) + sum( map_n_res_pro(n,res) , G_MARKET_PRO2M(n,res,h) + G_RES_PRO(n,res,h))
    $ontext
    $offtext
    )
This is the yearly sum of decentralized renewable generation in prosumage installations, which is only relevant if the prosumage module is switched on.

Right-hand side: reference
^^^^^^^^^^

RES share
*********

.. code::        

    =G= phi_min_res * phi_min_res_exog(n) 
These two factors specify the renewable share. One of them is usually 1, ad the other is a real number between 0 and 1. Note that one factor would suffice; there are two factors for legacy reasons related to the GAMS-based model.


Load, storage losses, and consumption of electric vehicles
***************************************************************

.. code::        
    
                                         * sum( h ,
    + d(n,h)
    + sum( map_n_sto(n,sto) , STO_IN(n,sto,h) - STO_OUT(n,sto,h))
    %EV_endogenous%$ontext
            + sum( map_n_ev(n,ev), EV_CHARGE(n,ev,h) - EV_DISCHARGE(n,ev,h))
    $ontext
    $offtext
            )
    ;

The renewable share shown above applies to the sum of (conventional) electric load, electricity storage losses, and electricity consumed by electric vehicles (also including charging losses). Please note that this formulation may result in unintended storage cycling during periods of renewable curtailment, and may require additional terms if othe sector coupling options are also used. An update and some guidance for good modeling practice in this respect will be added here soon.
