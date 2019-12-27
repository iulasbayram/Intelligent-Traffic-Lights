import numpy as np
import pandas as pd
import plotly.graph_objects as go  #plotly 4.0.0rc1


df1 = pd.read_csv('numOfVehicleWithoutRL.csv')
df2 = pd.read_csv('numOfVehicleWithRL.csv')
cum_nonRL_datas = y=df1["-gneE0"] + df1["-gneE1"] + df1["-gneE2"] + df1["-gneE3"]
cum_RL_datas = y=df2["-gneE0"] + df2["-gneE1"] + df2["-gneE2"] + df2["-gneE3"]
cum_nonRL_datas = cum_nonRL_datas.tolist()
cum_RL_datas = cum_RL_datas.tolist()
step_num = df1['step_num']
step_num = step_num.tolist() 
#low = df['AAPL.Low'].tolist()
#high = np.array(df['AAPL.High'])+20 # artificially added 20 to get the second graph above the first one

trace1 = go.Scatter(x=step_num[:2],
                    y=cum_nonRL_datas[:2],
                    name='Traditional',
                    mode='lines',
                    line=dict(width=2))

trace2 = go.Scatter(x = step_num[:2],
                    y = cum_RL_datas[:2],
                    name='Intelligent',
                    mode='lines',
                    line=dict(width=2))

frames = [dict(data= [dict(type='scatter',
                           x=step_num[:k+1],
                           y=cum_nonRL_datas[:k+1]),
                      dict(type='scatter',
                           x=step_num[:k+1],
                           y=cum_RL_datas[:k+1])],
               traces= [0, 1],  #this means that  frames[k]['data'][0]  updates trace1, and   frames[k]['data'][1], trace2 
              )for k  in  range(1, len(cum_nonRL_datas)-1)] 

layout = go.Layout(width=1200,
                   height=700,
                   showlegend=False,
                   hovermode='closest',
                   updatemenus=[dict(type='buttons', showactive=False,
                                y=1.05,
                                x=1.15,
                                xanchor='right',
                                yanchor='top',
                                pad=dict(t=0, r=10),
                                buttons=[dict(label='Play',
                                              method='animate',
                                              args=[None, 
                                                    dict(frame=dict(duration=120, 
                                                                    redraw=False),
                                                         transition=dict(duration=0),
                                                         fromcurrent=True,
                                                         mode='immediate')])])])


layout.update(title="Cumulative Result", yaxis_title="Cumulative Number of Vehicles Waiting",
            xaxis_title="Time Steps",xaxis =dict(range=[0,630], autorange=False),
              yaxis =dict(range=[0, 85], autorange=False));
fig = go.Figure(data=[trace1, trace2], frames=frames, layout=layout)
fig.show()