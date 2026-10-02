import unittest

from builders import label

MINER = "0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5"


class LabelTest(unittest.TestCase):
    def test_text_extradata(self):
        self.assertEqual(label("0x" + b"beaverbuild.org".hex(), MINER), "beaverbuild.org")

    def test_nonprintable_bytes_are_dropped(self):
        self.assertEqual(label("0x" + (b"\x00\x01Titan (titanbuilder.xyz)\xff").hex(), MINER), "Titan (titanbuilder.xyz)")

    def test_empty_or_binary_falls_back_to_miner(self):
        self.assertEqual(label("0x", MINER), MINER.lower())
        self.assertEqual(label("0x00ff01", MINER), MINER.lower())
        self.assertEqual(label(None, MINER), MINER.lower())

    def test_rlp_client_extradata_keeps_client_name(self):
        # geth's default extraData is RLP [version, "geth", go version, os]; the text part survives
        self.assertEqual(label("0xd883010d0e846765746888", MINER), "geth")


if __name__ == "__main__":
    unittest.main()
