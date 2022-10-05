import pandas as pd
import gc

# Prepare training data frames
def make_cite_train(path_x, path_y, path_meta):
    
    x = pd.read_hdf(path_x)
    y = pd.read_hdf(path_y)
    
    # load metadata
    meta = pd.read_csv(path_meta)
    meta = meta[meta.technology == 'citeseq'].set_index('cell_id')
    meta.drop(['technology'], axis=1, inplace=True)
    
    # match meta indexes with x & y
    meta = meta.reindex(x.index)
    
    return x, y, meta


# Prepare test data frames (fix mishandled inputs)
def make_cite_test(path_x, path_x2, path_meta, path_meta2):

    xdonor = 27678
    xday = 2

    # load metadata and remove cell_ids corresponding to xdonor and xday
    meta = pd.read_csv(path_meta)
    meta = meta[meta.technology == 'citeseq'].set_index('cell_id')
    meta.drop(columns=['technology'], inplace=True)

    # cell_ids to remove and keep
    xcell_drop = meta[(meta.donor == xdonor) & (meta.day == xday)].index
    meta = meta.drop(index = xcell_drop)

    # load extra metadata
    meta2 = pd.read_csv(path_meta2)
    meta2 = meta2[meta2.technology == 'citeseq'].set_index('cell_id')
    meta2.drop(columns=['technology'], inplace=True)

    # Concatenate meta data frames
    meta = pd.concat([meta, meta2])

    # Read x test and drop incorrect cell rows
    x = pd.read_hdf(path_x)
    x = x.drop(index=xcell_drop)
    gc.collect()

    # Read extra x test
    x2 = pd.read_hdf(path_x2)

    # Concatenate both x data frames
    x = pd.concat([x, x2])
    gc.collect()

    # Create index matching test inputs
    meta = meta.reindex(x.index)

    return x, meta

