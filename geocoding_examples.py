"""
地理编码使用示例
展示如何使用 NominatimGeocoder 进行地址查询
"""

from geocoding import NominatimGeocoder

def example_basic_usage():
    """基础用法示例"""
    print("=" * 50)
    print("示例 1: 基础用法")
    print("=" * 50)
    
    geocoder = NominatimGeocoder()
    
    # 示例地址列表
    addresses = [
        "北京天安门",
        "上海东方明珠",
        "Tokyo Tower, Japan",
        "Eiffel Tower, Paris",
        "1600 Amphitheatre Parkway, Mountain View, CA"
    ]
    
    for address in addresses:
        print(f"\n查询: {address}")
        coords = geocoder.get_coordinates(address)
        
        if coords:
            lat, lon = coords
            print(f"  ✅ 纬度: {lat}, 经度: {lon}")
        else:
            print(f"  ❌ 未找到")


def example_detailed_info():
    """获取详细信息示例"""
    print("\n" + "=" * 50)
    print("示例 2: 获取详细信息")
    print("=" * 50)
    
    geocoder = NominatimGeocoder()
    address = "清华大学"
    
    print(f"\n查询: {address}")
    result = geocoder.geocode(address)
    
    if result:
        print(f"\n完整信息:")
        print(f"  经度: {result['longitude']}")
        print(f"  纬度: {result['latitude']}")
        print(f"  显示名称: {result['display_name']}")
        
        if result['address']:
            print(f"\n  详细地址:")
            for key, value in result['address'].items():
                print(f"    {key}: {value}")


def example_batch_processing():
    """批量处理示例"""
    print("\n" + "=" * 50)
    print("示例 3: 批量处理")
    print("=" * 50)
    
    geocoder = NominatimGeocoder()
    
    cities = {
        "北京": None,
        "上海": None,
        "深圳": None,
        "广州": None,
        "杭州": None
    }
    
    print("\n正在批量查询中国主要城市...\n")
    
    for city in cities.keys():
        coords = geocoder.get_coordinates(city)
        cities[city] = coords
        if coords:
            print(f"{city:8s} -> 经度: {coords[1]:10.6f}, 纬度: {coords[0]:10.6f}")
        else:
            print(f"{city:8s} -> 查询失败")
    
    return cities


if __name__ == "__main__":
    # 运行所有示例
    example_basic_usage()
    example_detailed_info()
    example_batch_processing()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)
