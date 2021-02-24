# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""

"""
import base64
import os
import re
import pickle
import json
import uuid

import streamlit as st
from streamlit.hashing import _CodeHasher
import pandas as pd

from ..config import settings
from ..scripts import runopt
from ..scripts.report import SymbolsHandler, Symbol
from .plots import get_rldc, plot_rldc, color_code, color

import contextlib
from functools import wraps
from io import StringIO
import plotly.express as px
import plotly.graph_objects as go


try:
    # After Streamlit 0.65
    from streamlit.report_thread import get_report_ctx
    from streamlit.server.server import Server

    st.set_page_config(
        page_title="DIETERpy",
        page_icon=":power:",
        layout="wide",
        initial_sidebar_state="auto",
    )
except ModuleNotFoundError:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server


def main():
    state = _get_state()
    pages = {
        "1. Settings": page_settings,
        "2. Optimization": page_optimization,
        "3. Report": page_report,
    }

    st.sidebar.title("Model steps")
    page = st.sidebar.radio("", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()


def page_settings(state):
    st.title(":wrench: Settings")
    st.sidebar.subheader("Settings Sections:")
    state.checkbox_proj_var = st.sidebar.checkbox(
        "Project Variables", state.checkbox_proj_var, key="checkbox_proj_var"
    )
    if state.checkbox_proj_var:
        st.header("Project variables:")
        if st.button("Read Saved Variables"):
            get_proj_var(state)
        edit_proj_var(state)
        if st.button("Save changes"):
            update_proj_var(state)

    # state.checkbox_itermain = st.sidebar.checkbox("Model Runs setup", state.checkbox_itermain, key='checkbox_itermain')
    # if state.checkbox_itermain:
    #     st.header("Under cosntruction!")


def page_optimization(state):
    st.title("Optimization")
    st.write(
        "You can run DIETER by clicking the button 'Run optimization'. The optimization process may take a long time, depending on the size of the problem. If it occurs any issue, this will be displayed below for its debugging."
    )

    if st.button("Run optimization"):
        st.write("Optimization in progress ...")
        stprint = capture_output(runopt.main)
        stprint()


def page_report(state):

    st.title(":chart_with_upwards_trend: Report")

    placeholder0 = st.empty()
    placeholder0.warning("Click on Load Data")
    data_load = False
    button = st.button("Load Data")
    if button:
        Symbols = get_results(state)
        state.dfs = make_symbol_df(Symbols)
        state.rldc_table, state.rldc_info = cache_rldc(Symbols)
        data_load = True
    state.flag = True if data_load else state.flag
    if not state.flag:
        st.stop()
    placeholder0.success("Data is now loaded")

    st.sidebar.header("Report Sections:")

    st.subheader("Summary Report")
    st.write("Scenarios setup, system costs and solver status")

    # Plotting summary table
    df = state.dfs["Total Costs"].sort_values("id")
    col_sorted = []
    for sort in ["id", "long_id"]:
        for col in df.columns:
            if col == sort:
                col_sorted.append(col)
    for col in df.columns:
        if col not in col_sorted:
            if col not in ["System Cost [bn €]", "solver_msg"]:
                col_sorted.append(col)
    col_sorted = col_sorted + ["System Cost [bn €]", "solver_msg"]
    df = df[col_sorted]
    fig = plotly_table(df)
    st.plotly_chart(fig, use_container_width=True)

    state.set_ids = [ids for ids in df["id"].unique()]
    state.selected_ids = st.multiselect(
        "Select the scenarios to be compared:", state.set_ids, state.set_ids
    )

    if st.sidebar.checkbox("Energy Balance Table"):
        st.write("Generation, demand, transmission and infeasibility [TWh]")
        figsummary = plotly_table(
            state.dfs["Summary"][
                state.dfs["Summary"]["id"].isin(state.selected_ids)
            ].sort_values(["id", "n"])
        )
        st.plotly_chart(figsummary, use_container_width=True)

    if st.sidebar.checkbox("Technology Capacity"):

        st.subheader("Power Capacity by Technology")

        radio_opt = st.radio(
            "Axis options", ["id:x,n:col", "id:x,n:row", "id:row,n:col"], 0, key="ra"
        )
        if radio_opt == "id:x,n:col":
            col = "n"
            row = None
            x = "id"
        elif radio_opt == "id:x,n:row":
            col = None
            row = "n"
            x = "id"
        elif radio_opt == "id:row,n:col":
            col = "n"
            row = "id"
            x = "tech"

        height = st.number_input("Height", 400, None, 600, 50, key="na")

        df_tech_p = tech_order(state.dfs["N_TECHt"])
        df_tech_p = df_tech_p[df_tech_p["id"].isin(state.selected_ids)].sort_values(
            by=["id", "n", "tech"], ascending=[True, True, False]
        )
        df_tech_p.loc[:, "value"] = df_tech_p["value"] * 1e-3  # from MW to GW

        map_color = {}
        for t in df_tech_p["tech"].unique():
            f = False
            for k in color_code():
                if k in t:
                    map_color[t] = color_code()[k][0]
                    f = True
                    break
            if not f:
                map_color[t] = None

        fig_tech_p = px.bar(
            df_tech_p,
            x=x,
            y="value",
            color="tech",
            barmode="relative",
            facet_row=row,
            facet_col=col,
            width=None,
            height=height,
            labels=dict(value="Power Capacity [GW]"),
            color_discrete_map=map_color,
        )
        # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        st.plotly_chart(fig_tech_p, use_container_width=True)

        st.subheader("Overall Power Capacity by Technology")

        height = st.number_input("Height", 400, None, 600, 50, key="ni")
        width = st.number_input("Width", 200, None, 400, 50, key="wi")

        df_tech_p_n = tech_order(state.dfs["agg_nN_TECHt"])
        df_tech_p_n = df_tech_p_n[df_tech_p_n["id"].isin(state.selected_ids)]
        df_tech_p_n.loc[:, "value"] = df_tech_p_n["value"] * 1e-3  # from MW to GW

        fig_tech_p_n = px.bar(
            df_tech_p_n,
            x="id",
            y="value",
            color="tech",
            barmode="relative",
            facet_row=None,
            facet_col=None,
            width=width,
            height=height,
            labels=dict(value="Power Capacity [GW]", tech="Technology"),
            color_discrete_map=map_color,
        )
        # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        st.plotly_chart(fig_tech_p_n, use_container_width=False)

    if st.sidebar.checkbox("Reservoir Capacity"):

        st.subheader("Reservoir Energy Capacity")

        radio_opt = st.radio(
            "Axis options", ["id:x,n:col", "id:x,n:row", "id:row,n:col"], 0, key="rc"
        )
        if radio_opt == "id:x,n:col":
            col = "n"
            row = None
            x = "id"
        elif radio_opt == "id:x,n:row":
            col = None
            row = "n"
            x = "id"
        elif radio_opt == "id:row,n:col":
            col = "n"
            row = "id"
            x = "rsvr"

        height = st.number_input("Height", 400, None, 600, 50, key="nc")

        df_rsvr_e = state.dfs["N_RSVR_E"][
            state.dfs["N_RSVR_E"]["id"].isin(state.selected_ids)
        ].sort_values(["id", "n"])
        df_rsvr_e.loc[:, "value"] = df_rsvr_e["value"] * 1e-3  # from MWh to GWh

        map_color = {}
        for t in df_rsvr_e["rsvr"].unique():
            f = False
            for k in color_code():
                if k in t:
                    map_color[t] = color_code()[k][0]
                    f = True
                    break
            if not f:
                map_color[t] = None

        fig_rsvr_e = px.bar(
            df_rsvr_e,
            x=x,
            y="value",
            color="rsvr",
            barmode="relative",
            facet_row=row,
            facet_col=col,
            width=None,
            height=height,
            labels=dict(value="Energy Capacity [GWh]"),
            color_discrete_map=map_color,
        )
        # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        st.plotly_chart(fig_rsvr_e, use_container_width=True)

    if st.sidebar.checkbox("Storage Capacity"):
        st.subheader("Storage Power Capacity")

        radio_opt = st.radio(
            "Axis options", ["id:x,n:col", "id:x,n:row", "id:row,n:col"], 0, key="rd"
        )
        if radio_opt == "id:x,n:col":
            col = "n"
            row = None
            x = "id"
        elif radio_opt == "id:x,n:row":
            col = None
            row = "n"
            x = "id"
        elif radio_opt == "id:row,n:col":
            col = "n"
            row = "id"
            x = "sto"

        height = st.number_input("Height", 400, None, 600, 50, key="nd")

        df_sto_p = state.dfs["N_STO_P"][
            state.dfs["N_STO_P"]["id"].isin(state.selected_ids)
        ].sort_values(["id", "n"])
        df_sto_p.loc[:, "value"] = df_sto_p["value"] * 1e-3  # from MW to GW

        fig_sto_p = px.bar(
            df_sto_p,
            x=x,
            y="value",
            color="sto",
            barmode="relative",
            facet_row=row,
            facet_col=col,
            width=None,
            height=height,
            labels=dict(value="Power Capacity [GW]"),
        )
        # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        st.plotly_chart(fig_sto_p, use_container_width=True)

        st.subheader("Overall Storage Power Capacity")

        height = st.number_input("Height", 400, None, 600, 50, key="nj")
        width = st.number_input("Width", 200, None, 400, 50, key="wj")

        df_sto_p_n = state.dfs["agg_nN_STO_P"]
        df_sto_p_n = df_sto_p_n[df_sto_p_n["id"].isin(state.selected_ids)]
        df_sto_p_n.loc[:, "value"] = df_sto_p_n["value"] * 1e-3  # from MW to GW

        fig_sto_p_n = px.bar(
            df_sto_p_n,
            x="id",
            y="value",
            color="sto",
            barmode="relative",
            facet_row=None,
            facet_col=None,
            width=width,
            height=height,
            labels=dict(value="Power Capacity [GW]", sto="Storage"),
        )
        # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        st.plotly_chart(fig_sto_p_n, use_container_width=False)

        st.subheader("Storage Energy Capacity")
        radio_opt = st.radio(
            "Axis options", ["id:x,n:col", "id:x,n:row", "id:row,n:col"], 0, key="re"
        )
        if radio_opt == "id:x,n:col":
            col = "n"
            row = None
            x = "id"
        elif radio_opt == "id:x,n:row":
            col = None
            row = "n"
            x = "id"
        elif radio_opt == "id:row,n:col":
            col = "n"
            row = "id"
            x = "sto"

        height = st.number_input("Height", 400, None, 600, 50, key="ne")

        df_sto_e = state.dfs["N_STO_E"][
            state.dfs["N_STO_E"]["id"].isin(state.selected_ids)
        ].sort_values(["id", "n"])
        df_sto_e.loc[:, "value"] = df_sto_e["value"] * 1e-3  # from MWh to GWh

        fig_sto_e = px.bar(
            df_sto_e,
            x=x,
            y="value",
            color="sto",
            barmode="relative",
            facet_row=row,
            facet_col=col,
            width=None,
            height=height,
            labels=dict(value="Energy Capacity [GWh]"),
        )
        # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        st.plotly_chart(fig_sto_e, use_container_width=True)

        st.subheader("Overall Storage Energy Capacity")

        height = st.number_input("Height", 400, None, 600, 50, key="nk")
        width = st.number_input("Width", 200, None, 400, 50, key="wk")

        df_sto_e_n = state.dfs["agg_nN_STO_E"]
        df_sto_e_n = df_sto_e_n[df_sto_e_n["id"].isin(state.selected_ids)]
        df_sto_e_n.loc[:, "value"] = df_sto_e_n["value"] * 1e-3  # from MWh to GWh

        fig_sto_e_n = px.bar(
            df_sto_e_n,
            x="id",
            y="value",
            color="sto",
            barmode="relative",
            facet_row=None,
            facet_col=None,
            width=width,
            height=height,
            labels=dict(value="Energy Capacity [GWh]", sto="Storage"),
        )
        # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        st.plotly_chart(fig_sto_e_n, use_container_width=False)

    if st.sidebar.checkbox("Transmission Capacity"):
        st.subheader("Transmission Power Capacity")

        radio_opt = st.radio(
            "Axis options", ["id:x,l:col", "id:x,l:row", "id:row,l:x"], 0, key="rf"
        )
        if radio_opt == "id:x,l:col":
            col = "l"
            row = None
            x = "id"
        elif radio_opt == "id:x,l:row":
            col = None
            row = "l"
            x = "id"
        elif radio_opt == "id:row,l:x":
            col = None
            row = "id"
            x = "l"

        height = st.number_input("Height", 400, None, 600, 50, key="nf")

        df_line_p = state.dfs["NTC"][
            state.dfs["NTC"]["id"].isin(state.selected_ids)
        ].sort_values("id")

        fig_line_p = px.bar(
            df_line_p,
            x=x,
            y="value",
            color="l",
            barmode="relative",
            facet_row=row,
            facet_col=col,
            width=None,
            height=height,
            labels=dict(value="Power Capacity [MW]"),
        )
        # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        st.plotly_chart(fig_line_p, use_container_width=True)

    if st.sidebar.checkbox("Electricity Generation"):
        st.subheader("Electricity generation by technology")

        radio_opt = st.radio(
            "Axis options", ["id:x,n:col", "id:x,n:row", "id:row,n:col"], 0, key="rg"
        )
        if radio_opt == "id:x,n:col":
            col = "n"
            row = None
            x = "id"
        elif radio_opt == "id:x,n:row":
            col = None
            row = "n"
            x = "id"
        elif radio_opt == "id:row,n:col":
            col = "n"
            row = "id"
            x = "tech"

        height = st.number_input("Height", 400, None, 600, 50, key="ng")

        state.gtech_y_bmode = st.radio("Bar mode", ["relative", "group"], 0)

        df_gtech_y = tech_order(state.dfs["agg_hG_TECHt"])
        df_gtech_y = df_gtech_y[df_gtech_y["id"].isin(state.selected_ids)]
        df_gtech_y.loc[:, "value"] = df_gtech_y["value"] * 1e-6  # from MWh to TWh

        map_color = {}
        for t in df_gtech_y["tech"].unique():
            f = False
            for k in color_code():
                if k in t:
                    map_color[t] = color_code()[k][0]
                    f = True
                    break
            if not f:
                map_color[t] = None

        fig_gtech_y = px.bar(
            df_gtech_y,
            x=x,
            y="value",
            color="tech",
            barmode=state.gtech_y_bmode,
            facet_row=row,
            facet_col=col,
            width=None,
            height=height,
            labels=dict(value="Electricity Generation [TWh]"),
            color_discrete_map=map_color,
        )
        # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        st.plotly_chart(fig_gtech_y, use_container_width=True)

        st.subheader("Overall Electricity Genearion by technology")

        height = st.number_input("Height", 400, None, 600, 50, key="nl")
        width = st.number_input("Width", 200, None, 400, 50, key="wl")

        df_gtech_n = tech_order(state.dfs["agg_h_nG_TECH"])
        infes_zero = (df_gtech_n[df_gtech_n["tech"] == "infes"]["value"] == 0.0).all()
        if infes_zero:
            df_gtech_n = df_gtech_n[df_gtech_n["tech"] != "infes"]
        df_gtech_n = df_gtech_n[df_gtech_n["id"].isin(state.selected_ids)]
        df_gtech_n.loc[:, "value"] = df_gtech_n["value"] * 1e-6  # from MWh to TWh

        fig_gtech_n = px.bar(
            df_gtech_n,
            x="id",
            y="value",
            color="tech",
            barmode="relative",
            facet_row=None,
            facet_col=None,
            width=width,
            height=height,
            labels=dict(value="Electricity Generation [TWh]", tech="Technology"),
            color_discrete_map=map_color,
        )
        # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        st.plotly_chart(fig_gtech_n, use_container_width=False)

    if st.sidebar.checkbox("Electricity Import-Export"):
        st.subheader("Electricity Import-Export")

        radio_opt = st.radio(
            "Axis options", ["id:x,n:col", "id:x,n:row", "id:row,n:col"], 0, key="rh"
        )
        if radio_opt == "id:x,n:col":
            col = "n"
            row = None
            x = "id"
        elif radio_opt == "id:x,n:row":
            col = None
            row = "n"
            x = "id"
        elif radio_opt == "id:row,n:col":
            col = "n"
            row = "id"
            x = "l"

        height = st.number_input("Height", 400, None, 600, 50, key="nh")

        # state.gtech_y_bmode = st.radio('Bar mode', ['relative', 'group'], 0)
        df_flow_y = state.dfs["agg_hFn"][
            state.dfs["agg_hFn"]["id"].isin(state.selected_ids)
        ].sort_values(["id", "n"])
        df_flow_y.loc[:, "value"] = df_flow_y["value"] * 1e-6  # from MWh to TWh

        fig_flow_y = px.bar(
            df_flow_y,
            x=x,
            y="value",
            color="l",
            barmode="relative",
            facet_row=row,
            facet_col=col,
            width=None,
            height=height,
            labels=dict(value="Energy [TWh]"),
        )
        # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        st.plotly_chart(fig_flow_y, use_container_width=True)

    state.checkbox_rldc = st.sidebar.checkbox(
        "Residual Load Duration Curve", state.checkbox_rldc, key="show_rldc"
    )
    if state.checkbox_rldc:
        st.subheader("Residual Load Duration Curve")
        generate_rldc(state)

    state.checkbox_others = st.sidebar.checkbox(
        "Other Plots", state.checkbox_others, key="show_other"
    )
    if state.checkbox_others:
        st.subheader("Other plots")

        st.write("Storage output")

        radio_opt = st.radio(
            "Axis options", ["id:x,n:col", "id:x,n:row", "id:row,n:col"], 0, key="rm"
        )
        if radio_opt == "id:x,n:col":
            col = "n"
            row = None
            x = "id"
        elif radio_opt == "id:x,n:row":
            col = None
            row = "n"
            x = "id"
        elif radio_opt == "id:row,n:col":
            col = "n"
            row = "id"
            x = "sto"

        height = st.number_input("Height", 400, None, 600, 50, key="nm")

        # state.sto_out_y_bmode = st.radio('Bar mode', ['relative', 'group'], 0)

        df_sto_out_y = state.dfs["agg_hSTO_OUT"]
        df_sto_out_y = df_sto_out_y[df_sto_out_y["id"].isin(state.selected_ids)]
        df_sto_out_y.loc[:, "value"] = df_sto_out_y["value"] * 1e-6  # from MWh to TWh

        fig_sto_out_y = px.bar(
            df_sto_out_y,
            x=x,
            y="value",
            color="sto",
            barmode="relative",
            facet_row=row,
            facet_col=col,
            width=None,
            height=height,
            labels=dict(value="Storage Output [TWh]"),
        )
        # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        st.plotly_chart(fig_sto_out_y, use_container_width=True)

        # st.write('Overall Electricity Genearion')

        # height = st.number_input('Height', 400, None, 600, 50, key='nl')
        # width = st.number_input('Width', 200, None, 400, 50, key='wl')

        # df_gtech_n = tech_order(state.dfs['agg_h_nG_TECH'])
        # infes_zero = (df_gtech_n[df_gtech_n['tech'] == 'infes']['value'] == 0.0).all()
        # if infes_zero:
        #     df_gtech_n = df_gtech_n[df_gtech_n['tech'] != 'infes']
        # df_gtech_n = df_gtech_n[df_gtech_n['id'].isin(state.selected_ids)]
        # df_gtech_n.loc[:,'value'] = df_gtech_n['value']*1e-6  # from MWh to TWh

        # fig_gtech_n = px.bar(df_gtech_n, x='id', y="value", color='tech', barmode='relative',
        #                                     facet_row=None, facet_col=None, width=width, height=height,
        #                                     labels=dict(value="Electricity Generation [TWh]", tech="Technology"), color_discrete_map=map_color)
        # # fig_tech_p.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        # st.plotly_chart(fig_gtech_n,use_container_width=False)

    state.checkbox_custom = st.sidebar.checkbox(
        "Custom Plots", state.checkbox_custom, key="show_custom"
    )
    if state.checkbox_custom:
        st.subheader("Custom plots")
        generate_df(state)

    # state.checkbox_other = st.sidebar.checkbox("Time-Series Plots", state.checkbox_other, key='show_other')
    # if state.checkbox_other:
    #     st.write('Time-Series Plots')
    #     generate_df(state)


def get_proj_var(state):
    df = pd.read_csv(os.path.join(settings.BASE_DIR_ABS, "project_variables.csv"))
    state.scenarios_iteration = (
        True
        if df[df["feature"] == "scenarios_iteration"]["value"].values[0].lower()
        == "yes"
        else False
    )
    state.skip_input = (
        True
        if df[df["feature"] == "skip_input"]["value"].values[0].lower() == "yes"
        else False
    )
    state.skip_iteration_data_file = (
        True
        if df[df["feature"] == "skip_iteration_data_file"]["value"].values[0].lower()
        == "yes"
        else False
    )
    state.base_year = int(df[df["feature"] == "base_year"]["value"].values[0])
    state.end_hour = df[df["feature"] == "end_hour"]["value"].values[0]
    state.dispatch_only = (
        True
        if df[df["feature"] == "dispatch_only"]["value"].values[0].lower() == "yes"
        else False
    )
    state.network_transfer = (
        True
        if df[df["feature"] == "network_transfer"]["value"].values[0].lower() == "yes"
        else False
    )
    state.no_crossover = (
        True
        if df[df["feature"] == "no_crossover"]["value"].values[0].lower() == "yes"
        else False
    )
    state.GUSS = (
        True
        if df[df["feature"] == "GUSS"]["value"].values[0].lower() == "yes"
        else False
    )
    state.GUSS_parallel = (
        True
        if df[df["feature"] == "GUSS_parallel"]["value"].values[0].lower() == "yes"
        else False
    )
    state.GUSS_parallel_threads = int(
        df[df["feature"] == "GUSS_parallel_threads"]["value"].values[0]
    )
    state.data_input_file = df[df["feature"] == "data_input_file"]["value"].values[0]
    state.time_series_file = df[df["feature"] == "time_series_file"]["value"].values[0]
    state.iteration_data_file = df[df["feature"] == "iteration_data_file"][
        "value"
    ].values[0]
    state.gdx_convert_parallel_threads = int(
        df[df["feature"] == "gdx_convert_parallel_threads"]["value"].values[0]
    )
    state.gdx_convert_to_csv = (
        True
        if df[df["feature"] == "gdx_convert_to_csv"]["value"].values[0].lower() == "yes"
        else False
    )
    state.gdx_convert_to_pickle = (
        True
        if df[df["feature"] == "gdx_convert_to_pickle"]["value"].values[0].lower()
        == "yes"
        else False
    )
    state.gdx_convert_to_vaex = (
        True
        if df[df["feature"] == "gdx_convert_to_vaex"]["value"].values[0].lower()
        == "yes"
        else False
    )
    state.report_data = (
        True
        if df[df["feature"] == "report_data"]["value"].values[0].lower() == "yes"
        else False
    )


def edit_proj_var(state):
    state.scenarios_iteration = st.checkbox(
        "1. Run several scenarios", state.scenarios_iteration
    )
    state.skip_input = st.checkbox(
        "2. Skip input excel to gdx conversion", state.skip_input
    )
    if not state.skip_input:
        state.data_input_file = st.text_input(
            "2.a Data-input file name", state.data_input_file or ""
        )
        state.time_series_file = st.text_input(
            "2.b Time-series file name", state.time_series_file or ""
        )
    state.skip_iteration_data_file = st.checkbox(
        "3. Skip time-series scenario excel to gdx conversion",
        state.skip_iteration_data_file,
    )
    if not state.skip_iteration_data_file:
        state.iteration_data_file = st.text_input(
            "3.a Time-series scenario file name", state.iteration_data_file or ""
        )
    option_year = [n for n in range(2010, 2101, 2)]
    state.base_year = st.selectbox(
        "4. Select year of data (check time-series excel file)",
        option_year,
        option_year.index(state.base_year) if state.base_year else 0,
    )
    state.end_hour = st.text_input(
        "5. Select optimization end hour (check time-series excel file)",
        state.end_hour,
        5,
    )
    state.dispatch_only = st.checkbox("6. Model - dispatch only", state.dispatch_only)
    state.network_transfer = st.checkbox(
        "7. Model - network transport", state.network_transfer
    )
    state.no_crossover = st.checkbox("8. No crossover", state.no_crossover)
    state.GUSS = st.checkbox("9. Run scenarios with GUSS Tool", state.GUSS)
    if state.GUSS:
        state.GUSS_parallel = st.checkbox(
            "9.a Solve scenarios in parallel", state.GUSS_parallel
        )
        if state.GUSS_parallel:
            state.GUSS_parallel_threads = st.slider(
                "Number of cores for parallel runs. To select the maximum number of cores choose zero.",
                0,
                10,
                state.GUSS_parallel_threads,
            )

    state.gdx_convert_to_csv = st.checkbox(
        "10. Convert symbols from GDX to CSV files", state.gdx_convert_to_csv
    )
    state.gdx_convert_to_vaex = st.checkbox(
        "11. Convert symbols from GDX to VAEX files", state.gdx_convert_to_vaex
    )
    state.gdx_convert_to_pickle = st.checkbox(
        "12. Convert symbols from GDX to pickle files", state.gdx_convert_to_pickle
    )
    if any(
        [
            state.gdx_convert_to_csv,
            state.gdx_convert_to_pickle,
            state.gdx_convert_to_vaex,
        ]
    ):
        state.gdx_convert_parallel_threads = st.slider(
            "Number of cores for parallel dgx files conversion. To select the maximum number of cores choose zero.",
            0,
            10,
            state.gdx_convert_parallel_threads,
        )
    state.report_data = st.checkbox(
        "13. Summarize symbols across scenarios (one table per symbol)",
        state.report_data,
    )
    if state.report_data:
        if not state.gdx_convert_to_pickle:
            st.error(
                "Error: To summarize symbols across scenarios, pickle files must be active (12.)"
            )


def update_proj_var(state):
    df = pd.read_csv(os.path.join(settings.BASE_DIR_ABS, "project_variables.csv"))
    dfn = df.copy()
    for k in state.__dict__["_state"]["data"].keys():
        for i, row in df.iterrows():
            if k == row["feature"]:
                if isinstance(state[k], str):
                    value = state[k]
                elif isinstance(state[k], int):
                    value = str(state[k])
                if value == "True":
                    dfn.loc[i, "value"] = "yes"
                elif value == "False":
                    dfn.loc[i, "value"] = "no"
                else:
                    dfn.loc[i, "value"] = value

    dfn.to_csv(
        os.path.join(settings.BASE_DIR_ABS, "project_variables.csv"), index=False
    )
    st.info("Project variables updated!")


def get_results(state):
    SH = SymbolsHandler("folder")
    symbols = {}
    try:
        symbols["feat_node"] = Symbol(
            "feat_node", "v", "", {"": "Binary []"}, symbol_handler=SH
        )
        symbols["features"] = symbols["feat_node"].df["features"].unique().to_list()
    except:
        symbols["features"] = []

    symbols["Z"] = Symbol("Z", "v", "€", {"€": "System Cost [€]"}, symbol_handler=SH)
    symbols["Z"].header_name = {"bn €": "System Cost [bn €]"}
    symbols["Z"].get("conversion_factors").update({"€": {"€": 1, "bn €": 1e-9}})
    # capacity variables
    symbols["N_TECH"] = Symbol(
        "N_TECH", "v", "MW", {"MW": "Power Capacity [MW]"}, symbol_handler=SH
    )
    symbols["N_STO_P"] = Symbol(
        "N_STO_P", "v", "MW", {"MW": "Power Capacity [MW]"}, symbol_handler=SH
    )
    symbols["N_STO_E"] = Symbol(
        "N_STO_E", "v", "MWh", {"MWh": "Energy [MWh]"}, symbol_handler=SH
    )
    symbols["N_RSVR_P"] = Symbol(
        "N_RSVR_P", "v", "MW", {"MW": "Power Capacity [MW]"}, symbol_handler=SH
    )
    symbols["N_RSVR_E"] = Symbol(
        "N_RSVR_E", "v", "MWh", {"MWh": "Energy [MWh]"}, symbol_handler=SH
    )
    symbols["NTC"] = Symbol(
        "NTC", "v", "MW", {"MW": "Installed Capacity [MW]"}, symbol_handler=SH
    )
    # Generation variables (h)
    symbols["STO_IN"] = Symbol(
        "STO_IN", "v", "MW", {"MW": "Load [MW]"}, symbol_handler=SH
    )
    symbols["STO_OUT"] = Symbol(
        "STO_OUT", "v", "MW", {"MW": "Load [MW]"}, symbol_handler=SH
    )
    symbols["G_L"] = Symbol("G_L", "v", "MW", {"MW": "Load [MW]"}, symbol_handler=SH)
    symbols["G_RES"] = Symbol(
        "G_RES", "v", "MW", {"MW": "Load [MW]"}, symbol_handler=SH
    )
    symbols["RSVR_OUT"] = Symbol(
        "RSVR_OUT", "v", "MW", {"MW": "Load [MW]"}, symbol_handler=SH
    )
    # Ancillary variables (h)
    symbols["G_INFES"] = Symbol(
        "G_INFES", "v", "MW", {"MW": "Load [MW]"}, symbol_handler=SH
    )
    symbols["CU"] = Symbol("CU", "v", "MW", {"MW": "Load [MW]"}, symbol_handler=SH)
    symbols["F"] = Symbol("F", "v", "MW", {"MW": "Load [MW]"}, symbol_handler=SH)
    # Parameters
    symbols["phi_res"] = Symbol(
        "phi_res", "v", "", {"": "Capacity Factor []"}, symbol_handler=SH
    )
    symbols["d"] = Symbol("d", "v", "MW", {"MW": "Load [MW]"}, symbol_handler=SH)
    symbols["inc"] = Symbol(
        "inc", "v", "", {"": "Incidence Index []"}, symbol_handler=SH
    )
    # Shadow prices
    symbols["con1a_bal"] = Symbol(
        "con1a_bal", "m", "€/MW", {"€/MW": "Shadow Price [€/MW]"}, symbol_handler=SH
    )
    # Features variables and parameters
    if "ev_endogenous" in symbols["features"]:
        symbols["EV_CHARGE"] = Symbol(
            "EV_CHARGE", "v", "MW", {"MW": "Load [MW]"}, symbol_handler=SH
        )
        symbols["EV_DISCHARGE"] = Symbol(
            "EV_DISCHARGE", "v", "MW", {"MW": "Load [MW]"}, symbol_handler=SH
        )
        symbols["eta_ev_in"] = Symbol(
            "eta_ev_in", "v", "", {"": "Efficincy []"}, symbol_handler=SH
        )
        symbols["eta_ev_out"] = Symbol(
            "eta_ev_out", "v", "", {"": "Efficincy []"}, symbol_handler=SH
        )
        if "ev_exogenous" in symbols["features"]:
            pass
    if "reserves" in symbols["features"]:
        pass
    if "prosumage" in symbols["features"]:
        pass
    if "dsm" in symbols["features"]:
        pass
    if "heat" in symbols["features"]:
        pass
    # Calculated symbols
    if "ev_endogenous" in symbols["features"]:
        symbols["agg_hEV_CHARGE"] = symbols["EV_CHARGE"].dimreduc("h")
        symbols["agg_hEV_CHARGE"].name = "EV_CHARGE"
        symbols["agg_hEV_DISCHARGE"] = symbols["EV_DISCHARGE"].dimreduc("h")
        symbols["agg_hEV_DISCHARGE"].name = "EV_DISCHARGE"
        symbols["agg_h_evEV_CHARGE"] = symbols["agg_hEV_CHARGE"].dimreduc("ev")
        symbols["agg_h_evEV_CHARGE"].name = "EV_CHARGE"
        symbols["agg_h_evEV_DISCHARGE"] = symbols["agg_hEV_DISCHARGE"].dimreduc("ev")
        symbols["agg_h_evEV_DISCHARGE"].name = "EV_DISCHARGE"
        symbols["ev_demand_losses"] = symbols["agg_h_evEV_CHARGE"] + (
            symbols["agg_h_evEV_DISCHARGE"] * -1
        )
        if "ev_exogenous" in symbols["features"]:
            pass
    if "reserves" in symbols["features"]:
        pass
    if "prosumage" in symbols["features"]:
        pass
    if "dsm" in symbols["features"]:
        pass
    if "heat" in symbols["features"]:
        pass
    # create RLDC
    symbols["T_RES"] = symbols["N_TECH"] * symbols["phi_res"]
    symbols["agg_techT_RES"] = symbols["T_RES"].dimreduc("tech")
    symbols["RLDC"] = symbols["d"] + (symbols["agg_techT_RES"] * -1)
    symbols["con1a_bal"] = symbols["con1a_bal"] * -1
    symbols["con1a_bal"].name = "con1a_bal"
    # create flow with nodes
    symbols["Fn"] = symbols["F"] * symbols["inc"]
    symbols["Fn"].name = "Flow"
    symbols["agg_hFn"] = symbols["Fn"].dimreduc("h")
    # create G_TECH from G_L, G_RES, RSVR_OUT, G_INFES -> RSVR_OUT convert dim to tech, G_INFES added new dim tech
    symbols["G_TECH"] = symbols["G_L"].concat(symbols["G_RES"])
    symbols["RSVR_OUTtech"] = symbols["RSVR_OUT"] * 1
    symbols["RSVR_OUTtech"].df = symbols["RSVR_OUTtech"].df.rename(
        columns={"rsvr": "tech"}
    )
    symbols["RSVR_OUTtech"].dims = symbols["G_TECH"].get("dims")
    symbols["G_TECH"] = symbols["G_TECH"].concat(symbols["RSVR_OUTtech"])
    symbols["G_INFEStech"] = symbols["G_INFES"] * 1
    symbols["G_INFEStech"].df.loc[:, "tech"] = "infes"
    symbols["G_INFEStech"].dims = symbols["G_TECH"].get("dims")
    symbols["G_TECH"] = symbols["G_TECH"].concat(symbols["G_INFEStech"])
    symbols["G_TECH"].name = "G_TECH"
    symbols["agg_hG_TECH"] = symbols["G_TECH"].dimreduc("h")
    # Aggregate CU from tech
    symbols["agg_techCU"] = symbols["CU"].dimreduc("tech")
    symbols["agg_techCU"].name = "CU"
    # Calculate storage losses aggregated on h
    symbols["agg_hSTO_IN"] = symbols["STO_IN"].dimreduc("h")
    symbols["agg_h_stoSTO_IN"] = symbols["agg_hSTO_IN"].dimreduc("sto")
    symbols["agg_hSTO_OUT"] = symbols["STO_OUT"].dimreduc("h")
    symbols["agg_h_stoSTO_OUT"] = symbols["agg_hSTO_OUT"].dimreduc("sto")
    symbols["storage_losses"] = symbols["agg_h_stoSTO_IN"] + (
        symbols["agg_h_stoSTO_OUT"] * -1
    )
    # Determine total demand = demand + losses
    symbols["agg_hD"] = symbols["d"].dimreduc("h")
    symbols["total_demand"] = symbols["agg_hD"] + symbols["storage_losses"]
    if "ev_endogenous" in symbols["features"]:
        symbols["total_demand"] = symbols["total_demand"] + symbols["ev_demand_losses"]
    # Include rsvr_p to N_TECH
    symbols["N_RSVR_Pt"] = symbols["N_RSVR_P"] * 1
    symbols["N_RSVR_Pt"].df = symbols["N_RSVR_Pt"].df.rename(columns={"rsvr": "tech"})
    symbols["N_RSVR_Pt"].dims = symbols["N_TECH"].get("dims")
    symbols["N_TECHt"] = symbols["N_TECH"].concat(symbols["N_RSVR_Pt"])
    # Aggregate all nodes
    symbols["agg_nN_TECHt"] = symbols["N_TECHt"].dimreduc("n")
    symbols["agg_nN_STO_P"] = symbols["N_STO_P"].dimreduc("n")
    symbols["agg_nN_STO_E"] = symbols["N_STO_E"].dimreduc("n")
    symbols["agg_h_nG_TECH"] = symbols["agg_hG_TECH"].dimreduc("n")
    symbols["agg_h_nSTO_OUT"] = symbols["agg_hSTO_OUT"].dimreduc("n")

    return symbols


def generate_df(state):
    options = [
        "Z",
        "N_TECH",
        "N_STO_P",
        "N_STO_E",
        "N_RSVR_P",
        "N_RSVR_E",
        "NTC",
        "agg_hEV_CHARGE",
        "agg_hEV_DISCHARGE",
        "agg_hFn",
        "agg_hSTO_IN",
        "agg_hSTO_OUT",
        "agg_hG_TECHt",
        "share",
    ]
    names = [selected for selected in list(state.dfs.keys()) if selected in options]
    text = st.selectbox("Symbol Name", names, 0)
    df = state.dfs[text].astype("object").fillna(0)
    state.chart_type = st.radio("Chart type:", tuple(["Bar", "Line"]))
    columns = df.columns.to_list()
    state.x_gtech = st.selectbox("X Axis:", [None] + columns, 0)
    state.color_gtech = st.selectbox("Color:", [None] + columns, 0)
    state.row_gtech = st.selectbox("Row Section:", [None] + columns, 0)
    state.col_gtech = st.selectbox("Column Section:", [None] + columns, 0)
    if state.chart_type == "Bar":
        state.barmode_gtech = st.selectbox("Bar Mode:", ["relative", "group"], 0)

    if st.button("Show Plot", key="b_other"):
        if state.chart_type == "Line":
            fig = px.line(
                df,
                x=state.x_gtech,
                y="value",
                color=state.color_gtech,
                facet_row=state.row_gtech,
                facet_col=state.col_gtech,
                width=None,
                height=None,
            )
            # fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
            st.plotly_chart(fig, use_container_width=True)
        elif state.chart_type == "Bar":
            fig = px.bar(
                df,
                x=state.x_gtech,
                y="value",
                color=state.color_gtech,
                barmode=state.barmode_gtech,
                facet_row=state.row_gtech,
                facet_col=state.col_gtech,
                width=None,
                height=None,
            )
            # fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
            st.plotly_chart(fig, use_container_width=True)


def generate_rldc(state):
    state.options_id = list(state.rldc_table["id"].unique())
    state.scen = st.selectbox("Scenario name:", state.options_id, 0)
    state.options_ctr = list(
        state.rldc_table[state.rldc_table["id"] == state.scen]["n"].unique()
    )
    state.country = st.selectbox("Country code:", state.options_ctr, 0)
    df = state.rldc_table.query(
        f" id == '{state.scen}' & n == '{state.country}'"
    ).round(1)
    raw_tech_opt = [
        tech
        for tech in df.loc[:, (df != 0).any(axis=0)].columns.to_list()
        if tech not in ["id", "n", "h", "shadow", "RLDC", "hr"]
    ]
    state.options_tech = [tech for tech in state.rldc_info if tech in raw_tech_opt]
    max_rng = max(list(df["h"].unique()))
    state.tech_order = st.multiselect(
        "Sort technologies to display", state.options_tech, state.options_tech
    )
    state.rg0 = st.number_input("Select starting hour:", 1, max_rng - 1, 1, 1)
    state.rg1 = st.number_input("Select ending hour:", 2, max_rng, max_rng, 1)
    state.shadow = st.checkbox("Show shadow price", False)

    if st.button("Show Plot", key="b_rldc"):
        ch, fig2 = plot_rldc(
            df,
            state.rg0,
            state.rg1,
            state.scen,
            state.country,
            state.shadow,
            state.tech_order,
            state.rldc_info,
        )
        st.pyplot(fig2)
        # st.dataframe(state.ch[0:8])
        # keep running forever
        download_button_str = download_button(
            ch, "rldc.csv", "Download", pickle_it=False
        )
        st.markdown(download_button_str, unsafe_allow_html=True)


@st.cache(suppress_st_warning=True)
def make_symbol_df(symbols):
    dfs = {}
    for k, v in symbols.items():
        if k != "features":
            dfs[k] = v.df.copy().astype("object").fillna(-1)

    # Add custom df
    # Data for the first chart-table
    dfs["Total Costs"] = symbols["Z"].showm("bn €").reset_index().round(2)

    # Data for total generation, including columns with generation type, res & non-res
    df = symbols["G_TECH"].dimreduc("h").df
    infes_zero = (df[df["tech"] == "infes"]["value"] == 0.0).all()
    if infes_zero:
        df = df[df["tech"] != "infes"]
    df.loc[
        df["tech"].isin(["pv", "ror", "rsvr", "wind_off", "wind_on", "bio"]), "type"
    ] = "Renewable"
    df.loc[
        df["tech"].isin(["CCGT", "OCGT", "hc", "lig", "nuc", "oil", "other"]), "type"
    ] = "Non-Renewable"

    dfs["agg_hG_TECHt"] = df
    # Data for summary table => Balance
    pt = df.pivot_table(index=["id", "n"], columns="type", values="value", aggfunc=sum)
    dfs["share"] = (
        (pt.apply(lambda r: r / r.sum(), axis=1) * 100)
        .round(1)
        .stack()
        .reset_index()
        .rename(columns={0: "value"})
    )

    demand_gen = (
        symbols["total_demand"]
        .df.set_index(["id", "n"])
        .rename(columns={"value": "Total Demand"})
        .drop("symbol", axis=1)
        .join(
            pt.rename(
                columns={"Renewable": "Renewable", "Non-Renewable": "Non-Renewable"}
            )
        )
    )
    demand_gen.loc[:, "Total Generation"] = demand_gen[
        ["Renewable", "Non-Renewable"]
    ].sum(axis=1)
    demand_gen.loc[:, "Demand"] = symbols["agg_hD"].df.set_index(["id", "n"])["value"]
    demand_gen.loc[:, "Storage Losses"] = symbols["storage_losses"].df.set_index(
        ["id", "n"]
    )["value"]
    demand_gen.loc[:, "Net Import-Export"] = (
        symbols["Fn"].dimreduc("h").dimreduc("l").df.set_index(["id", "n"])["value"]
    )
    demand_gen.loc[:, "Infeasibility"] = (
        symbols["G_INFES"].dimreduc("h").df.set_index(["id", "n"])["value"]
    )

    try:
        demand_gen.loc[:, "EV Demand and Losses"] = symbols[
            "ev_demand_losses"
        ].df.set_index(["id", "n"])["value"]
    except:
        pass
    dem_gen_cols = []
    for header in [
        "Demand",
        "EV Demand and Losses",
        "Storage Losses",
        "Total Demand",
        "Non-Renewable",
        "Renewable",
        "Total Generation",
        "Net Import-Export",
        "Infeasibility",
    ]:
        for col in demand_gen.columns:
            if col == header:
                dem_gen_cols.append(col)

    summary = demand_gen[dem_gen_cols] * 1e-6

    summary.loc[:, "Demand - Gen"] = (
        summary["Total Demand"] - summary["Total Generation"]
    )
    dfs["Summary"] = summary.round(2).reset_index()
    return dfs


@st.cache(suppress_st_warning=True)
def cache_rldc(SymbolObjects):
    return get_rldc(SymbolObjects)


def display_state_values(state):
    st.write("Input state:", state.input)
    st.write("Slider state:", state.slider)
    st.write("Radio state:", state.radio)
    st.write("Checkbox state:", state.checkbox)
    st.write("Selectbox state:", state.selectbox)
    st.write("Multiselect state:", state.multiselect)
    for i in range(3):
        st.write(f"Value {i}:", state[f"State value {i}"])
    if st.button("Clear state"):
        state.clear()


def tech_order(df):

    order = [
        "wind_on",
        "wind_off",
        "pv",
        "ror",
        "rsvr",
        "bio",
        "nuc",
        "oil",
        "OCGT",
        "CCGT",
        "other",
        "hc",
        "lig",
    ]
    for head in df["tech"].unique():
        if head not in order:
            order.append(head)

    t = pd.CategoricalDtype(categories=order, ordered=True)
    df["tech"] = pd.Series(df["tech"], dtype=t)
    return df.sort_values(by=["id", "tech"], ascending=[True, False]).copy()


def download_button(
    object_to_download,
    download_filename: str,
    button_text: str,
    pickle_it: bool = False,
):
    """Generates a link to download the given object_to_download.

    Args:
        object_to_download ([type]): The object to be downloaded.
        download_filename (str): Filename and extension of file.
        button_text (str): Text to display on download button
        pickle_it (bool, optional): If True, pickle file. Defaults to False.

    Returns:
        [type]: the anchor tag to download object_to_download

    Examples:
        >>> download_button(your_df, 'YOUR_DF.csv', 'Click to download data!')
        >>> download_button(your_str, 'YOUR_STRING.txt', 'Click to download text!')
    """
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None

    else:
        if isinstance(object_to_download, bytes):
            pass

        elif isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub("\d+", "", button_uuid)

    custom_css = f"""
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;

            }}
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = (
        custom_css
        + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'
    )

    return dl_link


def plotly_table(df):
    col_order = [i for i in range(0, len(df.columns))]
    col_strlen = [len(col) for col in df.columns]
    col_elemlen = [
        max(df[col].apply(lambda x: len(x)).values)
        if isinstance(df[col].unique()[0], str)
        else max(df[col].apply(lambda x: len(str(x))).values)
        for col in df.columns
    ]
    col_ziplen = [
        max(tup) + 2 if i in [0, 1] else max(tup)
        for i, tup in enumerate(zip(col_strlen, col_elemlen))
    ]
    strlensum = sum(col_ziplen)
    col_strperc = [lencol / strlensum for lencol in col_ziplen]
    col_index = [i for i in range(0, len(df.columns))]

    fig = go.Figure(
        data=[
            go.Table(
                columnorder=col_index,
                columnwidth=col_strperc,
                header=dict(values=list(df.columns), align="center"),
                cells=dict(
                    values=df.transpose().values.tolist(),
                    fill=dict(
                        color=[  # unique color for the first column
                            [
                                "#f8f9fa" if (val % 2) == 0 else "#bee3db"
                                for i, val in enumerate(
                                    df["id"].str.extract("(\d+)").astype(int).values
                                )
                            ]
                        ]
                    ),
                    align="right",
                ),
            )
        ]
    )
    fig.update_layout(height=len(df) * 25 + 60, margin=dict(r=5, l=5, t=5, b=5))
    return fig


# df['B'].str.extract('(\d+)').astype(int)


class _SessionState:
    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(
                self._state["data"], None
            ):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state


def capture_output(func):
    """Capture output from running a function and write using streamlit."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Redirect output to string buffers
        stdout, stderr = StringIO(), StringIO()
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                return func(*args, **kwargs)
        except Exception as err:
            st.write(f"Failure while executing: {err}")
            if hasattr(err, "message"):
                st.code(getattr(err, "message", repr(err)))

        finally:
            flag = False
            _stderr = stderr.getvalue()
            if _stderr:
                st.error("An error occurred \n ")
                st.write("Execution stderr log:")
                st.code(_stderr)
                flag = True

            _stdout = stdout.getvalue()
            if _stdout:
                if not flag:
                    st.success("Optimization finished!\n ")
                st.write("Execution stdout log:")
                st.code(_stdout)

    return wrapper


if __name__ == "__main__":
    main()
