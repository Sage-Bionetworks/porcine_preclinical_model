import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import synapseclient
from synapseclient.table import build_table

"""
# this script provides examples of simple porcine preclinical model data analysis steps:
# -- pulling data from Synapse
# -- merging tables for analysis
# -- output simple data exploration plots
"""


# get synapse a synapse table by synapse id 
# using a synapse client instance
def syn_table_2_df(syn, syn_id):
    
    results = syn.tableQuery("SELECT * FROM %s " % syn_id)
    df = results.asDataFrame()

    return df


if __name__ == "__main__":

    # get a synapse client instance to login
    syn = synapseclient.Synapse()

    # if local credentials hasn't been setup
    # please consult the Synapse client login documentation
    # to supply username and password
    syn.login()


    # porcine preclinical model data on Synapse (synapse entities)
    porcine_characteristics_syn_id = "syn18415883"
    porcine_force_tests_syn_id = "syn18415887"
    porcine_weight_measurements_syn_id = "syn18415885"
    porcine_pain_scores_syn_id = "syn18415884"


    # get Synapse tables as dataframes
    porcine_characteristics_df = syn_table_2_df(syn, porcine_characteristics_syn_id) 
    porcine_force_ts_df = syn_table_2_df(syn, porcine_force_tests_syn_id) 
    porcine_weight_ts_df = syn_table_2_df(syn, porcine_weight_measurements_syn_id) 
    porcine_pain_score_ts_df = syn_table_2_df(syn, porcine_pain_scores_syn_id) 

    
    """
    # plot weight by genotype and sex
    """
    
    # clean non numeric values
    porcine_weight_ts_df["weight"] = pd.to_numeric(porcine_weight_ts_df["weight"], errors = "coerce") 
    # join weight timeseries with porcine model characteristics
    porcine_characteristics_weight_df = porcine_weight_ts_df.merge(porcine_characteristics_df, how = "left", on = "a_id")

    # clean NaNs
    porcine_characteristics_weight_df.dropna(subset = ["weight"], inplace = True)
    
    # plot weight of NF vs WT porcine 

    # set plot style
    sns.set(style="ticks")

    # instantiate figure
    f, ax = plt.subplots(figsize=(7, 6))

    # box plot of basic statistics
    sns.boxplot(x="weight", y="strain", data=porcine_characteristics_weight_df, whis="range", palette="vlag")
    # plot all weight measurements
    sns.swarmplot(x="weight", y="strain", data=porcine_characteristics_weight_df, size=2, color=".3", linewidth=0)
    
    # adjust plot grid and labels
    ax.xaxis.grid(True)
    ax.set(ylabel="")
    sns.despine(trim=True, left=True)

    # display plot
    plt.show()

    # plot weight of NF vs WT porcine wrt sex
    sns.violinplot(x="strain", y="weight", hue="Sex",
                   split=True, inner="quart",
                   palette={"F": "red", "M": "blue"},
                   data=porcine_characteristics_weight_df)
    
    # display plot
    plt.show()



    """
    # plot minimum force to expose pain (by genotype and sex)
    """

    # clean non numeric values 
    porcine_force_ts_df["min_force"] = pd.to_numeric(porcine_force_ts_df["min_force"], errors = "coerce")
    
    # find average force applied per porcine
    porcine_force_ts = porcine_force_ts_df.groupby(["a_id"]).agg({"min_force":np.mean})
    # ungroup
    porcine_force_ts.reset_index(inplace = True)
    
    # join force timeseries with porcine model characteristics
    porcine_characteristics_force_df = porcine_force_ts.merge(porcine_characteristics_df, how = "left", on = "a_id")
    # clean NaNs
    porcine_characteristics_force_df.dropna(subset = ["min_force"], inplace = True)

    # plot forces wrt genotype and sex 
    sns.violinplot(x="strain", y="min_force", hue="Sex",
                   split=True, inner="quart",
                   palette={"F": "red", "M": "blue"},
                   data=porcine_characteristics_force_df)
    
    # display plot
    plt.show()

    
    """
    # plot pain score (by genotype and sex)
    """

    # clean non numeric values 
    porcine_pain_score_ts_df["score"] = pd.to_numeric(porcine_pain_score_ts_df["score"], errors = "coerce")
    # sum over different pain parameters
    porcine_pain_score_ts = porcine_pain_score_ts_df.groupby(["a_id"]).agg({"score":np.sum})
    # ungroup
    porcine_pain_score_ts.reset_index(inplace = True)

    # join pain scores with porcine model characteristics 
    porcine_characteristics_pain_df = porcine_pain_score_ts.merge(porcine_characteristics_df, how = "left", on = "a_id")
    # clean NaNs
    porcine_characteristics_pain_df.dropna(subset = ["score"], inplace = True)

    # plot pain scores wrt genotype and sex 
    sns.violinplot(x="strain", y="score", hue="Sex",
                   split=True, inner="quart",
                   palette={"F": "red", "M": "blue"},
                   data=porcine_characteristics_pain_df)

    # display plot
    plt.show()
