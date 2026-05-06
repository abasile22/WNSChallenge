from unittest.mock import Mock, patch
from app.services.ocr import OCR


class TestOCR:
    def test_read_success(self):
        with patch('app.services.ocr.convert_from_bytes') as mock_convert:
            with patch('app.services.ocr.pytesseract.image_to_string') as mock_ocr:
                with patch.object(OCR, '_preprocess_image', return_value=Mock()):
                    mock_page = Mock()
                    mock_convert.return_value = [mock_page]
                    mock_ocr.return_value = "Tomate\n$10.50\nCebolla\n$5.00"

                    ocr = OCR(b"pdf_content")
                    result = ocr.read()

                    assert len(result) == 2
                    assert result[0]["name"] == "tomate"
                    assert result[0]["price"] == 1050
                    assert result[1]["name"] == "cebolla"
                    assert result[1]["price"] == 500

    def test_read_empty_content(self):
        with patch('app.services.ocr.convert_from_bytes') as mock_convert:
            mock_convert.return_value = []

            ocr = OCR(b"empty_pdf")
            result = ocr.read()

            assert result == []

    def test_read_exception(self):
        with patch('app.services.ocr.convert_from_bytes') as mock_convert:
            mock_convert.side_effect = Exception("PDF error")

            ocr = OCR(b"invalid_pdf")
            result = ocr.read()

            assert result == []

    def test_read_with_price_format_variations(self):
        with patch('app.services.ocr.convert_from_bytes') as mock_convert:
            with patch('app.services.ocr.pytesseract.image_to_string') as mock_ocr:
                with patch.object(OCR, '_preprocess_image', return_value=Mock()):
                    mock_page = Mock()
                    mock_convert.return_value = [mock_page]
                    mock_ocr.return_value = "Arroz\n$ 25.50\nPapa\n$1.000"

                    ocr = OCR(b"pdf_content")
                    result = ocr.read()

                    assert len(result) == 2
                    assert result[0]["price"] == 2550
                    assert result[1]["price"] == 1000

    def test_is_name_valid(self):
        ocr = OCR(b"dummy")
        assert ocr._is_name("Tomate") is True
        assert ocr._is_name("Cebolla") is True
        assert ocr._is_name("Ñame") is True
        assert ocr._is_name("tomate") is False
        assert ocr._is_name("123") is False
        assert ocr._is_name("$100") is False

    def test_parse_lines_empty(self):
        ocr = OCR(b"dummy")
        result = ocr._parse_lines([])

        assert result == []

    def test_parse_lines_no_prices(self):
        ocr = OCR(b"dummy")
        lines = ["Tomate", "Cebolla"]
        result = ocr._parse_lines(lines)

        assert result == []

    def test_parse_lines_with_valid_data(self):
        ocr = OCR(b"dummy")
        lines = ["Tomate", "$10.50", "Cebolla", "$5.00"]
        result = ocr._parse_lines(lines)

        assert len(result) == 2
        assert result[0]["name"] == "tomate"
        assert result[0]["price"] == 1050
        assert result[1]["name"] == "cebolla"
        assert result[1]["price"] == 500

    def test_extract_text_from_pages(self):
        with patch('app.services.ocr.pytesseract.image_to_string') as mock_ocr:
            with patch.object(OCR, '_preprocess_image', return_value=Mock()):
                mock_ocr.return_value = "Tomate\n$10.50"

                ocr = OCR(b"dummy")
                mock_pages = [Mock(), Mock()]
                result = ocr._extract_text_from_pages(mock_pages)

                assert "Tomate" in result
                assert "$10.50" in result
                assert mock_ocr.call_count == 2
