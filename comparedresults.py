import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly

def showComparedResult(withoutRL, withRL , edge, head_title ,y_axis_title, figure_name):
    df1 = pd.read_csv(withoutRL + ".csv")
    df2 = pd.read_csv(withRL + ".csv")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x= df1['step_num'], y=df1[edge],name="Without RL"))
    fig.add_trace(go.Scatter(x= df2['step_num'], y=df2[edge],name="With RL"))
    fig.update_layout(
        title= head_title,
        xaxis_title="# of Steps",
        yaxis_title=y_axis_title,
        font=dict(
            family="Courier New, monospace",
            size=15,
            color="#7f7f7f"
        )
    )
    fig.show()

def cumulativeComparedResult(withoutRL, withRL, head_title, y_axis_title, figure_name):
    df1 = pd.read_csv(withoutRL + ".csv")
    df2 = pd.read_csv(withRL + ".csv")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x= df1['step_num'], y=df1["-gneE0"] + df1["-gneE1"] + df1["-gneE2"] + df1["-gneE3"],name="Without RL"))
    fig.add_trace(go.Scatter(x= df2['step_num'], y=df2["-gneE0"] + df2["-gneE1"] + df2["-gneE2"] + df2["-gneE3"],name="With RL"))
    fig.update_layout(
        title= head_title,
        xaxis_title="# of Steps",
        yaxis_title=y_axis_title,
        font=dict(
            family="Courier New, monospace",
            size=15,
            color="#7f7f7f"
        )
    )
    fig.show()


# # Accumulated Waiting Time Results
# showComparedResult("withoutRL", "withRL", "-gneE0", "Northern Edge", "Accumulated Waiting Time", "Northern Edge - Accum_Waiting_Time")
# showComparedResult("withoutRL", "withRL", "-gneE1", "Eastern Edge", "Accumulated Waiting Time", "Eastern Edge - Accum_Waiting_Time")
# showComparedResult("withoutRL", "withRL", "-gneE2", "Southern Edge", "Accumulated Waiting Time", "Southern Edge - Accum_Waiting_Time")
# showComparedResult("withoutRL", "withRL", "-gneE3", "Western Edge", "Accumulated Waiting Time", "Western Edge - Accum_Waiting_Time")
# cumulativeComparedResult("withoutRL", "withRL", "Cumulative Result", "Accumulated Waiting Time", "Cumulative_Accum_Waiting_Time")

# # Number of Vehicles Results
# showComparedResult("numOfVehicleWithoutRL", "numOfVehicleWithRL", "-gneE0", "Northern Edge", "# of Vehicles", "Northern Edge - Num_Of_Vehicles")
# showComparedResult("numOfVehicleWithoutRL", "numOfVehicleWithRL", "-gneE1", "Eastern Edge", "# of Vehicles", "Eastern Edge - Num_Of_Vehicles")
# showComparedResult("numOfVehicleWithoutRL", "numOfVehicleWithRL", "-gneE2", "Southern Edge", "# of Vehicles", "Southern Edge - Num_Of_Vehicles")
# showComparedResult("numOfVehicleWithoutRL", "numOfVehicleWithRL", "-gneE3", "Western Edge", "# of Vehicles", "Western Edge - Num_Of_Vehicles")
# cumulativeComparedResult("numOfVehicleWithoutRL", "numOfVehicleWithRL", "Cumulative Result", "# of Vehicles", "Cumulative_Num_Of_Vehicles")

# #Traffic Density Results
# showComparedResult("trafficDensityWithoutRL", "trafficDensityWithRL", "-gneE0" , "Northern Edge", "Traffic Density (# of Vehicle / Edge Length", "Northern Edge - Traffic_Density")
# showComparedResult("trafficDensityWithoutRL", "trafficDensityWithRL", "-gneE1" , "Eastern Edge", "Traffic Density (# of Vehicle / Edge Length", "Eastern Edge - Traffic_Density")
# showComparedResult("trafficDensityWithoutRL", "trafficDensityWithRL", "-gneE2" , "Southern Edge", "Traffic Density (# of Vehicle / Edge Length", "Southern Edge - Traffic_Density")
# showComparedResult("trafficDensityWithoutRL", "trafficDensityWithRL", "-gneE3" , "Western Edge", "Traffic Density (# of Vehicle / Edge Length", "Western Edge - Traffic_Density")
cumulativeComparedResult("trafficDensityWithoutRL", "trafficDensityWithRL", "Cumulative Result", "Traffic Density (# of Vehicle / Edge Length", "Cumulative_Traffic_Density")