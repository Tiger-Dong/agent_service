#!/usr/bin/env python3
"""
天气功能完整测试套件
整合所有测试：地理编码、天气查询、集成功能、格式展示
"""

import sys
import traceback
from geocoding import NominatimGeocoder
from weather import OpenMeteoWeather


def test_geocoding():
    """测试1：地理编码功能"""
    print("=" * 60)
    print("1️⃣  测试地理编码功能")
    print("=" * 60)
    
    geocoder = NominatimGeocoder()
    
    test_addresses = [
        "北京天安门",
        "New York",
        "Paris, France"
    ]
    
    for address in test_addresses:
        print(f"\n🔍 查询: {address}")
        result = geocoder.geocode(address)
        
        if result:
            print(f"   ✅ 成功")
            print(f"   📍 经度: {result['longitude']}")
            print(f"   📍 纬度: {result['latitude']}")
            print(f"   📝 地址: {result['display_name'][:60]}...")
        else:
            print(f"   ❌ 失败")
            return False
    
    return True


def test_weather():
    """测试2：天气查询功能"""
    print("\n" + "=" * 60)
    print("2️⃣  测试天气查询功能")
    print("=" * 60)
    
    weather = OpenMeteoWeather()
    
    # 测试北京的天气
    beijing_lat = 39.9042
    beijing_lon = 116.4074
    
    print(f"\n🔍 查询: 北京 ({beijing_lat}, {beijing_lon})")
    result = weather.get_weather(beijing_lat, beijing_lon, forecast_days=3)
    
    if result:
        current = result["current"]
        print(f"   ✅ 成功")
        print(f"   🌡️  温度: {current['temperature']}°C")
        print(f"   ☁️  天气: {current['weather_description']}")
        print(f"   💧 湿度: {current['humidity']}%")
        
        # 测试穿衣建议
        advice = weather.get_clothing_advice(
            current['temperature'],
            current['weather_code']
        )
        print(f"   👔 建议: {advice.split('|')[0].strip()}")
        
        # 测试温度描述
        temp_desc = weather.get_temperature_description(current['temperature'])
        print(f"   📝 温度描述: {temp_desc}")
        
        return True
    else:
        print(f"   ❌ 失败")
        return False


def test_integration():
    """测试3：集成功能（地理编码 + 天气查询）"""
    print("\n" + "=" * 60)
    print("3️⃣  测试集成功能（地理编码 + 天气）")
    print("=" * 60)
    
    geocoder = NominatimGeocoder()
    weather = OpenMeteoWeather()
    
    test_locations = [
        ("上海", "Shanghai"),
        ("东京", "Tokyo")
    ]
    
    for cn_name, en_name in test_locations:
        print(f"\n🔍 查询: {cn_name}")
        
        # 步骤1：地理编码
        geo_result = geocoder.geocode(cn_name)
        if not geo_result:
            print(f"   ❌ 地理编码失败")
            return False
        
        lat = geo_result['latitude']
        lon = geo_result['longitude']
        print(f"   ✅ 坐标: ({lat}, {lon})")
        
        # 步骤2：天气查询
        weather_result = weather.get_weather(lat, lon, forecast_days=1)
        if not weather_result:
            print(f"   ❌ 天气查询失败")
            return False
        
        current = weather_result["current"]
        print(f"   ✅ 温度: {current['temperature']}°C")
        print(f"   ✅ 天气: {current['weather_description'].split('/')[0].strip()}")
    
    return True


def test_display_format():
    """测试4：新的结构化展示格式"""
    print("\n" + "=" * 60)
    print("4️⃣  测试结构化展示格式")
    print("=" * 60)
    
    geocoder = NominatimGeocoder()
    weather = OpenMeteoWeather()
    
    # 测试城市
    test_city = "北京"
    
    print(f"\n🔍 查询: {test_city}\n")
    
    # 步骤1：地理编码
    location = geocoder.geocode(test_city)
    if not location:
        print("❌ 地理编码失败")
        return False
    
    # 步骤2：查询天气
    weather_data = weather.get_weather(
        location['latitude'],
        location['longitude'],
        forecast_days=3
    )
    
    if not weather_data:
        print("❌ 天气查询失败")
        return False
    
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
    print("\n" + "─" * 60)
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
    
    print("─" * 60)
    
    # 显示未来预报
    if len(forecast) > 1:
        print(f"\n📅 未来预报 (Forecast):")
        for day in forecast[1:3]:  # 显示未来2天
            print(f"\n   {day['date']}:")
            print(f"   🌡️  {day['temp_min']}°C ~ {day['temp_max']}°C")
            print(f"   ☁️  {day['weather_description']}")
    
    return True


def test_multiple_cities():
    """测试5：多个城市对比"""
    print("\n" + "=" * 60)
    print("5️⃣  测试多个城市对比")
    print("=" * 60)
    
    geocoder = NominatimGeocoder()
    weather = OpenMeteoWeather()
    
    cities = ["上海", "广州", "深圳"]
    
    for city in cities:
        print(f"\n🔍 {city}:")
        location = geocoder.geocode(city)
        if not location:
            print(f"   ❌ 地理编码失败")
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
        else:
            print(f"   ❌ 天气查询失败")
    
    return True


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("🧪 天气功能完整测试套件")
    print("=" * 60)
    print("测试项目：地理编码、天气查询、集成功能、格式展示、多城市对比")
    print("=" * 60 + "\n")
    
    all_passed = True
    test_results = []
    
    # 运行所有测试
    tests = [
        ("地理编码测试", test_geocoding),
        ("天气查询测试", test_weather),
        ("集成功能测试", test_integration),
        ("格式展示测试", test_display_format),
        ("多城市对比测试", test_multiple_cities)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
            if not result:
                all_passed = False
        except Exception as e:
            print(f"\n❌ {test_name}出错: {e}")
            traceback.print_exc()
            test_results.append((test_name, False))
            all_passed = False
    
    # 显示测试结果总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {test_name}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有测试通过！天气功能运行正常。")
        print("\n💡 现在可以运行主程序了：")
        print("   uv run python main.py")
        print("\n然后尝试问：")
        print("   • 北京今天天气怎么样？")
        print("   • 明天去上海穿什么？")
        print("   • 达拉斯和休斯顿哪个更冷？")
    else:
        print("❌ 部分测试失败，请检查：")
        print("   • 网络连接是否正常")
        print("   • API 访问是否可用")
        print("   • 依赖是否正确安装")
        sys.exit(1)
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
