#!/usr/bin/env python3
"""
测试新的天气展示格式
"""

import json
from geocoding import NominatimGeocoder
from weather import OpenMeteoWeather


def test_new_format():
    """测试新的结构化展示格式"""
    print("=" * 70)
    print("测试新的天气展示格式")
    print("=" * 70)
    
    geocoder = NominatimGeocoder()
    weather = OpenMeteoWeather()
    
    # 测试城市
    test_city = "北京"
    
    print(f"\n🔍 查询: {test_city}\n")
    
    # 步骤1：地理编码
    location = geocoder.geocode(test_city)
    if not location:
        print("❌ 地理编码失败")
        return
    
    # 步骤2：查询天气
    weather_data = weather.get_weather(
        location['latitude'],
        location['longitude'],
        forecast_days=3
    )
    
    if not weather_data:
        print("❌ 天气查询失败")
        return
    
    # 获取数据
    current = weather_data['current']
    forecast = weather_data['forecast']
    today = forecast[0] if forecast else None
    
    # 温度描述
    temp_desc = weather.get_temperature_description(current['temperature'])
    
    # 穿衣建议
    advice = weather.get_clothing_advice(
        current['temperature'],
        current['weather_code']
    )
    
    # 展示格式
    print("✅ 查询成功！")
    print("\n" + "─" * 70)
    print(f"📍 查询地点 (Location): {location['display_name']}")
    print(f"🗺️  坐标 (Coordinates): ({location['latitude']}, {location['longitude']})")
    
    if today:
        print(f"☁️  天气状况 (Weather): {current['weather_description']}")
        print(f"🌡️  当天温度区间 (Today's Range): {today['temp_min']}°C ~ {today['temp_max']}°C")
    else:
        print(f"☁️  天气状况 (Weather): {current['weather_description']}")
    
    print(f"🌡️  当前温度 (Current): {current['temperature']}°C ({temp_desc})")
    print(f"    体感温度 (Feels like): {current['feels_like']}°C")
    
    print(f"\n👔 出行建议 (Travel Advice):")
    for line in advice.split('|'):
        print(f"    • {line.strip()}")
    
    # 额外信息
    print(f"\n💧 湿度 (Humidity): {current['humidity']}%")
    print(f"💨 风速 (Wind): {current['wind_speed']} km/h")
    if current['precipitation'] > 0:
        print(f"🌧️  降水 (Precipitation): {current['precipitation']} mm")
    
    print("─" * 70)
    
    # 显示未来预报
    if len(forecast) > 1:
        print(f"\n📅 未来预报 (Forecast):")
        for day in forecast[1:3]:  # 显示未来2天
            print(f"\n   {day['date']}:")
            print(f"   🌡️  {day['temp_min']}°C ~ {day['temp_max']}°C")
            print(f"   ☁️  {day['weather_description']}")
    
    print("\n" + "=" * 70)


def test_multiple_cities():
    """测试多个城市的展示"""
    print("\n测试多个城市:")
    print("=" * 70)
    
    geocoder = NominatimGeocoder()
    weather = OpenMeteoWeather()
    
    cities = ["上海", "广州"]
    
    for city in cities:
        print(f"\n🔍 {city}:")
        location = geocoder.geocode(city)
        if not location:
            continue
        
        weather_data = weather.get_weather(
            location['latitude'],
            location['longitude'],
            forecast_days=1
        )
        
        if weather_data:
            current = weather_data['current']
            forecast = weather_data['forecast']
            today = forecast[0] if forecast else None
            temp_desc = weather.get_temperature_description(current['temperature'])
            
            print(f"   📍 {location['display_name'][:50]}...")
            print(f"   🗺️  ({location['latitude']}, {location['longitude']})")
            print(f"   ☁️  {current['weather_description'].split('/')[0].strip()}")
            if today:
                print(f"   🌡️  {today['temp_min']}°C ~ {today['temp_max']}°C")
            print(f"   🌡️  当前: {current['temperature']}°C ({temp_desc})")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("\n🌤️  新格式天气展示测试\n")
    
    try:
        test_new_format()
        test_multiple_cities()
        
        print("\n✅ 测试完成！新格式更加清晰和结构化。\n")
        print("💡 提示：运行主程序测试 AI 对话模式：")
        print("   uv run python main.py")
        print("   然后问：北京今天天气怎么样？\n")
        
    except Exception as e:
        print(f"\n❌ 测试出错: {e}\n")
        import traceback
        traceback.print_exc()
