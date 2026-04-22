import json
import socket
import unittest

from fetchr.follow.phone_position_follower import PhonePositionFollower


class PhoneFollowerTests(unittest.TestCase):
    def test_receives_udp_position_packet(self):
        follower = PhonePositionFollower(bind_host='127.0.0.1', bind_port=9999, target_follow_distance_m=1.5)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(json.dumps({'x': 2.0, 'y': 0.0}).encode('utf-8'), ('127.0.0.1', 9999))
            # first call consumes packet and computes distance error
            dist_proxy = follower.read_distance_proxy()
            heading = follower.read_heading_error()
            self.assertAlmostEqual(dist_proxy, 0.5, places=2)
            self.assertAlmostEqual(heading, 0.0, places=2)
        finally:
            follower.close()
            sock.close()


if __name__ == '__main__':
    unittest.main()
