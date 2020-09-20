from collections import OrderedDict
from itertools import groupby
import matplotlib.pyplot as plt
import pandas as pd
import random
import re


_nsre = re.compile('([0-9]+)')
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]

def color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def get_symb(symbol, dimtojoin=None, factor=1, addstr = ''):
    df = symbol.df.copy()
    if dimtojoin is None:
        df.loc[:,'t'] = df['symbol'].astype(str) + addstr
        df.loc[:,'value'] = df['value']*factor
    else:
        df.loc[:,'t'] = df['symbol'].astype(str) +'-'+ df[dimtojoin].astype(str) + addstr
        df.loc[:,'value'] = df['value']*factor
    return df[['id','n','h','t','value']]

def get_symb_zeroUP(symbol, dimtojoin='tech', factor=1, addstr = ''):
    df = symbol.df.copy()
    df.loc[:,'t'] = df['symbol'].astype(str) +'-'+ df[dimtojoin].astype(str) + addstr
    df.loc[df.value >= 0.0, 'value'] = 0.0
    df.loc[df.value < 0.0,'value'] = df.loc[df.value < 0.0, 'value']*factor
    return df[['id','n','h','t','value']]

def get_symb_zeroLO(symbol, dimtojoin='tech', factor=1, addstr = ''):
    df = symbol.df.copy()
    df.loc[:,'t'] = df['symbol'].astype(str) +'-'+ df[dimtojoin].astype(str) + addstr
    df.loc[df.value <= 0.0, 'value'] = 0.0
    df.loc[df.value > 0.0,'value'] = df.loc[df.value > 0.0, 'value']*factor
    return df[['id','n','h','t','value']]

def get_changed(symbol, factor=1, addstr=''):
    df = symbol.df.copy()
    df.loc[:,'value'] = df['value']*factor
    head = df['symbol'].unique()[0]
    if addstr:
        head = head + addstr
    df = df.rename(columns={'value': head})
    return df[['id','n','h',head]]

def change_header(symbol, name):
    df = symbol.df.copy()
    df = df.rename(columns={'value': name})
    return df[['id','n','h',name]]

def get_rldc(symbols_dc):
    STO_IN = symbols_dc['STO_IN']
    G_L = symbols_dc['G_L']
    STO_OUT = symbols_dc['STO_OUT']
    CU = symbols_dc['agg_techCU']
    con1a_bal = symbols_dc['con1a_bal']
    G_INFES = symbols_dc['G_INFES']
    RLDC = symbols_dc['RLDC']
    RSVR_OUT = symbols_dc['RSVR_OUT']
    F = symbols_dc['Fn']  # dims l,h,n
    if 'ev_endogenous' in symbols_dc['features']:
        EV_CHARGE = symbols_dc['EV_CHARGE'].dimreduc('ev')
        EV_CHARGE.name = 'EV_CHARGE'
        EV_DISCHARGE = symbols_dc['EV_DISCHARGE'].dimreduc('ev')
        EV_DISCHARGE.name = 'EV_DISCHARGE'
    else:
        pass

    symbs_list = [get_symb(STO_IN,'sto',-1,'neg'),
                  get_symb(STO_IN,'sto',1),
                  get_symb(G_L,'tech'),
                  get_symb(RSVR_OUT,'rsvr'),
                  get_symb(STO_OUT,'sto'),
                  get_symb_zeroUP(F,'l',1,'neg'),
                  get_symb_zeroUP(F,'l',-1,'pos'),
                  get_symb_zeroLO(F,'l',1)]
    if 'ev_endogenous' in symbols_dc['features']:
        symbs_list.append(get_symb(EV_DISCHARGE))

    df = pd.concat(symbs_list)
    df = df.set_index(['id','n','h','t']).unstack('t').fillna(0.0)
    df = df.loc[:,(df != 0).any(axis=0)]
    df = df['value']
    df = df.join(get_changed(CU,-1,'neg').set_index(['id','n','h']))
    df = df.join(get_changed(CU,1).set_index(['id','n','h']))
    try:
        df = df.join(get_changed(EV_CHARGE,-1,'neg').set_index(['id','n','h']))
        df = df.join(get_changed(EV_CHARGE,1).set_index(['id','n','h']))
    except:
        pass
    df = df.join(change_header(con1a_bal,'shadow').set_index(['id','n','h']))
    df = df.join(change_header(G_INFES, 'infes').set_index(['id','n','h']))
    df = df.join(change_header(RLDC, 'RLDC').set_index(['id','n','h']))
    df = df.reset_index().sort_values(by= ['id', 'n', 'RLDC'],axis=0, ascending=False)

    lt = []
    for ix, gr in df.groupby(['id','n']):
        dt = gr.copy()
        dt.loc[:,'hr'] = [i for i in range(1,len(gr)+1)]
        lt.append(dt)
    data = pd.concat(lt)
    # database is already created

    # SORTING DATA TO BE DISPLAYED IN THE ORDER REQUIRED

    # This consist in give some sorting paterns. Flexible script

    headings = list(data.columns)
    rem = ['RLDC','shadow','h','hr','n','id']
    [headings.remove(r) for r in rem]

    # SECTION 1
    # Here tech that start with a symbol but is folowed by a number, pandas sort them naturaly in asscending order.
    # We want here, the tech that starts with "patern" be sortered in descending order

    # paterns = ['STO_OUT-Sto']  # ['STO_IN-Sto','STO_OUT-Sto']  **1
    # mask = []
    # for _ in range(len(headings)):
    #     mask.append(-1)
    # for i, patern in enumerate(paterns):
    #     for j, elem in enumerate(headings):
    #         if patern in elem:
    #             mask[j] = i

    # group = []
    # pairs = sorted(zip(headings, mask), key=lambda x: (x[1]))
    # for i, grp in groupby(pairs, lambda x: x[1]):
    #     group.append([item[0] for item in grp])

    # group[1].sort(key=natural_sort_key,reverse=True)
    # # group[2].sort(key=natural_sort_key,reverse=True)  # This is deactivated due to above in "paterns" 'STO_IN-Sto' has been removed **2
    # headings = group[1] + group[0]  #  group[1] + group[2] + group[0] **3

    # memory collect the roots of tech
    memory = []
    for item in headings:
        for elem in headings:
            if item in elem:
                if item not in memory:
                    for mem in memory:
                        if item in mem:
                            memory.remove(mem)
                    memory.append(item)
    colors_dc = {}
    for tech in memory:
        colors_dc[tech] = color()
        # print(tech, colors_dc[tech])

    # SECTION 2
    # here symbols with different names get the same color, for example STO_IN and STO_OUT

    for tech, colo in colors_dc.items():  # in this case all tech with this patern has an extension
        if 'STO_IN-' in tech:
            ix = tech.split('STO_IN-')[-1]
            if 'STO_OUT-' + ix in colors_dc:
                colors_dc['STO_OUT-' + ix] = colo

    for tech, colo in colors_dc.items(): # this case not all tech with this patern has an extension
        if 'EV_CHARGE' in tech:
            lst = tech.split('EV_CHARGE')
            if len(lst) > 1:
                ix = lst[-1]
            else:
                ix = ''
            if 'EV_DISCHARGE' + ix in colors_dc:
                colors_dc['EV_DISCHARGE' + ix] = colo

    # SECTION 3
    if 'infes' in colors_dc:
        colors_dc['infes'] = 'black'


    # SECTION 4
    # Here we want to sort tech that will be ploted. The name of the symbol is partially defined, with and e (ends) or s (starts) as preposition, that gives a clue.
    patern_order = ['eneg','sEV_CHARGE','sCU','epos','sSTO_IN','sRSVR_OUT', 'sG_L-bio', 'sG_L-lig', 'sG_L-hc', 'sG_L-other', 'sG_L-CCGT', 'sG_L', 'sSTO_OUT', None]
    pre_order = []
    for patern in patern_order:
        for header in headings:
            if patern is not None:
                if patern[0] == 'e':
                    if header.endswith(patern[1:]):
                        if header not in pre_order:
                            pre_order.append(header)
                elif patern[0] == 's':
                    if header.startswith(patern[1:]):
                        if header not in pre_order:
                            pre_order.append(header)
            else:
                if header not in pre_order:
                    pre_order.append(header)

    # SECTION 5
    # set an ordered dict to contain the order of tech and the color to pass to the next function (plot)
    ordered_tech_color = OrderedDict()
    for header in pre_order:
        color_list = [v for k, v in colors_dc.items() if k in header]
        # print(header)
        # print(color_list)
        ordered_tech_color[header] = color_list[0]
    return data, ordered_tech_color

def plot_rldc(data, rg0, rg1, scen, country, shadow, ordered_list, ordered_tech_color):
    df = data.copy()
    mask = df.eval(f'id == "{scen}" & n == "{country}"')
    df = df[mask].drop(['id','n'], axis=1)
    ch = df.set_index('hr').loc[:,(df != 0).any(axis=0)][rg0:rg1+1]

    cols = []
    color = []
    for item in ordered_list:
        if item in ch.columns:
            cols.append(item)
            for k, v in ordered_tech_color.items():
                if k in item:
                    color.append(v)
                    break
        else:
            print(f"{item} is not in data.")

    framecols = [col for col in ch.columns.to_list() if col not in ['h','shadow', 'RLDC']]
    for col in framecols:
        if col not in cols:
            print(f"{col} data item is not in the selected headings")

    hidden_label = []
    hidden_label_clue_starts = ['CU','EV_CHARGE','STO_IN','Flow']
    hidden_label_clue_ends = ['neg','pos']

    for col in cols:
        for clue_start in hidden_label_clue_starts:
            for clue_end in hidden_label_clue_ends:
                if col.startswith(clue_start) and col.endswith(clue_end):
                    hidden_label.append(col)


    x = ch.index.values
    y0 = ch['RLDC'].values
    y0_lab = 'RLDC'

    y1 = []
    y1_lab = []
    for col in cols:
        y1.append(ch[col].values)
        if col in hidden_label:
            y1_lab.append('_')
        else:
            y1_lab.append(col)
    if shadow:
        y2 = ch['shadow'].values
        y2_lab = 'shadow'

    fig = plt.figure(figsize=(20,12))
    ax1 = fig.add_subplot(111)
    ax1.stackplot(x, y1, labels=y1_lab, colors=color)
    ax1.plot(x,y0, label= 'RLDC', color='r')
    if shadow:
        ax2 = ax1.twinx()
        ax2.plot(x, y2, 'black')
        ax2.set_ylabel('Marginal price [Eur/MW]')
    ax1.set_xlabel('Hr')
    ax1.set_ylabel('Residual Load [MW]')

    fig.legend(loc='upper right')
    return ch, fig
