""" This module contains utility functions used during graph generation. """

import csv
import pandas as pd

def find_nodes(G, **attrs):
    """
    Finds the list of nodes in the graph associated that have attrs attributes.   
    Uses the predefined G.attrs_to_group and G.group_to_nodes dicts   
    (see graph.FileBasedGraph and generate.init_nodes())

    Parameters
    ----------
    G : FileBasedGraph instance

    Returns
    -------
    tuple (list, int)
        List contains all the node IDs
        int is the group ID
    """
    attrs_key = tuple(sorted(attrs.items()))
    
    group_id = G.attrs_to_group[attrs_key]
    if group_id is None:
        return []
    list_of_nodes = G.group_to_nodes[group_id]
    #print(attrs_key)
    #print(list_of_nodes[0], list_of_nodes[-1])
    return list_of_nodes, group_id

def read_file(path):
    """ 
    CSV and XLSX file reader. Returns pandas dataframe.
    """
    if path.endswith('.csv'):
        return pd.read_csv(path)
    elif path.endswith('.xlsx'):
        return pd.read_excel(path)
    else:
        raise ValueError("Unsupported file format: {}".format(path))

def desc_groups(pops_path, pop_column = 'n'):
    """
    Reads the group sizes file. (csv or xlsx)
    All column headers in the file are considered as group characteristics except for pop_collumn.
    
    Parameters
    ----------
    pops_path : string
        The filepath for the group sizes file. Can be csv or xlsx.
    pop_column : string
        The name of the column that contains the population value.
    Returns
    -------
    tuple (dict, list)
        The dict contains the group IDs as keys and the sizes (populations) as value.   
        The list contains the names of the group characteristic collumns.
    """
    df_group_pops = read_file(pops_path)

    # Identify characteristic columns (all except pop_column)
    characteristic_cols = [col for col in df_group_pops.columns if col != pop_column]

    # Each group gets a unique ID (row number)
    group_populations = {
        idx: {**{col: row[col] for col in characteristic_cols}, pop_column: row[pop_column]}
        for idx, row in df_group_pops.iterrows()
    }

    return group_populations, characteristic_cols

def export_group_to_attrs_csv(group_to_attrs, filename):
    """Exports the group_to_attrs dict to CSV."""
    # Get all attribute keys
    all_keys = set()
    for attrs in group_to_attrs.values():
        all_keys.update(attrs.keys())
    fieldnames = ['group_id'] + sorted(all_keys)
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for group_id, attrs in group_to_attrs.items():
            row = {'group_id': group_id}
            row.update(attrs)
            writer.writerow(row)

def export_group_to_nodes_csv(group_to_nodes, filename):
    """
    Exports the group_to_attrs dict to CSV.    
    The nodes are initialized sequentially
    so start and end IDs are all that is needed.
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['group_id', 'start_node_id', 'end_node_id'])
        for group_id, node_ids in group_to_nodes.items():
            if node_ids:
                writer.writerow([group_id, node_ids[0], node_ids[-1]])