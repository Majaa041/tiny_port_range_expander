import unittest

from tiny_port_range_expander import expand_ports, InvalidPortRange


class TestExpandPorts(unittest.TestCase):
    def test_empty_string_returns_empty_frozenset(self):
        result = expand_ports("")
        self.assertEqual(result, frozenset())
        self.assertIsInstance(result, frozenset)

    def test_single_port(self):
        self.assertEqual(expand_ports("80"), frozenset({80}))

    def test_multiple_single_ports(self):
        self.assertEqual(expand_ports("80,443,8080"), frozenset({80, 443, 8080}))

    def test_simple_range(self):
        self.assertEqual(
            expand_ports("8000-8002"),
            frozenset({8000, 8001, 8002}),
        )

    def test_mixed_single_and_range(self):
        self.assertEqual(
            expand_ports("80,443,8000-8001"),
            frozenset({80, 443, 8000, 8001}),
        )

    def test_whitespace_around_tokens(self):
        self.assertEqual(
            expand_ports("  80 , 443 , 8000-8001  "),
            frozenset({80, 443, 8000, 8001}),
        )

    def test_range_of_one(self):
        """'80-80' is a valid range spanning a single port."""
        self.assertEqual(expand_ports("80-80"), frozenset({80}))

    def test_duplicates_collapsed(self):
        self.assertEqual(expand_ports("80,80,80"), frozenset({80}))

    def test_overlapping_range_and_single(self):
        self.assertEqual(
            expand_ports("80,80-82"),
            frozenset({80, 81, 82}),
        )

    def test_large_range(self):
        result = expand_ports("0-5")
        self.assertEqual(result, frozenset({0, 1, 2, 3, 4, 5}))

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            expand_ports(80)  # type: ignore

    def test_empty_token_raises(self):
        with self.assertRaises(InvalidPortRange):
            expand_ports("80,,443")

    def test_negative_port_raises(self):
        with self.assertRaises(InvalidPortRange):
            expand_ports("-80")

    def test_reversed_range_raises(self):
        with self.assertRaises(InvalidPortRange):
            expand_ports("8001-8000")

    def test_multiple_dashes_raises(self):
        with self.assertRaises(InvalidPortRange):
            expand_ports("1-2-3")

    def test_non_numeric_raises(self):
        with self.assertRaises(InvalidPortRange):
            expand_ports("abc")

    def test_invalid_port_in_range_raises(self):
        with self.assertRaises(InvalidPortRange):
            expand_ports("80-abc")

    def test_invalid_port_type_is_value_error(self):
        """InvalidPortRange must be a ValueError subclass."""
        self.assertTrue(issubclass(InvalidPortRange, ValueError))

    def test_leading_zero_port(self):
        """'080' is accepted because str.isdigit() and int() handle it."""
        self.assertEqual(expand_ports("080"), frozenset({80}))


if __name__ == "__main__":
    unittest.main()
