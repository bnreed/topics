
# coding: utf-8

# In[26]:

from pathlib import Path

import pandas as pd
import numpy as np

from plotnine import *

task_data = pd.read_csv('../data/human/all_data/all_data.csv')

task_averages = task_data.groupby(['task', 'dataset', 'model', 'topic_idx'])[["scores_raw"]].mean().reset_index()

# (
#     ggplot(task_averages)
#     + geom_boxplot(aes(x="factor(model)", y="scores_raw"))
#     + facet_wrap("~dataset+task", scales="free_y")
#     + theme(
#         axis_line=element_line(size=1, colour="black"),
#         panel_grid_major=element_line(colour="#d3d3d3"),
#         panel_grid_minor=element_blank(),
#         panel_border=element_blank(),
#         panel_background=element_blank(),
#         plot_title=element_text(size=15, family="Tahoma", 
#                                 face="bold"),
#         text=element_text(family="Tahoma", size=11),
#         axis_text_x=element_text(colour="black", size=10),
#         axis_text_y=element_text(colour="black", size=10),
#     )
# )


# In[27]:

task_data_auto = task_data.drop(columns="scores_raw").rename(columns={"c_npmi_10_full": "scores_raw"}).copy()
task_data_auto["task"] = "Automated"
task_data_auto["confidences_raw"] = 1
task_data_plot = pd.concat([task_data, task_data_auto], ignore_index=True)
task_data_plot = task_data_plot.replace("intrusions", "Intrusion")
task_data_plot = task_data_plot.replace("ratings", "Ratings")
#task_data_plot.tail()


# In[28]:

task_averages = task_data_plot.groupby(['task', 'dataset', 'model', 'topic_idx'], sort=False)[["scores_raw"]].mean().reset_index()


# In[30]:



ggsave(
    ggplot(task_averages)
    + geom_boxplot(aes(x="factor(model)", y="scores_raw", fill='model'), show_legend = False)
    + facet_wrap("~dataset+task", scales="free_y", )
    + xlab("Model")
    + ylab("")
    + theme(
        axis_line=element_line(size=1, colour="black"),
        panel_grid_major=element_line(colour="#d3d3d3"),
        panel_grid_minor=element_blank(),
        panel_border=element_blank(),
        panel_background=element_blank(),
        plot_title=element_text(size=12, family="Tahoma", 
                                face="bold"),
        text=element_text(family="Tahoma", size=10),
        axis_text_x=element_text(colour="black", size=10),
        axis_text_y=element_text(colour="black", size=8),
        subplots_adjust={'wspace': 0.3, 'hspace': 0.5},
        strip_margin_x=0.3,
    )
    + scale_x_discrete(limits=("mallet", "dvae", "etm"))
    + theme(figure_size=(8, 4))
    + scale_fill_brewer(type="qual", palette="Set2"), filename="model_comparison_boxplot.pdf",
dpi=320)
#my_plot.save("my-plot.pdf")#"topics/analysis/model_comparison_boxplot.pdf")


task_data = pd.read_csv('../data/human/all_data/all_data.csv')
task_data = task_data.replace("intrusions", "Intrusion")
task_data = task_data.replace("ratings", "Ratings")

task_data_conf = task_data[task_data['confidences_raw']==1]
task_data_intrusion_filtered = task_data_conf[task_data_conf['task']=="Intrusion"]
task_data_intrusion_filtered["task"] = "Intrusion_filtered"

task_data_ratings_filtered = task_data_conf[task_data_conf['task']=="Ratings"]
task_data_ratings_filtered["task"] = "Ratings_filtered"

# task_data_auto = task_data.drop(columns="scores_raw").rename(columns={"c_npmi_10_full": "scores_raw"}).copy()
# task_data_auto["task"] = "Automated"
# task_data_auto["confidences_raw"] = 1


task_data_plot = pd.concat([task_data, task_data_intrusion_filtered, task_data_ratings_filtered], 
                           ignore_index=True)

#task_averages = task_data_plot.groupby(['task', 'dataset', 'model', 'topic_idx'], sort=False)[["scores_raw"]].mean().reset_index()

task_data_plot['subtask'] = task_data_plot['task'].copy()
task_data_plot['task'] = task_data_plot['task'].replace("Intrusion_filtered", "Intrusion")
task_data_plot['task'] = task_data_plot['task'].replace("Ratings_filtered", "Ratings")

task_filtered_vs_og = task_data_plot.groupby(['task', 'dataset', 'subtask', 'model', 'topic_idx'], sort=False)[["scores_raw"]].mean().reset_index()

ggsave(
    ggplot(task_filtered_vs_og, aes(x='factor(model)', y='scores_raw', fill='model+subtask'))
    + geom_col(stat='summary', fun_y= lambda x:np.mean(x), position='dodge', width=0.5, show_legend=False)
    + facet_wrap("~dataset+task", scales="free_y", ncol = 2, )
    + xlab("Model")
    + ylab("")
    + theme(
        axis_line=element_line(size=1, colour="black"),
        panel_grid_major=element_line(colour="#d3d3d3"),
        panel_grid_minor=element_blank(),
        panel_border=element_blank(),
        panel_background=element_blank(),
        plot_title=element_text(size=12, family="Tahoma", 
                                face="bold"),
        text=element_text(family="Tahoma", size=10),
        axis_text_x=element_text(colour="black", size=10),
        axis_text_y=element_text(colour="black", size=8),
        subplots_adjust={'wspace': 0.1, 'hspace': 0.4},
        strip_margin_x=0.3,
    )
    + scale_x_discrete(limits=("mallet", "dvae", "etm"))
    + theme(figure_size=(10, 4))
    + scale_fill_manual(values = ["#66c2a5", "#b2e0d2",
                                  "#66c2a5", "#b2e0d2",
                                  "#fc8d62", "#fdc6b0",
                                  "#fc8d62", "#fdc6b0",
                                  "#8da0cb", "#c6cfe5",
                                  "#8da0cb", "#c6cfe5", 
                                  "#66c2a5", "#b2e0d2",
                                  "#66c2a5", "#b2e0d2",
                                  "#fc8d62", "#fdc6b0", 
                                  "#fc8d62", "#fdc6b0",
                                  "#8da0cb", "#c6cfe5",
                                  "#8da0cb", "#c6cfe5"])#scale_fill_brewer(type="qual", palette="Set2")
, filename="barplot_effect_of_familiarity.pdf",
dpi=320)


