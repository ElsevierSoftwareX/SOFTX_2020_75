.. _eq_balance:

Energy Balance
===============
The energy balance ensures that electricity supply and demand perfectly match in every hour.

Demand
------

Load
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

    con1a_bal(n,hh) ..
        ( 1 - phi_pro_load(n) ) * d(n,hh) + sum( map_n_sto(n,sto) , STO_IN(n,sto,hh) )

 This is the total electric load of the traditional power sector, i.e., without sector coupling, and also excluding prosumage households, plus electricity storage loading.

Demand side management (DSM)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

    %DSM%$ontext
        + sum( map_n_dsm(n,dsm_shift) , DSM_UP_DEMAND(n,dsm_shift,hh) )
    $ontext
    $offtext

This is upward load shifting, i.e., a temporal increase of the electric load, in case the DSM module is switched on.

Endogenous electric vehicles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

    %EV_endogenous%$ontext
        + sum( map_n_ev(n,ev) , EV_CHARGE(n,ev,hh) )
    $ontext
    $offtext

This term reflects the electricity that flows into electric vehicle batteries, be it for driving use, or for feeding back electricity to the grid at a later point in time.

Prosumage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::
       
    %prosumage%$ontext
        + G_MARKET_M2PRO(n,hh)
        + sum( map_n_sto_pro(n,sto) , STO_IN_M2PRO(n,sto,hh))
        + sum( map_n_sto_pro(n,sto) , STO_IN_M2M(n,sto,hh))
    $ontext
    $offtext

These terms reflect electricity flowing from the grid to prosumage households, either for direct consumption, or into the prosumage battery for later use in the household or for feeding it back to the electricity grid.

Heat
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

    %heat%$ontext
        + sum( (bu,ch) , theta_dir(n,bu,ch) * (H_DIR(n,bu,ch,hh) + H_DHW_DIR(n,bu,ch,hh)) )
        + sum( (bu,ch) , theta_sets(n,bu,ch) * (H_SETS_IN(n,bu,ch,hh) + H_DHW_AUX_ELEC_IN(n,bu,ch,hh)) )
        + sum( (bu,hp) , theta_hp(n,bu,hp) * H_HP_IN(n,bu,hp,hh) )
        + sum( (bu,hel) , theta_elec(n,bu,hel) * H_ELECTRIC_IN(n,bu,hel,hh) )
    $ontext
    $offtext
                
        =E=

These terms represent the electric load of residential power-to-heat options, including direct electric space and water heating, smart electric thermal storage heaters and related hot water heating systems, heat pumps, and hybrid heating systems.

Supply
------

Base module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dispatchable power plants
******************************

.. code::
    
    sum(map_n_tech(n,dis) , G_L(n,dis,hh))

This is dispatchable generation.

Non-dispatchable power plants
******************************

.. code::

    + sum(map_n_tech(n,nondis) , G_RES(n,nondis,hh))

This is variable renewable generation.

Storage
******************************

.. code::

    + sum(sto , STO_OUT(n,sto,hh))
  
This is generation from electricity storage facilities.

Reservoirs
******************************

.. code::

    + sum(map_n_rsvr(n,rsvr) , RSVR_OUT(n,rsvr,hh))

This is electricity generation from hydro reservoirs.

Cross-nodal flow
******************************

.. code::

    + sum( map_l(l) , inc(l,n) * F(l,hh))
  
Net electricity imports from other nodes.

Reserves
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

    %reserves%$ontext
    *Balancing Correction Factor
            + sum( map_n_tech(n,dis) ,
            sum( reserves_do ,  RP_DIS(n,reserves_do,dis,hh) * phi_reserves_call(n,reserves_do,hh))
            - sum( reserves_up ,  RP_DIS(n,reserves_up,dis,hh) * phi_reserves_call(n,reserves_up,hh))
            )
    $ontext
    $offtext

This correction factor for dispatchable generators makes sure that their contribution to reserve provision is properly accounted for in the energy balance.

Demand side management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^
.. code::

    %DSM%$ontext
        + sum( map_n_dsm(n,dsm_curt) , DSM_CU(n,dsm_curt,hh))
        + sum( map_n_dsm(n,dsm_shift) , DSM_DO_DEMAND(n,dsm_shift,hh))
    $ontext
    $offtext

In case the DSM module is switched on, this term adds load curtailment and downward load shifting.

Endogenous electric vehicles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::
    
    %EV_endogenous%$ontext
        + sum( map_n_ev(n,ev) , EV_DISCHARGE(n,ev,hh) )
    $ontext
    $offtext

This term reflects electricity that flows back from electric vehicle batteries to the grid (vehicle-to-grid).

Prosumage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

    %prosumage%$ontext
        + sum( map_n_res_pro(n,res) , G_MARKET_PRO2M(n,res,hh) )
        + sum( map_n_sto_pro(n,sto) , STO_OUT_PRO2M(n,sto,hh))
        + sum( map_n_sto_pro(n,sto) , STO_OUT_M2M(n,sto,hh))
    $ontext
    $offtext

This is electricity that flows from prosumage households to the grid, either directly from the PV installation or from the battery, in the latter case either electricity that was generated in the decentralized PV installation, or that was previously charged from the grid.

Infeasibility
-------------

.. code::
    
    + G_INFES(n,hh)
    ;

In case an infeasibility variable is used, it adds to the supply-side of the energy balance to ensure feasible solutions in capacity-constrained settings.
