"""Plots radar backscatter and microwave brightness temperature series"""
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns

import reader
import plotting


RADAR_COLORS = ['tab:red',
                'tab:red',
                'tab:blue',
                'tab:blue',
                'tab:green',
                'tab:green']
RADAR_LINESTYLES = ['-',
                    '--',
                    '-',
                    '--',
                    '-',
                    '--']
RADAR_SHADE = [True,
               False,
               True,
               False,
               True,
               False]
SBR_COLORS = ['tab:red',
              'tab:red',
              'tab:blue',
              'tab:blue']
SBR_LINESTYLES = ['-',
                  '--',
                  '-',
                  '--']
SBR_MARKERS = ['.',
               '+',
               '.',
               '+']
SBR_SHADE = [True,
             False,
             True,
             False]


def plot_ku(df, ax=None, fig_label=None):
    """Plots Ku radar channels"""
    if not ax: plt.gca()
    plotting.add_panel(ax=ax, fig_label=fig_label)
    df.plot(ax=ax, color=RADAR_COLORS, style=RADAR_LINESTYLES)
    ax.set_ylim(-35, 5)
    ax.set_ylabel("Backscatter (dB)")
    ax.set_yticks(range(-35, 15, 5))
    ax.legend(loc="lower left", ncol=2)
    return ax


def plot_ka(df, ax=None, fig_label=None):
    """Plots Ka radar channels"""
    if not ax: plt.gca()
    plotting.add_panel(ax=ax, fig_label=fig_label)
    df.plot(ax=ax, color=RADAR_COLORS, style=RADAR_LINESTYLES)
    ax.set_ylim(-35, 5)
    ax.set_ylabel("Backscatter (dB)")
    ax.set_yticks(range(-35, 15, 5))
    ax.legend(loc="lower left", ncol=2)
    return ax


def plot_sbr(df, ax=None, fig_label=None):
    """Plots SBR Tb"""
    if not ax: plt.gca()
    plotting.add_panel(ax=ax, fig_label=fig_label)
    for chan, color, lines in zip(df.columns, SBR_COLORS, SBR_LINESTYLES):
        ax.plot(df.index.values, df[chan].values,
                color=color, linestyle=lines,
                label=chan)
    ax.set_ylim(100, 300)
    ax.set_ylabel("Brightness Temperature (K)")
    ax.legend(loc="lower left", ncol=2)



def kd_plot(df, variables, colors, shading, linestyle, ax=None, fig_label=None):
    """Creates kernal density plot panel
    :df: pandas.Dataframe with data
    :variables: variables to plot"""
    if not ax: ax = plt.gca()
    for var, col, shd, ls in zip(variables, colors, shading, linestyle):
        sns.kdeplot(data=df, y=var, color=col, shade=shd, linestyle=ls, ax=ax)
    if fig_label: plotting.add_fig_label(fig_label, ax)
    return ax


def split_kuka(kuka, frequency):
    """Split kuka dataframe into Ku and Ka"""
    df = kuka.loc[:,[frequency in col for col in kuka.columns]]
    df.columns = [c.replace(f"{frequency}_", "") for c in df.columns]
    return df


def plot_microwave():
    """Creates microwave backscatter/Tb figure for MOSAiC ROS paper"""
    kuka = reader.kukadata()
    sbr = reader.sbrdata()
    
    # For now, split Ku and Ka channels into separate Dataframes
    ku_df = split_kuka(kuka, "Ku")
    ka_df = split_kuka(kuka, "Ka")

    fig = plt.figure(figsize=(7, 9), constrained_layout=False)
    gs = GridSpec(3, 5, figure=fig)
    ax0 = fig.add_subplot(gs[0, :-1])
    plot_ku(ku_df, ax=ax0, fig_label="a) Ku")

    ax1 = fig.add_subplot(gs[1, :-1], sharex=ax0)
    plot_ka(ka_df, ax=ax1, fig_label="b) Ka")
    ax1.tick_params(labelbottom=False)
    ax1.set_xlabel('')

    ax2 = fig.add_subplot(gs[2, :-1], sharex=ax0)
    plot_sbr(sbr, ax=ax2, fig_label="c) SBR")
    ax2.set_xlabel('September 2020')
    
    # Kernal density plots, following Vishnu's method
    ax3 = fig.add_subplot(gs[0, 4], sharey=ax0)
    ax3.tick_params(labelleft=False, left=False,  labelbottom=False)
    kd_plot(ku_df,
            ku_df.columns,
            RADAR_COLORS,
            RADAR_SHADE,
            RADAR_LINESTYLES,
            ax=ax3,
            fig_label=None)

    ax4 = fig.add_subplot(gs[1, 4], sharey=ax1, sharex=ax3)
    ax4.tick_params(labelleft=False, left=False)
    kd_plot(ka_df,
            ka_df.columns,
            RADAR_COLORS,
            RADAR_SHADE,
            RADAR_LINESTYLES,
            ax=ax4,
            fig_label=None)
    ax4.set_xlabel('')
    ax4.set_xticks([0., 0.2])
    ax4.set_xticklabels(['0', '0.2'])


    ax5 = fig.add_subplot(gs[2, 4], sharey=ax2)
    ax5.tick_params(labelleft=False, left=False)
    kd_plot(sbr,
            sbr.columns,
            SBR_COLORS,
            SBR_SHADE,
            SBR_LINESTYLES,
            ax=ax5,
            fig_label=None)
    ax5.set_xticks([0., 0.02])
    ax5.set_xticklabels(['0', '0.02'])


    fig.subplots_adjust(wspace=0.15)
    plt.show()

    fig.savefig("mosaic_rain_on_snow_microwave.png")
    return


if __name__ == "__main__":
    plot_microwave()
