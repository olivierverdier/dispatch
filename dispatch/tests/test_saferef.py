from dispatch.saferef import *

import unittest

class Test1(object):
    def x(self):
        pass

def dummy(obj):
    pass

class Test2(object):
    def __call__(self, obj):
        pass

class Tester(unittest.TestCase):
    def setUp(self):
        ts = []
        ss = []
        self.closureCount = 0
        for x in range(5000):
            t = Test1()
            ts.append(t)
            s = safeRef(t.x, self._closure)
            ss.append(s)
        ts.append(dummy)
        ss.append(safeRef(dummy, self._closure))
        for x in range(30):
            t = Test2()
            ts.append(t)
            s = safeRef(t, self._closure)
            ss.append(s)
        self.ts = ts
        self.ss = ss
    
    def tearDown(self):
        del self.ts
        del self.ss
    
    def testIn(self):
        """Test the "in" operator for safe references (cmp)"""
        for t in self.ts[:50]:
            self.assertIn(safeRef(t.x), self.ss)
    
    def testValid(self):
        """Test that the references are valid (return instance methods)"""
        for s in self.ss:
            self.assertTrue(s())
    
    def testShortCircuit (self):
        """Test that creation short-circuits to reuse existing references"""
        sd = {}
        for s in self.ss:
            sd[s] = 1
        for t in self.ts:
            if hasattr(t, 'x'):
                self.assertTrue(sd.has_key(safeRef(t.x)))
                self.assertTrue(safeRef(t.x) in sd)
            else:
                self.assertTrue(sd.has_key(safeRef(t)))
                self.assertTrue(safeRef(t) in sd)
    
    def testRepresentation (self):
        """Test that the reference object's representation works
        
        XXX Doesn't currently check the results, just that no error
            is raised
        """
        repr(self.ss[-1])
        
    def _closure(self, ref):
        """Dumb utility mechanism to increment deletion counter"""
        self.closureCount +=1

def getSuite():
    return unittest.makeSuite(Tester,'test')

if __name__ == "__main__":
    unittest.main()
