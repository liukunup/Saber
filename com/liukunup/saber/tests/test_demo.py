# -*- coding: UTF-8 -*-
# Test: demo

from com.liukunup.saber.tests.base_test import BaseTest


class DemoTestCase(BaseTest):

    def test_demo(self):
        # Mock
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        resp = self.client.get(f"{self.url_prefix}/demo", headers=headers)
        obj = resp.json
        # Check
        self.expectRet(obj)
        self.expectSuccess(obj)

    def test_demo_with_param(self):
        # Test Point
        with_param = 999
        # Mock
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        resp = self.client.get(f"{self.url_prefix}/demo/{with_param}", headers=headers)
        obj = resp.json
        # Check
        self.expectRet(obj)
        self.expectSuccess(obj)
        self.assertEqual(obj["data"], with_param)
