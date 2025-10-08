# KS5009 Smart Home - Complete Hardware Validation Suite
# Run all hardware tests and provide comprehensive system status

import gc
import time

def print_header():
    """Print test suite header"""
    print("🏠 KS5009 SMART HOME HARDWARE VALIDATION SUITE")
    print("=" * 60)
    print("Testing all hardware components before software implementation")
    print("Based on reference implementations from Docs/Python/microPython Code/")
    print("=" * 60)

def print_system_info():
    """Print ESP32 system information"""
    print("\n💻 SYSTEM INFORMATION")
    print("-" * 30)
    import machine
    print(f"Platform: {machine.unique_id()}")
    print(f"Frequency: {machine.freq()} Hz")
    print(f"Available Memory: {gc.mem_free()} bytes")

    # Try to get more system info
    try:
        import esp32
        print(f"Flash Size: {esp32.flash_size()} bytes")
        print(f"Temperature: {(esp32.raw_temperature() - 32) * 5/9:.1f}°C")
    except:
        pass

def run_hardware_tests():
    """Run the main hardware connection tests"""
    print("\n🔧 HARDWARE CONNECTION TESTS")
    print("-" * 40)

    try:
        # Import and run the hardware test
        from test_connections import main as test_hardware
        hardware_results = test_hardware()
        return hardware_results
    except ImportError as e:
        print(f"❌ Could not import hardware tests: {e}")
        return {}
    except Exception as e:
        print(f"❌ Hardware tests failed: {e}")
        return {}

def run_wifi_tests():
    """Run WiFi connectivity tests"""
    print("\n📡 WIFI CONNECTIVITY TESTS")
    print("-" * 40)

    try:
        # Import and run the WiFi test
        from test_wifi import main as test_wifi
        wifi_results = test_wifi()
        return wifi_results
    except ImportError as e:
        print(f"❌ Could not import WiFi tests: {e}")
        return {}
    except Exception as e:
        print(f"❌ WiFi tests failed: {e}")
        return {}

def generate_report(hardware_results, wifi_results):
    """Generate comprehensive test report"""
    print(f"\n{'='*60}")
    print("📊 COMPREHENSIVE TEST REPORT")
    print(f"{'='*60}")

    all_results = {}
    all_results.update(hardware_results)
    all_results.update(wifi_results)

    # Calculate statistics
    total_tests = len(all_results)
    passed_tests = sum(1 for result in all_results.values() if result)
    failed_tests = total_tests - passed_tests

    print(f"\n📈 OVERALL STATISTICS")
    print("-" * 25)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")

    # Detailed results
    print(f"\n📋 DETAILED RESULTS")
    print("-" * 25)

    # Hardware results
    if hardware_results:
        print("\n🔧 Hardware Components:")
        for test_name, result in hardware_results.items():
            status = "✅ OPERATIONAL" if result else "❌ FAILED"
            print(f"   {test_name:<20}: {status}")

    # WiFi results
    if wifi_results:
        print("\n📡 Network Connectivity:")
        for test_name, result in wifi_results.items():
            status = "✅ OPERATIONAL" if result else "❌ FAILED"
            print(f"   {test_name:<20}: {status}")

    # System readiness assessment
    print(f"\n🎯 SYSTEM READINESS ASSESSMENT")
    print("-" * 35)

    critical_components = [
        "I2C Bus", "Digital Inputs", "Digital Outputs", "WiFi Connection"
    ]

    critical_passed = sum(1 for comp in critical_components
                         if all_results.get(comp, False))

    if critical_passed == len(critical_components):
        readiness = "🟢 READY FOR SOFTWARE IMPLEMENTATION"
        recommendation = "All critical components operational. Proceed with T003-T005."
    elif critical_passed >= len(critical_components) * 0.75:
        readiness = "🟡 MOSTLY READY - MINOR ISSUES"
        recommendation = "Most components working. Review failed tests and proceed with caution."
    else:
        readiness = "🔴 NOT READY - MAJOR ISSUES"
        recommendation = "Critical hardware problems detected. Fix hardware before proceeding."

    print(f"Status: {readiness}")
    print(f"Recommendation: {recommendation}")

    # Next steps
    print(f"\n📋 RECOMMENDED NEXT STEPS")
    print("-" * 30)

    if critical_passed == len(critical_components):
        print("1. ✅ T002 Complete - Hardware validation passed")
        print("2. 🔄 Proceed to T003 - Configure development environment")
        print("3. 🔄 Continue to T004-T005 - Additional hardware validation")
        print("4. 🔄 Begin Phase 3.2 - Contract Tests (TDD)")
    else:
        print("1. 🔧 Review and fix failed hardware components")
        print("2. 📋 Check wiring and component connections")
        print("3. 🔄 Re-run hardware validation tests")
        print("4. 📖 Refer to KS5009 documentation for troubleshooting")

    return {
        'total': total_tests,
        'passed': passed_tests,
        'failed': failed_tests,
        'success_rate': passed_tests/total_tests*100,
        'ready': critical_passed == len(critical_components)
    }

def main():
    """Main test runner"""
    start_time = time.time()

    # Print header and system info
    print_header()
    print_system_info()

    # Run all test suites
    hardware_results = run_hardware_tests()
    wifi_results = run_wifi_tests()

    # Generate comprehensive report
    summary = generate_report(hardware_results, wifi_results)

    # Final summary
    end_time = time.time()
    test_duration = end_time - start_time

    print(f"\n⏱️  Test Duration: {test_duration:.1f} seconds")
    print(f"💾 Final Memory: {gc.mem_free()} bytes")

    if summary['ready']:
        print("\n🎉 HARDWARE VALIDATION COMPLETE - READY TO PROCEED!")
        print("Next: Run T003 (Development Environment Setup)")
    else:
        print("\n⚠️  HARDWARE ISSUES DETECTED - REVIEW AND FIX")
        print("Fix hardware issues before proceeding to software implementation")

    print(f"\n{'='*60}")

    return summary

if __name__ == "__main__":
    main()