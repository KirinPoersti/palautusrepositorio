"""Demonstration of unittest.mock functionality"""
from unittest.mock import Mock

print("=== Mock Object Basics ===")
mock = Mock()
print(f"Mock object: {mock}")
print(f"mock.foo: {mock.foo}")
print(f"mock.foo.bar(): {mock.foo.bar()}")

print("\n=== Setting return_value ===")
mock.foo.bar.return_value = "Foobar"
print(f"mock.foo.bar() returns: {mock.foo.bar()}")

print("\n=== Using side_effect ===")
mock.foo.bar.side_effect = lambda name: f"{name}: Foobar"
print(f"mock.foo.bar('Kalle') returns: {mock.foo.bar('Kalle')}")

print("\n=== Mock as a function ===")
get_name_mock = Mock(return_value="Matti")
print(f"get_name_mock() returns: {get_name_mock()}")

print("\n=== Testing assert_called ===")
mock.foo.bar.assert_called()
print("✓ assert_called passed for bar (it was called)")

try:
    mock.foo.doo.assert_called()
    print("✓ assert_called passed for doo")
except AssertionError as e:
    print(f"✗ assert_called failed for doo: {e}")

print("\n=== Mock demonstration complete ===")
