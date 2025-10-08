# WiFi Connectivity Test
# Based on KS5009 reference implementation
# Tests network connectivity before IoT implementation

import time
import network
import gc
from wifi_config import WIFI_SSID, WIFI_PASSWORD

# WiFi Configuration
# NOTE: Update these credentials for your network
# WIFI_SSID = 'CyFi'        # Replace with your WiFi name
# WIFI_PASSWORD = 'SecurityA40'  # Replace with your WiFi password

# Connection timeout (seconds)
CONNECTION_TIMEOUT = 30

def setup_wifi_station(ssid, password):
    """
    Set up ESP32 as WiFi station and connect to router
    Based on pj12_1_wifi_sta.py reference implementation
    """
    print("=== WiFi Station Setup ===")
    print(f"Attempting to connect to: {ssid}")

    # Create station interface
    sta_if = network.WLAN(network.STA_IF)

    try:
        # Activate station mode
        sta_if.active(True)
        print("📡 WiFi station mode activated")

        # Check if already connected
        if sta_if.isconnected():
            print("✅ Already connected to WiFi")
            config = sta_if.ifconfig()
            print(f"📍 Current IP address: {config[0]}")
            return sta_if, True

        # Scan for available networks
        print("🔍 Scanning for available networks...")
        networks = sta_if.scan()
        available_ssids = [net[0].decode('utf-8') for net in networks]
        print(f"📶 Found {len(available_ssids)} networks")

        # Check if target network is available
        if ssid not in available_ssids:
            print(f"❌ Network '{ssid}' not found in available networks:")
            for i, network_ssid in enumerate(available_ssids[:5]):  # Show first 5
                print(f"   {i+1}. {network_ssid}")
            return sta_if, False

        print(f"✅ Target network '{ssid}' found")

        # Initiate connection
        print(f"🔗 Connecting to {ssid}...")
        sta_if.connect(ssid, password)

        # Wait for connection with timeout
        start_time = time.time()
        while not sta_if.isconnected():
            if time.time() - start_time > CONNECTION_TIMEOUT:
                print(f"❌ Connection timeout after {CONNECTION_TIMEOUT} seconds")
                return sta_if, False

            print("⏳ Connecting...", end=' ')
            time.sleep(1)

        # Connection successful
        config = sta_if.ifconfig()
        print(f"\n✅ Connected successfully!")
        print(f"📍 IP Address: {config[0]}")
        print(f"📍 Subnet Mask: {config[1]}")
        print(f"📍 Gateway: {config[2]}")
        print(f"📍 DNS Server: {config[3]}")

        return sta_if, True

    except Exception as e:
        print(f"❌ WiFi setup failed: {e}")
        return sta_if, False

def test_internet_connectivity(sta_if):
    """Test internet connectivity with HTTP request"""
    print("\n=== Internet Connectivity Test ===")

    if not sta_if.isconnected():
        print("❌ WiFi not connected, skipping internet test")
        return False

    try:
        import urequests

        # Test with a reliable endpoint
        test_urls = [
            "http://httpbin.org/ip",
            "http://www.google.com",
            "http://www.example.com"
        ]

        for url in test_urls:
            try:
                print(f"🌐 Testing connection to: {url}")
                response = urequests.get(url, timeout=10)

                if response.status_code == 200:
                    print(f"✅ HTTP request successful (Status: {response.status_code})")
                    if 'httpbin.org' in url:
                        print(f"📡 Response: {response.text[:100]}...")
                    response.close()
                    return True
                else:
                    print(f"⚠️  HTTP request returned status: {response.status_code}")
                    response.close()

            except Exception as e:
                print(f"❌ Request to {url} failed: {e}")
                continue

        print("❌ All internet connectivity tests failed")
        return False

    except ImportError:
        print("⚠️  urequests library not available")
        print("💡 Install via Thonny: Tools -> Manage packages -> urequests")
        return False

def test_wifi_signal_strength(sta_if):
    """Test and report WiFi signal strength"""
    print("\n=== WiFi Signal Strength Test ===")

    if not sta_if.isconnected():
        print("❌ WiFi not connected, skipping signal test")
        return False

    try:
        # Get current network info
        networks = sta_if.scan()
        current_ssid = WIFI_SSID

        # Find current network in scan results
        current_network = None
        for net in networks:
            if net[0].decode('utf-8') == current_ssid:
                current_network = net
                break

        if current_network:
            ssid, bssid, channel, rssi, authmode, hidden = current_network
            print(f"📶 Connected to: {ssid.decode('utf-8')}")
            print(f"📡 Signal Strength (RSSI): {rssi} dBm")
            print(f"📻 Channel: {channel}")

            # Interpret signal strength
            if rssi > -30:
                quality = "Excellent"
            elif rssi > -50:
                quality = "Good"
            elif rssi > -70:
                quality = "Fair"
            elif rssi > -80:
                quality = "Poor"
            else:
                quality = "Very Poor"

            print(f"📊 Signal Quality: {quality}")
            return True
        else:
            print("⚠️  Could not find current network in scan results")
            return False

    except Exception as e:
        print(f"❌ Signal strength test failed: {e}")
        return False

def test_network_recovery():
    """Test network disconnection and reconnection"""
    print("\n=== Network Recovery Test ===")

    try:
        sta_if = network.WLAN(network.STA_IF)

        if not sta_if.isconnected():
            print("❌ WiFi not connected, skipping recovery test")
            return False

        print("🔌 Testing network disconnection...")
        sta_if.disconnect()
        time.sleep(2)

        if sta_if.isconnected():
            print("⚠️  Disconnect command may not have worked")
        else:
            print("✅ Successfully disconnected")

        print("🔗 Testing automatic reconnection...")
        reconnected, success = setup_wifi_station(WIFI_SSID, WIFI_PASSWORD)

        if success:
            print("✅ Network recovery test passed")
            return True
        else:
            print("❌ Network recovery test failed")
            return False

    except Exception as e:
        print(f"❌ Network recovery test failed: {e}")
        return False

def check_wifi_credentials():
    """Check if WiFi credentials have been configured"""
    if WIFI_SSID == 'YOUR_WIFI_SSID' or WIFI_PASSWORD == 'YOUR_WIFI_PASSWORD':
        print("⚠️  WiFi credentials not configured!")
        print("📝 Please edit test_wifi.py and update:")
        print(f"   WIFI_SSID = '{WIFI_SSID}'")
        print(f"   WIFI_PASSWORD = '{WIFI_PASSWORD}'")
        print("💡 Use your actual WiFi network name and password")
        return False
    return True

def main():
    """Run all WiFi connectivity tests"""
    print("📡 WiFi Connectivity Hardware Validation")
    print("=" * 50)

    # Memory check
    print(f"💾 Available Memory: {gc.mem_free()} bytes")

    # Check credentials
    if not check_wifi_credentials():
        print("\n❌ Cannot proceed without WiFi credentials")
        return {"WiFi Setup": False}

    # Run tests
    tests = {}

    try:
        # WiFi connection test
        print(f"\n{'='*20}")
        sta_if, connected = setup_wifi_station(WIFI_SSID, WIFI_PASSWORD)
        tests["WiFi Connection"] = connected

        if connected:
            # Additional tests only if connected
            tests["Internet Access"] = test_internet_connectivity(sta_if)
            tests["Signal Strength"] = test_wifi_signal_strength(sta_if)
            tests["Network Recovery"] = test_network_recovery()
        else:
            tests["Internet Access"] = False
            tests["Signal Strength"] = False
            tests["Network Recovery"] = False

    except Exception as e:
        print(f"❌ WiFi test suite crashed: {e}")
        tests = {"WiFi Connection": False, "Internet Access": False,
                "Signal Strength": False, "Network Recovery": False}

    # Cleanup
    try:
        sta_if = network.WLAN(network.STA_IF)
        # Keep connection for development, but could disconnect here if needed
        # sta_if.disconnect()
    except:
        pass

    gc.collect()

    # Summary
    print(f"\n{'='*50}")
    print("📡 WIFI VALIDATION SUMMARY")
    print(f"{'='*50}")

    passed = 0
    total = len(tests)

    for test_name, result in tests.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20}: {status}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All WiFi tests passed! Ready for IoT implementation.")
    elif passed >= 1:  # At least basic connection works
        print("⚠️  Basic WiFi works, some advanced features may need attention.")
    else:
        print("❌ WiFi connectivity failed. Check credentials and network.")

    return tests

if __name__ == "__main__":
    main()