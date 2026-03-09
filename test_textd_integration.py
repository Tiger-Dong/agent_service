#!/usr/bin/env python3
"""测试 textD 集成 - 验证所有新增的文本键"""
import sys
from main import t, SETTINGS

def test_new_keys():
    """测试新添加的所有文本键"""
    print("=" * 60)
    print("测试 textD 新增文本键")
    print("=" * 60)
    
    # 测试工具显示消息
    test_keys = [
        ("tool_switch_lang", {"lang": "中文"}),
        ("tool_thinking_status", {"status": "开启"}),
        ("tool_navigation", {"action": "退出程序"}),
        ("lang_auto_switch", {}),
        ("action_exit", {}),
        ("action_menu", {}),
        ("lang_name_cn", {}),
        ("lang_name_en", {}),
        ("error_timeout", {}),
        ("error_connection", {}),
        ("error_json", {"error": "test error"}),
        ("error_keyerror", {"error": "test key"}),
        ("error_unknown", {"error": "test unknown"}),
        ("error_details", {"trace": "test trace"}),
        ("error_no_response", {}),
        ("ai_chat_tips_cn", {}),
        ("ai_chat_tips_en", {}),
        ("welcome_title", {}),
        ("welcome_subtitle", {}),
        ("welcome_prompt", {}),
        ("welcome_examples_cn", {}),
        ("welcome_examples_en", {}),
    ]
    
    errors = []
    
    # 测试中文
    SETTINGS['language'] = 'cn'
    print("\n测试中文文本:")
    for key, params in test_keys:
        try:
            result = t(key, **params)
            print(f"✓ {key}: {result[:50]}...")
        except Exception as e:
            errors.append(f"❌ {key} (CN): {e}")
            print(f"❌ {key}: {e}")
    
    # 测试英文
    SETTINGS['language'] = 'en'
    print("\n测试英文文本:")
    for key, params in test_keys:
        try:
            result = t(key, **params)
            print(f"✓ {key}: {result[:50]}...")
        except Exception as e:
            errors.append(f"❌ {key} (EN): {e}")
            print(f"❌ {key}: {e}")
    
    # 输出结果
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ 发现 {len(errors)} 个错误:")
        for error in errors:
            print(f"   {error}")
        sys.exit(1)
    else:
        print(f"✅ 所有 {len(test_keys)} 个文本键测试通过！")
        sys.exit(0)


if __name__ == "__main__":
    test_new_keys()
