.. _principal_equations:

******************************
Principal equations
******************************

Explaination to be added; possibly latex code to be added as well.

Objective Function
-------------------

.. code:: 

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


Renewable Energy constraint
----------------------------

