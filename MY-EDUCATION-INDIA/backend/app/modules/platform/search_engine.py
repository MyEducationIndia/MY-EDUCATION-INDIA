"""Module 20: Global Search Engine"""
class GlobalSearchEngine:
    @staticmethod
    def filter_search_index(search_records: list, query: str, limit: int = 20) -> list:
        q = query.lower().strip()
        if not q:
            return []
        matches = []
        for rec in search_records:
            haystack = f"{rec.get('title', '')} {rec.get('subtitle', '')} {rec.get('keywords_tsv', '')}".lower()
            if q in haystack:
                matches.append(rec)
            if len(matches) >= limit:
                break
        return matches
