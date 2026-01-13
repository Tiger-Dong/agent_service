#!/usr/bin/env python3
"""
天气功能快速演示
展示如何在代码中直接使用天气和地理编码功能
"""

from geocoding import NominatimGeocoder
from weather import OpenMeteoWeather


def demo_basic():
    """演示：基础用法"""
    print("=" * 60)
    print("演示 1: 基础用法 - 查询北京天气")
    print("=" * 60)
    
    # 初始化
    geocoder = NominatimGeocoder()
    weather = OpenMeteoWeather()
    
    # 步骤1：获取坐标
    print("\n📍 步骤1: 地理编码")
    location = geocoder.geocode("北京")
    if location:
        print(f"   地址: {location['display_name']}")
        print(f"   坐标: ({location['latitude']}, {location['longitude']})")
    
    # 步骤2：查询天气
    print("\n🌤️  步骤2: 查询天气")
    weather_data = weather.get_weather(
        location['latitude'], 
        location['longitude'],
        forecast_days=3
    )
    
    if weather_data:
        current = weather_data['current']
        print(f"   温度: {current['temperature']}°C")
        print(f"   体感: {current['feels_like']}°C")
        print(f"   天气: {current['weather_description']}")
        
        # 步骤3：穿衣建议
        print("\n👔 步骤3: 穿衣建议")
        advice = weather.get_clothing_advice(
            current['temperature'],
            current['weather_code']
        )
        print(f"   {advice}")


def demo_compare():
    """演示：对比多个城市"""
    print("\n" + "=" * 60)
    print("演示 2: 对比多个城市的天气")
    print("=" * 60)
    
    geocoder = NominatimGeocoder()
    weather = OpenMeteoWeather()
    
    cities = ["北京", "上海", "广州"]
    results = []
    
    for city in cities:
        print(f"\n🔍 正在查询: {city}")
        
        # 获取坐标
        location = geocoder.geocode(city)
        if not location:
            continue
        
        # 查询天气
        weather_data = weather.get_weather(
            location['latitude'],
            location['longitude'],
            forecast_days=1
        )
        
        if weather_data:
            current = weather_data['current']
            results.append({
                'city': city,
                'temp': current['temperature'],
                'weather': current['weather_description'].split('/')[0].strip()
            })
            print(f"   ✅ 温度: {current['temperature']}°C")
    
    # 显示对比
    print("\n📊 温度对比:")
    results.sort(key=lambda x: x['temp'])
    print(f"   最冷: {results[0]['city']} ({results[0]['temp']}°C)")
    print(f"   最热: {results[-1]['city']} ({results[-1]['temp']}°C)")


def demo_forecast():
    """演示：未来天气预报"""
    print("\n" + "=" * 60)
    print("演示 3: 未来天气预报")
    print("=" * 60)
    
    geocoder = NominatimGeocoder()
    weather = OpenMeteoWeather()
    
    print("\n🔍 查询: 东京未来3天天气")
    
    # 获取东京坐标
    location = geocoder.geocode("Tokyo")
    if location:
        # 查询天气
        weather_data = weather.get_weather(
            location['latitude'],
            location['longitude'],
            forecast_days=3
        )
        
        if weather_data:
            print("\n📅 未来3天预报:")
            for day in weather_data['forecast'][:3]:
                print(f"\n   {day['date']}:")
                print(f"   🌡️  {day['temp_min']}°C ~ {day['temp_max']}°C")
                print(f"   ☁️  {day['weather_description'].split('/')[0].strip()}")
                
                # 给出穿衣建议
                avg_temp = (day['temp_min'] + day['temp_max']) / 2
                advice = weather.get_clothing_advice(avg_temp, day['weather_code'])
                print(f"   👔 {advice.split('|')[0].strip()}")


def demo_clothing():
    """演示：不同温度的穿衣建议"""
    print("\n" + "=" * 60)
    print("演示 4: 不同温度的穿衣建议")
    print("=" * 60)
    
    weather = OpenMeteoWeather()
    
    scenarios = [
        (-15, "极寒天气"),
        (0, "冰点温度"),
        (10, "凉爽天气"),
        (20, "温和天气"),
        (30, "炎热天气")
    ]
    
    for temp, desc in scenarios:
        advice = weather.get_clothing_advice(temp, 0)
        print(f"\n🌡️  {temp}°C ({desc}):")
        print(f"   {advice.split('|')[0].strip()}")


if __name__ == "__main__":
    print("\n🌤️  天气功能快速演示\n")
    
    try:
        demo_basic()
        demo_compare()
        demo_forecast()
        demo_clothing()
        
        print("\n" + "=" * 60)
        print("✅ 演示完成！")
        print("\n💡 提示：运行主程序体验 AI 对话模式：")
        print("   uv run python main.py")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ 演示出错: {e}")
        print("请检查网络连接和依赖安装。\n")
