#!/usr/bin/env python3
"""
天气功能测试脚本
快速验证地理编码和天气查询功能是否正常工作
"""

import sys
from geocoding import NominatimGeocoder
from weather import OpenMeteoWeather


def test_geocoding():
    """测试地理编码功能"""
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
    """测试天气查询功能"""
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
        
        return True
    else:
        print(f"   ❌ 失败")
        return False


def test_integration():
    """测试集成功能（地理编码 + 天气查询）"""
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


def main():
    """运行所有测试"""
    print("\n🧪 开始测试天气功能...\n")
    
    all_passed = True
    
    # 测试1：地理编码
    if not test_geocoding():
        print("\n❌ 地理编码测试失败")
        all_passed = False
    
    # 测试2：天气查询
    if not test_weather():
        print("\n❌ 天气查询测试失败")
        all_passed = False
    
    # 测试3：集成功能
    if not test_integration():
        print("\n❌ 集成测试失败")
        all_passed = False
    
    # 结果总结
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有测试通过！天气功能运行正常。")
        print("\n💡 现在可以运行主程序了：")
        print("   uv run python main.py")
    else:
        print("❌ 部分测试失败，请检查网络连接和 API 访问。")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
