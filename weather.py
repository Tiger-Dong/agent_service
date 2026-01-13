"""
Open-Meteo Weather API 包装器
使用免费的 Open-Meteo API 查询天气信息
文档: https://open-meteo.com/
"""

import requests
from typing import Optional, Dict
from datetime import datetime


class OpenMeteoWeather:
    """
    使用 Open-Meteo API 查询天气信息
    Open-Meteo 是免费的天气 API，无需 API key
    """
    
    def __init__(self):
        """初始化 Open-Meteo 天气查询器"""
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; AgentService/1.0)"
        }
    
    def get_weather(
        self, 
        latitude: float, 
        longitude: float, 
        forecast_days: int = 7
    ) -> Optional[Dict]:
        """
        根据经纬度获取天气信息
        
        Args:
            latitude: 纬度
            longitude: 经度
            forecast_days: 预报天数 (1-16)
        
        Returns:
            包含天气信息的字典，失败返回 None
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": [
                    "temperature_2m",           # 当前气温
                    "relative_humidity_2m",     # 相对湿度
                    "apparent_temperature",     # 体感温度
                    "precipitation",            # 降水量
                    "weather_code",             # 天气代码
                    "wind_speed_10m",           # 风速
                ],
                "daily": [
                    "weather_code",             # 天气代码
                    "temperature_2m_max",       # 最高温度
                    "temperature_2m_min",       # 最低温度
                    "precipitation_sum",        # 降水总量
                    "wind_speed_10m_max",       # 最大风速
                ],
                "timezone": "auto",             # 自动时区
                "forecast_days": forecast_days
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            # 解析并格式化数据
            return self._format_weather_data(data)
            
        except requests.exceptions.RequestException as e:
            print(f"天气查询请求错误: {e}")
            return None
        except (KeyError, ValueError, IndexError) as e:
            print(f"天气数据解析错误: {e}")
            return None
    
    def _format_weather_data(self, data: Dict) -> Dict:
        """
        格式化天气数据为易读格式
        
        Args:
            data: Open-Meteo API 返回的原始数据
        
        Returns:
            格式化后的天气数据
        """
        current = data.get("current", {})
        daily = data.get("daily", {})
        
        # 当前天气
        current_weather = {
            "temperature": current.get("temperature_2m"),
            "feels_like": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "precipitation": current.get("precipitation"),
            "wind_speed": current.get("wind_speed_10m"),
            "weather_code": current.get("weather_code"),
            "weather_description": self._get_weather_description(current.get("weather_code")),
            "time": current.get("time")
        }
        
        # 未来天气预报
        forecast = []
        if daily and "time" in daily:
            for i in range(len(daily["time"])):
                forecast.append({
                    "date": daily["time"][i],
                    "temp_max": daily["temperature_2m_max"][i],
                    "temp_min": daily["temperature_2m_min"][i],
                    "precipitation": daily["precipitation_sum"][i],
                    "wind_speed": daily["wind_speed_10m_max"][i],
                    "weather_code": daily["weather_code"][i],
                    "weather_description": self._get_weather_description(daily["weather_code"][i])
                })
        
        return {
            "current": current_weather,
            "forecast": forecast,
            "timezone": data.get("timezone"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude")
        }
    
    def _get_weather_description(self, code: int) -> str:
        """
        根据 WMO 天气代码返回天气描述
        
        Args:
            code: WMO 天气代码
        
        Returns:
            天气描述（中英双语）
        """
        weather_codes = {
            0: "晴天 / Clear sky",
            1: "基本晴朗 / Mainly clear",
            2: "局部多云 / Partly cloudy",
            3: "阴天 / Overcast",
            45: "有雾 / Foggy",
            48: "雾凇 / Depositing rime fog",
            51: "小毛毛雨 / Light drizzle",
            53: "毛毛雨 / Moderate drizzle",
            55: "强毛毛雨 / Dense drizzle",
            61: "小雨 / Slight rain",
            63: "中雨 / Moderate rain",
            65: "大雨 / Heavy rain",
            71: "小雪 / Slight snow",
            73: "中雪 / Moderate snow",
            75: "大雪 / Heavy snow",
            77: "雪粒 / Snow grains",
            80: "小阵雨 / Slight rain showers",
            81: "阵雨 / Moderate rain showers",
            82: "大阵雨 / Violent rain showers",
            85: "小阵雪 / Slight snow showers",
            86: "大阵雪 / Heavy snow showers",
            95: "雷暴 / Thunderstorm",
            96: "雷暴伴小冰雹 / Thunderstorm with slight hail",
            99: "雷暴伴大冰雹 / Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, f"未知天气 / Unknown ({code})")
    
    def get_clothing_advice(self, temperature: float, weather_code: int) -> str:
        """
        根据温度和天气状况给出穿衣建议
        
        Args:
            temperature: 气温（摄氏度）
            weather_code: 天气代码
        
        Returns:
            穿衣建议（中英双语）
        """
        advice = []
        
        # 根据温度给建议
        if temperature < -10:
            advice.append("非常寒冷，建议穿羽绒服、厚毛衣、保暖内衣")
            advice.append("Very cold - heavy down jacket, thick sweater, thermal underwear")
        elif temperature < 0:
            advice.append("寒冷，建议穿厚外套、毛衣、长裤")
            advice.append("Cold - thick coat, sweater, long pants")
        elif temperature < 10:
            advice.append("较冷，建议穿夹克、卫衣、长裤")
            advice.append("Cool - jacket, hoodie, long pants")
        elif temperature < 20:
            advice.append("温和，建议穿长袖衬衫、薄外套")
            advice.append("Mild - long-sleeve shirt, light jacket")
        elif temperature < 28:
            advice.append("温暖，建议穿短袖、长裤")
            advice.append("Warm - short sleeves, pants")
        else:
            advice.append("炎热，建议穿短袖、短裤")
            advice.append("Hot - t-shirt, shorts")
        
        # 根据天气状况补充建议
        if weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            advice.append("有雨，记得带伞")
            advice.append("Rainy - bring an umbrella")
        elif weather_code in [71, 73, 75, 77, 85, 86]:
            advice.append("有雪，注意保暖和防滑")
            advice.append("Snowy - dress warm and watch for slippery surfaces")
        elif weather_code in [95, 96, 99]:
            advice.append("雷暴天气，尽量避免外出")
            advice.append("Thunderstorm - avoid going out if possible")
        
        return " | ".join(advice)
    
    def get_temperature_description(self, temperature: float) -> str:
        """
        根据温度返回描述性文字
        
        Args:
            temperature: 气温（摄氏度）
        
        Returns:
            温度描述（中英双语）
        """
        if temperature < -20:
            return "极寒天气 / Extreme cold"
        elif temperature < -10:
            return "严寒天气 / Very cold"
        elif temperature < 0:
            return "冰点以下 / Below freezing"
        elif temperature == 0:
            return "冰点温度 / Freezing point"
        elif temperature < 10:
            return "凉爽天气 / Cool"
        elif temperature < 15:
            return "微凉天气 / Slightly cool"
        elif temperature < 20:
            return "温和天气 / Mild"
        elif temperature < 25:
            return "舒适温度 / Comfortable"
        elif temperature < 30:
            return "温暖天气 / Warm"
        elif temperature < 35:
            return "炎热天气 / Hot"
        else:
            return "酷热天气 / Very hot"


def main():
    """命令行交互式天气查询工具"""
    print("🌤️  Open-Meteo 天气查询工具")
    print("=" * 60)
    print("提示：需要提供经纬度坐标\n")
    
    weather = OpenMeteoWeather()
    
    while True:
        try:
            lat_input = input("请输入纬度 (或输入 'exit' 退出): ").strip()
            if lat_input.lower() in ("exit", "quit", "退出"):
                print("再见！")
                break
            
            lon_input = input("请输入经度: ").strip()
            
            latitude = float(lat_input)
            longitude = float(lon_input)
            
            print(f"\n🔍 正在查询坐标 ({latitude}, {longitude}) 的天气...")
            result = weather.get_weather(latitude, longitude)
            
            if result:
                current = result["current"]
                print(f"\n✅ 查询成功！")
                print(f"\n📍 当前天气 ({current['time']}):")
                print(f"   🌡️  温度: {current['temperature']}°C")
                print(f"   🤔 体感温度: {current['feels_like']}°C")
                print(f"   💧 湿度: {current['humidity']}%")
                print(f"   🌧️  降水: {current['precipitation']} mm")
                print(f"   💨 风速: {current['wind_speed']} km/h")
                print(f"   ☁️  天气: {current['weather_description']}")
                
                # 穿衣建议
                advice = weather.get_clothing_advice(
                    current['temperature'], 
                    current['weather_code']
                )
                print(f"\n👔 穿衣建议:\n   {advice}")
                
                # 显示未来几天预报
                print(f"\n📅 未来预报:")
                for day in result["forecast"][:3]:  # 只显示前3天
                    print(f"\n   {day['date']}:")
                    print(f"   🌡️  温度: {day['temp_min']}°C ~ {day['temp_max']}°C")
                    print(f"   ☁️  {day['weather_description']}")
            else:
                print(f"\n❌ 天气查询失败")
            
            print("\n" + "-" * 60 + "\n")
            
        except ValueError:
            print("❌ 请输入有效的数字坐标\n")
        except Exception as e:
            print(f"❌ 错误: {e}\n")


if __name__ == "__main__":
    main()
