"""Launcher regression tests; OS mutex, processes and browser are simulated."""
from __future__ import annotations

from contextlib import contextmanager
import importlib.util
import io
import json
from pathlib import Path
import sys
import threading
import time
import types
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


class LauncherTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("_launcher_audit", ROOT / "launch.py")
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.messages = mock.Mock()
        tkinter = types.ModuleType("tkinter")
        tkinter.messagebox = self.messages
        modules = mock.patch.dict(sys.modules, {"tkinter": tkinter})
        modules.start()
        self.addCleanup(modules.stop)
        args = mock.patch.object(sys, "argv", ["launch.py"])
        args.start()
        self.addCleanup(args.stop)

    def test_double_click_serializes_health_check_and_start(self):
        lock = threading.Lock()
        ready = {False: False, True: False}
        barrier = threading.Barrier(2)
        results = []

        @contextmanager
        def simulated_mutex():
            with lock:
                yield

        def simulated_start(cosmology=False):
            # Keep the first click inside the critical section while the second enters.
            time.sleep(0.02)
            ready[cosmology] = True

        def click():
            barrier.wait(timeout=2)
            results.append(self.module.main())

        with mock.patch.object(self.module, "launch_lock", side_effect=simulated_mutex), \
                mock.patch.object(self.module, "is_our_bench", side_effect=lambda cosmology=False: ready[cosmology]), \
                mock.patch.object(self.module, "start", side_effect=simulated_start) as start, \
                mock.patch.object(self.module.webbrowser, "open") as browser:
            threads = [threading.Thread(target=click, daemon=True) for _ in range(2)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=3)
            self.assertTrue(all(not thread.is_alive() for thread in threads))
            self.assertEqual(results, [0, 0])
            self.assertEqual(start.call_args_list, [mock.call(), mock.call(True)])
            self.assertEqual(browser.call_count, 2)
            self.assertEqual(browser.call_args_list,
                             [mock.call(self.module.COSMOS_URL + "/explore", new=2)] * 2)
        self.messages.showerror.assert_not_called()

    def test_cosmos_failure_still_opens_already_healthy_gw(self):
        # Regression: an optional service must not hide the already-running GW UI.
        @contextmanager
        def simulated_mutex():
            yield

        with mock.patch.object(self.module, "launch_lock", side_effect=simulated_mutex), \
                mock.patch.object(self.module, "is_our_bench", side_effect=lambda cosmology=False: not cosmology), \
                mock.patch.object(self.module, "start", side_effect=RuntimeError("cosmos unavailable")) as start, \
                mock.patch.object(self.module.webbrowser, "open") as browser:
            self.assertEqual(self.module.main(), 1)
            start.assert_called_once_with(True)
            browser.assert_called_once_with(self.module.URL + "/universe", new=2)
        self.messages.showerror.assert_called_once()

    def test_healthy_services_open_explore_without_starting_processes(self):
        events = []

        @contextmanager
        def simulated_mutex():
            events.append("lock")
            yield
            events.append("unlock")

        def check(cosmology=False):
            self.assertEqual(events[-1], "lock")
            return True

        def open_browser(*args, **kwargs):
            self.assertEqual(events[-1], "unlock")

        with mock.patch.object(self.module, "launch_lock", side_effect=simulated_mutex), \
                mock.patch.object(self.module, "is_our_bench", side_effect=check) as health, \
                mock.patch.object(self.module, "start") as start, \
                mock.patch.object(self.module.webbrowser, "open", side_effect=open_browser) as browser:
            self.assertEqual(self.module.main(), 0)
            health.assert_has_calls([mock.call(), mock.call(True)])
            start.assert_not_called()
            browser.assert_called_once_with(self.module.COSMOS_URL + "/explore", new=2)
        self.messages.showerror.assert_not_called()

    def test_gw_start_failure_keeps_existing_launcher_failure_guard(self):
        @contextmanager
        def simulated_mutex():
            yield

        with mock.patch.object(self.module, "launch_lock", side_effect=simulated_mutex), \
                mock.patch.object(self.module, "is_our_bench", return_value=False), \
                mock.patch.object(self.module, "start", side_effect=RuntimeError("GW unavailable")) as start, \
                mock.patch.object(self.module.webbrowser, "open") as browser:
            self.assertEqual(self.module.main(), 1)
            start.assert_called_once_with()
            browser.assert_not_called()
        self.messages.showerror.assert_called_once()

    def test_mutex_failure_does_not_start_services_or_open_browser(self):
        with mock.patch.object(self.module, "launch_lock", side_effect=RuntimeError("mutex unavailable")), \
                mock.patch.object(self.module, "is_our_bench") as health, \
                mock.patch.object(self.module, "start") as start, \
                mock.patch.object(self.module.webbrowser, "open") as browser:
            self.assertEqual(self.module.main(), 1)
            health.assert_not_called()
            start.assert_not_called()
            browser.assert_not_called()
        self.messages.showerror.assert_called_once()

    def test_check_reports_explore_without_mutex_start_or_browser(self):
        stdout = io.StringIO()
        with mock.patch.object(sys, "argv", ["launch.py", "--check"]), \
                mock.patch.object(self.module, "is_our_bench", return_value=True), \
                mock.patch.object(self.module, "launch_lock") as lock, \
                mock.patch.object(self.module, "start") as start, \
                mock.patch.object(self.module.webbrowser, "open") as browser, \
                mock.patch.object(sys, "stdout", stdout):
            self.assertEqual(self.module.main(), 0)
            lock.assert_not_called()
            start.assert_not_called()
            browser.assert_not_called()
        report = json.loads(stdout.getvalue())
        self.assertTrue(report["running"])
        self.assertTrue(report["cosmology_running"])
        self.assertEqual(report["cosmology_url"], self.module.COSMOS_URL + "/explore")
        self.messages.showerror.assert_not_called()


if __name__ == "__main__":
    unittest.main()
