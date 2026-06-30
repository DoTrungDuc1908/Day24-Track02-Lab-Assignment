from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern, EntityRecognizer, RecognizerResult
from presidio_analyzer.nlp_engine import NlpEngineProvider

class VietnamesePersonRecognizer(EntityRecognizer):
    def __init__(self):
        super().__init__(
            supported_entities=["PERSON"],
            supported_language="vi"
        )

    def load(self) -> None:
        pass

    def analyze(self, text: str, entities: list, nlp_artifacts=None) -> list:
        results = []
        if "PERSON" not in entities:
            return results
        
        import re
        # Find any sequence of 2 or more capitalized words.
        words = list(re.finditer(r"[^\W\d_]+", text))
        i = 0
        while i < len(words):
            w = words[i]
            val = w.group(0)
            if val[0].isupper():
                start = w.start()
                end = w.end()
                j = i + 1
                while j < len(words) and words[j].group(0)[0].isupper():
                    end = words[j].end()
                    j += 1
                if j - i >= 2:
                    results.append(RecognizerResult(
                        entity_type="PERSON",
                        start=start,
                        end=end,
                        score=0.85
                    ))
                    i = j
                    continue
            i += 1
        return results

def build_vietnamese_analyzer() -> AnalyzerEngine:
    """
    TODO: Xây dựng AnalyzerEngine với các recognizer tùy chỉnh cho VN.
    """

    # --- TASK 2.2.1 ---
    # Tạo CCCD recognizer: số CCCD VN có đúng 12 chữ số
    cccd_pattern = Pattern(
        name="cccd_pattern",
        regex=r"\b\d{11,12}\b",          # TODO: điền regex cho 11 hoặc 12 chữ số
        score=0.9
    )
    cccd_recognizer = PatternRecognizer(
        supported_entity="VN_CCCD",
        patterns=[cccd_pattern],
        context=["cccd", "căn cước", "chứng minh", "cmnd"],
        supported_language="vi"
    )

    # --- TASK 2.2.2 ---
    # Tạo phone recognizer: số điện thoại VN (0[3|5|7|8|9]xxxxxxxx)
    phone_recognizer = PatternRecognizer(
        supported_entity="VN_PHONE",
        patterns=[Pattern(
            name="vn_phone",
            regex=r"\b0?[35789]\d{8}\b",      # TODO: điền regex
            score=0.85
        )],
        context=["điện thoại", "sdt", "phone", "liên hệ"],
        supported_language="vi"
    )

    # --- TASK 2.2.3 ---
    # Tạo NLP engine dùng spaCy Vietnamese model
    provider = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "vi", 
                    "model_name": "vi_core_news_lg"}]   # TODO: điền model name
    })
    nlp_engine = provider.create_engine()

    # --- TASK 2.2.4 ---
    # Khởi tạo AnalyzerEngine và add các recognizer
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
    analyzer.registry.add_recognizer(cccd_recognizer)   # TODO
    analyzer.registry.add_recognizer(phone_recognizer)   # TODO

    # Đăng ký custom VietnamesePersonRecognizer
    person_recognizer = VietnamesePersonRecognizer()
    analyzer.registry.add_recognizer(person_recognizer)

    from presidio_analyzer.predefined_recognizers import EmailRecognizer
    email_recognizer = EmailRecognizer(supported_language="vi")
    analyzer.registry.add_recognizer(email_recognizer)

    return analyzer


def detect_pii(text: str, analyzer: AnalyzerEngine) -> list:
    """
    TODO: Detect PII trong text tiếng Việt.
    Trả về list các RecognizerResult.
    Entities cần detect: PERSON, EMAIL_ADDRESS, VN_CCCD, VN_PHONE
    """
    results = analyzer.analyze(
        text=text,       # TODO
        language="vi",   # TODO
        entities=["PERSON", "EMAIL_ADDRESS", "VN_CCCD", "VN_PHONE"]    # TODO
    )
    return results
