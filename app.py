import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# 设置页面配置
st.set_page_config(page_title="5G 信号可视化看板", layout="wide")

st.title("📡 5G 信号可视化看板")
st.markdown("欢迎来到 **'Code with AI' 极客探索赛**！")


@st.cache_data
def load_data():
    """
    加载5G信号数据

    从CSV文件中读取信号样本数据，包含经纬度、小区ID、频段、
    信号强度(RSRP)、信噪比(SINR)、终端类型和下载速率等信息。

    Returns:
        pd.DataFrame: 包含信号数据的DataFrame
    """
    df = pd.read_csv('data/signal_samples.csv')
    return df


def get_signal_color(rsrp):
    """
    根据RSRP信号强度返回对应的颜色

    信号强度等级：
    - 大于 -90 dBm: 绿色 (信号优秀)
    - -90 到 -110 dBm: 黄色 (信号一般)
    - 小于 -110 dBm: 红色 (信号较差)

    Args:
        rsrp (float): 信号强度值(dBm)

    Returns:
        list: RGB颜色值 [R, G, B]
    """
    if rsrp > -90:
        return [0, 255, 0]  # 绿色 - 信号好
    elif rsrp > -110:
        return [255, 255, 0]  # 黄色 - 信号一般
    else:
        return [255, 0, 0]  # 红色 - 信号差


def create_2d_map_layer(df):
    """
    创建2D散点地图图层

    根据信号强度(RSRP)为每个数据点设置不同颜色：
    - 绿色: RSRP > -90 dBm
    - 黄色: -110 dBm < RSRP <= -90 dBm
    - 红色: RSRP <= -110 dBm

    Args:
        df (pd.DataFrame): 信号数据DataFrame

    Returns:
        pdk.Layer: PyDeck散点图层
    """
    df['color'] = df['RSRP_dBm'].apply(get_signal_color)

    layer = pdk.Layer(
        'ScatterplotLayer',
        df,
        get_position=['Longitude', 'Latitude'],
        get_color='color',
        get_radius=100,
        pickable=True,
        opacity=0.8,
    )
    return layer


def create_3d_map_layer(df):
    """
    创建3D柱状地图图层

    将信号点以3D柱状形式展示，柱子高度与下载速率成正比。
    颜色根据信号强度(RSRP)设置。

    Args:
        df (pd.DataFrame): 信号数据DataFrame

    Returns:
        pdk.Layer: PyDeck 3D柱状图层
    """
    df['color'] = df['RSRP_dBm'].apply(get_signal_color)
    df['elevation'] = df['Download_Mbps'] * 10  # 高度与下载速率成正比

    layer = pdk.Layer(
        'ColumnLayer',
        df,
        get_position=['Longitude', 'Latitude'],
        get_elevation='elevation',
        elevation_scale=1,
        radius=80,
        get_fill_color='color',
        pickable=True,
        auto_highlight=True,
    )
    return layer


def render_map(df, use_3d=False):
    """
    渲染地图

    根据参数选择渲染2D散点地图或3D柱状地图

    Args:
        df (pd.DataFrame): 信号数据DataFrame
        use_3d (bool): 是否使用3D视图，默认为False

    Returns:
        pdk.Deck: PyDeck地图对象
    """
    view_state = pdk.ViewState(
        latitude=df['Latitude'].mean(),
        longitude=df['Longitude'].mean(),
        zoom=12,
        pitch=50 if use_3d else 0,
        bearing=0
    )

    if use_3d:
        layer = create_3d_map_layer(df)
    else:
        layer = create_2d_map_layer(df)

    tooltip = {
        "html": "<b>小区ID:</b> {CellID}<br/>"
                "<b>频段:</b> {Band}<br/>"
                "<b>RSRP:</b> {RSRP_dBm} dBm<br/>"
                "<b>SINR:</b> {SINR_dB} dB<br/>"
                "<b>终端类型:</b> {TerminalType}<br/>"
                "<b>下载速率:</b> {Download_Mbps} Mbps",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style='mapbox://styles/mapbox/light-v9'
    )
    return deck


def create_band_chart(df):
    """
    创建频段分布柱状图

    统计各频段的基站数量，使用Streamlit原生图表展示

    Args:
        df (pd.DataFrame): 信号数据DataFrame
    """
    band_counts = df['Band'].value_counts().reset_index()
    band_counts.columns = ['频段', '数量']

    st.subheader("📊 各频段基站数量统计")
    st.bar_chart(band_counts.set_index('频段'))


def create_terminal_chart(df):
    """
    创建终端类型分布饼图

    统计不同类型终端的占比

    Args:
        df (pd.DataFrame): 信号数据DataFrame
    """
    terminal_counts = df['TerminalType'].value_counts().reset_index()
    terminal_counts.columns = ['终端类型', '数量']

    st.subheader("📱 终端类型分布")
    st.bar_chart(terminal_counts.set_index('终端类型'))


def main():
    """
    主函数

    构建5G信号可视化看板的完整界面，包括：
    1. 侧边栏筛选器（频段、RSRP范围）
    2. 数据概览统计
    3. 2D/3D地图可视化
    4. 数据图表展示
    """
    # 加载数据
    df = load_data()

    # 侧边栏筛选器
    st.sidebar.header("🔍 数据筛选")

    # 频段筛选
    bands = ['全部'] + list(df['Band'].unique())
    selected_band = st.sidebar.selectbox("选择频段", bands)

    # RSRP范围筛选
    rsrp_min, rsrp_max = st.sidebar.slider(
        "RSRP范围 (dBm)",
        float(df['RSRP_dBm'].min()),
        float(df['RSRP_dBm'].max()),
        (float(df['RSRP_dBm'].min()), float(df['RSRP_dBm'].max()))
    )

    # 终端类型筛选
    terminal_types = ['全部'] + list(df['TerminalType'].unique())
    selected_terminal = st.sidebar.selectbox("终端类型", terminal_types)

    # 地图视图切换
    st.sidebar.header("🗺️ 地图设置")
    use_3d = st.sidebar.checkbox("启用3D视图", value=False)

    # 应用筛选
    filtered_df = df.copy()
    if selected_band != '全部':
        filtered_df = filtered_df[filtered_df['Band'] == selected_band]
    if selected_terminal != '全部':
        filtered_df = filtered_df[filtered_df['TerminalType'] == selected_terminal]
    filtered_df = filtered_df[
        (filtered_df['RSRP_dBm'] >= rsrp_min) &
        (filtered_df['RSRP_dBm'] <= rsrp_max)
        ]

    # 显示数据统计
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总样本数", len(filtered_df))
    with col2:
        st.metric("平均RSRP", f"{filtered_df['RSRP_dBm'].mean():.2f} dBm")
    with col3:
        st.metric("平均SINR", f"{filtered_df['SINR_dB'].mean():.2f} dB")
    with col4:
        st.metric("平均下载速率", f"{filtered_df['Download_Mbps'].mean():.2f} Mbps")

    st.markdown("---")

    # 地图区域
    st.subheader("🗺️ 信号覆盖地图")
    st.markdown("""
    <style>
    .legend {
        display: flex;
        gap: 20px;
        margin-bottom: 10px;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .color-box {
        width: 20px;
        height: 20px;
        border-radius: 3px;
    }
    </style>
    <div class="legend">
        <div class="legend-item">
            <div class="color-box" style="background-color: #00ff00;"></div>
            <span>信号优秀 (> -90 dBm)</span>
        </div>
        <div class="legend-item">
            <div class="color-box" style="background-color: #ffff00;"></div>
            <span>信号一般 (-90 ~ -110 dBm)</span>
        </div>
        <div class="legend-item">
            <div class="color-box" style="background-color: #ff0000;"></div>
            <span>信号较差 (< -110 dBm)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    deck = render_map(filtered_df, use_3d=use_3d)
    st.pydeck_chart(deck)

    st.markdown("---")

    # 图表区域
    col1, col2 = st.columns(2)
    with col1:
        create_band_chart(filtered_df)
    with col2:
        create_terminal_chart(filtered_df)

    # 数据表格
    st.markdown("---")
    st.subheader("📋 详细数据")
    st.dataframe(filtered_df, use_container_width=True)


if __name__ == "__main__":
    main()
