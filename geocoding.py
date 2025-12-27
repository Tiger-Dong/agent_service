import requests
import time
from typing import Optional, Dict

class NominatimGeocoder:
    """
    使用 OpenStreetMap Nominatim API 进行地理编码
    将地址转换为经纬度坐标
    """
    
    def __init__(self, user_agent: str = "Mozilla/5.0 (compatible; AgentService/1.0; +https://github.com/Tiger-Dong/agent_service)"):
        """
        初始化 Nominatim 地理编码器
        Args:
            user_agent: 用户代理标识（Nominatim 要求提供完整的 User-Agent）
        """
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {
            "User-Agent": user_agent,
            "Accept": "application/json",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
        self.last_request_time = 0
        # Nominatim 要求请求间隔至少 1 秒
        self.min_request_interval = 1.0
    
    def _rate_limit(self):
        """确保请求间隔符合 Nominatim 使用政策（最少 1 秒）"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        
        self.last_request_time = time.time()
    
    def geocode(self, address: str) -> Optional[Dict[str, any]]:
        """
        将地址转换为经纬度
        Args:
            address: 要查询的地址（可以是中文或英文）
        Returns:
            包含经纬度和详细信息的字典，如果查询失败则返回 None
        """
        try:
            # 遵守速率限制
            self._rate_limit()
            
            params = {
                "q": address,
                "format": "json",
                "limit": 1,  # 只返回最佳匹配结果
                "addressdetails": 1  # 包含详细地址信息
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json()
            
            if not results:
                return None
            
            result = results[0]
            
            return {
                "latitude": float(result["lat"]),
                "longitude": float(result["lon"]),
                "display_name": result["display_name"],
                "address": result.get("address", {}),
                "importance": result.get("importance", 0)
            }
            
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return None
        except (KeyError, ValueError, IndexError) as e:
            print(f"数据解析错误: {e}")
            return None
    
    def get_coordinates(self, address: str) -> Optional[tuple]:
        """
        简化版：只返回经纬度坐标
        Args:
            address: 要查询的地址
        Returns:
            (纬度, 经度) 元组，如果查询失败则返回 None
        """
        result = self.geocode(address)
        if result:
            return (result["latitude"], result["longitude"])
        return None


def main():
    """命令行交互式地理编码工具"""
    print("🌍 OpenStreetMap 地理编码工具")
    print("=" * 50)
    print("输入地址获取经纬度，输入 'exit' 退出\n")
    
    geocoder = NominatimGeocoder()
    
    while True:
        address = input("请输入地址: ").strip()
        
        if address.lower() in ("exit", "quit", "退出"):
            print("再见！")
            break
        
        if not address:
            continue
        
        print(f"\n🔍 正在查询: {address}")
        result = geocoder.geocode(address)
        
        if result:
            print(f"\n✅ 查询成功！")
            print(f"📍 经度 (Longitude): {result['longitude']}")
            print(f"📍 纬度 (Latitude): {result['latitude']}")
            print(f"📝 完整地址: {result['display_name']}")
            print(f"⭐ 匹配度: {result['importance']:.2f}")
        else:
            print(f"\n❌ 未找到该地址，请尝试更具体的地址")
        
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()
