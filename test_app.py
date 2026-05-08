import unittest
import pandas as pd
import numpy as np
from app import load_data, get_signal_color


class TestSignalDashboard(unittest.TestCase):
    """
    5G信号可视化看板单元测试类

    测试数据加载、信号颜色计算等核心功能
    """

    def test_load_data(self):
        """
        测试数据加载功能

        验证：
        1. 数据成功加载
        2. 返回的是DataFrame类型
        3. 包含必需的列
        4. 数据不为空
        """
        df = load_data()

        # 验证返回类型
        self.assertIsInstance(df, pd.DataFrame)

        # 验证必需列存在
        required_columns = ['Latitude', 'Longitude', 'CellID', 'Band',
                           'RSRP_dBm', 'SINR_dB', 'TerminalType', 'Download_Mbps']
        for col in required_columns:
            self.assertIn(col, df.columns)

        # 验证数据不为空
        self.assertGreater(len(df), 0)

    def test_get_signal_color_excellent(self):
        """
        测试优秀信号颜色计算

        RSRP > -90 dBm 应返回绿色 [0, 255, 0]
        """
        color = get_signal_color(-80)
        self.assertEqual(color, [0, 255, 0])

        color = get_signal_color(-85)
        self.assertEqual(color, [0, 255, 0])

    def test_get_signal_color_good(self):
        """
        测试一般信号颜色计算

        -110 dBm < RSRP <= -90 dBm 应返回黄色 [255, 255, 0]
        """
        color = get_signal_color(-95)
        self.assertEqual(color, [255, 255, 0])

        color = get_signal_color(-100)
        self.assertEqual(color, [255, 255, 0])

        # -110 是边界值，属于较差信号
        color = get_signal_color(-109)
        self.assertEqual(color, [255, 255, 0])

    def test_get_signal_color_poor(self):
        """
        测试较差信号颜色计算

        RSRP <= -110 dBm 应返回红色 [255, 0, 0]
        """
        color = get_signal_color(-115)
        self.assertEqual(color, [255, 0, 0])

        color = get_signal_color(-120)
        self.assertEqual(color, [255, 0, 0])

    def test_data_ranges(self):
        """
        测试数据范围合理性

        验证：
        1. 经纬度在合理范围内
        2. RSRP在合理范围内
        3. SINR在合理范围内
        4. 下载速率为正数
        """
        df = load_data()

        # 验证经纬度范围（上海地区）
        self.assertTrue((df['Latitude'] >= 31.0).all() and (df['Latitude'] <= 31.5).all())
        self.assertTrue((df['Longitude'] >= 121.0).all() and (df['Longitude'] <= 122.0).all())

        # 验证RSRP范围（5G信号典型范围）
        self.assertTrue((df['RSRP_dBm'] >= -130).all() and (df['RSRP_dBm'] <= -50).all())

        # 验证SINR范围
        self.assertTrue((df['SINR_dB'] >= -10).all() and (df['SINR_dB'] <= 35).all())

        # 验证下载速率为正
        self.assertTrue((df['Download_Mbps'] > 0).all())

    def test_band_values(self):
        """
        测试频段值的有效性

        验证数据中的频段值是预期的n28、n41、n78
        """
        df = load_data()
        valid_bands = ['n28', 'n41', 'n78']
        unique_bands = df['Band'].unique()

        for band in unique_bands:
            self.assertIn(band, valid_bands)

    def test_terminal_types(self):
        """
        测试终端类型值的有效性

        验证数据中的终端类型是预期的Smartphone、CPE、IoT
        """
        df = load_data()
        valid_types = ['Smartphone', 'CPE', 'IoT']
        unique_types = df['TerminalType'].unique()

        for t in unique_types:
            self.assertIn(t, valid_types)


if __name__ == '__main__':
    unittest.main()
