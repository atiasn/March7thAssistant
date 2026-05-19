from module.ocr.ocr import OCR


class TestOCRNormalizeMachine:
    def test_amd64_to_x86_64(self):
        ocr = OCR.__new__(OCR)
        # 需要 mock platform.machine()
        import platform
        original = platform.machine
        try:
            platform.machine = lambda: "AMD64"
            assert ocr._normalize_machine() == "x86_64"
        finally:
            platform.machine = original

    def test_x86_64_unchanged(self):
        ocr = OCR.__new__(OCR)
        import platform
        original = platform.machine
        try:
            platform.machine = lambda: "x86_64"
            assert ocr._normalize_machine() == "x86_64"
        finally:
            platform.machine = original

    def test_arm64(self):
        ocr = OCR.__new__(OCR)
        import platform
        original = platform.machine
        try:
            platform.machine = lambda: "arm64"
            assert ocr._normalize_machine() == "arm64"
        finally:
            platform.machine = original


class TestOCRVersionAtLeast:
    def test_higher_version(self):
        ocr = OCR.__new__(OCR)
        assert ocr._version_at_least("1.2.3", "1.0.0") is True

    def test_same_version(self):
        ocr = OCR.__new__(OCR)
        assert ocr._version_at_least("1.0.0", "1.0.0") is True

    def test_lower_version(self):
        ocr = OCR.__new__(OCR)
        assert ocr._version_at_least("0.9.0", "1.0.0") is False

    def test_major_version_diff(self):
        ocr = OCR.__new__(OCR)
        assert ocr._version_at_least("2.0.0", "1.9.9") is True


class TestOCRConvertFormat:
    def test_none_returns_false(self):
        ocr = OCR.__new__(OCR)
        assert ocr.convert_format(None) is False

    def test_valid_result(self):
        ocr = OCR.__new__(OCR)
        result = [
            {"box": [[0, 0], [10, 0], [10, 10], [0, 10]], "txt": "hello", "score": 0.99},
            {"box": [[20, 0], [30, 0], [30, 10], [20, 10]], "txt": "world", "score": 0.95},
        ]
        converted = ocr.convert_format(result)
        assert len(converted) == 2
        # convert_format returns [[box, (txt, score)], ...]
        assert converted[0][0] == [[0, 0], [10, 0], [10, 10], [0, 10]]
        assert converted[0][1] == ("hello", 0.99)
        assert converted[1][0] == [[20, 0], [30, 0], [30, 10], [20, 10]]
        assert converted[1][1] == ("world", 0.95)


class TestOCRReplaceStrings:
    def _create_ocr_with_mock_logger(self):
        from unittest.mock import MagicMock
        ocr = OCR.__new__(OCR)
        ocr.logger = MagicMock()
        ocr.replacements = None
        return ocr

    def test_none_returns_none(self):
        ocr = self._create_ocr_with_mock_logger()
        assert ocr.replace_strings(None) is None

    def test_empty_returns_empty(self):
        ocr = self._create_ocr_with_mock_logger()
        assert ocr.replace_strings([]) == []

    def test_no_replacements(self):
        ocr = self._create_ocr_with_mock_logger()
        results = [{"txt": "hello", "score": 0.99}]
        assert ocr.replace_strings(results) == results

    def test_direct_replacement(self):
        ocr = self._create_ocr_with_mock_logger()
        ocr.replacements = {"direct": {"hello": "world"}, "conditional": {}}
        results = [{"txt": "hello", "score": 0.99}]
        replaced = ocr.replace_strings(results)
        assert replaced[0]["txt"] == "world"
