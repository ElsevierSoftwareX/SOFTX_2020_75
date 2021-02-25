.. _eq_balance:

Energy Balance
---------------

.. code::

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