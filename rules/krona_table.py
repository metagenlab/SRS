import pandas as pd
import numpy as np
def calculate_reads(table,total):
    reads_to_sim=[]
    for i in range(len(table)):
        acc=table['AssemblyNames'][i]
        prop=table.loc[i]['PercentReads']
        read_nb=int(prop*total)
        mean = read_nb
        sd = 2.0
        read_nb_sample = round(np.random.normal(mean, sd))
        # This adds variability for the number of simulated reads between replicates
        reads_to_sim.append(read_nb_sample)
        print(f"{read_nb_sample} reads for {acc} , replicate {snakemake.wildcards.rep}")
    return reads_to_sim
"""
Main
"""
checkpoint_output = snakemake.input[0]
table=pd.read_csv(checkpoint_output,delimiter='\t')
total=snakemake.config['total_amount_reads']
nb_reads_list=calculate_reads(table,total)
tax_df=table.loc[:,['superkingdom','phylum','order','family','genus','species']]
tax_df.index=table['AssemblyNames']
tax_df.insert(loc=0,column='SimReads',value=nb_reads_list)
tax_df.to_csv(snakemake.output[0],sep='\t',index=True)
