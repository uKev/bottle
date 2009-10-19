#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys, os.path
from bottle import route, Router, BaseController
from wsgiref.util import setup_testing_defaults


class TestRoutes(unittest.TestCase):

    def test_static(self):
        """ Routes: Static routes """
        rt = Router()
        token = 'abc'
        routes = ['','/','/abc','abc','/abc/','/abc/def','/abc/def.ghi']
        for r in routes:
            rt.add_route(r, token, simple=True)
        for r in routes:
            self.assertEqual(token, rt.match_url(r)[0])

    def test_dynamic(self):
        """ Routes: Dynamic routes """ 
        rt = Router()
        token = 'abcd'
        rt.add_route('/:a/:b', token)
        self.assertEqual(token, rt.match_url('/aa/bb')[0])
        self.assertEqual(None, rt.match_url('/aa')[0])
        self.assertEqual(repr({'a':'aa','b':'bb'}), repr(rt.match_url('/aa/bb')[1]))

    def test_default(self):
        """ Routes: Decorator and default routes """
        rt = Router()
        def test1(): return 'test1'
        def test2(): return 'test2'
        rt.add_route('/exists', test1)
        rt.set_default(test2)
        self.assertEqual(test1, rt.match_url('/exists')[0])
        self.assertNotEqual(test2, rt.match_url('/exists')[0])
        self.assertEqual(test2, rt.match_url('/does_not_exist')[0])
        self.assertNotEqual(test1, rt.match_url('/does_not_exist')[0])

    def test_controller(self):
        """ Routes: Controller Syntax """
        """ Not testing decorator mode here because it is a SyntaxError in Python 2.5 """
        rt = Router()
        class CTest(BaseController): 
            def _no(self): return 'no'
            def yes(self): return 'yes'
            def yes2(self, test): return test
        rt.add_route('/ctest/{action}', CTest)
        rt.add_route('/ctest/yes/:test', CTest, action='yes2')

        self.assertEqual(None, rt.match_url('/ctest/no')[0])
        self.assertEqual(None, rt.match_url('/ctest/_no')[0])
        self.assertEqual('yes', rt.match_url('/ctest/yes')[0]())
        self.assertEqual('test', rt.match_url('/ctest/yes/test')[0](test='test'))


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestRoutes))

if __name__ == '__main__':
    unittest.main()
