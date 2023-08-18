import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
# st.set_page_config(layout="wide")
st.header("Calculate Field Curvature of TC lens system")

file = st.file_uploader("File Select", ['txt'])

tab1, tab2 = st.tabs(["Data manipulation", "Visualization"])
with tab1:
    if file is not None:
        if file.name.split('.')[-1] == 'txt':
            df = pd.read_csv('test.txt', delimiter='\t')
            
        st.dataframe(df)


    select = st.selectbox(label = "Scanning mode", options=['Default Field Editor',
                                        'MC Editor', 'None'], index = 2)
    if (select is not 'None') and file is not None:
        if select == 'Default Field Editor':
            Hx_X_map = df.groupby('Hx')['X_sample'].mean()
            Hy_Y_map = df.groupby('Hy')['Y_sample'].mean()
            df['X'] = df['Hx'].map(Hx_X_map)
            df['Y'] = df['Hy'].map(Hy_Y_map)
        elif select == 'MC Editor':   
            Hx_X_map = df.groupby('Hx')['Y_sample'].mean()
            Hy_Y_map = df.groupby('Hy')['X_sample'].mean()
            df['X'] = -df['Hx'].map(Hx_X_map)
            df['Y'] = -df['Hy'].map(Hy_Y_map)

        st.dataframe(df)
if (select is not 'None') and file is not None:
    with tab2:
        data_list = df.columns[6:9]
        title_list = ['Curvature Sagital', 'Curvature Tangential', 'Field Curvature']
        ctitle_list = ['Sagital (mm)', 'Tangential (mm)', 'Best focus (mm)']
        interp = st.selectbox(label = "Scanning mode", options=['none', 'nearest', 'bilinear', 'bicubic', 'spline16',
           'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
           'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos'], index = 0)
        fig, axes = plt.subplots(3,1, figsize=(3,7.5))
        for i in range(3):
            pivot = df.pivot_table(values=data_list[i], index='X', columns='Y')
            graph = axes[i].imshow(pivot, extent = [min(pivot.columns), max(pivot.columns), min(pivot.index), max(pivot.index)], cmap = 'jet', interpolation=interp)
            axes[i].set_title(title_list[i])
            axes[i].set_xlabel('Spot Position X (mm)')
            axes[i].set_ylabel('Spot Position Y (mm)')
                
            fig.colorbar(graph, ax=axes[i],label=ctitle_list[i], shrink=1)
        plt.tight_layout()
        st.pyplot(fig)