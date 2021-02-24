import pandas as pd

def process_bins(df,key):


    bin_size = int(df[key].max() - df[key].min())
    binned, bin_labels = pd.cut(df[key], bin_size, retbins=True)
    # Make xtick labels for plot
    xtick_bin = []
    for i in range(len(bin_labels) - 1):
        lower = round(bin_labels[i], 2)
        upper = round(bin_labels[i + 1], 2)
        xtick_bin.append(str(lower) + "-" + str(upper))

    df_binned_weight = df.groupby(binned).mean()

    return df_binned_weight, xtick_bin