"""
天气模块使用示例
演示如何使用 Open-Meteo API 查询天气
"""

from weather import OpenMeteoWeather


def example_basic_weather():
    """示例1：基础天气查询"""
    print("=" * 60)
    print("示例1：基础天气查询 - 北京")
    print("=" * 60)
    
    weather = OpenMeteoWeather()
    
    # 北京的坐标
    beijing_lat = 39.9042
    beijing_lon = 116.4074
    
    result = weather.get_weather(beijing_lat, beijing_lon, forecast_days=3)
    
    if result:
        current = result["current"]
        print(f"\n📍 当前天气:")
        print(f"   🌡️  温度: {current['temperature']}°C")
        print(f"   🤔 体感温度: {current['feels_like']}°C")
        print(f"   💧 湿度: {current['humidity']}%")
        print(f"   ☁️  天气: {current['weather_description']}")
        print(f"   💨 风速: {current['wind_speed']} km/h")
        
        # 穿衣建议
        advice = weather.get_clothing_advice(
            current['temperature'],
            current['weather_code']
        )
        print(f"\n👔 穿衣建议:")
        print(f"   {advice}")
        
        # 未来预报
        print(f"\n📅 未来3天预报:")
        for day in result["forecast"][:3]:
            print(f"\n   {day['date']}:")
            print(f"   🌡️  {day['temp_min']}°C ~ {day['temp_max']}°C")
            print(f"   ☁️  {day['weather_description']}")
    
    print("\n")


def example_multiple_locations():
    """示例2：对比多个城市的天气"""
    print("=" * 60)
    print("示例2：对比多个城市的天气")
    print("=" * 60)
    
    weather = OpenMeteoWeather()
    
    cities = {
        "北京": (39.9042, 116.4074),
        "上海": (31.2304, 121.4737),
        "纽约": (40.7128, -74.0060),
        "伦敦": (51.5074, -0.1278),
        "东京": (35.6895, 139.6917)
    }
    
    for city_name, (lat, lon) in cities.items():
        result = weather.get_weather(lat, lon, forecast_days=1)
        
        if result:
            current = result["current"]
            print(f"\n{city_name}:")
            print(f"   🌡️  {current['temperature']}°C ({current['weather_description'].split('/')[0].strip()})")
            
            # 简化的穿衣建议
            temp = current['temperature']
            if temp < 10:
                clothes = "厚外套"
            elif temp < 20:
                clothes = "薄外套"
            else:
                clothes = "短袖"
            print(f"   👔 建议: {clothes}")
    
    print("\n")


def example_clothing_advice():
    """示例3：针对不同温度的穿衣建议"""
    print("=" * 60)
    print("示例3：不同温度的穿衣建议")
    print("=" * 60)
    
    weather = OpenMeteoWeather()
    
    # 测试不同温度
    test_temps = [-15, -5, 5, 15, 25, 35]
    
    for temp in test_temps:
        advice = weather.get_clothing_advice(temp, 0)  # 0 = 晴天
        print(f"\n{temp}°C:")
        print(f"   {advice.split('|')[0].strip()}")
    
    print("\n")


def example_weather_conditions():
    """示例4：不同天气状况的建议"""
    print("=" * 60)
    print("示例4：不同天气状况的穿衣建议")
    print("=" * 60)
    
    weather = OpenMeteoWeather()
    
    # 测试不同天气代码
    weather_conditions = {
        0: "晴天",
        61: "小雨",
        71: "小雪",
        95: "雷暴"
    }
    
    temp = 20  # 固定温度20°C
    
    for code, desc in weather_conditions.items():
        advice = weather.get_clothing_advice(temp, code)
        print(f"\n{desc} ({temp}°C):")
        for line in advice.split('|'):
            print(f"   {line.strip()}")
    
    print("\n")


if __name__ == "__main__":
    print("\n🌤️  天气模块使用示例\n")
    
    # 运行所有示例
    example_basic_weather()
    example_multiple_locations()
    example_clothing_advice()
    example_weather_conditions()
    
    print("=" * 60)
    print("✅ 所有示例运行完成！")
    print("=" * 60)
