import time
import unittest

from fastrq.queue import Queue, CappedQueue, OfCappedQueue


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue("fastrq_queue")
        self.queue.destruct()
    
    def tearDown(self):
        self.queue.destruct()
    
    def test_push_pop(self):
        ql = self.queue.push((1, 2))
        self.assertEqual(ql, 2)
        self.assertEqual(self.queue.length(), 2)
        head = self.queue.pop()
        self.assertEqual(head, '1')
        self.assertEqual(self.queue.length(), 1)
        self.assertEqual(len(self.queue), 1)
        
        self.queue.push((3, 4, 5))
        head3 = self.queue.pop(3)
        self.assertEqual(head3, ['2', '3', '4'])
        self.assertEqual(self.queue.pop(), '5')
        self.assertEqual(self.queue.pop(), None)
    
    def test_range(self):
        self.queue.push((1, 2, 3, 4))
        self.assertEqual(self.queue.range(0, -1), ['1', '2', '3', '4'])
        self.assertEqual(self.queue.range(0, 2), ['1', '2', '3'])
        self.assertEqual(self.queue.range(0, 0), ['1'])
        self.queue.destruct()
        self.assertEqual(self.queue.range(0, -1), [])
    
    def test_expire(self):
        self.queue.push((1, 2))
        self.assertEqual(self.queue.ttl(), -1)
        self.queue.expire(10)
        self.assertEqual(self.queue.ttl(), 10)
        time.sleep(11)
        self.assertEqual(self.queue.ttl(), -2)


class TestCappedQueue(unittest.TestCase):
    def setUp(self):
        self.queue = CappedQueue("fastrq_capped_queue", 3)
        self.queue.destruct()
    
    def tearDown(self):
        self.queue.destruct()
    
    def test_push(self):
        self.assertEqual(self.queue.push((1, 2, 3)), 3)
        self.assertEqual(self.queue.push(4), 'err_qf')


class TestOfCappedQueue(unittest.TestCase):
    def setUp(self):
        self.queue = OfCappedQueue("fastrq_of_capped_queue", 3)
        self.queue.destruct()
    
    def tearDown(self):
        self.queue.destruct()
    
    def test_push(self):
        self.assertEqual(self.queue.push((1, 2, 3)), [3, []])
        self.assertEqual(self.queue.push(4), [3, ['1']])
        self.assertEqual(self.queue.range(0, -1), ['2', '3', '4'])