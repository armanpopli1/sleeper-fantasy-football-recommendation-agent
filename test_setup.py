#!/usr/bin/env python3
"""
Test script to verify Fantasy Football Roast Agent setup
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import requests
        print("  ✅ requests")
    except ImportError:
        print("  ❌ requests - run: pip install requests")
        return False
    
    try:
        import jinja2
        print("  ✅ jinja2")
    except ImportError:
        print("  ❌ jinja2 - run: pip install jinja2")
        return False
    
    try:
        from duckduckgo_search import DDGS
        print("  ✅ duckduckgo_search")
    except ImportError:
        print("  ❌ duckduckgo_search - run: pip install duckduckgo-search")
        return False
    
    try:
        from strands import Agent, tool
        print("  ✅ strands")
    except ImportError:
        print("  ❌ strands - run: pip install strands")
        return False
    
    return True

def test_config():
    """Test configuration setup"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import get_config
        config = get_config()
        print("  ✅ config.py loaded")
        
        # Check required fields
        required_fields = ['league_id', 'season', 'target_display_name', 'model_id']
        for field in required_fields:
            if field in config and config[field]:
                print(f"  ✅ {field}: {config[field]}")
            else:
                print(f"  ❌ {field}: not configured")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Config error: {e}")
        return False

def test_sleeper_api():
    """Test Sleeper API connectivity"""
    print("\n🏈 Testing Sleeper API...")
    
    try:
        from sleeper_tools import get_nfl_state
        result = get_nfl_state()
        
        if result.get("success"):
            print("  ✅ NFL state retrieved")
            print(f"    Week: {result['data'].get('current_week')}")
            print(f"    Season: {result['data'].get('season')}")
            return True
        else:
            print(f"  ❌ NFL state failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"  ❌ Sleeper API error: {e}")
        return False

def test_web_search():
    """Test web search functionality"""
    print("\n🌐 Testing web search...")
    
    try:
        from web_tools import search_fantasy_trends
        result = search_fantasy_trends()
        
        if result.get("success"):
            print("  ✅ Web search working")
            print(f"    Found {len(result['data']['results'])} results")
            return True
        else:
            print(f"  ❌ Web search failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"  ❌ Web search error: {e}")
        return False

def test_files():
    """Test that required files exist"""
    print("\n📁 Testing files...")
    
    required_files = [
        "config.py",
        "sleeper_tools.py", 
        "web_tools.py",
        "roast_agent.py",
        "run_roast.py",
        "report_template.html",
        "requirements.txt"
    ]
    
    all_exist = True
    for file_name in required_files:
        if Path(file_name).exists():
            print(f"  ✅ {file_name}")
        else:
            print(f"  ❌ {file_name} - missing")
            all_exist = False
    
    # Check if reports directory exists
    if Path("reports").exists():
        print("  ✅ reports/ directory")
    else:
        print("  ❌ reports/ directory - creating...")
        Path("reports").mkdir(exist_ok=True)
        print("  ✅ reports/ directory created")
    
    return all_exist

def main():
    """Run all tests"""
    print("🔥 Fantasy Football Roast Agent Setup Test 🔥\n")
    
    tests = [
        ("Files", test_files),
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Sleeper API", test_sleeper_api),
        ("Web Search", test_web_search)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 Test Results Summary:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 All tests passed! Ready to generate savage roast reports!")
        print("\nNext steps:")
        print("1. Configure your league details in config.py")
        print("2. Set up AWS credentials for Bedrock")
        print("3. Run: python run_roast.py --list-users")
        print("4. Run: python run_roast.py --target 'username'")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Run: pip install -r requirements.txt")
        print("- Update config.py with your league information")
        print("- Check your internet connection")
        print("- Verify AWS credentials are configured")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 