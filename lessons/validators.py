import re

from rest_framework.serializers import ValidationError


class AllowedLinksValidator:
    def __init__(self, field: str):
        self.field = field
        self.url_pattern = r"""((?:(?:https|ftp|http)?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|org|uk)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|uk|ac)\b/?(?!@)))"""
        self.allowed_prefixes = [
            "https://youtube",
            "youtube",
            "https://youtu.be",
            "youtu.be",
        ]

    def starts_with_allowed_prefix(self, url: str) -> bool:
        return any(map(lambda x: url.startswith(x), self.allowed_prefixes))

    def __call__(self, value):
        text = dict(value).get(self.field)

        all_urls = re.findall(self.url_pattern, text)

        for url in all_urls:
            if not self.starts_with_allowed_prefix(url):
                raise ValidationError("Only YouTube video links is allowed")
